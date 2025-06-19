import pygame
from constants import *

class Button:
    """Класс для создания кнопок"""
    
    def __init__(self, x, y, width, height, text, color=(60, 80, 120), hover_color=(80, 100, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        """Отрисовка кнопки"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        """Проверка наведения мыши"""
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event, sound_manager=None):
        """Проверка клика по кнопке"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                if sound_manager:
                    sound_manager.play_sound('button')
                return True
        return False


class VolumeSlider:
    """Класс для ползунка громкости"""
    
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value
        self.dragging = False
        self.slider_width = 20
        
    def draw(self, screen, font_small):
        """Отрисовка ползунка"""
        # Рисуем фон ползунка
        pygame.draw.rect(screen, DARK_GRAY, self.rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=5)
        
        # Рисуем заполненную часть
        filled_width = int(self.rect.width * self.value)
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, filled_width, self.rect.height)
        pygame.draw.rect(screen, LIGHT_BLUE, filled_rect, border_radius=5)
        
        # Рисуем ползунок
        slider_x = self.rect.x + filled_width - self.slider_width // 2
        slider_rect = pygame.Rect(slider_x, self.rect.y - 5, self.slider_width, self.rect.height + 10)
        pygame.draw.rect(screen, WHITE, slider_rect, border_radius=3)
        pygame.draw.rect(screen, BLACK, slider_rect, 2, border_radius=3)
        
        # Рисуем иконку звука
        icon_x = self.rect.x - 35
        icon_y = self.rect.y + self.rect.height // 2
        # Динамик
        pygame.draw.polygon(screen, WHITE, [
            (icon_x, icon_y - 5),
            (icon_x + 10, icon_y - 10),
            (icon_x + 10, icon_y + 10),
            (icon_x, icon_y + 5)
        ])
        # Звуковые волны
        if self.value > 0:
            pygame.draw.arc(screen, WHITE, (icon_x + 12, icon_y - 8, 8, 16), -0.5, 0.5, 2)
        if self.value > 0.5:
            pygame.draw.arc(screen, WHITE, (icon_x + 16, icon_y - 12, 12, 24), -0.5, 0.5, 2)
        
        # Показываем процент громкости
        percent_text = font_small.render(f"{int(self.value * 100)}%", True, WHITE)
        screen.blit(percent_text, (self.rect.x + self.rect.width + 10, self.rect.y))
    
    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(event.pos[0])
                return True
        return False
    
    def update_value(self, mouse_x):
        """Обновление значения"""
        relative_x = mouse_x - self.rect.x
        self.value = max(0.0, min(1.0, relative_x / self.rect.width))


class NameInput:
    """Класс для поля ввода имени"""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False
        self.max_length = 15
        
    def draw(self, screen, font_small, font_medium, prompt="Введите имя:"):
        """Отрисовка поля ввода"""
        # Рисуем подсказку
        prompt_text = font_small.render(prompt, True, WHITE)
        screen.blit(prompt_text, (self.rect.x, self.rect.y - 30))
        
        # Рисуем поле ввода
        color = WHITE if self.active else GRAY
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        
        # Рисуем текст
        if self.text:
            text_surface = font_medium.render(self.text, True, WHITE)
        else:
            text_surface = font_medium.render("Нажмите для ввода", True, GRAY)
        
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        # Курсор
        if self.active:
            cursor_x = text_rect.right + 2
            pygame.draw.line(screen, WHITE, (cursor_x, text_rect.top), (cursor_x, text_rect.bottom), 2)
    
    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True  # Сигнал о завершении ввода
            elif len(self.text) < self.max_length:
                if event.unicode.isprintable():
                    self.text += event.unicode
        return False