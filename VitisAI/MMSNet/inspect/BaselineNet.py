# GENETARED BY NNDCT, DO NOT EDIT!

import torch
from torch import tensor
import pytorch_nndct as py_nndct

class BaselineNet(py_nndct.nn.NndctQuantModel):
    def __init__(self):
        super(BaselineNet, self).__init__()
        self.module_0 = py_nndct.nn.Input() #BaselineNet::input_0(BaselineNet::nndct_input_0)
        self.module_1 = py_nndct.nn.Conv3d(in_channels=1, out_channels=32, kernel_size=[5, 3, 5], stride=[2, 1, 2], padding=[0, 0, 0], dilation=[1, 1, 1], groups=1, bias=True) #BaselineNet::BaselineNet/Conv3d[cv1]/ret.3(BaselineNet::nndct_conv3d_1)
        self.module_2 = py_nndct.nn.Conv3d(in_channels=32, out_channels=32, kernel_size=[3, 3, 3], stride=[1, 1, 1], padding=[0, 0, 0], dilation=[1, 1, 1], groups=1, bias=True) #BaselineNet::BaselineNet/Conv3d[cv2]/ret.5(BaselineNet::nndct_conv3d_2)
        self.module_3 = py_nndct.nn.Module('aten::max_pool3d') #BaselineNet::BaselineNet/MaxPool3d[pol1]/ret.7(BaselineNet::aten_max_pool3d_3)
        self.module_4 = py_nndct.nn.Module('nndct_flatten') #BaselineNet::BaselineNet/ret.9(BaselineNet::nndct_flatten_4)
        self.module_5 = py_nndct.nn.Linear(in_features=6912, out_features=128, bias=True) #BaselineNet::BaselineNet/Linear[fc1]/ret.11(BaselineNet::nndct_dense_5)
        self.module_6 = py_nndct.nn.ReLU(inplace=False) #BaselineNet::BaselineNet/ReLU[act1]/ret.13(BaselineNet::nndct_relu_6)
        self.module_7 = py_nndct.nn.Linear(in_features=128, out_features=4, bias=True) #BaselineNet::BaselineNet/Linear[fc2]/ret.15(BaselineNet::nndct_dense_7)
        self.module_8 = py_nndct.nn.Softmax(dim=1) #BaselineNet::BaselineNet/Softmax[act2]/ret(BaselineNet::nndct_softmax_8)

    @py_nndct.nn.forward_processor
    def forward(self, *args):
        output_module_0 = self.module_0(input=args[0])
        output_module_0 = self.module_1(output_module_0)
        output_module_0 = self.module_2(output_module_0)
        output_module_0 = self.module_3({'self': output_module_0,'kernel_size': [2,2,2],'stride': [2,2,2],'padding': [0,0,0],'dilation': [1,1,1],'ceil_mode': False})
        output_module_0 = self.module_4(input=output_module_0, start_dim=1, end_dim=-1)
        output_module_0 = self.module_5(output_module_0)
        output_module_0 = self.module_6(output_module_0)
        output_module_0 = self.module_7(output_module_0)
        output_module_0 = self.module_8(output_module_0)
        return output_module_0
