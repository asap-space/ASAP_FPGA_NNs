# import numpy
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
import sys

# from torch.utils.data import DataLoader, Dataset
# -------------------------#
# PyTorch Lightning model #
# -------------------------#


class vaemodel1(pl.LightningModule):
    def __init__(self, latent_dim=64):

        super().__init__()
        self.ld = latent_dim

        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(16),
            nn.Softplus(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(32),
            nn.Softplus(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(64),
            nn.Softplus(),
            nn.Conv2d(64, 128, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(128),
            nn.Softplus(),
            nn.Conv2d(128, 256, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(256),
            nn.Softplus(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
        )

        self.mu = nn.Linear(256, self.ld)  # Reduced latent space size
        self.std = nn.Linear(256, self.ld)  # Reduced latent space size

    def encode(self, x):
        a = self.encoder(x)
        mu = self.mu(a)
        lvar = self.std(a)
        return a, mu, lvar

    def forward(self, x):
        z, mu, lvar = self.encode(x)
        return z, mu, lvar
