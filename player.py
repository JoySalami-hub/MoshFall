import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.hp = 100
        self.max_hp = 100
        self.damage = 10

        self.relics = []
        self.story_items = set()
        self.flags = set()

        self.mercy = 0
        self.power = 0
        self.knowledge = 0

        self.combat_x = 610
        self.combat_y = 520

    def add_relic(self, relic):
        if relic["name"] not in [r["name"] for r in self.relics]:
            self.relics.append(relic)

    def get_rect_world(self):
        return pygame.Rect(self.x, self.y, 24, 24)

    def move_world(self, keys, obstacles, world_width, world_height):
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        new_rect_x = pygame.Rect(self.x + dx, self.y, 24, 24)
        blocked_x = any(new_rect_x.colliderect(obj) for obj in obstacles)
        if not blocked_x:
            self.x += dx

        new_rect_y = pygame.Rect(self.x, self.y + dy, 24, 24)
        blocked_y = any(new_rect_y.colliderect(obj) for obj in obstacles)
        if not blocked_y:
            self.y += dy

        self.x = max(240, min(self.x, world_width - 24))
        self.y = max(0, min(self.y, world_height - 24))

    def draw_world(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, (70, 220, 120), (self.x - camera_x, self.y - camera_y, 24, 24))

    def update_boss_combat(self, bounds):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.combat_y -= self.speed
        if keys[pygame.K_s]:
            self.combat_y += self.speed
        if keys[pygame.K_a]:
            self.combat_x -= self.speed
        if keys[pygame.K_d]:
            self.combat_x += self.speed

        self.combat_x = max(bounds.left, min(self.combat_x, bounds.right - 18))
        self.combat_y = max(bounds.top, min(self.combat_y, bounds.bottom - 18))

    def draw_boss_combat(self, screen):
        arena = pygame.Rect(260, 90, 700, 540)
        pygame.draw.rect(screen, (10, 10, 10), arena)
        pygame.draw.rect(screen, (255, 255, 255), arena, 2)
        pygame.draw.rect(screen, (70, 220, 120), (self.combat_x, self.combat_y, 18, 18))
