import pygame
import sys
from constants import *
from game import Game

def main():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Морской Бой')
    
    game = Game(screen)
    game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()