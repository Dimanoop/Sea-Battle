import random
from constants import GRID_SIZE

class ComputerAI:
    """Класс для управления искусственным интеллектом компьютера"""
    
    def __init__(self):
        self.last_hit = None
        self.hit_cells = []
        self.possible_targets = []
        self.hunt_mode = False
        self.ship_direction = None
        
    def get_next_shot(self, board):
        """Получить следующий ход компьютера"""
        # Если есть возможные цели рядом с попаданием
        if self.possible_targets:
            target = random.choice(self.possible_targets)
            self.possible_targets.remove(target)
            return target
        
        # Если было попадание, ищем клетки рядом
        if self.hit_cells:
            # Если есть несколько попаданий, определяем направление
            if len(self.hit_cells) >= 2:
                x_coords = [hit[0] for hit in self.hit_cells]
                y_coords = [hit[1] for hit in self.hit_cells]
                
                # Проверяем, все ли попадания на одной линии
                if len(set(y_coords)) == 1:
                    # Корабль горизонтальный
                    self.ship_direction = 'horizontal'
                    y = y_coords[0]
                    min_x = min(x_coords)
                    max_x = max(x_coords)
                    
                    # Проверяем только клетки слева и справа
                    if min_x > 0 and board.shots[y][min_x - 1] == 0:
                        self.possible_targets.append((min_x - 1, y))
                    if max_x < GRID_SIZE - 1 and board.shots[y][max_x + 1] == 0:
                        self.possible_targets.append((max_x + 1, y))
                        
                elif len(set(x_coords)) == 1:
                    # Корабль вертикальный
                    self.ship_direction = 'vertical'
                    x = x_coords[0]
                    min_y = min(y_coords)
                    max_y = max(y_coords)
                    
                    # Проверяем только клетки сверху и снизу
                    if min_y > 0 and board.shots[min_y - 1][x] == 0:
                        self.possible_targets.append((x, min_y - 1))
                    if max_y < GRID_SIZE - 1 and board.shots[max_y + 1][x] == 0:
                        self.possible_targets.append((x, max_y + 1))
                else:
                    # Попадания не на одной линии
                    self.add_adjacent_targets(board)
            
            # Если только одно попадание, проверяем все 4 стороны
            elif len(self.hit_cells) == 1:
                x, y = self.hit_cells[0]
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(directions)
                
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board.shots[ny][nx] == 0:
                        self.possible_targets.append((nx, ny))
            
            # Если есть цели, выбираем одну
            if self.possible_targets:
                target = random.choice(self.possible_targets)
                self.possible_targets.remove(target)
                return target
        
        # Случайный выстрел в шахматном порядке для эффективности
        valid_moves = []
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if board.shots[y][x] == 0:
                    # Предпочитаем клетки в шахматном порядке
                    if (x + y) % 2 == 0:
                        valid_moves.append((x, y))
        
        # Если нет клеток в шахматном порядке, берем любые
        if not valid_moves:
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    if board.shots[y][x] == 0:
                        valid_moves.append((x, y))
        
        if valid_moves:
            return random.choice(valid_moves)
        
        return None
    
    def add_adjacent_targets(self, board):
        """Добавляет соседние клетки для всех попаданий"""
        for x, y in self.hit_cells:
            # Если направление уже определено, добавляем только клетки в этом направлении
            if self.ship_direction == 'horizontal':
                for dx in [-1, 1]:
                    nx = x + dx
                    if 0 <= nx < GRID_SIZE and board.shots[y][nx] == 0:
                        if (nx, y) not in self.possible_targets:
                            self.possible_targets.append((nx, y))
            elif self.ship_direction == 'vertical':
                for dy in [-1, 1]:
                    ny = y + dy
                    if 0 <= ny < GRID_SIZE and board.shots[ny][x] == 0:
                        if (x, ny) not in self.possible_targets:
                            self.possible_targets.append((x, ny))
            else:
                # Направление неизвестно, проверяем все 4 стороны
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board.shots[ny][nx] == 0:
                        if (nx, ny) not in self.possible_targets:
                            self.possible_targets.append((nx, ny))
    
    def register_hit(self, x, y):
        """Регистрация попадания"""
        self.last_hit = (x, y)
        self.hit_cells.append((x, y))
        self.hunt_mode = True
        
        # Если уже есть попадания, пытаемся определить направление
        if len(self.hit_cells) >= 2 and self.ship_direction is None:
            x_coords = [hit[0] for hit in self.hit_cells]
            y_coords = [hit[1] for hit in self.hit_cells]
            
            if len(set(y_coords)) == 1:
                self.ship_direction = 'horizontal'
                self.possible_targets = []
            elif len(set(x_coords)) == 1:
                self.ship_direction = 'vertical'
                self.possible_targets = []
    
    def register_miss(self, x, y):
        """Регистрация промаха"""
        if (x, y) in self.possible_targets:
            self.possible_targets.remove((x, y))
    
    def register_sunk(self):
        """Регистрация потопления корабля"""
        self.last_hit = None
        self.hit_cells = []
        self.possible_targets = []
        self.hunt_mode = False
        self.ship_direction = None