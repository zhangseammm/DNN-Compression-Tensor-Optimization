# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2021/9/16 23:16

import tensorly as tl
from tensorly.decomposition import parafac, partial_tucker
import numpy as np
import torch
import math
import torch.nn as nn

from torch import Tensor
from torch.nn import Parameter, ParameterList
import torch.nn.functional as F
from torch.nn import init
from torch.nn.modules import Module
from torch.nn.modules.utils import _single, _pair, _triple, _reverse_repeat_tuple
from torch.nn.common_types import _size_1_t, _size_2_t, _size_3_t
from typing import Optional, List, Tuple

tl.set_backend('pytorch')


class TKConv2dC(Module):
    def __init__(self, in_channels, out_channels, ranks,
                 kernel_size, stride=1, padding=0, dilation=1, groups=1,
                 bias=True, padding_mode='zeros',
                 from_dense=False, dense_w=None, dense_b=None):
        super().__init__()

        self.in_channels = in_channels
        self.out_channels = out_channels
        (out_rank, in_rank) = ranks
        self.in_rank = ranks[1]
        self.out_rank = ranks[0]

        # A pointwise convolution that reduces the channels from S to R3
        self.first_conv = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_rank,
                                          kernel_size=1, stride=1, padding=0, dilation=dilation,
                                          groups=groups, bias=False, padding_mode=padding_mode)

        # A regular 2D convolution layer with R3 input channels
        # and R3 output channels
        self.core_conv = torch.nn.Conv2d(in_channels=in_rank, out_channels=out_rank,
                                         kernel_size=kernel_size, stride=stride, padding=padding,
                                         dilation=dilation, groups=groups, bias=False,
                                         padding_mode=padding_mode)

        # A pointwise convolution that increases the channels from R4 to T
        self.last_conv = torch.nn.Conv2d(in_channels=out_rank, out_channels=out_channels,
                                         kernel_size=1, stride=1, padding=0, dilation=dilation,
                                         bias=bias, padding_mode=padding_mode)

        if bias:
            self.bias = Parameter(torch.zeros(out_channels))
        else:
            self.register_parameter('bias', None)

        if from_dense:
            core_tensor, [last_factor, first_factor] = partial_tucker(dense_w, modes=[0, 1],
                                                                      rank=[out_rank, in_rank], init='svd')
            self.first_conv.weight.data = torch.transpose(first_factor, 1, 0).unsqueeze(-1).unsqueeze(-1)
            self.last_conv.weight.data = last_factor.unsqueeze(-1).unsqueeze(-1)
            self.core_conv.weight.data = core_tensor

            if bias:
                self.bias.data = dense_b
        else:
            self.reset_parameters()

    def reset_parameters(self) -> None:
        self.first_conv.reset_parameters()
        self.core_conv.reset_parameters()
        self.last_conv.reset_parameters()

    def forward(self, x):
        out = self.first_conv(x)
        out = self.core_conv(out)
        out = self.last_conv(out)
        return out


class TKConv2dM(Module):
    def __init__(self, in_channels, out_channels, ranks,
                 kernel_size, stride=1, padding=0, dilation=1, groups=1,
                 bias=True, padding_mode='zeros',
                 from_dense=False, dense_w=None, dense_b=None):
        super().__init__()

        self.in_channels = in_channels
        self.out_channels = out_channels
        (out_rank, in_rank) = ranks
        self.in_rank = ranks[1]
        self.out_rank = ranks[0]

        self.first_factor = Parameter(torch.Tensor(in_rank, in_channels))
        self.core_conv = torch.nn.Conv2d(in_channels=in_rank, out_channels=out_rank, kernel_size=kernel_size,
                                         stride=stride, padding=padding, dilation=dilation,
                                         groups=groups, bias=False, padding_mode=padding_mode)
        self.last_factor = Parameter(torch.Tensor(out_channels, out_rank))

        if bias:
            self.bias = Parameter(torch.zeros(out_channels))
        else:
            self.register_parameter('bias', None)

        if from_dense:
            core_tensor, (last_factor, first_factor) = partial_tucker(dense_w, modes=[0, 1],
                                                                      rank=[out_rank, in_rank], init='svd')
            self.first_factor.data = torch.transpose(first_factor, 1, 0)
            self.last_factor.data = last_factor
            self.core_conv.weight.data = core_tensor

            if bias:
                self.bias.data = dense_b
        else:
            self.reset_parameters()

    def reset_parameters(self):
        init.xavier_uniform_(self.first_factor)
        init.xavier_uniform_(self.last_factor)
        self.core_conv.reset_parameters()

    def forward(self, x: Tensor) -> Tensor:
        batch_size, channels, height, width = x.shape
        out = self.first_factor.mm(x.permute(1, 0, 2, 3).reshape(channels, -1))
        out = out.reshape(self.in_rank, batch_size, height, width).permute(1, 0, 2, 3)

        out = self.core_conv(out)
        _, _, height_, width_ = out.shape

        out = self.last_factor.mm(out.permute(1, 0, 2, 3).reshape(self.out_rank, -1))
        out = out.reshape(self.out_channels, batch_size, height_, width_).permute(1, 0, 2, 3)

        if self.bias is not None:
            out += self.bias

        return out


