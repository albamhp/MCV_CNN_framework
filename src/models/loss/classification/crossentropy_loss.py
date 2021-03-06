import torch.nn as nn

from .classification_loss import ClassificationLoss


class CrossEntropyLoss(ClassificationLoss):
    def __init__(self, cf, weight=None, ignore_index=255):
        super(CrossEntropyLoss, self).__init__(cf, weight, ignore_index)
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, inputs, targets):
        loss = self.criterion(inputs, targets.view(-1))
        return loss
