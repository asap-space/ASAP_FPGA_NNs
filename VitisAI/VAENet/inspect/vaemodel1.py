# GENETARED BY NNDCT, DO NOT EDIT!

import torch
import pytorch_nndct as py_nndct
class vaemodel1(torch.nn.Module):
    def __init__(self):
        super(vaemodel1, self).__init__()
        self.module_0 = py_nndct.nn.Input() #vaemodel1::input_0
        self.module_1 = py_nndct.nn.Conv2d(in_channels=3, out_channels=16, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[0]/input.3
        self.module_2 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[2]/input.7
        self.module_3 = py_nndct.nn.Conv2d(in_channels=16, out_channels=32, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[3]/input.9
        self.module_4 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[5]/input.13
        self.module_5 = py_nndct.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[6]/input.15
        self.module_6 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[8]/input.19
        self.module_7 = py_nndct.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[9]/input.21
        self.module_8 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[11]/input.25
        self.module_9 = py_nndct.nn.Conv2d(in_channels=128, out_channels=256, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[12]/input.27
        self.module_10 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[14]/input.31
        self.module_11 = py_nndct.nn.AdaptiveAvgPool2d(output_size=1) #vaemodel1::vaemodel1/Sequential[encoder]/AdaptiveAvgPool2d[15]/719
        self.module_12 = py_nndct.nn.Module('permute') #vaemodel1::vaemodel1/725
        self.module_13 = py_nndct.nn.Module('flatten') #vaemodel1::vaemodel1/input
        self.module_14 = py_nndct.nn.Linear(in_features=256, out_features=64, bias=True) #vaemodel1::vaemodel1/Linear[mu]/729
        self.module_15 = py_nndct.nn.Linear(in_features=256, out_features=64, bias=True) #vaemodel1::vaemodel1/Linear[std]/730
        self.module_16 = py_nndct.nn.Cat() #vaemodel1::vaemodel1/733

    def forward(self, *args):
        output_module_0 = self.module_0(input=args[0])
        output_module_0 = self.module_1(output_module_0)
        output_module_0 = self.module_2(output_module_0)
        output_module_0 = self.module_3(output_module_0)
        output_module_0 = self.module_4(output_module_0)
        output_module_0 = self.module_5(output_module_0)
        output_module_0 = self.module_6(output_module_0)
        output_module_0 = self.module_7(output_module_0)
        output_module_0 = self.module_8(output_module_0)
        output_module_0 = self.module_9(output_module_0)
        output_module_0 = self.module_10(output_module_0)
        output_module_0 = self.module_11(output_module_0)
        output_module_0 = self.module_12(dims=[0,2,3,1], input=output_module_0)
        output_module_0 = self.module_13(input=output_module_0, start_dim=1, end_dim=3)
        output_module_14 = self.module_14(output_module_0)
        output_module_15 = self.module_15(output_module_0)
        output_module_14 = self.module_16(dim=1, tensors=[output_module_14,output_module_15])
        return output_module_14
