import pygame

"""
A button is a zone of the screen used to do something
For exemple the buttons in the menu that change the screen to the asked page.
"""
class Button(pygame.Rect):
    
    def __init__(self, center : int[2], width : int, height : int, text : str):
        self.pos = center
        self.width = width
        self.height = height
        self.text = text

