import torch
import numpy

old_model = 'PreTrained_Weights/models_baseline/model_baseline_s-42.pth'
old_model2 = '../PreTrained_Weights/models_reduced/model_reduced_s-42.pth'
new_model = 'PreTrained_Weights/BaselineNet_42.pth'

old_dict = torch.load(old_model, map_location=torch.device('cpu'))
print(old_dict)
new_dict = {}
new_dict['fc1.weight'] = old_dict['encoder.2.weight']
new_dict['fc1.bias'] = old_dict['encoder.2.bias']
torch.save(new_dict, new_model)
print(torch.load(new_model, map_location=torch.device('cpu')))
print('Done')

## Check if new pretrained weights are working
dict1 = torch.load("../mms-classification-nn/models_baseline/model_baseline_s-336.pth", weights_only=True, map_location=torch.device("cpu"))
dict2 = torch.load("PreTrained_weights/BaselineNet_336.pth", weights_only=True, map_location=torch.device("cpu"))
numpy.array_equal(dict1['encoder.0.weight'], dict2['cv1.weight'])

dict1 = torch.load("../mms-classification-nn/models_logistc/model_logistc_s-84.pth", weights_only=True, map_location=torch.device("cpu"))
dict2 = torch.load("PreTrained_weights/LogisticNet_84.pth", weights_only=True, map_location=torch.device("cpu"))
numpy.array_equal(dict1['encoder.2.weight'], dict2['fc1.weight'])
