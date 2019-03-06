import os

import numpy as np
import wget

import torch
from torch import nn


class Net(nn.Module):
    def __init__(self, cf):
        super(Net, self).__init__()
        self.url = None
        self.net_name = None
        self.loss = None
        self.optimizer = None
        self.scheduler = None
        self.cf = cf

    def forward(self, x):
        pass

    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                m.weight.data.zero_()
                if m.bias is not None:
                    m.bias.data.zero_()
            if isinstance(m, nn.ConvTranspose2d):
                assert m.kernel_size[0] == m.kernel_size[1]
                initial_weight = self.get_upsampling_weight(
                    m.in_channels, m.out_channels, m.kernel_size[0])
                m.weight.data.copy_(initial_weight)

    # https://github.com/shelhamer/fcn.berkeleyvision.org/blob/master/surgery.py
    def get_upsampling_weight(self, in_channels, out_channels, kernel_size):
        """Make a 2D bilinear kernel suitable for upsampling"""
        factor = (kernel_size + 1) // 2
        if kernel_size % 2 == 1:
            center = factor - 1
        else:
            center = factor - 0.5
        og = np.ogrid[:kernel_size, :kernel_size]
        filt = (1 - abs(og[0] - center) / factor) * \
               (1 - abs(og[1] - center) / factor)
        weight = np.zeros((in_channels, out_channels, kernel_size, kernel_size),
                          dtype=np.float64)
        weight[range(in_channels), range(out_channels), :, :] = filt
        return torch.from_numpy(weight).float()

    def load_basic_weights(self):
        os.makedirs(self.cf.basic_models_path, exist_ok=True)
        filename = os.path.join(self.cf.basic_models_path, 'basic_{}.pth'.format(self.net_name.lower()))
        self.download_if_not_exist(filename)
        self.restore_weights(filename)

    def download_if_not_exist(self, filename):
        # Download the file if it does not exist
        if not os.path.isfile(filename) and self.url is not None:
            wget.download(self.url, filename)

    def restore_weights(self, filename):
        print('Loading weights from ' + filename)
        if self.cf.model_type.lower() == 'ssd512':
            self.load_state_dict(torch.load(filename), strict=False)
        else:
            self.load_state_dict2(torch.load(filename))

    def load_state_dict2(self, pretrained_dict):
        model_dict = self.state_dict()

        for k, v in pretrained_dict.items():
            if v.size() != model_dict[k].size():
                print('WARNING: Could not load layer {} with shape: {} and {}'.format(k, v.size(), model_dict[k].size()))
            else:
                model_dict[k] = v

        super(Net, self).load_state_dict(model_dict)
