import pygame
from constants import *
from board import Board
from sound_manager import SoundManager

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "menu"
        self.player_board = Board()
        self.opponent_board = Board()
        self.ship_placement_index = 0
        self.ship_horizontal = True
        
        self.fonts = {
            'big': pygame.font.SysFont('Arial', 36),
            'medium': pygame.font.SysFont('Arial', 24),
            'small': pygame.font.SysFont('Arial', 20)
        }

        self.sound_manager = SoundManager()

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.state == "place_ships":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.try_place_ship(mouse_x, mouse_y)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Поворот корабля
                        self.ship_horizontal = not self.ship_horizontal
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == "menu":
                        self.state = "place_ships"
        
        return True
    
    def try_place_ship(self, x, y):
        """Попытка разместить корабль"""
        if self.ship_placement_index < len(SHIPS):
            ship_length = SHIPS[self.ship_placement_index]
            
            # Переводим координаты в индексы сетки
            grid_x = (x - BOARD1_X) // CELL_SIZE
            grid_y = (y - BOARD1_Y) // CELL_SIZE
            
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                if self.player_board.place_ship(ship_length, grid_x, grid_y, self.ship_horizontal):
                    self.ship_placement_index += 1
                    
                    if self.ship_placement_index >= len(SHIPS):
                        self.state = "game"
                        # Размещаем корабли компьютера случайно
                        self.place_computer_ships()
    
    def place_computer_ships(self):
        """Случайная расстановка кораблей компьютера"""
        import random
        for ship_length in SHIPS:
            placed = False
            while not placed:
                x = random.randint(0, GRID_SIZE-1)
                y = random.randint(0, GRID_SIZE-1)
                horizontal = random.choice([True, False])
                if self.opponent_board.place_ship(ship_length, x, y, horizontal):
                    placed = True

    def try_shoot(self, x, y):
        """Попытка выстрела с чередованием ходов"""
        if self.current_player == 0:  # Ход игрока
            grid_x = (x - BOARD2_X) // CELL_SIZE
            grid_y = (y - BOARD2_Y) // CELL_SIZE
            
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                hit, message = self.opponent_board.shoot(grid_x, grid_y)
                if message != "Недопустимый ход":
                    if not hit:  # Если промах, передаем ход
                        self.current_player = 1
                        self.computer_turn()
    
    def computer_turn(self):
        """Ход компьютера"""
        import time
        time.sleep(0.5)  # Небольшая задержка
        
        target = self.computer_ai.get_next_shot(self.player_board)
        if target:
            x, y = target
            hit, message = self.player_board.shoot(x, y)
            if not hit:  # Если промах, передаем ход игроку
                self.current_player = 0

    def try_shoot(self, x, y):
        """Выстрел со звуком"""
        # ... код выстрела
        if hit:
            self.sound_manager.play_sound('hit')
        else:
            self.sound_manager.play_sound('miss')