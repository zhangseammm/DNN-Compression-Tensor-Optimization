# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2021/11/3 23:05

class HyperParamsDictRatio2x:
    kernel_shapes = {
        'blocks.0.0.conv_dw.weight': [32, 1, 3, 3],
        'blocks.0.0.conv_pw.weight': [16, 32, 1, 1],
        'blocks.1.0.conv_pw.weight': [96, 16, 1, 1],
        'blocks.1.0.conv_dw.weight': [96, 1, 3, 3],
        'blocks.1.0.conv_pwl.weight': [24, 96, 1, 1],
        'blocks.1.1.conv_pw.weight': [144, 24, 1, 1],
        'blocks.1.1.conv_dw.weight': [144, 1, 3, 3],
        'blocks.1.1.conv_pwl.weight': [24, 144, 1, 1],
        'blocks.2.0.conv_pw.weight': [144, 24, 1, 1],
        'blocks.2.0.conv_dw.weight': [144, 1, 3, 3],
        'blocks.2.0.conv_pwl.weight': [32, 144, 1, 1],
        'blocks.2.1.conv_pw.weight': [192, 32, 1, 1],
        'blocks.2.1.conv_dw.weight': [192, 1, 3, 3],
        'blocks.2.1.conv_pwl.weight': [32, 192, 1, 1],
        'blocks.2.2.conv_pw.weight': [192, 32, 1, 1],
        'blocks.2.2.conv_dw.weight': [192, 1, 3, 3],
        'blocks.2.2.conv_pwl.weight': [32, 192, 1, 1],
        'blocks.3.0.conv_pw.weight': [192, 32, 1, 1],
        'blocks.3.0.conv_dw.weight': [192, 1, 3, 3],
        'blocks.3.0.conv_pwl.weight': [64, 192, 1, 1],
        'blocks.3.1.conv_pw.weight': [384, 64, 1, 1],
        'blocks.3.1.conv_dw.weight': [384, 1, 3, 3],
        'blocks.3.1.conv_pwl.weight': [64, 384, 1, 1],
        'blocks.3.2.conv_pw.weight': [384, 64, 1, 1],
        'blocks.3.2.conv_dw.weight': [384, 1, 3, 3],
        'blocks.3.2.conv_pwl.weight': [64, 384, 1, 1],
        'blocks.3.3.conv_pw.weight': [384, 64, 1, 1],
        'blocks.3.3.conv_dw.weight': [384, 1, 3, 3],
        'blocks.3.3.conv_pwl.weight': [64, 384, 1, 1],
        'blocks.4.0.conv_pw.weight': [384, 64, 1, 1],
        'blocks.4.0.conv_dw.weight': [384, 1, 3, 3],
        'blocks.4.0.conv_pwl.weight': [96, 384, 1, 1],
        'blocks.4.1.conv_pw.weight': [576, 96, 1, 1],
        'blocks.4.1.conv_dw.weight': [576, 1, 3, 3],
        'blocks.4.1.conv_pwl.weight': [96, 576, 1, 1],
        'blocks.4.2.conv_pw.weight': [576, 96, 1, 1],
        'blocks.4.2.conv_dw.weight': [576, 1, 3, 3],
        'blocks.4.2.conv_pwl.weight': [96, 576, 1, 1],
        'blocks.5.0.conv_pw.weight': [576, 96, 1, 1],
        'blocks.5.0.conv_dw.weight': [576, 1, 3, 3],
        'blocks.5.0.conv_pwl.weight': [160, 576, 1, 1],
        'blocks.5.1.conv_pw.weight': [960, 160, 1, 1],
        'blocks.5.1.conv_dw.weight': [960, 1, 3, 3],
        'blocks.5.1.conv_pwl.weight': [160, 960, 1, 1],
        'blocks.5.2.conv_pw.weight': [960, 160, 1, 1],
        'blocks.5.2.conv_dw.weight': [960, 1, 3, 3],
        'blocks.5.2.conv_pwl.weight': [160, 960, 1, 1],
        'blocks.6.0.conv_pw.weight': [960, 160, 1, 1],
        'blocks.6.0.conv_dw.weight': [960, 1, 3, 3],
        'blocks.6.0.conv_pwl.weight': [320, 960, 1, 1],
        'conv_head.weight': [1280, 320, 1, 1],
    }

    ranks = {
        # 'blocks.0.0.conv_dw.weight': [32, 1, 3, 3],
        # 'blocks.0.0.conv_pw.weight': [16, 32, 1, 1],
        'blocks.1.0.conv_pw.weight': [14, 14],
        # 'blocks.1.0.conv_dw.weight': [96, 1, 3, 3],
        'blocks.1.0.conv_pwl.weight': [18, 18],
        'blocks.1.1.conv_pw.weight': [18, 18],
        # 'blocks.1.1.conv_dw.weight': [144, 1, 3, 3],
        'blocks.1.1.conv_pwl.weight': [18, 18],
        'blocks.2.0.conv_pw.weight': [18, 18],
        # 'blocks.2.0.conv_dw.weight': [144, 1, 3, 3],
        'blocks.2.0.conv_pwl.weight': [24, 24],
        'blocks.2.1.conv_pw.weight': [22, 22],
        # 'blocks.2.1.conv_dw.weight': [192, 1, 3, 3],
        'blocks.2.1.conv_pwl.weight': [22, 22],
        'blocks.2.2.conv_pw.weight': [22, 22],
        # 'blocks.2.2.conv_dw.weight': [192, 1, 3, 3],
        'blocks.2.2.conv_pwl.weight': [22, 22],
        'blocks.3.0.conv_pw.weight': [24, 24],
        # 'blocks.3.0.conv_dw.weight': [192, 1, 3, 3],
        'blocks.3.0.conv_pwl.weight': [22, 22],
        'blocks.3.1.conv_pw.weight': [28, 28],
        # 'blocks.3.1.conv_dw.weight': [384, 1, 3, 3],
        'blocks.3.1.conv_pwl.weight': [28, 28],
        'blocks.3.2.conv_pw.weight': [28, 28],
        # 'blocks.3.2.conv_dw.weight': [384, 1, 3, 3],
        'blocks.3.2.conv_pwl.weight': [28, 28],
        'blocks.3.3.conv_pw.weight': [28, 28],
        # 'blocks.3.3.conv_dw.weight': [384, 1, 3, 3],
        'blocks.3.3.conv_pwl.weight': [28, 28],
        'blocks.4.0.conv_pw.weight': [30, 30],
        # 'blocks.4.0.conv_dw.weight': [384, 1, 3, 3],
        'blocks.4.0.conv_pwl.weight': [35, 35],
        'blocks.4.1.conv_pw.weight': [35, 35],
        # 'blocks.4.1.conv_dw.weight': [576, 1, 3, 3],
        'blocks.4.1.conv_pwl.weight': [40, 40],
        'blocks.4.2.conv_pw.weight': [40, 40],
        # 'blocks.4.2.conv_dw.weight': [576, 1, 3, 3],
        'blocks.4.2.conv_pwl.weight': [40, 40],
        'blocks.5.0.conv_pw.weight': [40, 40],
        # 'blocks.5.0.conv_dw.weight': [576, 1, 3, 3],
        'blocks.5.0.conv_pwl.weight': [64, 64],
        'blocks.5.1.conv_pw.weight': [60, 60],
        # 'blocks.5.1.conv_dw.weight': [960, 1, 3, 3],
        'blocks.5.1.conv_pwl.weight': [60, 60],
        'blocks.5.2.conv_pw.weight': [60, 60],
        # 'blocks.5.2.conv_dw.weight': [960, 1, 3, 3],
        'blocks.5.2.conv_pwl.weight': [60, 60],
        'blocks.6.0.conv_pw.weight': [60, 60],
        # 'blocks.6.0.conv_dw.weight': [960, 1, 3, 3],
        'blocks.6.0.conv_pwl.weight': [100, 100],
        'conv_head.weight': [100, 100],
    }