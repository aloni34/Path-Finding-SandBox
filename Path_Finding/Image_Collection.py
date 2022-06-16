from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk
from Utilities.Values import *
from Utilities.Values import *


class ImageCollection(object):


    # region Constructer
    def __init__(self, root):

        # region info
        """
            This class allows easy work with images

            :param self.root: the root to the main tkinter page
            :type self.root: TK

            :return: Nothing
            :rtype: None
        """

        # endregion

        self.root = root
        self.image_list = self.decompress_images()
    # endregion

    # region Methods
    def decompress_images(self):

        # region info
        """
            This function compresses images based on a path and name I give him

            :return: Nothing
            :rtype: None
        """

        # endregion

        # Insert all the images I want to decompress
        image_list = []
        image_names = ["Restart.png", "white_sign.png", "black_sign.png", "empty_black_image.png", "play.png", "load_game.png", "Settings.png", "rules.png", "back.png", "Size.png", "1920x1080.png", "1632x810.png", "1200x600.png", "960x540.png", "menu.png", "mode.png", "difficulty.png", "easy.png", "medium.png", "hard.png", "quit.png", "start_side.png", "black.png", "white.png", "black_ai.png", "white_ai.png", "black_player.png", "white_player.png", "ai_player.png", "chess_rules.png", "test.png", "check.png"]

        # Different resizing
        for i in range(len(image_names)):

            image = Image.open("Images" + '\\' + image_names[i])
            image = image.resize((S_T.WIDTH // 15, S_T.HEIGHT // 18), Image.ANTIALIAS)
            logo1 = ImageTk.PhotoImage(image)
            image_list.append((logo1))



        return image_list

    def get_image_list(self):

        return self.image_list
    # endregion

