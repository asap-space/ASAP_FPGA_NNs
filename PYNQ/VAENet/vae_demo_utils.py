import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
import numpy as np
import time
import os
import matplotlib.pyplot as plt
from IPython.display import clear_output

# Try importing hardware-specific libraries, fallback if running elsewhere
try:
    from pynq import get_rails, DataRecorder
    from pynq_dpu import DpuOverlay
except ImportError:
    print("Warning: PYNQ/DPU libraries not found. Ensure this runs on the Zynq board.")

# -----------------------------------------------------------------------------#
#    CPU MODEL SETUP                                                           #
# -----------------------------------------------------------------------------#
class vaemodel1(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, 3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 256, 3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.mu = nn.Linear(256, 6)
        self.std = nn.Linear(256, 6)

    def forward(self, x):
        a = self.encoder(x).permute(0, 2, 3, 1)
        a = torch.flatten(a, start_dim=1)
        mu = self.mu(a)
        lvar = self.std(a)
        out = torch.cat((mu, lvar), dim=1)
        return out


def setup_cpu_model(weights_path="pre_trained_w_encoder.pt"):
    """Initialize the PyTorch model for the CPU."""
    model = vaemodel1()
    if os.path.exists(weights_path):
        model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu'), weights_only=True))
    else:
        print(f"Warning: CPU weights '{weights_path}' not found, using random weights.")
    model.eval()
    return model


# -----------------------------------------------------------------------------#
#    DPU MODEL SETUP                                                           #
# -----------------------------------------------------------------------------#
def setup_dpu_model(bitstream_path="../vitisai_bitstream/dpu.bit", model_path="zcu104_vaemodel1.xmodel"):
    """Load the DPU overlay and prepare the model for inference."""
    try:
        overlay = DpuOverlay(bitstream_path)
        overlay.load_model(model_path)
        dpu = overlay.runner

        inputTensors = dpu.get_input_tensors()
        outputTensors = dpu.get_output_tensors()

        shapeIn = tuple(inputTensors[0].dims)
        shapeOut = tuple(outputTensors[0].dims)

        output_data = [np.empty(shapeOut, dtype=np.float32, order="C")]
        input_data = [np.empty(shapeIn, dtype=np.float32, order="C")]

        return overlay, dpu, input_data, output_data
    except Exception as e:
        print(f"Failed to load DPU model: {e}")
        return None, None, None, None


# -----------------------------------------------------------------------------#
#    DATA LOADING & POWER RECORDING                                            #
# -----------------------------------------------------------------------------#
def get_dataloader(img_path='dataset', num_samples=1000):
    """Setup and load a subset of the image dataset."""
    full_dataset = datasets.ImageFolder(
        img_path,
        transforms.Compose([
            transforms.Resize((128, 256)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0])
        ])
    )
    # Ensure we don't request more samples than available
    subset_size = min(num_samples, len(full_dataset))
    dataset = Subset(full_dataset, list(range(subset_size)))
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=1)
    return dataloader, dataset


def setup_power_recorder():
    """Returns the DataRecorder attached to the board's INT power rail."""
    try:
        rails = get_rails()
        recorder = DataRecorder(rails['INT'].power)
        return recorder
    except Exception as e:
        print(f"Could not setup power recorder: {e}")
        return None


# -----------------------------------------------------------------------------#
#    INFERENCE FUNCTIONS                                                       #
# -----------------------------------------------------------------------------#
def run_cpu_inference(model, dataloader, recorder=None, plot_every=0):
    """Runs a batch of inferences on the CPU and measures time."""
    cpu_latents = []
    
    # Mark start of execution
    if recorder:
        time.sleep(0.5)  # Allow background power recording thread to start
        recorder.mark()

    inference_time = 0.0
    count = 0
    with torch.no_grad():
        for image, _ in dataloader:
            count += 1
            # Start strict timing
            start_t = time.time()
            pred = model(image)
            inference_time += (time.time() - start_t)
            
            o_data = pred.squeeze().cpu().numpy().reshape(2, 6)
            std = np.exp(o_data[1] * 0.5)
            eps = np.random.randn(*std.shape)
            latent_z = o_data[0] + eps * std
            
            cpu_latents.append(latent_z)
            
            if plot_every > 0 and count % plot_every == 0:
                progress_msg = f"CPU Inference Progress: {count} / {len(dataloader.dataset)} images"
                plot_input_and_latent(image, latent_z, progress_text=progress_msg)
                
            
    # Mark end of execution
    if recorder:
        recorder.mark()
        time.sleep(0.1)  # Ensure mark is registered before proceeding

    num_samples = len(dataloader.dataset)
    avg_time = inference_time / num_samples if num_samples > 0 else 0

    return cpu_latents, avg_time, inference_time


