import pygame

class Boss:
    def __init__(self, region):
        region_order = ["Forest", "Village", "Caverns", "Citadel"]
        self.region_level = region_order.index(region) if region in region_order else 0
        self.name = f"{region} Moss Bear"
        self.hp = 220 + self.region_level * 70
        self.max_hp = self.hp
        self.projectile_damage = 1 + self.region_level
        self.x = 560
        self.y = 170
        self.vx = 3 + self.region_level
        self.vy = 2 + self.region_level // 2
        self.attack_timer = 0
        self.shot_cooldown = 0
        self.projectiles = []
        self.player_pellets = []

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 80, 62)

    def update_survivor_style(self, player, bounds):
        self.attack_timer += 1
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1

        self.x += self.vx
        self.y += self.vy
        boss_rect = self.get_rect()
        boss_top_limit = bounds.top
        boss_bottom_limit = bounds.top + 210

        if boss_rect.left <= bounds.left or boss_rect.right >= bounds.right:
            self.vx *= -1
            self.x = max(bounds.left, min(self.x, bounds.right - boss_rect.width))
        if boss_rect.top <= boss_top_limit or boss_rect.bottom >= boss_bottom_limit:
            self.vy *= -1
            self.y = max(boss_top_limit, min(self.y, boss_bottom_limit - boss_rect.height))

        if self.attack_timer % max(22, 42 - self.region_level * 5) == 0:
            self.spawn_attack()

        player_rect = pygame.Rect(player.combat_x, player.combat_y, 18, 18)
        for proj in self.projectiles:
            proj["rect"].x += proj["vx"]
            proj["rect"].y += proj["vy"]
            if self.region_level == 2 and (proj["rect"].left <= bounds.left or proj["rect"].right >= bounds.right):
                proj["vx"] *= -1
            if proj["rect"].colliderect(player_rect):
                player.hp = max(0, player.hp - self.projectile_damage)
                proj["rect"].y = bounds.bottom + 100

        self.projectiles = [p for p in self.projectiles if p["rect"].top < bounds.bottom and p["rect"].right > bounds.left and p["rect"].left < bounds.right]

        for pellet in self.player_pellets:
            pellet.y -= 8
            if pellet.colliderect(self.get_rect()):
                self.hp -= player.damage
                pellet.y = bounds.top - 100

        self.player_pellets = [p for p in self.player_pellets if p.bottom > bounds.top]

    def fire_player_pellet(self, player):
        if self.shot_cooldown == 0:
            self.player_pellets.append(pygame.Rect(player.combat_x + 7, player.combat_y - 10, 5, 10))
            if "Forest Gate Key" in player.story_items:
                self.player_pellets.append(pygame.Rect(player.combat_x + 4, player.combat_y - 16, 11, 5))
            if "Village Gate Key" in player.story_items:
                self.player_pellets.append(pygame.Rect(player.combat_x - 4, player.combat_y - 8, 5, 10))
                self.player_pellets.append(pygame.Rect(player.combat_x + 18, player.combat_y - 8, 5, 10))
            if "Caverns Gate Key" in player.story_items:
                self.player_pellets.append(pygame.Rect(player.combat_x + 4, player.combat_y - 18, 10, 5))
            if "Citadel Gate Key" in player.story_items:
                self.player_pellets.append(pygame.Rect(player.combat_x + 6, player.combat_y - 26, 8, 8))
            self.shot_cooldown = 12
            return True
        return False

    def spawn_attack(self):
        if self.region_level == 0:
            for offset in (10, 34, 58):
                self.projectiles.append({"rect": pygame.Rect(self.x + offset, self.y + 30, 12, 12), "vx": 0, "vy": 5})
        elif self.region_level == 1:
            for vx in (-2, 0, 2):
                self.projectiles.append({"rect": pygame.Rect(self.x + 38, self.y + 30, 12, 12), "vx": vx, "vy": 5})
        elif self.region_level == 2:
            for offset, vx in ((8, 3), (34, -3), (60, 3)):
                self.projectiles.append({"rect": pygame.Rect(self.x + offset, self.y + 30, 12, 12), "vx": vx, "vy": 4})
        else:
            for vx, vy in ((-3, 4), (-1, 5), (1, 5), (3, 4), (0, 6)):
                self.projectiles.append({"rect": pygame.Rect(self.x + 38, self.y + 30, 12, 12), "vx": vx, "vy": vy})

    def draw(self, screen):
        pygame.draw.rect(screen, (90, 55, 35), (self.x, self.y, 80, 62))
        pygame.draw.rect(screen, (55, 120, 70), (self.x + 8, self.y - 14, 64, 20))
        pygame.draw.rect(screen, (180, 220, 180), (self.x + 18, self.y + 12, 12, 12))
        pygame.draw.rect(screen, (180, 220, 180), (self.x + 50, self.y + 12, 12, 12))
        pygame.draw.rect(screen, (45, 30, 20), (self.x + 12, self.y + 45, 56, 12))

        for pellet in self.player_pellets:
            pygame.draw.rect(screen, (240, 245, 150), pellet)
        for proj in self.projectiles:
            pygame.draw.rect(screen, (120, 255, 120), proj["rect"])
