import torchvision.models.vgg as models
from easydict import EasyDict
from torch import nn

from models.networks.network import Net


class VGG16Torch(Net):

    def __init__(self, cf: EasyDict, num_classes: int = 1000, pretrained: bool = False, net_name: str = 'vgg16torch'):
        super().__init__(cf)

        self.pretrained = pretrained
        self.net_name = net_name

        if pretrained:
            self.model = models.vgg16(pretrained=True)

            for param in self.model.parameters():
                param.requires_grad = False

            num_ftrs = self.model.classifier[6].in_features
            self.model.classifier[6] = nn.Linear(num_ftrs, num_classes)
        else:
            self.model = models.vgg16(pretrained=False, num_classes=num_classes)

    def forward(self, x):
        return self.model.forward(x)

    def load_basic_weights(self):
        pass
