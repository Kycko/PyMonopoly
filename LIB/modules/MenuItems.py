# -*- coding: utf-8 -*-
from TransparentText import AlphaText

class MenuItem():
    def __init__(self, text, type, group, number=None):
        self.type = type
        self.text = AlphaText(text, group, number)
        self.init_for_group(group)
    def init_for_group(self, group):
        self.tooltip = None