def run_dpu_inference(dpu, input_data, output_data, dataloader, recorder=None):
    """Runs a batch of inferences on the DPU and measures time."""
    if dpu is None:
        return [], 0.0, 0.0
        
    dpu_latents = []

    # Mark start of execution
    if recorder:
        time.sleep(0.1)  # Ensure separation from previous executions
        recorder.mark()

    inference_time = 0.0
    for image, _ in dataloader:
        # Move PyTorch's NCHW format to the DPU's NHWC format
        data = image.permute(0, 2, 3, 1).numpy()
        input_data[0][...] = data
        
        # Start strict timing
        start_t = time.time()
        job_id = dpu.execute_async(input_data, output_data)
        dpu.wait(job_id)
        inference_time += (time.time() - start_t)
        
        o_data = output_data[0].reshape(2, 6)
        std = np.exp(o_data[1] * 0.5)
        eps = np.random.randn(*std.shape)
        latent_z = o_data[0] + eps * std
        
        dpu_latents.append(latent_z)
        
    # Mark end of execution
    if recorder:
        recorder.mark()
        time.sleep(0.5)  # Prevent recorder.stop() from executing too quickly

    num_samples = len(dataloader.dataset)
    avg_time = inference_time / num_samples if num_samples > 0 else 0

    return dpu_latents, avg_time, inference_time


