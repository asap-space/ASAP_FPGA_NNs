import torch
import torch.nn as nn
import torch.optim as optim


class LogisticNet(nn.Module):
    def __init__(self):
        super(LogisticNet, self).__init__()
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(2048, 4)
        self.act1 = nn.Softmax(dim=1)

    def forward(self, input):
        p1 = self.pol1(input)
        p1 = torch.flatten(p1, 1)
        s1 = self.fc1(p1)
        output = self.act1(s1)
        return output


def train(net, dataset_loader):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=1e-5)  # in your training loop:
    for epoch in range(2):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(dataset_loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                print(f"[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}")
                running_loss = 0.0

    print("Finished Training")


def test():
    # TO DO
    return


def load_dataset():
    # TO DO
    training_dataset_loader = 0
    test_dataset_loader = 0
    return training_dataset_loader, test_dataset_loader


net = LogisticNet()
print(net)
params = list(net.parameters())
print(len(params))
print(params[0].size())
