import torch
import torch.nn as nn
from sklearn.metrics import confusion_matrix, f1_score

class EspertaPyTorch(nn.Module):
    """
    PyTorch implementation optimized for ONNX conversion
    """
    def __init__(self, weights, threshold):
        super().__init__()
        self.threshold = threshold
        
        # Define linear layer with fixed weights
        self.linear = nn.Linear(in_features=4, out_features=1, bias=False)
        
        with torch.no_grad():
            self.linear.weight = nn.Parameter(torch.tensor(weights, dtype=torch.float32).view(1, -1))
        
        # Freeze parameters
        for param in self.parameters():
            param.requires_grad_(False)

    def forward(self, x):
        """Directly returns binary predictions with thresholding"""
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x, dtype=torch.float32)
            
        # Compute probabilities
        probabilities = torch.sigmoid(self.linear(x))
        
        # Apply threshold and convert to binary
        return (probabilities > self.threshold).float()

def ConfMatrix(predictions, true_labels):
    return confusion_matrix(true_labels, predictions)

def get_scores(predictions, true_labels):
    """
    Calculate performance metrics
    Note: Convert tensors to numpy arrays if needed
    """
    if isinstance(predictions, torch.Tensor):
        predictions = predictions.numpy()
    if isinstance(true_labels, torch.Tensor):
        true_labels = true_labels.numpy()
        
    C = ConfMatrix(predictions, true_labels)
    POD_score = C[1, 1] / (C[1, 1] + C[0, 1])
    FAR_score = C[1, 0] / (C[1, 1] + C[1, 0])
    f1 = f1_score(true_labels, predictions)
    return POD_score, FAR_score, f1


class MultiEsperta(nn.Module):
    """
    Compound model containing all 6 ESPERTA configurations
    Handles parallel inference across all models
    """
    def __init__(self, configurations):
        super().__init__()
        self.models = nn.ModuleList()
        
        # Configuration format: [(weights, threshold), ...]
        for weights, threshold in configurations:
            model = EspertaPyTorch(weights, threshold)
            self.models.append(model)

    def forward(self, x):
        """Returns predictions from all models in parallel"""
        # Input shape: (batch_size, 4)
        # Output shape: (batch_size, 6) - one column per model
        return torch.cat([model(x) for model in self.models], dim=1)
