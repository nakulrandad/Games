##############################################################################
# Run this script from main directory ("Games") to start the game

# Primary Contributor: Nakul Randad
##############################################################################

##############################################################################
# Package imports
##############################################################################
import os
import sys
import pygame
import random

# import numpy as np

##############################################################################
# Initialisation
##############################################################################
pygame.init()

FPS = 60
ASPECT_RATIO = (16, 9)
SCALE_FACTOR = 90
WIDTH, HEIGHT = ASPECT_RATIO[0] * SCALE_FACTOR, ASPECT_RATIO[1] * SCALE_FACTOR
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")

##############################################################################
# Load Images
##############################################################################
asset_file_loc = os.path.join(os.getcwd(), "Dino-Runner", "assets")

# Bird images
BIRD = [
    pygame.image.load(os.path.join(asset_file_loc, "Bird", "Bird1.png")),
    pygame.image.load(os.path.join(asset_file_loc, "Bird", "Bird2.png")),
]

# Cactus images
LARGE_CACTUS = [
    pygame.image.load(
        os.path.join(asset_file_loc, "Cactus", "LargeCactus1.png")
    ),
    pygame.image.load(
        os.path.join(asset_file_loc, "Cactus", "LargeCactus2.png")
    ),
    pygame.image.load(
        os.path.join(asset_file_loc, "Cactus", "LargeCactus3.png")
    ),
]

SMALL_CACTUS = [
    pygame.image.load(
        os.path.join(asset_file_loc, "Cactus", "SmallCactus1.png")
    ),
    pygame.image.load(
        os.path.join(asset_file_loc, "Cactus", "SmallCactus2.png")
    ),
    pygame.image.load(
        os.path.join(asset_file_loc, "Cactus", "SmallCactus3.png")
    ),
]

# Dino images
DINO_DEAD = pygame.image.load(
    os.path.join(asset_file_loc, "Dino", "DinoDead.png")
)

DINO_DUCK = [
    pygame.image.load(os.path.join(asset_file_loc, "Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join(asset_file_loc, "Dino", "DinoDuck2.png")),
]

DINO_RUN = [
    pygame.image.load(os.path.join(asset_file_loc, "Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join(asset_file_loc, "Dino", "DinoRun2.png")),
]

DINO_START = pygame.image.load(
    os.path.join(asset_file_loc, "Dino", "DinoStart.png")
)

# Other images
CLOUD = pygame.image.load(os.path.join(asset_file_loc, "Other", "Cloud.png"))

GAME_OVER = pygame.image.load(
    os.path.join(asset_file_loc, "Other", "GameOver.png")
)

TRACK = pygame.image.load(os.path.join(asset_file_loc, "Other", "Track.png"))

RESET = pygame.image.load(os.path.join(asset_file_loc, "Other", "Reset.png"))

# Game icon
ICON = pygame.image.load(os.path.join(asset_file_loc, "DinoWallpaper.png"))

ICON_INVERT = pygame.image.load(
    os.path.join(asset_file_loc, "DinoWallpaperInvert.png")
)

##############################################################################
# Main Game
##############################################################################
# Set game icon
pygame.display.set_icon(ICON_INVERT)

# Set game fps
FPS = 60
pygame.time.Clock()


class Dino:
    def __init__(self):
        self.dino_img = None
        self.duck_img = None
        self.dead_img = None
        self.jump_img = None
        self.my_img = None
        self.mask = pygame.mask.from_surface(self.my_img)

        self.x_pos = None
        self.y_pos = None
        self.speed = None
        self.score = None

        self.is_running = True
        self.is_jumping = False
        self.is_ducking = False
        self.is_dead = False

        self.jump_height = None
        self.jump_time = 1  # in seconds
        self.jump_frame_limit = self.jump_time * FPS

    def jump(self):
        pass

    def duck(self):
        pass

    def run(self):
        pass

    def dead(self):
        pass

    def draw(self, window):
        pass


class Obstacle:
    def __init__(self):
        self.x_pos = None
        self.y_pos = None

        self.my_img = None
        self.mask = pygame.mask.from_surface(self.my_img)

    def draw(self, window):
        pass


def is_colliding(obj1, obj2):
    offset_x = int(obj2.x_pos - obj1.x_pos)
    offset_y = int(obj2.y_pos - obj1.y_pos)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    is_run = True

    # while is_run:
    WIN.blit(TRACK, (0, 0))


if __name__ == "__main__":
    main()

