from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk
from Utilities.Values import *
from controller import *


class Start(object):

    def __init__(self):

        # region info
        """
            This class allows to start the menu and work with it

            :param self.root: the root to the main tkinter page
            :type self.root: TK
            :param self.menu: the connection to the menu class
            :type self.menu: GameMenu
            :param self.image_collection: the connection to the image collection class
            :type self.image_collection: ImageCollection

            :return: Nothing
            :rtype: None
        """

        # endregion

        self.root = ""
        self.menu = ""
        self.image_collection = ""
        self.start_menu()

    def start_menu(self):

        # region info
        """
            start the menu from the main class

            :return: Nothing
            :rtype: None
        """

        # endregion


        self.root = Tk()
        self.root.title("Chess")
        self.root.geometry(str(S_T.WIDTH)+"x"+str(S_T.HEIGHT))
        self.root.resizable(0, 0)
        self.root['bg'] = C_V.PAGE_COLOR
        self.controller = Controller(self.root)








        self.root.mainloop()


def Main():

    start = Start()


if __name__ == "__main__":
    Main()

