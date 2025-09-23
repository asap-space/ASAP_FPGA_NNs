import torch
import torch.nn as nn
import torch.nn.functional as F

class CNetPlusScalar(nn.Module):
    """
    CNetPlusScalar inherits from CNet but rewrites the forward method by introducing a scalar value to the output.
    The difference is that x is now a dictionary with the key 'image' and 'scalar'.
    old CNN applicable to 512x512 images

    Compared to the original CNet, this model assumes only one extra feature (scalar) to be concatenated to the output of the last convolutional layer and one input channel. This extra feature is the background value. Furthermore, the original leaky ReLU activation function is replaced by the ReLU activation function.
    """
    def __init__(self):
        super().__init__()
        self.pool = nn.MaxPool2d(2, 2) 
        self.conv1 = nn.Conv2d(1, 6, 5) 
        self.conv2 = nn.Conv2d(6, 16, 5) 
        self.conv3 = nn.Conv2d(16, 32, 5) 
        self.conv4 = nn.Conv2d(32, 32, 5)
        self.fc1 = nn.Linear(32 * 28 * 28, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84+1, 1)

    def forward(self, image, scalar):
        x = self.pool(F.relu(self.conv1(image))) 
        x = self.pool(F.relu(self.conv2(x))) 
        x = self.pool(F.relu(self.conv3(x))) 
        x = self.pool(F.relu(self.conv4(x))) 
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = torch.cat((x, scalar), dim=1) # adding the scalar value
        x = self.fc3(x)
        return x
