import pygame, sys
from random import randrange
from pygame.locals import *
from ctypes import windll

pygame.init()
clock = pygame.time.Clock()
icon_bomb = pygame.image.load("bomb.png")
pygame.display.set_icon(icon_bomb)
screen = pygame.display.set_mode((350, 400))
pygame.display.set_caption("Minesweeper")

color_brown = pygame.Color(84, 51, 16)
color_beige = pygame.Color(254, 253, 237)
color_red = pygame.Color(255, 0, 0)
color_green = pygame.Color(0, 255, 0)
color_blue = pygame.Color(0, 0, 255)
color_white = pygame.Color(255, 255, 255)
color_black = pygame.Color(0, 0, 0)

game_font = pygame.font.Font("UniversLTStd-BoldEx.otf", 36)
