import pygame
from constants import *

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    def draw(self, screen, x, y):
        """Отрисовка доски"""
        # Рисуем сетку
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, BLACK, 
                           (x, y + i * CELL_SIZE), 
                           (x + GRID_SIZE * CELL_SIZE, y + i * CELL_SIZE), 2)
            pygame.draw.line(screen, BLACK, 
                           (x + i * CELL_SIZE, y), 
                           (x + i * CELL_SIZE, y + GRID_SIZE * CELL_SIZE), 2)
        
        # Рисуем содержимое клеток
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == 1:
                    cell_rect = pygame.Rect(x + col * CELL_SIZE, 
                                          y + row * CELL_SIZE, 
                                          CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, GREEN, cell_rect)