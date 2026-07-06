import pygame

class DialogueBox:
    def __init__(self, text, choices):
        self.text = text
        self.choices = choices
        self.choice_rects = []
        self.font = pygame.font.SysFont("consolas", 22)
        self.small_font = pygame.font.SysFont("consolas", 18)

    def wrap_text(self, text, max_width):
        words = text.split(" ")
        lines = []
        current = ""

        for word in words:
            test = current + word + " "
            if self.font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current.strip())
                current = word + " "
        if current:
            lines.append(current.strip())
        return lines

    def draw(self, screen):
        self.choice_rects = []

        box = pygame.Rect(100, 400, 1000, 240)
        pygame.draw.rect(screen, (0, 0, 0), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)

        old_clip = screen.get_clip()
        text_area = pygame.Rect(125, 422, 930, 96)
        screen.set_clip(text_area)
        lines = self.wrap_text(self.text, 930)
        for i, line in enumerate(lines[:3]):
            screen.blit(self.font.render(line, True, (255, 255, 255)), (125, 425 + i * 28))
        screen.set_clip(old_clip)

        choice_area = pygame.Rect(125, 520, 900, 104)
        pygame.draw.rect(screen, (8, 8, 8), choice_area)

        old_clip = screen.get_clip()
        screen.set_clip(choice_area)
        visible_count = min(len(self.choices), 5)
        button_h = 20 if visible_count > 4 else 24
        gap = 1 if visible_count > 4 else 4

        for i, choice in enumerate(self.choices[:visible_count]):
            rect = pygame.Rect(125, 524 + i * (button_h + gap), 760, button_h)
            pygame.draw.rect(screen, (45, 45, 45), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)

            label = choice["text"]
            while self.small_font.size(label)[0] > rect.width - 16 and len(label) > 4:
                label = label[:-4] + "..."
            screen.blit(self.small_font.render(label, True, (255, 255, 255)), (rect.x + 8, rect.y + 2))
            self.choice_rects.append((rect, choice))
        screen.set_clip(old_clip)

    def click(self, pos):
        for rect, choice in self.choice_rects:
            if rect.collidepoint(pos):
                return choice
        return None
