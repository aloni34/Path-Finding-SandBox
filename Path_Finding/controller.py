from model import *
from view import *


class Controller(object):

    def __init__(self, root):

        self.view = View(root, self)
        self.model = Model(self.view)


    def draw(self, state, row, col):
        self.model.draw(state, row, col)

    def restart_board(self):
        self.model.restart_board()

    def print_board(self):
        self.model.print_board("")

    def BFA(self, start_position, end_position):
        return self.model.BFA_Root(start_position, end_position)
