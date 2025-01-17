import sys
import torch
import torch.nn as nn
import torch.optim as optim

import brevitas.nn as qnn
from brevitas.export import export_onnx_qcdq


class LogisticNet(nn.Module):
    def __init__(self):
        super(LogisticNet, self).__init__()
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.QuantLinear(2048, 4, bias=True, weight_bit_width=4)
        self.act1 = nn.Softmax(dim=1)

    def forward(self, input):
        out = self.pol1(input)
        out = torch.flatten(out, 1)
        out = self.fc1(out)
        out = self.act1(out)
        return out


class ReducedNet(nn.Module):
    def __init__(self):
        super(ReducedNet, self).__init__()
        self.cv1 = nn.QuantConv3d(
            1, 1, kernel_size=(5, 3, 5), stride=(2, 1, 2), padding=0, weight_bit_width=4
        )
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.QuantLinear(343, 128, weight_bit_width=4)
        self.act1 = nn.ReLU()
        self.fc2 = nn.QuantLinear(128, 4, weight_bit_width=4)
        self.act2 = nn.Softmax(dim=1)

    def forward(self, input):
        c1 = self.cv1(input)
        p1 = self.pol1(c1)
        s1 = self.fc1(torch.flatten(p1, 1))
        a1 = self.act1(s1)
        s2 = self.fc2(a1)
        output = self.act2(s2)
        return output


class BaselineNet(nn.Module):
    def __init__(self):
        super(BaselineNet, self).__init__()
        self.cv1 = nn.QuantConv3d(
            1,
            32,
            kernel_size=(5, 3, 5),
            stride=(2, 1, 2),
            padding=0,
            weight_bit_width=4,
        )
        self.cv2 = nn.QuantConv3d(
            32,
            32,
            kernel_size=(3, 3, 3),
            stride=(1, 1, 1),
            padding=0,
            weight_bit_width=4,
        )
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.QuantLinear(6912, 128, weight_bit_width=4)
        self.act1 = nn.ReLU()
        self.fc2 = nn.QuantLinear(128, 4, weight_bit_width=4)
        self.act2 = nn.Softmax(dim=1)

    def forward(self, input):
        c1 = self.cv1(input)
        c2 = self.cv2(c1)
        p1 = self.pol1(c2)
        s1 = self.fc1(torch.flatten(p1, 1))
        a1 = self.act1(s1)
        s2 = self.fc2(a1)
        output = self.act2(s2)
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


def export_ONNX(model):
    tensor_x = torch.rand((1, 1, 32, 16, 32))
    export_onnx_qcdq(
        model,
        (tensor_x,),
        f"ONNX_model/{model.__class__.__name__}.onnx",  # filename of the ONNX model
        input_names=["input"],  # Rename inputs for the ONNX model
        dynamo=False,  # True or False to select the exporter to use
    )


def usage(possible_NN):
    print(f"Usage: python NetGen.py <model_name>")
    print(f"Available models: {', '.join(possible_NN)}")


def main():
    possible_NN = {
        "Baseline": BaselineNet,
        "Reduced": ReducedNet,
        "Logistic": LogisticNet,
    }

    if (len(sys.argv) != 2) or sys.argv[-1] not in possible_NN:
        usage(possible_NN.keys())
        exit(-1)

    # Dynamically select and call the appropriate network function/class
    selected_model = sys.argv[-1]
    net = possible_NN[selected_model]()
    print(net)
    params = list(net.parameters())
    # print(len(params))
    # print(params[0].size())
    print(params)
    export_ONNX(net)
    exit()


if __name__ == "__main__":
    main()
