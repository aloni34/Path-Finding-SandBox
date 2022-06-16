from Utilities.Values import *
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk
from Image_Collection import *

class View(object):

    def __init__(self, root, controller):

        self.root = root
        self.controller = controller
        self.image_collection = ImageCollection(self.root)

        # region UI
        self.play_panel_frame = self.play_panel_frame(self.root)
        self.right_frame = self.create_right_frame(self.root)

        self.entry_board_size = self.construct_entry_board_size(self.right_frame)
        self.button_board_size = self.construct_button_board_size(self.right_frame)

        self.list_of_right_labels = self.construct_labels_right_frame(self.right_frame)

        self.construct_drop_box_size = self.construct_drop_box_size(self.right_frame)

        self.drop_box_state_list = self.construct_drop_box_state(self.right_frame)

        self.drop_box_trigger_mode_list = self.construct_drop_box_trigger_mode(self.right_frame)

        #self.entry_delay_modifier = self.construct_entry_delay_modifier(self.right_frame)
        #self.construct_button_delay_modifier = self.construct_button_delay_modifier(self.right_frame)

        self.center_frame = self.create_center_frame(self.root)


        self.play_button = self.construct_button_play(self.play_panel_frame)

        # endregion





        # Board drawing
        self.current_build_state = "Empty"
        self.current_trigger_state = "Click"
        self.color_draw_dict = self.create_draw_dict()

        self.current_start_position = []
        self.current_end_position = []



        self.board = self.create_board()
        self.number_of_deleted_board_labels = 0 # allows to calculate new constructions of new boards without restaring the entire game

        self.path_found_from_path_finding = ""

        # bind functions to the root
        self.bind_to_root_for_option_menus(self.root)




    def play_panel_frame(self, root):

        control_panel_frame = ttk.Frame(root)

        control_panel_frame.place(relx = 0.2, rely = 0.01, relwidth = 0.5667, relheight = 0.09)
        control_panel_frame.config(padding=(30, 15))

        return control_panel_frame

    # region controller panel

    def construct_button_play(self, root):

        play_button = ttk.Button(root, image=self.image_collection.get_image_list()[4], command = self.BFA)
        play_button.place(relx=0.375, rely=0.2, relwidth=0.25, relheight=0.8)
        return play_button

    def selected_state(self, event):
        self.current_build_state = str(event)

    def create_draw_dict(self):

        dict = {
            "Empty": C_V.EMPTY_LABEL_COLOR,
            "Barrier": 'Black',
            "Start": 'Green',
            "End": 'Yellow',
        }

        return dict

    def selected_size(self, event):

        size = str(event).split("x")
        if str(size[1]) != str(S_T.WIDTH):

            S_T.WIDTH = str(size[1])
            S_T.HEIGHT = str(size[0])
            self.root.geometry(S_T.WIDTH + "x" + S_T.HEIGHT)
            self.root.resizable(0, 0)

    def apply_board_size(self):

        input = self.entry_board_size.get()

        if "X" in input:

            self.number_of_deleted_board_labels += int(S_T.BOARD_HEIGHT) * int(S_T.BOARD_WIDTH)
            board_size = input.split("X")
            S_T.BOARD_HEIGHT = int(board_size[0])
            S_T.BOARD_WIDTH = int(board_size[1])

            # reset end and start positions to none
            self.current_start_position = []
            self.current_end_position = []

            self.destroy_board(self.board)
            self.controller.restart_board()
            self.board = self.create_board()
        else:
            self.entry_board_size.delete(0, "end")
            self.entry_board_size.insert(0, "Invalid Input, must be: Num X Num")

    def update_delay_modifier(self):

        input = self.entry_board_size.get()
        S_T.DELAY_MODIFIER = int(input) * 0.01

    def update_trigger_mode(self, event):

        if str(event) == "Click":
            self.current_trigger_state = "Click"
        elif str(event) == "Hover":
            self.current_trigger_state = "Hover"
        else:
            self.current_trigger_state = "Disabled"

    # endregion

    def create_center_frame(self, root):

        center_frame = ttk.Frame(root)
        center_frame.place(relx = 0.2, rely = 0.13, relwidth = 0.5667, relheight = 0.8)
        center_frame.config(padding=(30, 15))

        return center_frame

    # region Right Frame (Settings)

    def create_right_frame(self, root):

        right_frame = ttk.Frame(root)
        right_frame.place(relx = 0.8, rely = 0.13, relwidth = 0.18, relheight = 0.8)
        right_frame.config(padding=(30, 15))

        return right_frame

    def construct_labels_right_frame(self, root):

        list_of_labels_in_right_frame = []

        size_label_board = ttk.Label(root, text="Board Size", foreground="black", anchor=CENTER, relief=RIDGE, background = "Red", font = 24)
        size_label_board.place(relx=0.1, rely=0.008, relwidth=0.8, relheight=0.05)

        size_label_page = ttk.Label(root, text="Page Size", foreground="black", anchor=CENTER, relief=RIDGE, background = "Orange", font = 24)
        size_label_page.place(relx=0.1, rely=0.20, relwidth=0.8, relheight=0.05)

        state_label_board = ttk.Label(root, text="Build Mode", foreground="black", anchor=CENTER, relief=RIDGE, background = "Yellow", font = 24)
        state_label_board.place(relx=0.1, rely=0.3192, relwidth=0.8, relheight=0.05)

        event_trigger_label_board = ttk.Label(root, text="Trigger Mode", foreground="black", anchor=CENTER, relief=RIDGE, background = "green", font = 24)
        event_trigger_label_board.place(relx=0.1, rely=0.4384, relwidth=0.8, relheight=0.05)

        list_of_labels_in_right_frame.append(size_label_board)
        list_of_labels_in_right_frame.append(size_label_page)
        list_of_labels_in_right_frame.append(state_label_board)
        list_of_labels_in_right_frame.append(event_trigger_label_board)

        return list_of_labels_in_right_frame

    def construct_entry_board_size(self, root):

        entry = ttk.Entry(root)
        entry.place(relx=0.1, rely=0.06, relwidth=0.8, relheight=0.03)
        return entry

    def construct_button_board_size(self, root):

        button = ttk.Button(root, command = self.apply_board_size, text = "Apply: Size")
        button.place(relx=0.2, rely=0.12, relwidth=0.6, relheight=0.06)
        return button

    def construct_drop_box_size(self, root):

        options = [
            str(S_T.HEIGHT) + "x" + str(S_T.WIDTH),
            "600x1067",
            "800x1442",
            "1000x1778",
            "1080x1920",
        ]

        clicked = StringVar()
        clicked.set(options[0])

        drop = OptionMenu(root, clicked, *options, command=self.selected_size)
        drop.place(relx=0.2, rely=0.26, relwidth=0.6, relheight=0.06)
        return drop





    def construct_drop_box_state(self, root):

        options = [
            "Empty",
            "Empty",
            "Barrier",
            "Start",
            "End"
        ]

        clicked = StringVar()
        clicked.set(options[0])

        drop = OptionMenu(root, clicked, *options, command = self.selected_state)
        drop.place(relx=0.2, rely=0.3792, relwidth=0.6, relheight=0.06)
        return [drop, clicked, options]

    def construct_drop_box_trigger_mode(self, root):

        options = [
            "Click",
            "Click",
            "Hover",
            "Disabled"
        ]

        clicked = StringVar()
        clicked.set(options[0])

        drop = OptionMenu(root, clicked, *options, command = self.update_trigger_mode)

        drop.place(relx=0.2, rely=0.4984, relwidth=0.6, relheight=0.06)
        return [drop, clicked, options]

    def update_drop_box_trigger_mode_first_part(self, list_to_change):

        temp_option_menu = list_to_change[0]
        list_to_change[0] = 0
        temp_option_menu.destroy()
        temp_options = list_to_change[2]
        list_to_change = []

        return temp_options

    def update_drop_box_trigger_mode_second_part(self, root, default, options, new_command, rel_x, rel_y, rel_width, rel_height):


        clicked = StringVar()
        clicked.set(default)
        options[0] = default
        drop = OptionMenu(root, clicked, *options, command=new_command)

        drop.place(relx = rel_x, rely = rel_y, relwidth = rel_width, relheight = rel_height)
        return [drop, clicked, options]

    def construct_button_delay_modifier(self, root):

        button = ttk.Button(root, command = self.update_delay_modifier, text = "Apply: Delay")
        button.place(relx=0.2, rely=0.7, relwidth=0.6, relheight=0.06)
        return button

    def construct_entry_delay_modifier(self, root):

        entry = ttk.Entry(root)
        entry.place(relx=0.1, rely=0.75, relwidth=0.8, relheight=0.03)
        return entry


    # endregion

    def create_board(self):

        empty_label_color = C_V.EMPTY_LABEL_COLOR
        list_of_labels_board = []
        y = S_T.BOARD_HEIGHT
        x = S_T.BOARD_WIDTH

        for i in range(y):

            sub_list1 = []

            for j in range(x):

                label = ttk.Label(self.center_frame, text="", foreground="Yellow", anchor=CENTER, relief=RIDGE, background = empty_label_color)
                label.bind("<Button-1>", self.onaction_click)
                label.bind("<Enter>", self.onaction_hover) # by hovering it will call the function

                label.place(relx= j / x, rely= i / y, relwidth= 1 / x, relheight= 1 / y)
                sub_list1.append(label)

            list_of_labels_board.append(sub_list1)

        return list_of_labels_board

    def destroy_board(self, board):

        temp = ""

        for i in range(len(board)):
            for j in range(len(board[0])):
                temp = board[i][j]
                board[i][j] = [0]
                temp.destroy()

        board = []



    # region board actions

    def onaction_click(self, event):
        if not self.current_trigger_state == "Click":
            return
        self.onaction(event)

    def onaction_hover(self, event):
        if not self.current_trigger_state == "Hover":
            return
        self.onaction(event)

    def onaction(self, event):


        row, col = self.get_label_location(event)
        state = self.current_build_state

        # region Task: check if there is existing start or end
        if state == "Start" or state == "End":
            if not self.is_empty_of_start_or_end_points(state):
                return None
            else:
                if state == "Start" and self.current_end_position != [] and self.current_end_position[0] == row and self.current_end_position[1] == col:
                    self.current_end_position = []
                elif state == "End" and self.current_start_position != [] and self.current_start_position[0] == row and self.current_start_position[1] == col:
                    self.current_start_position = []

                self.update_start_or_end_points(state, row, col)

        # endregion

        # region Task: update to no empty start or end if was replaced
        else:
            if self.current_start_position != []:
                if self.current_start_position[0] == row and self.current_start_position[1] == col:
                    self.current_start_position = []
            if self.current_end_position != []:
                if self.current_end_position[0] == row and self.current_end_position[1] == col:
                    self.current_end_position = []
        # endregion

        # region Task: draw
        self.board[row][col].config(background = self.color_draw_dict[state])
        self.controller.draw(state, row, col)
        #self.controller.print_board()
        # endregion

        # region Task: print details

        #self.controller.print_board()

        # endregion


    # endregion

    # region Options Actions
    def bind_to_root_for_option_menus(self, root):

        root.bind("<Shift-Q>", self.update_trigger_to_click)
        root.bind("<Shift-W>", self.update_trigger_to_hover)
        root.bind("<Shift-E>", self.update_trigger_to_disabled)

        root.bind("1", self.update_build_mode_to_Empty)
        root.bind("2", self.update_build_mode_to_Barrier)
        root.bind("3", self.update_build_mode_to_Start)
        root.bind("4", self.update_build_mode_to_End)

    # region Build Mode
    def update_build_mode_to_Empty(self, event):

        self.current_build_state = "Empty"
        self.drop_box_state_list = self.update_drop_box_trigger_mode_second_part(self.right_frame, "Empty", self.update_drop_box_trigger_mode_first_part(self.drop_box_state_list), self.selected_state, 0.2, 0.3792, 0.6, 0.06)

    def update_build_mode_to_Barrier(self, event):

        self.current_build_state = "Barrier"
        self.drop_box_state_list = self.update_drop_box_trigger_mode_second_part(self.right_frame, "Barrier", self.update_drop_box_trigger_mode_first_part(self.drop_box_state_list), self.selected_state, 0.2, 0.3792, 0.6, 0.06)

    def update_build_mode_to_Start(self, event):

        self.current_build_state = "Start"
        self.drop_box_state_list = self.update_drop_box_trigger_mode_second_part(self.right_frame, "Start", self.update_drop_box_trigger_mode_first_part(self.drop_box_state_list), self.selected_state, 0.2, 0.3792, 0.6, 0.06)

    def update_build_mode_to_End(self, event):

        self.current_build_state = "End"
        self.drop_box_state_list = self.update_drop_box_trigger_mode_second_part(self.right_frame, "End", self.update_drop_box_trigger_mode_first_part(self.drop_box_state_list), self.selected_state, 0.2, 0.3792, 0.6, 0.06)


    # endregion

    # region Trigger Mode

    def update_trigger_to_click(self, event):

        self.current_trigger_state = "Click"
        self.drop_box_trigger_mode_list = self.update_drop_box_trigger_mode_second_part(self.right_frame, "Click", self.update_drop_box_trigger_mode_first_part(self.drop_box_trigger_mode_list), self.update_trigger_mode, 0.2, 0.4984, 0.6, 0.06)

    def update_trigger_to_hover(self, event):

        self.current_trigger_state = "Hover"
        self.drop_box_trigger_mode_list = self.update_drop_box_trigger_mode_second_part(self.right_frame, "Hover", self.update_drop_box_trigger_mode_first_part(self.drop_box_trigger_mode_list), self.update_trigger_mode, 0.2, 0.4984, 0.6, 0.06)

    def update_trigger_to_disabled(self, event):
        self.current_trigger_state = "Disabled"
        self.drop_box_trigger_mode_list = self.update_drop_box_trigger_mode_second_part(self.right_frame, "Disabled", self.update_drop_box_trigger_mode_first_part(self.drop_box_trigger_mode_list), self.update_trigger_mode, 0.2, 0.4984, 0.6, 0.06)

    # endregion

    # endregion

    # region Methods

    def update_start_or_end_points(self, state, row, col):
        if state == "Start":
            self.current_start_position = [row, col]
        elif state == "End":
            self.current_end_position = [row, col]

    def is_empty_of_start_or_end_points(self, state):
        if state == "Start":
            if self.current_start_position == []:
                return True
            return False
        if state == "End":
            if self.current_end_position == []:
                return True
            return False

    def get_label_location(self, event):

        # region info
        """
            # return the event label location


            :return: Nothing
            :rtype: None
        """
        # endregion

        row = 0
        col = 0

        if not len(str(event.widget)) == 15:

            value = int(str(event.widget)[15:]) - 1 - self.number_of_deleted_board_labels # last variable in case of new boards created without restarting the game. Python continues to sum the total amount of labels which existed overall.
            limit_row = S_T.BOARD_HEIGHT
            limit_col = S_T.BOARD_WIDTH
            if limit_row == limit_col:

                row = value // limit_row
                col = value % limit_col

            elif limit_row > limit_col:

                row = value // limit_col
                col = value % limit_col

            else:

                row = value // limit_col
                col = value % limit_col

        return row, col

    def BFA(self):

        self.path_found_from_path_finding =  self.controller.BFA(self.current_start_position, self.current_end_position)
        self.highlight_labels(self.path_found_from_path_finding, C_V.HIGHLIGHT_PATH_COLOR)
        self.board[self.current_start_position[0]][self.current_start_position[1]].config(background = self.color_draw_dict["Start"])
        self.board[self.current_end_position[0]][self.current_end_position[1]].config(background=self.color_draw_dict["End"])

    def highlight_labels(self, labels, color):

        high_light_color = color

        for label in labels:
            self.board[label[0]][label[1]].config(background = high_light_color)



    # endregion