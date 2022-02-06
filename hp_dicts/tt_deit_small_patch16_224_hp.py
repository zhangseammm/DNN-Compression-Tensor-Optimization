# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2022/1/19 22:04

class HyperParamsDictRatio2x:
    depth = 12
    num_heads = 6
    embed_dim = 384
    tt_shapes = {
        'blocks.0.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.0.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.0.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.0.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.1.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.1.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.1.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.1.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.2.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.2.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.2.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.2.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.3.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.3.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.3.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.3.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.4.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.4.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.4.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.4.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.5.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.5.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.5.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.5.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.6.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.6.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.6.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.6.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.7.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.7.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.7.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.7.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.8.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.8.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.8.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.8.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.9.attn.qkv.weight':   (36, 32, 16, 24),
        'blocks.9.attn.proj.weight':  (24, 16, 16, 24),
        'blocks.9.mlp.fc1.weight':    (48, 32, 16, 24),
        'blocks.9.mlp.fc2.weight':    (24, 16, 32, 48),
        'blocks.10.attn.qkv.weight':  (36, 32, 16, 24),
        'blocks.10.attn.proj.weight': (24, 16, 16, 24),
        'blocks.10.mlp.fc1.weight':   (48, 32, 16, 24),
        'blocks.10.mlp.fc2.weight':   (24, 16, 32, 48),
        'blocks.11.attn.qkv.weight':  (36, 32, 16, 24),
        'blocks.11.attn.proj.weight': (24, 16, 16, 24),
        'blocks.11.mlp.fc1.weight':   (48, 32, 16, 24),
        'blocks.11.mlp.fc2.weight':   (24, 16, 32, 48),
    }

    ranks = {
        # state_dict key: (output channel, input channel)
        'blocks.0.attn.qkv.weight':   (1, 35, 320, 23, 1),
        'blocks.0.attn.proj.weight':  (1, 22, 320, 22, 1),
        'blocks.0.mlp.fc1.weight':    (1, 42, 320, 22, 1),
        'blocks.0.mlp.fc2.weight':    (1, 22, 320, 42, 1),
        'blocks.1.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.1.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.1.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.1.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.2.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.2.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.2.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.2.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.3.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.3.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.3.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.3.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.4.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.4.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.4.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.4.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.5.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.5.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.5.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.5.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.6.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.6.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.6.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.6.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.7.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.7.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.7.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.7.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.8.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.8.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.8.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.8.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.9.attn.qkv.weight':   (1, 25, 256, 18, 1),
        'blocks.9.attn.proj.weight':  (1, 18, 256, 18, 1),
        'blocks.9.mlp.fc1.weight':    (1, 30, 256, 18, 1),
        'blocks.9.mlp.fc2.weight':    (1, 18, 256, 30, 1),
        'blocks.10.attn.qkv.weight':  (1, 25, 256, 18, 1),
        'blocks.10.attn.proj.weight': (1, 18, 256, 18, 1),
        'blocks.10.mlp.fc1.weight':   (1, 30, 256, 18, 1),
        'blocks.10.mlp.fc2.weight':   (1, 18, 256, 30, 1),
        'blocks.11.attn.qkv.weight':  (1, 25, 256, 18, 1),
        'blocks.11.attn.proj.weight': (1, 18, 256, 18, 1),
        'blocks.11.mlp.fc1.weight':   (1, 30, 256, 18, 1),
        'blocks.11.mlp.fc2.weight':   (1, 18, 256, 30, 1),
    }