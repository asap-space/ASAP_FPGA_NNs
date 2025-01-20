import sys, os
import torch
import torch.nn as nn
import torch.optim as optim


# Setting seeds for reproducibility
seed = 84
torch.manual_seed(seed)

class LogisticNet(nn.Module):
    def __init__(self):
        super(LogisticNet, self).__init__()
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(2048, 4)
        self.act1 = nn.Softmax(dim=1)

    def forward(self, input):
        p1 = torch.flatten(self.pol1(input), 1)
        s1 = self.fc1(p1)
        output = self.act1(s1)
        return output


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
        self.cv1 = nn.Conv3d(1, 32, kernel_size=(5, 3, 5), stride=(2, 1, 2), padding=0)
        self.cv2 = nn.Conv3d(32, 32, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=0)
        self.pol1 = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(6912, 128)
        self.act1 = nn.ReLU()
        self.fc2 = nn.Linear(128, 4)
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


def load_pretrained_weights(net, weight_file):
    """
    Loads pre-trained weights into a PyTorch model.

    Args:
        net (torch.nn.Module): The PyTorch model to load the weights into.
        weight_file (str): The file path to the pre-trained weights file.

    Raises:
        FileNotFoundError: If the weight file does not exist.
        RuntimeError: If the weight file is not compatible with the model.
    """
    if not os.path.exists(weight_file):
        raise FileNotFoundError(f"Weight file not found: {weight_file}")

    try:
        net.load_state_dict(torch.load(weight_file, weights_only=True, map_location=torch.device('cpu')))
    except RuntimeError as e:
        raise RuntimeError(f"Error loading weights: {e}")


def export_ONNX(model):
    """
    Exports a PyTorch model to the ONNX format.

    Args:
        model (torch.nn.Module): The PyTorch model to be exported.
                                 The model must be compatible with ONNX export.

    Workflow:
        1. Creates a dummy input tensor of shape `(1, 1, 32, 16, 32)` with `float32` data type.
        2. Exports the model to an ONNX file named after the model's class, stored in the
           "ONNX_model" directory.
        3. Configures input names for the ONNX model as `["input"]`.
        4. Uses the `torch.onnx.export` function for the conversion, with the `dynamo` option disabled.

    ONNX Export Details:
        - File Path: "ONNX_model/<model_class_name>.onnx"
        - Input Names: `["input"]`
        - Exporter Type: Controlled by the `dynamo` parameter (currently set to `False`).

    Note:
        Ensure that the "ONNX_model" directory exists before calling this function,
        or the export will fail.

    Example:
        from your_module import MyModel
        model = MyModel()
        export_ONNX(model)

    Raises:
        RuntimeError: If the model cannot be exported due to unsupported operations or configuration issues.
        FileNotFoundError: If the output directory does not exist.

    Dependencies:
        - PyTorch (`torch`)
        - ONNX Runtime (optional, for testing the exported model)

    """
    tensor_x = torch.rand((1, 1, 32, 16, 32), dtype=torch.float32)
    torch.onnx.export(
        model,
        (tensor_x,),
        f"ONNX_model/{model.__class__.__name__}.onnx",  # filename of the ONNX model
        input_names=["input"],  # Rename inputs for the ONNX model
        dynamo=False,  # True or False to select the exporter to use
    )


def usage(possible_NN):
    """
    Prints usage instructions for the script.

    Args:
        possible_NN (iterable): A list or iterable containing the names of the possible models
                                that can be selected (e.g., ["Baseline", "Reduced", "Logistic"]).

    Example:
        usage(["Baseline", "Reduced", "Logistic"])
        # Output:
        # Usage: python NetGen.py (optional: --pretrained_weights <weight_file>) <model_name>
        # Available models: Baseline, Reduced, Logistic
    """
    print(
        f"Usage: python NetGen.py (optional: --pretrained_weights <weight_file>) <model_name>"
    )
    print(f"Available models: {', '.join(possible_NN)}")


def main():
    """
    The main function of the script. It selects and initializes a specific neural network model
    based on the command-line argument.

    Command-line Usage:
        python NetGen.py (optional: --pretrained_weights <weight_file>) <model_name>

    Models Available:
        - Baseline
        - Reduced
        - Logistic

    Steps:
        1. Checks the command-line arguments to ensure a valid model name is provided.
        2. Dynamically selects and initializes the corresponding model.
        3. Prints the selected model and its instance.

    Exits:
        - Exits with code -1 if no valid model name is provided.

    Example:
        Command:
            python script.py Logistic
        Output:
            Selected model: Logistic
            LogisticNet instance created
    """
    possible_NN = {
        "Baseline": BaselineNet,
        "Reduced": ReducedNet,
        "Logistic": LogisticNet,
    }

    if sys.argv[-1] not in possible_NN:
        usage(possible_NN.keys())
        exit(-1)

    # Dynamically select and call the appropriate network function/class
    selected_model = sys.argv[-1]
    net = possible_NN[selected_model]()

    if "--pretrained_weights" in sys.argv:
        weight_file = sys.argv[sys.argv.index("--pretrained_weights") + 1]
        print(f"Using pre-trained weights from: {weight_file}")
        load_pretrained_weights(net, weight_file)

    compare_net = torch.load(weight_file, map_location=torch.device('cpu'))
    print(compare_net)
    print(net)
    params = list(net.parameters())
    # print(len(params))
    # print(params[0].size())
    print(params)
    torch.save(net.state_dict(), f"PreTrained_Weights/{net.__class__.__name__}_{seed}.pth")
    export_ONNX(net)
    exit()


if __name__ == "__main__":
    main()
