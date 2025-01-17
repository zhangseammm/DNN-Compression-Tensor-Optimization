# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2021/9/23 21:13


import numpy as np
import torch
import math
import torch.nn as nn
import timm

from torch.nn import Parameter, ParameterList
import torch.nn.functional as F
from torch.nn import init
from torch.nn.modules import Module
from functools import partial

from timm.data import IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD, IMAGENET_INCEPTION_MEAN, IMAGENET_INCEPTION_STD
from timm.models.helpers import build_model_with_cfg, named_apply, adapt_input_conv
from timm.models.layers import PatchEmbed, Mlp, DropPath, trunc_normal_, lecun_normal_
from timm.models.registry import register_model

from timm.models.vision_transformer import VisionTransformer
from timm.models.vision_transformer import _cfg, Block, Attention, Mlp

import utils
from TTLinear import TTLinearM, TTLinearR
from TKLinear import TKLinearM, TKLinearR
from typing import Type, Any, Callable, Union, List, Optional


class TTAttention(Attention):
    def __init__(self, dim, num_heads=8, qkv_bias=False, attn_drop=0., proj_drop=0.,
                 linear=Union[TTLinearM, TTLinearR, TKLinearM, TKLinearR],
                 block_id=None, hp_dict=None, dense_dict=None):
        super().__init__(dim, num_heads, qkv_bias, attn_drop, proj_drop)
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = head_dim ** -0.5

        qkv_name = 'blocks.' + str(block_id) + '.attn.qkv.'
        w_name = qkv_name + 'weight'
        b_name = qkv_name + 'bias'
        if w_name in hp_dict.ranks:
            self.qkv = linear(dim, dim * 3, bias=qkv_bias, hp_dict=hp_dict, name=w_name,
                              dense_w=None if dense_dict is None else dense_dict[w_name],
                              dense_b=None if dense_dict is None else dense_dict[b_name])
        else:
            self.qkv = nn.Linear(dim, dim * 3, bias=qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop)
        proj_name = 'blocks.' + str(block_id) + '.attn.proj.'
        w_name = proj_name + 'weight'
        b_name = proj_name + 'bias'
        if w_name in hp_dict.ranks:
            self.proj = linear(dim, dim, hp_dict=hp_dict, name=w_name,
                               dense_w=None if dense_dict is None else dense_dict[w_name],
                               dense_b=None if dense_dict is None else dense_dict[b_name])
        else:
            self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)


class TTMlp(Mlp):
    def __init__(self, in_features, hidden_features=None, out_features=None, act_layer=nn.GELU, drop=0.,
                 linear=Union[TTLinearM, TTLinearR, TKLinearM, TKLinearR],
                 block_id=None, hp_dict=None, dense_dict=None):
        super().__init__(in_features, hidden_features, out_features, act_layer, drop)
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features

        fc1_name = 'blocks.' + str(block_id) + '.mlp.fc1.'
        w_name = fc1_name + 'weight'
        b_name = fc1_name + 'bias'

        if w_name in hp_dict.ranks:
            self.fc1 = linear(in_features, hidden_features, hp_dict=hp_dict, name=w_name,
                              dense_w=None if dense_dict is None else dense_dict[w_name],
                              dense_b=None if dense_dict is None else dense_dict[b_name])
        else:
            self.fc1 = nn.Linear(in_features, hidden_features)

        self.act = act_layer()

        fc2_name = 'blocks.' + str(block_id) + '.mlp.fc2.'
        w_name = fc2_name + 'weight'
        b_name = fc2_name + 'bias'
        if w_name in hp_dict.ranks:
            self.fc2 = linear(hidden_features, out_features, hp_dict=hp_dict, name=w_name,
                              dense_w=None if dense_dict is None else dense_dict[w_name],
                              dense_b=None if dense_dict is None else dense_dict[b_name])
        else:
            self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(drop)


