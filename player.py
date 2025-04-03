import pygame

class Player:

    def __init__(self, x, y, width, height, color, screen_height, up_key, down_key):
        self.initial_x = x  # Store initial position for reset
        self.initial_y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.screen_height = screen_height
        self.up_key = up_key
        self.down_key = down_key
        self.speed = 0
        self.score = 0

    def move(self):
        self.rect.y += self.speed
        # Keep paddle within screen bounds
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.down_key:
                self.speed += 7
            if event.key == self.up_key:
                self.speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == self.down_key:
                self.speed -= 7
            if event.key == self.up_key:
                self.speed += 7

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def reset(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.speed = 0
        self.score = 0 # Reset score as well
