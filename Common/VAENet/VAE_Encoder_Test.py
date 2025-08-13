import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import datasets, transforms
import numpy as np
from VAE_Encoder import vae_encoder

def main():
    ## DIRECTORIES with datasets
    img_path = 'dataset'
    # Dataset with Transformation (using only 100 images)
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
    dataset = torch.utils.data.Subset(full_dataset, list(range(100)))

    print(f"Dataset size: {len(dataset)}")
    dataloader = DataLoader(dataset , batch_size=1, shuffle=False, num_workers=1)

    model = vae_encoder()
    model.load_state_dict(torch.load('pre_trained_w_encoder.pt', weights_only=True))

    model.eval()
    with torch.no_grad():
        cpu_output = []
        for image, _ in dataloader:
            # Run inference for each image individually
            pred = model(image)
            cpu_output.append(pred)

    # Convert list to numpy array
    cpu_output = np.array(cpu_output)

    output_min = cpu_output.min()
    output_max = cpu_output.max()
    output_range = output_max - output_min
    print(f"Output range: min={output_min:.6f}, max={output_max:.6f}, difference={output_range:.6f}")
    print("Output shape:", cpu_output.shape)
    print("Output:", cpu_output)

if __name__ == "__main__":
    main()