class TTBlock(Block):
    def __init__(self, dim, num_heads, mlp_ratio=4., qkv_bias=False, drop=0., attn_drop=0.,
                 drop_path=0., act_layer=nn.GELU, norm_layer=nn.LayerNorm,
                 linear=Union[TTLinearM, TTLinearR, TKLinearM, TKLinearR],
                 block_id=None, hp_dict=None, dense_dict=None):
        super().__init__(dim, num_heads, mlp_ratio, qkv_bias, drop, attn_drop, drop_path, act_layer, norm_layer)
        self.norm1 = norm_layer(dim)
        self.attn = TTAttention(dim, num_heads=num_heads, qkv_bias=qkv_bias, attn_drop=attn_drop, proj_drop=drop,
                                linear=linear, block_id=block_id, hp_dict=hp_dict, dense_dict=dense_dict)
        # NOTE: drop path for stochastic depth, we shall see if this is better than dropout here
        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = norm_layer(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = TTMlp(in_features=dim, hidden_features=mlp_hidden_dim, act_layer=act_layer, drop=drop,
                         linear=linear, block_id=block_id, hp_dict=hp_dict, dense_dict=dense_dict)


class TTVisionTransformer(VisionTransformer):
    def __init__(self, img_size=224, patch_size=16, in_chans=3, num_classes=1000, embed_dim=768, depth=12,
                 num_heads=12, mlp_ratio=4., qkv_bias=True, representation_size=None, distilled=False,
                 drop_rate=0., attn_drop_rate=0., drop_path_rate=0., embed_layer=PatchEmbed, norm_layer=None,
                 act_layer=None, weight_init='', linear=Union[TTLinearM, TTLinearR], hp_dict=None, dense_dict=None):
        super().__init__(img_size, patch_size, in_chans, num_classes, embed_dim, depth, num_heads, mlp_ratio,
                         qkv_bias, representation_size, distilled, drop_rate, attn_drop_rate, drop_path_rate,
                         embed_layer, norm_layer, act_layer, weight_init)

        norm_layer = norm_layer or partial(nn.LayerNorm, eps=1e-6)
        act_layer = act_layer or nn.GELU
        dpr = [x.item() for x in torch.linspace(0, drop_path_rate, depth)]  # stochastic depth decay rule
        self.blocks = nn.Sequential(*[
            TTBlock(
                dim=embed_dim, num_heads=num_heads, mlp_ratio=mlp_ratio, qkv_bias=qkv_bias, drop=drop_rate,
                attn_drop=attn_drop_rate, drop_path=dpr[i], norm_layer=norm_layer, act_layer=act_layer,
                linear=linear, block_id=i, hp_dict=hp_dict, dense_dict=dense_dict)
            for i in range(depth)])


def _tt_vit(patch_size=16, embed_dim=384, depth=12, num_heads=6, mlp_ratio=4, qkv_bias=True,
            linear=Union[TTLinearM, TTLinearR, TKLinearM, TKLinearR], hp_dict=None, dense_dict=None, **kwargs):
    model = TTVisionTransformer(
        patch_size=patch_size, embed_dim=embed_dim, depth=depth, num_heads=num_heads, mlp_ratio=mlp_ratio,
        qkv_bias=qkv_bias, linear=linear, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    if dense_dict is not None:
        tt_dict = model.state_dict()
        for key in tt_dict.keys():
            if key in dense_dict.keys():
                tt_dict[key].data = dense_dict[key]
        model.load_state_dict(tt_dict)

    return model


@register_model
def ttm_vit_small_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('vit_small_patch16_224', pretrained=True, **kwargs).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=384, depth=12, num_heads=6,
                    linear=TTLinearM, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    # model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def ttr_vit_small_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('vit_small_patch16_224', pretrained=True, **kwargs).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=384, depth=12, num_heads=6,
                    linear=TTLinearR, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    # model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def ttm_deit_tiny_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('deit_tiny_patch16_224', pretrained=True, **kwargs).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=192, depth=12, num_heads=3, mlp_ratio=4, qkv_bias=True,
                    linear=TTLinearM, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def ttr_deit_tiny_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('deit_tiny_patch16_224', pretrained=True, **kwargs).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=192, depth=12, num_heads=3, mlp_ratio=4, qkv_bias=True,
                    linear=TTLinearR, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def ttm_deit_small_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('deit_small_patch16_224', pretrained=True).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=384, depth=12, num_heads=6, mlp_ratio=4, qkv_bias=True,
                    linear=TTLinearM, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def ttr_deit_small_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('deit_small_patch16_224', pretrained=True).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=384, depth=12, num_heads=6, mlp_ratio=4, qkv_bias=True,
                    linear=TTLinearR, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def tkm_deit_tiny_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('deit_tiny_patch16_224', pretrained=True).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=192, depth=12, num_heads=3, mlp_ratio=4, qkv_bias=True,
                    linear=TKLinearM, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def tkr_deit_tiny_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('deit_tiny_patch16_224', pretrained=True).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=192, depth=12, num_heads=3, mlp_ratio=4, qkv_bias=True,
                    linear=TKLinearR, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def tkm_deit_small_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('deit_small_patch16_224', pretrained=True).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=384, depth=12, num_heads=6, mlp_ratio=4, qkv_bias=True,
                    linear=TKLinearM, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


@register_model
def tkr_deit_small_patch16_224(hp_dict, pretrained=False, decompose=False, path=None, **kwargs):
    if decompose:
        if path is None:
            dense_dict = timm.create_model('deit_small_patch16_224', pretrained=True).state_dict()
        elif path.startswith('http'):
            dense_dict = torch.hub.load_state_dict_from_url(url=path, map_location="cpu", check_hash=True)
        else:
            dense_dict = torch.load(path, map_location='cpu')
    else:
        dense_dict = None
    model = _tt_vit(patch_size=16, embed_dim=384, depth=12, num_heads=6, mlp_ratio=4, qkv_bias=True,
                    linear=TKLinearR, hp_dict=hp_dict, dense_dict=dense_dict, **kwargs)
    model.default_cfg = _cfg()
    if pretrained and not decompose:
        state_dict = torch.load(path, map_location='cpu')
        model.load_state_dict(state_dict)
    return model


if __name__ == '__main__':
    baseline = 'deit_tiny_patch16_224'
    model_name = 'ttm_' + baseline
    hp_dict = utils.get_hp_dict(model_name, '2')
    model = timm.create_model(model_name, hp_dict=hp_dict, decompose=None)
    tk_params = 0
    for name, p in model.named_parameters():
        if p.requires_grad:
            print(name, p.shape)
            tk_params += int(np.prod(p.shape))
    print('Compressed # parameters: {}'.format(tk_params))

    base_params = 0
    model = timm.create_model(baseline)
    for name, p in model.named_parameters():
        if p.requires_grad:
            # print(name, p.shape)
            base_params += int(np.prod(p.shape))
    print('Baseline # parameters: {}'.format(base_params))
    print('Compression ratio: {}'.format(base_params / tk_params))

    dummy_input = torch.randn(1, 3, 224, 224, requires_grad=True)

    print(model)
    # Export the model
    torch.onnx.export(model,         # model being run
                      dummy_input,       # model input (or a tuple for multiple inputs)
                      model_name + ".onnx",       # where to save the model
                      export_params=True,  # store the trained parameter weights inside the model file
                      opset_version=17,    # the ONNX version to export the model to
                      do_constant_folding=True,  # whether to execute constant folding for optimization
                      input_names = ['modelInput'],   # the model's input names
                      output_names = ['modelOutput'], # the model's output names
                      )
