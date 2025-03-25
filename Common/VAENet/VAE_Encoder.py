import torch
import torch.nn as nn

class vae_encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 256, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.mu = nn.Linear(256, 6)  # Reduced latent space size
        self.std = nn.Linear(256, 6)  # Reduced latent space size

    def forward(self, x):
        a = self.encoder(x).permute(0,2,3,1)
        a = torch.flatten(a, start_dim=1)
        mu = self.mu(a)
        lvar = self.std(a)
        out = torch.cat((mu, lvar), dim=1)
        return out