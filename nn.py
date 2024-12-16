import torch
import torch.nn as nn
import torch.optim as optim


class LogisticNet(nn.Module):
    def __init__(self):
        super(LogisticNet, self).__init__()
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(2048, 4)
        self.act1 = nn.Softmax(dim = 1)    

    def forward(self, input):
        p1 = self.pol1(input)
        p1 = torch.flatten(p1, 1)
        s1 = self.fc1(p1)
        output = self.act1(s1)
        return output

def train(net):
    target = torch.randn(10)  # a dummy target, for example, target is the expected label
    target = target.view(1, -1)  # make it the same shape as output # the size -1 is inferred from other dimensions
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.01)# in your training loop:
    optimizer.zero_grad()   # zero the gradient buffers
    output = net(input)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()    # Does the update

net = LogisticNet()
print(net)
params = list(net.parameters())
print(len(params))
print(params[0].size())
