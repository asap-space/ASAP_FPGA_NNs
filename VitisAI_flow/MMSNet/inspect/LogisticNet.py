# GENETARED BY NNDCT, DO NOT EDIT!

import torch
from torch import tensor
import pytorch_nndct as py_nndct

class LogisticNet(py_nndct.nn.NndctQuantModel):
    def __init__(self):
        super(LogisticNet, self).__init__()
        self.module_0 = py_nndct.nn.Input() #LogisticNet::input_0(LogisticNet::nndct_input_0)
        self.module_1 = py_nndct.nn.Module('aten::max_pool3d') #LogisticNet::LogisticNet/MaxPool3d[pol1]/ret.3(LogisticNet::aten_max_pool3d_1)
        self.module_2 = py_nndct.nn.Module('nndct_flatten') #LogisticNet::LogisticNet/ret.5(LogisticNet::nndct_flatten_2)
        self.module_3 = py_nndct.nn.Linear(in_features=2048, out_features=4, bias=True) #LogisticNet::LogisticNet/Linear[fc1]/ret.7(LogisticNet::nndct_dense_3)
        self.module_4 = py_nndct.nn.Softmax(dim=1) #LogisticNet::LogisticNet/Softmax[act1]/ret(LogisticNet::nndct_softmax_4)

    @py_nndct.nn.forward_processor
    def forward(self, *args):
        output_module_0 = self.module_0(input=args[0])
        output_module_0 = self.module_1({'self': output_module_0,'kernel_size': [2,2,2],'stride': [2,2,2],'padding': [0,0,0],'dilation': [1,1,1],'ceil_mode': False})
        output_module_0 = self.module_2(input=output_module_0, start_dim=1, end_dim=-1)
        output_module_0 = self.module_3(output_module_0)
        output_module_0 = self.module_4(output_module_0)
        return output_module_0
