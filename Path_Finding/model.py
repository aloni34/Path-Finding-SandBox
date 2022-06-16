from Utilities.Values import *
import time
import copy


class Model(object):

    def __init__(self, view):

        self.view = view
        self.board = self.create_board()
        self.draw_dict = self.create_draw_dict()

    def create_board(self):

        board = [[0 for x in range(S_T.BOARD_WIDTH)] for y in range(S_T.BOARD_HEIGHT)]
        return board

    def print_board(self, board):

        print("\n\n")
        if board == "":
            board = self.board

        for i in range(len(board)):
            print(board[i])

    def restart_board(self):
        self.board = self.create_board()

    def draw(self, state, row, col):

        self.board[row][col] = self.draw_dict[state]



    def create_draw_dict(self):

        dict = {
            "Empty": 0,
            "Barrier": 1,
            "Start": 2,
            "End": 3,
        }

        return dict

    def get_next_moves(self, x, y):
        return {
            'left': [x, y - 1],
            'right': [x, y + 1],
            'up': [x - 1, y],
            'down': [x + 1, y],
        }.values()


    def BFA_Root(self, start_coordinate, end_coordinate):

        copy_board = copy.deepcopy(self.board)

        shortest_path = self.BFA_Brain(start_coordinate, end_coordinate, copy_board)

        #for coordinate in shortest_path:
         #   x, y = coordinate
          #  copy_board[x][y] = "."


        #self.print_board(copy_board)

        return shortest_path

    def BFA_Brain(self, start_coordinate, end_coordinate, copy_board):

        sum_checks = 0
        search_paths = [[start_coordinate]]
        visited_coordinates = [start_coordinate]

        while search_paths != []:
            current_path = search_paths.pop(0)
            current_coordinate = current_path[-1]

            current_x, current_y =  current_coordinate

            if current_coordinate == end_coordinate:
                print(sum_checks)
                return current_path

            for next_coordinate in self.get_next_moves(current_x, current_y):

                sum_checks += 1
                next_x, next_y = next_coordinate

                if next_x < 0 or next_x >= len(copy_board):
                    continue

                if next_y < 0 or next_y >= len(copy_board[0]):
                    continue

                if next_coordinate in visited_coordinates:
                    continue

                if copy_board[next_x][next_y] == 1:
                    continue


                search_paths.append(current_path + [next_coordinate])
                visited_coordinates += [next_coordinate]

                self.view.highlight_labels([next_coordinate], C_V.HIGHLIGHT_SEARCH_COLOR)

                if S_T.DELAY_MODIFIER > 0:

                    self.view.root.update()
                    time.sleep(S_T.DELAY_MODIFIER)

