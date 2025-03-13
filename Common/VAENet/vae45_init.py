import os

import numpy as numpy
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import Dataset, DataLoader, random_split
import pytorch_lightning as pl

import sys
import datetime

from torchvision import datasets, transforms

pl.seed_everything()

#-----------------------------------------------------------------------------#
#    IMAGE PREPROCESSING                                                      #
#-----------------------------------------------------------------------------#

## DIRECTORIES with datasets
img_path = 'dataset'


# Dataset with Transformation
dataset = datasets.ImageFolder(
    img_path,
    transforms.Compose([
        transforms.Resize((128, 256)),
        transforms.ToTensor(),
        transforms.Normalize(
              mean=[0.0, 0.0, 0.0], 
              std=[1.0, 1.0, 1.0])])
)



# Data split
trainpctg  = 0.8
train_size = int(trainpctg * len(dataset))
test_size = len(dataset) - train_size
trainset, testset = random_split(dataset, [train_size, test_size])

print(f"Training set size: {len(trainset)}, Testing set size: {len(testset)}")


#-----------------------------------------------------------------------------#
#    DATA LOADER                                                              #
#-----------------------------------------------------------------------------#

# For a smaller subset
smallsz     = 50
subidx      = numpy.random.choice(len(trainset), smallsz, replace=False)
trainsubset = torch.utils.data.Subset(trainset, subidx)
subidx      = numpy.random.choice(len(testset),  smallsz, replace=False)
testsubset  = torch.utils.data.Subset(testset, subidx)

large = True
batchsz  = 64
sys_workers = int(os.getenv("SLURM_CPUS_PER_TASK", 4))  # Default to 4 if not set


# Data Loaderd
if large:
    trainloader = DataLoader(trainset, 
                             batch_size=batchsz, 
                             shuffle=True, 
                             drop_last=True, 
                             num_workers=sys_workers, 
                             pin_memory=True, 
                             prefetch_factor=2)
    testloader = DataLoader(testset,
                            batch_size=batchsz,
                            shuffle=False,
                            drop_last=False,
                            num_workers=sys_workers,
                            pin_memory=True)  # Optional but recommended if using a GPU
else:
    trainloader = DataLoader(trainsubset, batch_size=1, shuffle=True, num_workers=sys_workers)
    testloader = DataLoader(testsubset , batch_size=1, shuffle=False, num_workers=sys_workers)

# print(dataset)
# print(dataloader)
print("Min/Max:", dataset[0][0].min(), dataset[0][0].max())

#-----------------------------------------------------------------------------#
#    TRAINING                                                                 #
#-----------------------------------------------------------------------------#

## Import working model / N.B.
import vae_model_relu as vaemodel
# import vae_model_new as vaemodel
model = vaemodel.vaemodel1()

# model file name
fname = model.__class__.__name__

# TRAINING 
logger = pl.loggers.TensorBoardLogger('lightning_logs', 'vaelog/'+fname)
trainer = pl.Trainer(accelerator="auto", devices=1, max_epochs=1000, check_val_every_n_epoch=10, log_every_n_steps=50, logger=logger)
trainer.fit(model, train_dataloaders=trainloader, val_dataloaders=testloader, ckpt_path="last")
# trainer.save_checkpoint("last")

#-----------------------------------------------------------------------------#
#    SAVE TRAINED MODELS                                                      #
#-----------------------------------------------------------------------------#

# SAVE Trained MODEL
save_path ='./'
torch.save(model.state_dict(), save_path+'state_'+fname+'.st')
torch.save(model, save_path+fname+'.pth')
print('Model saved:'+fname)



