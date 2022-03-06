# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2022/3/6 14:39

class HyperParamsDictRatio2x:
    ranks = {
        # 'features.0.weight': [64, 3, 3, 3],
        'features.3.weight': [32, 64],
        'features.7.weight': [32, 64],
        'features.10.weight': [64, 64],
        'features.14.weight': [64, 128],
        'features.17.weight': [128, 128],
        'features.20.weight': [128, 128],
        'features.24.weight': [128, 128],
        'features.27.weight': [160, 196],
        'features.30.weight': [160, 196],
        'features.34.weight': [160, 196],
        'features.37.weight': [160, 196],
        'features.40.weight': [160, 196],
        'pre_logits.fc1.weight': [256, 256],
        # 'pre_logits.fc2.weight': [4096, 4096, 1, 1],
        # 'head.fc.weight': [1000, 4096],
    }