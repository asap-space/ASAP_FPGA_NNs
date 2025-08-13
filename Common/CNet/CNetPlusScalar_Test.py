import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import datasets, transforms
import numpy as np
from CNetPlusScalar import CNetPlusScalar

class RandomDataset(Dataset):
    def __init__(self, num_samples: int):
        self.img = torch.randn(num_samples, 1, 512, 512)
        self.scalar = torch.randn(num_samples, 1)
        self.label = torch.randn(num_samples, 1)

    def __len__(self):
        return len(self.img)

    def __getitem__(self, idx):
        image = self.img[idx]
        scalar = self.scalar[idx]
        label = self.label[idx]
        return image, scalar, label

def main():
    dataset = RandomDataset(1000)
    dataloader = DataLoader(dataset , batch_size=1, shuffle=False, num_workers=1)

    model = CNetPlusScalar()
    model.load_state_dict(torch.load('pre_trained_w.pt', weights_only=True))

    print("Passed Here!!")

    model.eval()
    with torch.no_grad():
        cpu_output = []
        for image, scalar, _ in dataloader:
            # Run inference for each image individually
            pred = model(image, scalar)
            cpu_output.append(pred)

    # Convert list to numpy array
    cpu_output = np.array(cpu_output)

    output_min = cpu_output.min()
    output_max = cpu_output.max()
    output_range = output_max - output_min
    print(f"Output range: min={output_min:.6f}, max={output_max:.6f}, difference={output_range:.6f}")

if __name__ == "__main__":
    main()