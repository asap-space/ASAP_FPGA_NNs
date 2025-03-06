#import numpy
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
import sys

# from torch.utils.data import DataLoader, Dataset
#-------------------------#
# PyTorch Lightning model #
#-------------------------#

class vaemodel1(pl.LightningModule):
    def __init__(self, 
                 lr: float = 5e-4, 
                 beta = 2.5, 
                 latent_dim = 64, 
                 **kwargs):
        
        super().__init__()
        self.lr = lr
        self.betavae = beta
        self.ld = latent_dim

        self.encoder = nn.Sequential(
            nn.BatchNorm2d(3),
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

        self.decoder = nn.Sequential(
            nn.Linear(self.ld, 256),  # Adjusted for reduced latent space size
            nn.Softplus(),
            nn.Linear(256, 512),
            nn.Softplus(),
            nn.Linear(512, 4*8*self.ld),  # Adjusted for reduced latent space size
            nn.Softplus(),
            nn.Unflatten(-1, torch.Size([self.ld, 4, 8])),
            nn.ConvTranspose2d(self.ld, 64, 3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(64),
            nn.Softplus(),
            nn.ConvTranspose2d(64, 32, 3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(32),
            nn.Softplus(),
            nn.ConvTranspose2d(32, 16, 3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(16),
            nn.Softplus(),
            nn.ConvTranspose2d(16, 8, 3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(8),
            nn.Softplus(),
            nn.ConvTranspose2d(8, 3, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid(),
            nn.AdaptiveAvgPool2d((128, 256))
        )


    def encode(self, x):
        a    = self.encoder(x)
        mu   = self.mu(a)
        lvar = self.std(a)

        # Reparametrization
        std  = torch.exp(lvar*0.5)
        eps  = torch.randn_like(std)
        z    = mu + eps * std
        return z, mu, lvar

    def decode(self, z, in_shape):
        return self.decoder(z)

    def forward(self, x):
        in_shape = list(x.shape)
        z, mu, lvar = self.encode(x)
        y = self.decode(z, in_shape)
        #y = self.decode(z)
        return y, mu, lvar

    def lossfct(self, y, x, mu, lvar):
        # BCE = F.binary_cross_entropy(y, x, size_average=False)
        BCE = F.binary_cross_entropy(y, x, reduction='sum')  # or reduction='mean'
        KLD = -0.5 * self.betavae * torch.sum(1 + lvar - mu.pow(2) - lvar.exp())
        return BCE + KLD, BCE, KLD

#####
    def training_step(self, batch, batch_idx):
        x, y = batch
        y, mu, lvar = self.forward(x)
        lossVAE,lossbce,losskld = self.lossfct(y, x, mu, lvar)
        loss = lossVAE
        self.log('train_loss', loss)
        self.log('BCE_loss', lossbce)
        self.log('KLD_loss',losskld)
        self.logger.experiment.add_scalar("Loss TOT", loss,    self.current_epoch)
        self.logger.experiment.add_scalar("Loss BCE", lossbce, self.current_epoch)
        self.logger.experiment.add_scalar("Loss KLD", losskld, self.current_epoch)
        return loss

    def validation_step(self, batch, batch_ix):
        x, y = batch
        y, mu, lvar = self.forward(x)
        lossVAE,_,_ = self.lossfct(y, x, mu, lvar)
        loss = lossVAE
        self.log('tests_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr, weight_decay=5e-3)

    def predict_step(self, batch, batch_idx):
        x, y = batch
        y, mu, lvar = self.forward(x)
        lossVAE,_,_ = self.lossfct(y, x, mu, lvar)
        loss = lossVAE
        return loss





