##############################################################################
# Run this script to start the game

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
# Bird images
BIRD = [
    pygame.image.load(
        os.path.join(os.getcwd(), "Dino-Runner", "assets", "Bird", "Bird1.png")
    ),
    pygame.image.load(
        os.path.join(os.getcwd(), "Dino-Runner", "assets", "Bird", "Bird2.png")
    ),
]

# Cactus images
LARGE_CACTUS = [
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Cactus", "LargeCactus1.png"
        )
    ),
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Cactus", "LargeCactus2.png"
        )
    ),
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Cactus", "LargeCactus3.png"
        )
    ),
]

SMALL_CACTUS = [
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Cactus", "SmallCactus1.png"
        )
    ),
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Cactus", "SmallCactus2.png"
        )
    ),
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Cactus", "SmallCactus3.png"
        )
    ),
]

# Dino images
DINO_DEAD = pygame.image.load(
    os.path.join(os.getcwd(), "Dino-Runner", "assets", "Dino", "DinoDead.png")
)

DINO_DUCK = [
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Dino", "DinoDuck1.png"
        )
    ),
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Dino", "DinoDuck2.png"
        )
    ),
]

DINO_RUN = [
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Dino", "DinoRun1.png"
        )
    ),
    pygame.image.load(
        os.path.join(
            os.getcwd(), "Dino-Runner", "assets", "Dino", "DinoRun2.png"
        )
    ),
]

DINO_START = pygame.image.load(
    os.path.join(os.getcwd(), "Dino-Runner", "assets", "Dino", "DinoStart.png")
)

# Other images
CLOUD = pygame.image.load(
    os.path.join(os.getcwd(), "Dino-Runner", "assets", "Other", "Cloud.png")
)

GAME_OVER = pygame.image.load(
    os.path.join(os.getcwd(), "Dino-Runner", "assets", "Other", "GameOver.png")
)

TRACK = pygame.image.load(
    os.path.join(os.getcwd(), "Dino-Runner", "assets", "Other", "Track.png")
)

RESET = pygame.image.load(
    os.path.join(os.getcwd(), "Dino-Runner", "assets", "Other", "Reset.png")
)

# Game icon
ICON = pygame.image.load(
    os.path.join(os.getcwd(), "Dino-Runner", "assets", "DinoWallpaper.png")
)

##############################################################################
# Main Game
##############################################################################
# Set game icon
pygame.display.set_icon(ICON)


def main():
    is_run = True

    # while is_run:
    WIN.blit(TRACK, (0, 0))


if __name__ == "__main__":
    main()

