# -*- coding: utf-8 -*-

class GameField():
    def __init__(self):
        self.cells = tuple([GameCell(i) for i in range(40)])
    def render(self):
        print('yup')
class GameCell():
    def __init__(self, number):
        print(number)
