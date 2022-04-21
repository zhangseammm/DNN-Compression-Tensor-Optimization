# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2021/10/12 21:19

# general TT FC layer

import torch
import numpy as np
import torch.nn.functional as F

torch.manual_seed(20211012)

batch_size = 1

tt_params = 0
tt_flops = 0

# in_tt_shapes = [4, 20, 20, 36]
# out_tt_shapes = [8, 8, 4]
# tt_ranks = [1, 3, 5, 9, 14, 6, 5, 1]

in_tt_shapes = [5, 7, 9]
out_tt_shapes = [4, 8, 16]
tt_ranks = [1, 2, 3, 4, 2, 2, 1]

in_tt_order = len(in_tt_shapes)
out_tt_order = len(out_tt_shapes)
tt_shapes = out_tt_shapes + in_tt_shapes
in_features = int(np.prod(in_tt_shapes))
out_features = int(np.prod(out_tt_shapes))
params = in_features * out_features
flops = batch_size * in_features * out_features

tt_cores = [torch.randn(tt_ranks[i], tt_shapes[i], tt_ranks[i+1]) for i in range(len(tt_shapes))]
for i in range(len(tt_cores)):
    tt_params += int(np.prod(tt_cores[i].shape))
print('Compression ratio: {}'.format(params/tt_params))

x = torch.randn(batch_size, in_features)

out_shape = list(x.shape)
out_shape[-1] = out_features
out = x
for i in range(in_tt_order - 1, -1, -1):
    a = tt_cores[i + out_tt_order].reshape(
        -1, in_tt_shapes[i] * tt_ranks[i + out_tt_order + 1])
    b = out.reshape(-1, in_tt_shapes[i] * tt_ranks[i + out_tt_order + 1]).t()
    out = a.mm(b).t()
    tt_flops += a.shape[0] * a.shape[1] * b.shape[1]


for i in range(out_tt_order - 1, -1, -1):
    a = tt_cores[i].reshape(-1, tt_ranks[i + 1])
    b = out.reshape(-1, tt_ranks[i + 1]).t()
    out = a.mm(b)
    out = out.reshape(tt_ranks[i], -1).t()
    tt_flops += a.shape[0] * a.shape[1] * b.shape[1]

print('Speedup: {}'.format(flops/tt_flops))
out = out.reshape(out_features, -1).t().reshape(out_shape)