class TKConv2dR(Module):
    def __init__(self,
                 in_channels: int,
                 out_channels: int,
                 ranks: list,
                 kernel_size: _size_2_t,
                 stride: _size_2_t = 1,
                 padding: _size_2_t = 0,
                 dilation: _size_2_t = 1,
                 groups: int = 1,
                 bias: bool = True,
                 padding_mode: str = 'zeros',
                 from_dense: bool = False,
                 dense_w: Tensor = None,
                 dense_b: Tensor = None,
                 ):
        kernel_size = _pair(kernel_size)
        stride = _pair(stride)
        padding = _pair(padding)
        dilation = _pair(dilation)

        super().__init__()

        self.in_channels = in_channels
        self.out_channels = out_channels
        (out_rank, in_rank) = ranks
        self.in_rank = ranks[1]
        self.out_rank = ranks[0]

        if in_channels % groups != 0:
            raise ValueError('in_channels must be divisible by groups')
        if out_channels % groups != 0:
            raise ValueError('out_channels must be divisible by groups')
        valid_padding_modes = {'zeros', 'reflect', 'replicate', 'circular'}
        if padding_mode not in valid_padding_modes:
            raise ValueError("padding_mode must be one of {}, but got padding_mode='{}'".format(
                valid_padding_modes, padding_mode))
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.transposed = False
        self.output_padding = _pair(0)
        self.groups = groups
        self.padding_mode = padding_mode
        # `_reversed_padding_repeated_twice` is the padding to be passed to
        # `F.pad` if needed (e.g., for non-zero padding types that are
        # implemented as two ops: padding + conv). `F.pad` accepts paddings in
        # reverse order than the dimension.
        self._reversed_padding_repeated_twice = _reverse_repeat_tuple(self.padding, 2)
        self.kernel_shape = [out_channels, in_channels // groups, *kernel_size]

        self.filter_dim = int(self.kernel_shape[2] * self.kernel_shape[3])

        self.first_factor = Parameter(torch.Tensor(in_rank, in_channels))
        self.core_tensor = Parameter(torch.Tensor(out_rank, in_rank, self.kernel_shape[2], self.kernel_shape[3]))
        self.last_factor = Parameter(torch.Tensor(out_channels, out_rank))

        if bias:
            self.bias = Parameter(torch.zeros(out_channels))
        else:
            self.register_parameter('bias', None)

        if from_dense:
            core_tensor, (last_factor, first_factor) = partial_tucker(dense_w, modes=[0, 1],
                                                                      rank=[out_rank, in_rank], init='svd')
            self.first_factor.data = torch.transpose(first_factor, 1, 0)
            self.last_factor.data = last_factor
            self.core_tensor = core_tensor

            if bias:
                self.bias.data = dense_b
        else:
            self.reset_parameters()

    def reset_parameters(self):
        init.xavier_uniform_(self.first_factor)
        init.xavier_uniform_(self.core_tensor)
        init.xavier_uniform_(self.last_factor)
        weight = self._recover_weight()
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(weight)
            bound = 1 / math.sqrt(fan_in)
            init.uniform_(self.bias, -bound, bound)

    def _recover_weight(self):
        w = tl.tucker_to_tensor((self.core_tensor, (self.last_factor, self.first_factor.t())))
        return w

    def _conv_forward(self, x, weight):
        if self.padding_mode != 'zeros':
            return F.conv2d(F.pad(x, self._reversed_padding_repeated_twice, mode=self.padding_mode),
                            weight, self.bias, self.stride,
                            _pair(0), self.dilation, self.groups)
        return F.conv2d(x, weight, self.bias, self.stride,
                        self.padding, self.dilation, self.groups)

    def forward(self, x: Tensor) -> Tensor:
        return self._conv_forward(x, self._recover_weight())