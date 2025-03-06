# GENETARED BY NNDCT, DO NOT EDIT!

import torch
from torch import tensor
import pytorch_nndct as py_nndct

class vaemodel1(py_nndct.nn.NndctQuantModel):
    def __init__(self):
        super(vaemodel1, self).__init__()
        self.module_0 = py_nndct.nn.Module('nndct_const') #vaemodel1::1044(vaemodel1::nndct_const_0)
        self.module_1 = py_nndct.nn.Input() #vaemodel1::input_0(vaemodel1::nndct_input_1)
        self.module_2 = py_nndct.nn.Conv2d(in_channels=3, out_channels=16, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[0]/ret.3(vaemodel1::nndct_conv2d_2)
        self.module_3 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[2]/ret.7(vaemodel1::nndct_relu_3)
        self.module_4 = py_nndct.nn.Conv2d(in_channels=16, out_channels=32, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[3]/ret.9(vaemodel1::nndct_conv2d_4)
        self.module_5 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[5]/ret.13(vaemodel1::nndct_relu_5)
        self.module_6 = py_nndct.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[6]/ret.15(vaemodel1::nndct_conv2d_6)
        self.module_7 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[8]/ret.19(vaemodel1::nndct_relu_7)
        self.module_8 = py_nndct.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[9]/ret.21(vaemodel1::nndct_conv2d_8)
        self.module_9 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[11]/ret.25(vaemodel1::nndct_relu_9)
        self.module_10 = py_nndct.nn.Conv2d(in_channels=128, out_channels=256, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #vaemodel1::vaemodel1/Sequential[encoder]/Conv2d[12]/ret.27(vaemodel1::nndct_conv2d_10)
        self.module_11 = py_nndct.nn.ReLU(inplace=False) #vaemodel1::vaemodel1/Sequential[encoder]/ReLU[14]/ret.31(vaemodel1::nndct_relu_11)
        self.module_12 = py_nndct.nn.AdaptiveAvgPool2d(output_size=[1, 1]) #vaemodel1::vaemodel1/Sequential[encoder]/AdaptiveAvgPool2d[15]/996(vaemodel1::nndct_adaptive_avg_pool2d_12)
        self.module_13 = py_nndct.nn.Module('nndct_flatten') #vaemodel1::vaemodel1/Sequential[encoder]/Flatten[16]/ret.33(vaemodel1::nndct_flatten_13)
        self.module_14 = py_nndct.nn.Linear(in_features=256, out_features=64, bias=True) #vaemodel1::vaemodel1/Linear[mu]/ret.35(vaemodel1::nndct_dense_14)
        self.module_15 = py_nndct.nn.Linear(in_features=256, out_features=64, bias=True) #vaemodel1::vaemodel1/Linear[std]/ret.37(vaemodel1::nndct_dense_15)
        self.module_16 = py_nndct.nn.Module('nndct_elemwise_mul') #vaemodel1::vaemodel1/ret.39(vaemodel1::nndct_elemwise_mul_16)
        self.module_17 = py_nndct.nn.Module('nndct_elemwise_exp') #vaemodel1::vaemodel1/ExpModule[exp]/ret.41(vaemodel1::nndct_elemwise_exp_17)
        self.module_18 = py_nndct.nn.Module('aten::zeros_like') #vaemodel1::vaemodel1/ret.43(vaemodel1::aten_zeros_like_18)
        self.module_19 = py_nndct.nn.Module('nndct_elemwise_mul') #vaemodel1::vaemodel1/ret.45(vaemodel1::nndct_elemwise_mul_19)
        self.module_20 = py_nndct.nn.Add() #vaemodel1::vaemodel1/ret(vaemodel1::nndct_elemwise_add_20)

    @py_nndct.nn.forward_processor
    def forward(self, *args):
        output_module_0 = self.module_0(data=0.5, dtype=torch.float, device='cpu')
        output_module_1 = self.module_1(input=args[0])
        output_module_1 = self.module_2(output_module_1)
        output_module_1 = self.module_3(output_module_1)
        output_module_1 = self.module_4(output_module_1)
        output_module_1 = self.module_5(output_module_1)
        output_module_1 = self.module_6(output_module_1)
        output_module_1 = self.module_7(output_module_1)
        output_module_1 = self.module_8(output_module_1)
        output_module_1 = self.module_9(output_module_1)
        output_module_1 = self.module_10(output_module_1)
        output_module_1 = self.module_11(output_module_1)
        output_module_1 = self.module_12(output_module_1)
        output_module_1 = self.module_13(input=output_module_1, start_dim=1, end_dim=-1)
        output_module_14 = self.module_14(output_module_1)
        output_module_15 = self.module_15(output_module_1)
        output_module_15 = self.module_16(input=output_module_15, other=output_module_0)
        output_module_15 = self.module_17(input=output_module_15)
        output_module_18 = self.module_18({'self': output_module_15,'dtype': torch.float,'layout': 0,'device': torch.device('cpu'),'pin_memory': False,'memory_format': None})
        output_module_18 = self.module_19(input=output_module_18, other=output_module_15)
        output_module_14 = self.module_20(input=output_module_14, other=output_module_18, alpha=1)
        return output_module_14