# -----------------------------------------------------------------------------#
#    VISUALIZATION UTILS                                                       #
# -----------------------------------------------------------------------------#
def plot_input_and_latent(image_tensor, latent_vector, progress_text=None):
    """
    Plots the original input image and a bar chart showing the compressed
    6-value scalar vector that the image is reduced to.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={'width_ratios': [2, 1]})

    # Process image for display (denormalize assuming basic normalization behavior)
    # The original images were normalized: (x - 0) / 1, so they are mostly 0..1
    img = image_tensor.squeeze().permute(1, 2, 0).numpy()
    img = np.clip(img, 0, 1)

    ax1.imshow(img)
    ax1.set_title("1. Original Input Image\n(~98,000 values)", fontsize=14)
    ax1.axis('off')

    # Process latent vector: the VAE encoder produces 12 values (6 mu, 6 log_var).
    if isinstance(latent_vector, torch.Tensor):
        vec = latent_vector.detach().squeeze().numpy()
    else:
        vec = np.array(latent_vector).squeeze()

    # Extract just the 6 'mu' values representing the encoded state
    vec_mu = vec[:6] if len(vec) >= 6 else vec

    ax2.bar(range(1, 7), vec_mu, color='teal')
    ax2.set_title("2. Compressed Latent Vector\n(6 scalar values)", fontsize=14)
    ax2.set_xticks(range(1, 7))
    ax2.set_xlabel("Latent Features", fontsize=12)
    ax2.set_ylabel("Activation Value", fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    clear_output(wait=True)
    plt.show()
    if progress_text:
        print(progress_text)


def get_average_power(recorder):
    """
    Parses marks from the power recorder and returns the average power
    for the CPU and FPGA execution segments.
    """
    if recorder is None:
        return 0.0, 0.0

    mark_indices = []
    last_mark = 0.0
    for i, mark in enumerate(recorder.frame['Mark']):
        if mark > last_mark:
            mark_indices.append(i)
            last_mark = mark
            
    if len(mark_indices) < 4:
        return 0.0, 0.0

    power_data = recorder.frame['INT_power']
    avg_cpu = np.mean(power_data[mark_indices[0]:mark_indices[1]])
    avg_fpga = np.mean(power_data[mark_indices[2]:mark_indices[3]])
    
    return avg_cpu, avg_fpga


def plot_power_consumption(recorder):
    """
    Parses marks from the power recorder and plots a curve comparing the CPU
    and FPGA consumption during inference.
    """
    if recorder is None:
        print("No recorder provided. Cannot plot power.")
        return

    # Extract marks where execution started/ended
    mark_indices = []
    last_mark = 0.0
    for i, mark in enumerate(recorder.frame['Mark']):
        if mark > last_mark:
            mark_indices.append(i)
            last_mark = mark
            
    if len(mark_indices) < 4:
        print(f"Notice: Expected 4 recording marks, but got {len(mark_indices)}. Plotting full trace without colors.")
        power_data = recorder.frame['INT_power']
        time_data = recorder.frame.index
        elapsed_time = (time_data - time_data[0]).total_seconds()
        
        plt.figure(figsize=(12, 6))
        plt.plot(elapsed_time, power_data, color='gray')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (W)')
        plt.title('Power Consumption Profile')
        plt.show()
        return

    power_data = recorder.frame['INT_power']
    time_data = recorder.frame.index
    elapsed_time = (time_data - time_data[0]).total_seconds()

    plt.figure(figsize=(10, 5))

    # Base line
    plt.plot(elapsed_time, power_data, color='lightgray', alpha=0.5, label='Idle Power')

    # CPU Execution chunk
    plt.plot(elapsed_time[mark_indices[0]:mark_indices[1]], 
             power_data[mark_indices[0]:mark_indices[1]], 
             color='royalblue', linewidth=2, label='CPU Inference')

    # FPGA Execution chunk
    plt.plot(elapsed_time[mark_indices[2]:mark_indices[3]], 
             power_data[mark_indices[2]:mark_indices[3]], 
             color='darkorange', linewidth=2, label='FPGA Inference')

    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Power (W)', fontsize=14)
    plt.title('Board Power Profile: CPU vs DPU (FPGA)', fontsize=16)
    plt.legend(fontsize=12, loc='upper left')

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    # Calculate Max Power
    max_cpu = max(power_data[mark_indices[0]:mark_indices[1]])
    max_fpga = max(power_data[mark_indices[2]:mark_indices[3]])
    
    stats_text = f"CPU Max Power: {max_cpu:.2f} W\nFPGA Max Power: {max_fpga:.2f} W"
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black')
    plt.gca().text(0.95, 0.95, stats_text, transform=plt.gca().transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()
    plt.show()


def print_performance_summary(cpu_avg_time, dpu_avg_time, recorder=None):
    """
    Calculates and prints the inference time speedup and energy efficiency
    using the recorded telemetry data.
    """
    print("=== Performance & Energy Summary ===")
    print(f"CPU Average Inference Time: {cpu_avg_time*1000:.2f} ms / frame")
    print(f"DPU Average Inference Time: {dpu_avg_time*1000:.2f} ms / frame")

    speedup = cpu_avg_time / dpu_avg_time if dpu_avg_time > 0 else 0
    print(f"-> Speedup Score:  {speedup:.1f}x Faster on DPU!\n")

    if recorder:
        cpu_power, dpu_power = get_average_power(recorder)
        if cpu_power > 0 and dpu_power > 0:
            cpu_energy = cpu_power * cpu_avg_time
            dpu_energy = dpu_power * dpu_avg_time
            energy_eff = cpu_energy / dpu_energy if dpu_energy > 0 else 0
            
            print(f"CPU Average Power: {cpu_power:.2f} W  --> Energy per Image: {cpu_energy * 1000:.2f} mJ")
            print(f"DPU Average Power: {dpu_power:.2f} W  --> Energy per Image: {dpu_energy * 1000:.2f} mJ")
            print(f"-> Energy Efficiency: {energy_eff:.1f}x More Efficient on DPU!\n")

