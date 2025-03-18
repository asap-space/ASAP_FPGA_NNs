import torch
import torch.nn as nn
import torch.nn.functional as F

class LogisticNet(nn.Module):
    def __init__(self):
        super(LogisticNet, self).__init__()
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(2048, 4)
        self.act1 = nn.Softmax(dim=1)

    def forward(self, input):
        out = torch.flatten(self.pol1(input), 1)
        out = self.fc1(out)
        #out = self.act1(out)
        return out


class ReducedNet(nn.Module):
    def __init__(self):
        super(ReducedNet, self).__init__()
        self.cv1 = nn.Conv3d(1, 1, kernel_size=(5, 3, 5), stride=(2, 1, 2), padding=0)
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(343, 128)
        self.act1 = nn.ReLU()
        self.fc2 = nn.Linear(128, 4)
        self.act2 = nn.Softmax(dim=1)

    def forward(self, input):
        out = self.cv1(input)
        out = self.pol1(out)
        out = self.fc1(torch.flatten(out, 1))
        out = self.act1(out)
        out = self.fc2(out)
        #out = self.act2(out)
        return out


class BaselineNet(nn.Module):
    def __init__(self):
        super(BaselineNet, self).__init__()
        self.cv1 = nn.Conv3d(1, 32, kernel_size=(5, 3, 5), stride=(2, 1, 2), padding=0)
        self.cv2 = nn.Conv3d(32, 32, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=0)
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(6912, 128)
        self.act1 = nn.ReLU()
        self.fc2 = nn.Linear(128, 4)
        self.act2 = nn.Softmax(dim=1)

    def forward(self, input):
        out = self.cv1(input)
        out = self.cv2(out)
        out = self.pol1(out)
        out = self.fc1(torch.flatten(out, 1))
        out = self.act1(out)
        out = self.fc2(out)
        #out = self.act2(out)
        return out