import pygame
from constants import *

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []
    
    def can_place_ship(self, length, x, y, horizontal):
        """Проверка возможности размещения корабля"""
        if horizontal:
            if x + length > GRID_SIZE:
                return False
            for i in range(length):
                if self.grid[y][x + i] != 0:
                    return False
        else:
            if y + length > GRID_SIZE:
                return False
            for i in range(length):
                if self.grid[y + i][x] != 0:
                    return False
        return True
    
    def place_ship(self, length, x, y, horizontal):
        """Размещение корабля на доске"""
        if not self.can_place_ship(length, x, y, horizontal):
            return False
        
        ship_cells = []
        if horizontal:
            for i in range(length):
                self.grid[y][x + i] = 1
                ship_cells.append((x + i, y))
        else:
            for i in range(length):
                self.grid[y + i][x] = 1
                ship_cells.append((x, y + i))
        
        self.ships.append(ship_cells)
        return True
    
    def draw(self, screen, x, y):
        """Отрисовка доски"""
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, BLACK, 
                           (x, y + i * CELL_SIZE), 
                           (x + GRID_SIZE * CELL_SIZE, y + i * CELL_SIZE), 2)
            pygame.draw.line(screen, BLACK, 
                           (x + i * CELL_SIZE, y), 
                           (x + i * CELL_SIZE, y + GRID_SIZE * CELL_SIZE), 2)
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == 1:
                    cell_rect = pygame.Rect(x + col * CELL_SIZE, 
                                          y + row * CELL_SIZE, 
                                          CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, GREEN, cell_rect)