# GENETARED BY NNDCT, DO NOT EDIT!

import torch
import pytorch_nndct as py_nndct
class CNetPlusScalar_simple_noback(torch.nn.Module):
    def __init__(self):
        super(CNetPlusScalar_simple_noback, self).__init__()
        self.module_0 = py_nndct.nn.Input() #CNetPlusScalar_simple_noback::input_0
        self.module_1 = py_nndct.nn.Conv2d(in_channels=3, out_channels=3, kernel_size=[5, 5], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Conv2d[conv1]/579
        self.module_2 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/580
        self.module_3 = py_nndct.nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], dilation=[1, 1], ceil_mode=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/MaxPool2d[pool]/input.3
        self.module_4 = py_nndct.nn.Conv2d(in_channels=3, out_channels=3, kernel_size=[3, 3], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Conv2d[conv2]/613
        self.module_5 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/614
        self.module_6 = py_nndct.nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], dilation=[1, 1], ceil_mode=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/MaxPool2d[pool]/input.5
        self.module_7 = py_nndct.nn.Conv2d(in_channels=3, out_channels=3, kernel_size=[3, 3], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Conv2d[conv3]/647
        self.module_8 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/648
        self.module_9 = py_nndct.nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], dilation=[1, 1], ceil_mode=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/MaxPool2d[pool]/input.7
        self.module_10 = py_nndct.nn.Conv2d(in_channels=3, out_channels=3, kernel_size=[3, 3], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Conv2d[conv4]/681
        self.module_11 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/682
        self.module_12 = py_nndct.nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], dilation=[1, 1], ceil_mode=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/MaxPool2d[pool]/input.9
        self.module_13 = py_nndct.nn.Conv2d(in_channels=3, out_channels=3, kernel_size=[3, 3], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Conv2d[conv5]/715
        self.module_14 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/716
        self.module_15 = py_nndct.nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], dilation=[1, 1], ceil_mode=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/MaxPool2d[pool]/input.11
        self.module_16 = py_nndct.nn.Conv2d(in_channels=3, out_channels=3, kernel_size=[3, 3], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Conv2d[conv6]/749
        self.module_17 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/750
        self.module_18 = py_nndct.nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], dilation=[1, 1], ceil_mode=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/MaxPool2d[pool]/input.13
        self.module_19 = py_nndct.nn.Conv2d(in_channels=3, out_channels=3, kernel_size=[3, 3], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Conv2d[conv7]/783
        self.module_20 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/784
        self.module_21 = py_nndct.nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], dilation=[1, 1], ceil_mode=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/MaxPool2d[pool]/798
        self.module_22 = py_nndct.nn.Module('flatten') #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/input.15
        self.module_23 = py_nndct.nn.Linear(in_features=12, out_features=30, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Linear[fc1]/802
        self.module_24 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/input.17
        self.module_25 = py_nndct.nn.Linear(in_features=30, out_features=30, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Linear[fc2]/804
        self.module_26 = py_nndct.nn.ReLU(inplace=False) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/input
        self.module_27 = py_nndct.nn.Linear(in_features=30, out_features=1, bias=True) #CNetPlusScalar_simple_noback::CNetPlusScalar_simple_noback/Linear[fc3]/806

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
        output_module_0 = self.module_12(output_module_0)
        output_module_0 = self.module_13(output_module_0)
        output_module_0 = self.module_14(output_module_0)
        output_module_0 = self.module_15(output_module_0)
        output_module_0 = self.module_16(output_module_0)
        output_module_0 = self.module_17(output_module_0)
        output_module_0 = self.module_18(output_module_0)
        output_module_0 = self.module_19(output_module_0)
        output_module_0 = self.module_20(output_module_0)
        output_module_0 = self.module_21(output_module_0)
        output_module_0 = self.module_22(input=output_module_0, start_dim=1, end_dim=3)
        output_module_0 = self.module_23(output_module_0)
        output_module_0 = self.module_24(output_module_0)
        output_module_0 = self.module_25(output_module_0)
        output_module_0 = self.module_26(output_module_0)
        output_module_0 = self.module_27(output_module_0)
        return output_module_0
