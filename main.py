import pygame
import random
from player import Player
from world import World
from dialogue import DialogueBox
from boss import Boss
from upgrades import generate_upgrades
from relics import apply_relics
from save import save_game, load_game, slot_label

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
WORLD_WIDTH, WORLD_HEIGHT = 3200, 2200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mossfall")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)
small_font = pygame.font.SysFont("consolas", 16)

MENU = "menu"
HOW_TO = "how_to"
DIALOGUE = "dialogue"
EXPLORE = "explore"
BOSS_DIALOGUE = "boss_dialogue"
BOSS_COMBAT = "boss_combat"
BOSS_REWARD = "boss_reward"
UPGRADE_DELAY = "upgrade_delay"
LEVELUP = "levelup"
PAUSE = "pause"
SLOT_SAVE = "slot_save"
SLOT_LOAD = "slot_load"
GAME_OVER = "game_over"
ENDING = "ending"

state = MENU

player = Player(500, 500)
world = World()
boss = None
dialogue = None
upgrade_options = []

camera_x = 0
camera_y = 0

toast_message = ""
toast_timer = 0
item_popup = None
item_popup_timer = 0
boss_mood = 65
boss_result_text = ""
boss_reward_relic = None
upgrade_delay_timer = 0
game_over_tick = 0
slot_back_state = MENU

def show_toast(text, duration=180):
    global toast_message, toast_timer
    toast_message = text
    toast_timer = duration

def show_item_popup(title, description, duration=210):
    global item_popup, item_popup_timer
    item_popup = {"title": title, "description": description}
    item_popup_timer = duration

def relic_description(relic):
    descriptions = {
        "Moss Lens": "A veined lens that reveals patterns in living moss. Knowledge +1.",
        "Root Charm": "A warm charm that teaches old roots to be kind. Max health +20 and fully heals you.",
        "Ancient Acorn": "A seed from before the blight. Max health +20.",
        "Moss Crown": "A thorned crown of green iron. Damage +5.",
        "Broken Compass": "It points toward danger before north. Speed +1."
    }
    return descriptions.get(relic["name"], "A strange forest relic hums softly in your pack.")

def draw_text(text, x, y, color=(255, 255, 255), use_small=False):
    active_font = small_font if use_small else font
    screen.blit(active_font.render(str(text), True, color), (x, y))

def draw_menu_button(rect, label, mouse):
    color = (70, 94, 66) if rect.collidepoint(mouse) else (42, 58, 42)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (230, 230, 190), rect, 3)
    text = font.render(label, True, (245, 245, 220))
    screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

def menu_play_rect():
    return pygame.Rect(470, 390, 260, 54)

def menu_load_rect():
    return pygame.Rect(470, 460, 260, 54)

def menu_how_to_rect():
    return pygame.Rect(470, 530, 260, 54)

def menu_exit_rect():
    return pygame.Rect(470, 600, 260, 54)

def menu_back_rect():
    return pygame.Rect(470, 570, 260, 54)

def boss_continue_rect():
    return pygame.Rect(470, 420, 260, 54)

def pause_save_rect():
    return pygame.Rect(470, 250, 220, 50)

def pause_load_rect():
    return pygame.Rect(470, 320, 220, 50)

def pause_exit_rect():
    return pygame.Rect(470, 390, 220, 50)

def slot_one_rect():
    return pygame.Rect(430, 300, 340, 54)

def slot_two_rect():
    return pygame.Rect(430, 370, 340, 54)

def slot_back_rect():
    return pygame.Rect(470, 470, 260, 54)

def game_over_load_rect():
    return pygame.Rect(470, 430, 260, 54)

def game_over_menu_rect():
    return pygame.Rect(470, 500, 260, 54)

def game_over_exit_rect():
    return pygame.Rect(470, 570, 260, 54)

def draw_pixel_forest_art():
    pygame.draw.rect(screen, (14, 22, 20), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, 18):
        shade = 18 + (y // 18) % 4 * 4
        pygame.draw.rect(screen, (shade, shade + 12, shade + 4), (0, y, SCREEN_WIDTH, 18))

    pygame.draw.rect(screen, (36, 72, 46), (0, 500, SCREEN_WIDTH, 200))
    for x in range(80, 1120, 120):
        pygame.draw.rect(screen, (58, 40, 26), (x, 250, 34, 270))
        pygame.draw.rect(screen, (34, 95, 52), (x - 42, 190, 118, 86))
        pygame.draw.rect(screen, (28, 78, 44), (x - 26, 146, 86, 70))
        pygame.draw.rect(screen, (95, 150, 125), (x - 6, 268, 22, 22))

    pygame.draw.rect(screen, (44, 120, 76), (530, 350, 140, 130))
    pygame.draw.rect(screen, (90, 60, 38), (585, 292, 34, 80))
    pygame.draw.rect(screen, (80, 160, 220), (554, 274, 96, 42))
    pygame.draw.rect(screen, (165, 230, 245), (576, 284, 52, 18))

    pygame.draw.rect(screen, (72, 52, 34), (920, 380, 100, 76))
    pygame.draw.rect(screen, (52, 115, 70), (930, 340, 80, 45))
    pygame.draw.rect(screen, (220, 230, 170), (948, 362, 12, 12))
    pygame.draw.rect(screen, (220, 230, 170), (988, 362, 12, 12))

def draw_menu(mouse):
    draw_pixel_forest_art()
    title = pygame.font.SysFont("consolas", 64, bold=True).render("MOSSFALL", True, (240, 245, 220))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 110))
    draw_text("A quiet forest, a lost map, and a bear that remembers too much.", 310, 200, (220, 230, 200), use_small=True)
    draw_menu_button(menu_play_rect(), "PLAY", mouse)
    draw_menu_button(menu_load_rect(), "LOAD GAME", mouse)
    draw_menu_button(menu_how_to_rect(), "HOW TO PLAY", mouse)
    draw_menu_button(menu_exit_rect(), "EXIT GAME", mouse)

def draw_how_to(mouse):
    draw_pixel_forest_art()
    panel = pygame.Rect(260, 120, 680, 410)
    pygame.draw.rect(screen, (18, 22, 20), panel)
    pygame.draw.rect(screen, (230, 230, 190), panel, 3)

    draw_text("HOW TO PLAY", 520, 150, (240, 245, 220))
    lines = [
        "WASD: Move through the world and dodge during boss fights.",
        "Mouse Click: Talk to NPCs, inspect places, and choose dialogue.",
        "Space: Fire a pellet upward during boss combat.",
        "Escape: Pause, then save from the pause menu.",
        "Goal: Help forest dwellers, gain Knowledge, earn Elder Rowan's trust,",
        "find the shrine, survive or soothe the Moss Bear, then open the gate."
    ]
    for i, line in enumerate(lines):
        draw_text(line, 310, 210 + i * 34, (225, 230, 210), use_small=True)

    draw_menu_button(menu_back_rect(), "BACK", mouse)

def draw_slot_select(mouse, saving):
    draw_pixel_forest_art()
    title = "SAVE GAME" if saving else "LOAD GAME"
    draw_text(title, 535, 210, (240, 245, 220))
    draw_menu_button(slot_one_rect(), slot_label(1), mouse)
    draw_menu_button(slot_two_rect(), slot_label(2), mouse)
    draw_menu_button(slot_back_rect(), "BACK", mouse)

def draw_game_over(mouse):
    screen.fill((8, 8, 12))
    for i in range(18):
        x = 120 + i * 58
        h = 80 + ((game_over_tick + i * 13) % 90)
        pygame.draw.rect(screen, (30, 80, 48), (x, 620 - h, 28, h))
        pygame.draw.rect(screen, (70, 130, 80), (x - 8, 612 - h, 44, 18))

    pulse = 20 + (game_over_tick % 60)
    pygame.draw.rect(screen, (90 + pulse, 30, 35), (520, 180, 160, 120))
    pygame.draw.rect(screen, (35, 18, 20), (545, 215, 30, 26))
    pygame.draw.rect(screen, (35, 18, 20), (625, 215, 30, 26))
    pygame.draw.rect(screen, (230, 220, 180), (560, 270, 80, 12))

    title = pygame.font.SysFont("consolas", 54, bold=True).render("GAME OVER", True, (245, 220, 210))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 330))
    draw_text("The moss remembers your footsteps. Try another path.", 365, 390, (220, 230, 210), use_small=True)
    draw_menu_button(game_over_load_rect(), "LOAD GAME", mouse)
    draw_menu_button(game_over_menu_rect(), "MAIN MENU", mouse)
    draw_menu_button(game_over_exit_rect(), "EXIT GAME", mouse)

def draw_ending():
    screen.fill((12, 18, 16))
    for i, relic in enumerate(player.relics[:8]):
        x = 270 + i * 82
        pygame.draw.rect(screen, (80, 140, 95), (x, 240 + (i % 2) * 28, 46, 46))
        pygame.draw.rect(screen, (235, 230, 180), (x, 240 + (i % 2) * 28, 46, 46), 2)
    title = pygame.font.SysFont("consolas", 46, bold=True).render("THE MOSS REMEMBERS", True, (240, 245, 220))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 140))
    draw_text("Your relics root themselves into the last gate.", 390, 340, (225, 230, 210))
    draw_text("The blight does not vanish, but it learns your name and lets the road breathe.", 275, 380, (225, 230, 210), use_small=True)
    draw_text("Press Escape to return to the title.", 450, 470, (255, 255, 140), use_small=True)

def draw_health_bar(surface, x, y, width, height, hp, max_hp):
    pygame.draw.rect(surface, (18, 18, 18), (x, y - 24, width, height + 30))
    pygame.draw.rect(surface, (255, 255, 255), (x, y - 24, width, height + 30), 2)
    draw_text("Wanderer Health", x + 8, y - 20, (255, 255, 255), use_small=True)

    ratio = 0 if max_hp <= 0 else max(0, min(1, hp / max_hp))
    pygame.draw.rect(surface, (90, 20, 20), (x, y, width, height))
    pygame.draw.rect(surface, (40, 180, 70), (x, y, int(width * ratio), height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

    draw_text(f"{hp}/{max_hp}", x + width - 70, y - 20, (220, 220, 220), use_small=True)

def draw_inventory(surface, player):
    panel_x = 0
    panel_w = 240

    pygame.draw.rect(surface, (18, 18, 18), (panel_x, 0, panel_w, SCREEN_HEIGHT))
    pygame.draw.rect(surface, (255, 255, 255), (panel_x, 0, panel_w, SCREEN_HEIGHT), 2)

    draw_text("INVENTORY", 18, 18)
    draw_text("Relics", 18, 108, (200, 230, 200))

    if player.relics:
        for i, relic in enumerate(player.relics[:10]):
            draw_text(f"- {relic['name']}", 18, 138 + i * 24, use_small=True)
    else:
        draw_text("- none", 18, 138, use_small=True)

    draw_text("Quest Items", 18, 330, (200, 230, 200))
    if player.story_items:
        for i, item in enumerate(sorted(player.story_items)[:8]):
            draw_text(f"- {item}", 18, 360 + i * 24, use_small=True)
    else:
        draw_text("- none", 18, 360, use_small=True)

    draw_text("Traits", 18, 540, (200, 230, 200))
    draw_text(f"Mercy: {player.mercy}", 18, 570, use_small=True)
    draw_text(f"Power: {player.power}", 18, 594, use_small=True)
    draw_text(f"Knowledge: {player.knowledge}", 18, 618, use_small=True)

def draw_region_header():
    draw_text(f"Region: {world.region}", 270, 12)
    for i, goal in enumerate(world.region_goal_texts(player)[:4]):
        draw_text(goal, 270, 40 + i * 22, (220, 220, 180), use_small=True)

def draw_toast():
    global toast_timer
    if toast_timer > 0:
        box_w = 360
        box_h = 56
        box_x = (SCREEN_WIDTH - box_w) // 2
        box_y = (SCREEN_HEIGHT - box_h) // 2

        box = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(screen, (20, 20, 20), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 2)
        draw_text(toast_message, box_x + 20, box_y + 16, (255, 255, 140))
        toast_timer -= 1

def draw_item_popup():
    global item_popup_timer, item_popup
    if not item_popup or item_popup_timer <= 0:
        return

    panel = pygame.Rect(330, 245, 540, 150)
    pygame.draw.rect(screen, (16, 20, 18), panel)
    pygame.draw.rect(screen, (235, 230, 180), panel, 3)
    draw_text(item_popup["title"], panel.x + 24, panel.y + 24, (255, 245, 180))
    words = item_popup["description"].split(" ")
    line = ""
    y = panel.y + 66
    for word in words:
        test = line + word + " "
        if small_font.size(test)[0] > panel.width - 48:
            draw_text(line.strip(), panel.x + 24, y, (225, 230, 210), use_small=True)
            y += 24
            line = word + " "
        else:
            line = test
    if line:
        draw_text(line.strip(), panel.x + 24, y, (225, 230, 210), use_small=True)
    item_popup_timer -= 1
    if item_popup_timer <= 0:
        item_popup = None

def draw_boss_reward(mouse):
    screen.fill((10, 12, 12))
    panel = pygame.Rect(300, 190, 600, 310)
    pygame.draw.rect(screen, (18, 24, 20), panel)
    pygame.draw.rect(screen, (235, 230, 180), panel, 3)
    key_name = world.get_region_key_item()
    draw_text(key_name, 500, 230, (255, 245, 180))
    draw_text("The guardian falls quiet. In the shrine roots, an iron key waits.", 350, 285, (225, 230, 210), use_small=True)
    draw_text(f"You got the {key_name}.", 430, 325, (255, 255, 140), use_small=True)
    if boss_reward_relic:
        draw_text(f"Relic found: {boss_reward_relic['name']}", 455, 360, (200, 230, 200), use_small=True)
    continue_rect = boss_continue_rect()
    draw_menu_button(continue_rect, "CONTINUE", mouse)
    return continue_rect

def fade_to_black(message=None):
    for alpha in range(0, 256, 12):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(player, world)
                pygame.quit()
                raise SystemExit
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        if message:
            draw_text(message, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 12, (255, 255, 255))
        pygame.display.flip()
        clock.tick(60)

def make_boss_intro_dialogue():
    choices = [
        {"text": "Fight", "effect": "boss:fight"},
        {"text": "Speak softly", "effect": "boss:speak_menu"}
    ]
    if player.knowledge > 5:
        choices.append({"text": "Attempt purification", "effect": "boss:purify"})
    else:
        choices.append({"text": "Purification locked (Need 6 Knowledge)", "effect": "boss:purify_locked"})

    return DialogueBox(
        "The shrine trembles. Moss gathers into the shape of a bear. Will you begin?",
        choices
    )

def make_boss_speak_dialogue():
    region_level = world.get_region_index()
    penalty = region_level * 8
    options = [
        ("Hum the old root-song", 35, 18),
        ("Name what the blight took", 45, 20),
        ("Offer silent patience", 25, 28),
        ("Share a relic's memory", 55, 16)
    ]
    choices = []
    for text, chance, gain in options:
        adjusted = max(5, chance - penalty)
        choices.append({"text": f"{text} ({adjusted}%)", "effect": f"boss:speak:{adjusted}:{gain}"})
    choices.append({"text": "Ready your weapon", "effect": "boss:fight"})

    return DialogueBox(
        "The guardian listens, but each region has taught it new reasons to doubt you. Lift its mood above 80 to pass without battle.",
        choices
    )

def draw_boss_mood():
    draw_text("Boss Mood", 995, 130, (220, 230, 220))
    bar = pygame.Rect(1010, 165, 26, 260)
    pygame.draw.rect(screen, (50, 35, 35), bar)
    filled = int(bar.height * max(0, min(100, boss_mood)) / 100)
    pygame.draw.rect(screen, (100, 210, 130), (bar.x, bar.bottom - filled, bar.width, filled))
    pygame.draw.rect(screen, (255, 255, 255), bar, 2)
    pygame.draw.line(screen, (255, 220, 120), (bar.x - 8, bar.y + bar.height // 2), (bar.right + 8, bar.y + bar.height // 2), 2)
    draw_text(f"{boss_mood}%", 996, 440, use_small=True)
    draw_text("Fight below 50", 955, 466, (255, 220, 120), use_small=True)
    if boss_result_text:
        draw_text(boss_result_text, 280, 360, (255, 255, 140), use_small=True)

def grant_boss_reward():
    global state, upgrade_options, boss_reward_relic
    boss_reward_relic = world.get_random_relic()
    player.relics.append(boss_reward_relic)
    apply_relics(player)
    player.hp = player.max_hp
    player.flags.add(world.get_boss_defeated_flag())
    player.flags.discard(world.get_shrine_unlocked_flag())
    key_name = world.get_region_key_item()
    if key_name not in player.story_items:
        fade_to_black("The shrine goes quiet...")
        player.story_items.add(key_name)
    upgrade_options = generate_upgrades()
    state = BOSS_REWARD

def save_to_slot(slot):
    save_game(player, world, slot)
    show_toast(f"Saved to slot {slot}")

def load_saved_game(slot):
    global player, world, state
    data = load_game(player, slot)
    if not data:
        show_toast(f"Slot {slot} is empty")
        return

    world = World()
    target_region = data.get("region")
    if not target_region:
        target_region = "Village" if "left_forest" in player.flags else "Forest"
    while world.region != target_region and target_region in world.regions:
        world.next_region()
    state = EXPLORE
    show_toast(f"Loaded slot {slot}")

def trigger_dialogue(dialogue_id):
    global dialogue, state
    data = world.get_dialogue(dialogue_id, player)
    if not data:
        return
    dialogue = DialogueBox(data["text"], data["choices"])
    state = DIALOGUE

def handle_effect(effect):
    global state, boss, dialogue, upgrade_options, boss_mood, boss_result_text

    if effect == "next:explore":
        state = EXPLORE

    elif effect.startswith("dialogue:"):
        trigger_dialogue(effect.split(":", 1)[1])

    elif effect == "gain:knowledge":
        player.knowledge += 1
        state = EXPLORE

    elif effect == "gain:mercy":
        player.mercy += 1
        player.flags.add("hunter_resolved")
        state = EXPLORE

    elif effect == "gain:power":
        player.power += 1
        player.flags.add("hunter_resolved")
        state = EXPLORE

    elif effect == "quest:forager_accept":
        player.flags.add("forager_listened")
        trigger_dialogue("forager_story_2")

    elif effect == "quest:forager_reject":
        player.flags.add("forager_refused")
        trigger_dialogue("forager_refused")

    elif effect == "quest:child_accept":
        player.flags.add("child_quest_started")
        trigger_dialogue("child_quest_accepted")

    elif effect == "find:forest_map":
        if "Forest Map" not in player.story_items:
            player.story_items.add("Forest Map")
            show_item_popup("Forest Map", "A muddy village map rescued from the glowing stump. Return it to the lost child.")
        state = EXPLORE

    elif effect == "quest:child_turn_in":
        player.flags.add("child_quest_complete")
        trigger_dialogue("child_return_complete")

    elif effect == "find:moss_lens":
        if "forager_quest_complete" not in player.flags:
            player.add_relic({"name": "Moss Lens", "effect": "knowledge"})
            player.knowledge += 1
            player.flags.add("forager_quest_complete")
            show_item_popup("Moss Lens", relic_description({"name": "Moss Lens", "effect": "knowledge"}))
        trigger_dialogue("forager_reward")

    elif effect == "find:root_charm":
        if "child_reward_taken" not in player.flags:
            player.add_relic({"name": "Root Charm", "effect": "heal"})
            apply_relics(player)
            player.hp = player.max_hp
            player.flags.add("child_reward_taken")
            show_item_popup("Root Charm", relic_description({"name": "Root Charm", "effect": "heal"}))
        state = EXPLORE

    elif effect == "gain:elder_trust":
        player.flags.add("elder_trust")
        trigger_dialogue("elder_trust")

    elif effect.startswith("learn:"):
        lesson = effect.split(":", 1)[1]
        flag = f"learned_{lesson}"
        if flag not in player.flags:
            player.flags.add(flag)
            player.knowledge += 1
            show_toast("Knowledge +1")
        state = EXPLORE

    elif effect.startswith("task:"):
        _, flag, label = effect.split(":", 2)
        if flag not in player.flags:
            player.flags.add(flag)
            show_item_popup(label, "The task is complete. The region trusts you a little more.")
        state = EXPLORE

    elif effect == "unlock:shrine":
        player.flags.add(world.get_shrine_unlocked_flag())
        show_toast("Shrine location revealed")
        state = EXPLORE

    elif effect == "boss:fight":
        boss_result_text = ""
        state = BOSS_COMBAT

    elif effect == "boss:speak_menu":
        dialogue = make_boss_speak_dialogue()
        state = BOSS_DIALOGUE

    elif effect.startswith("boss:speak:"):
        parts = effect.split(":")
        chance = int(parts[2])
        gain = int(parts[3])
        if random.randint(1, 100) <= chance:
            boss_mood = min(100, boss_mood + gain)
            boss_result_text = f"Success. Mood rises to {boss_mood}%."
            if boss_mood >= 80:
                player.mercy += 1
                grant_boss_reward()
                return
        else:
            boss_mood = max(0, boss_mood - 18)
            boss_result_text = f"Failed. Mood falls to {boss_mood}%."
            if boss_mood < 50:
                state = BOSS_COMBAT
                return
        dialogue = make_boss_speak_dialogue()
        state = BOSS_DIALOGUE

    elif effect == "boss:purify_locked":
        show_toast("Need more Knowledge")
        dialogue = make_boss_intro_dialogue()
        state = BOSS_DIALOGUE

    elif effect == "boss:talk":
        if boss:
            player.knowledge += 1
            boss.hp -= 40
        state = BOSS_COMBAT

    elif effect == "boss:purify":
        if player.knowledge > 5:
            player.mercy += 1
            boss_mood = 100
            boss_result_text = "The bear remembers itself."
            grant_boss_reward()
        else:
            show_toast("Need more Knowledge")
            state = BOSS_DIALOGUE

    elif effect.startswith("region:"):
        next_region = effect.split(":", 1)[1].title()
        fade_to_black(f"Leaving for the {next_region}...")
        world.next_region()
        player.flags.add(f"reached_{world.get_region_key()}")
        player.x = 320
        player.y = 560
        state = EXPLORE

    elif effect == "ending:relics":
        if len(player.relics) >= 3:
            fade_to_black("The relics remember the road...")
            state = ENDING
        else:
            show_toast("Need at least 3 relics")
            state = EXPLORE

    elif effect == "stay":
        state = EXPLORE

running = True
while running:
    screen.fill(world.get_color())
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(player, world, 1)
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if state == EXPLORE:
                    state = PAUSE
                elif state == PAUSE:
                    state = EXPLORE
                elif state == ENDING:
                    state = MENU
            elif event.key == pygame.K_SPACE and state == BOSS_COMBAT and boss:
                boss.fire_player_pellet(player)

        if event.type == pygame.MOUSEWHEEL:
            if state in (DIALOGUE, BOSS_DIALOGUE) and dialogue:
                dialogue.scroll_choices(event.y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU:
                if menu_play_rect().collidepoint(mouse):
                    trigger_dialogue("intro_1")
                elif menu_load_rect().collidepoint(mouse):
                    slot_back_state = MENU
                    state = SLOT_LOAD
                elif menu_how_to_rect().collidepoint(mouse):
                    state = HOW_TO
                elif menu_exit_rect().collidepoint(mouse):
                    running = False

            elif state == HOW_TO:
                if menu_back_rect().collidepoint(mouse):
                    state = MENU

            elif state == SLOT_SAVE:
                if slot_one_rect().collidepoint(mouse):
                    save_to_slot(1)
                    state = PAUSE
                elif slot_two_rect().collidepoint(mouse):
                    save_to_slot(2)
                    state = PAUSE
                elif slot_back_rect().collidepoint(mouse):
                    state = slot_back_state

            elif state == SLOT_LOAD:
                if slot_one_rect().collidepoint(mouse):
                    load_saved_game(1)
                elif slot_two_rect().collidepoint(mouse):
                    load_saved_game(2)
                elif slot_back_rect().collidepoint(mouse):
                    state = slot_back_state

            elif state == GAME_OVER:
                if game_over_load_rect().collidepoint(mouse):
                    slot_back_state = GAME_OVER
                    state = SLOT_LOAD
                elif game_over_menu_rect().collidepoint(mouse):
                    state = MENU
                elif game_over_exit_rect().collidepoint(mouse):
                    running = False

            elif state == BOSS_REWARD:
                if boss_continue_rect().collidepoint(mouse):
                    show_item_popup(boss_reward_relic["name"], relic_description(boss_reward_relic))
                    upgrade_delay_timer = 300
                    state = UPGRADE_DELAY

            elif state == DIALOGUE:
                choice = dialogue.click(mouse)
                if choice:
                    handle_effect(choice.get("effect", "stay"))

            elif state == EXPLORE:
                npc = world.get_nearby_npc(player)
                if npc:
                    trigger_dialogue(npc.dialogue_id)
                else:
                    player_rect = player.get_rect_world()

                    if world.can_interact_with_stump(player) and "Forest Map" not in player.story_items:
                        handle_effect("find:forest_map")

                    elif (
                        world.get_shrine_unlocked_flag() in player.flags and
                        world.get_boss_defeated_flag() not in player.flags and
                        player_rect.colliderect(world.get_shrine_rect())
                    ):
                        boss = Boss(world.region)
                        boss_mood = max(35, 65 - world.get_region_index() * 8)
                        boss_result_text = ""
                        dialogue = make_boss_intro_dialogue()
                        state = BOSS_DIALOGUE

                    elif player_rect.colliderect(world.get_gate_rect()):
                        if world.get_region_key_item() in player.story_items:
                            trigger_dialogue(world.get_gate_open_dialogue_id())
                        else:
                            trigger_dialogue(world.get_gate_locked_dialogue_id())

            elif state == BOSS_DIALOGUE:
                choice = dialogue.click(mouse)
                if choice:
                    handle_effect(choice.get("effect", "stay"))

            elif state == LEVELUP:
                for i, opt in enumerate(upgrade_options):
                    rect = pygame.Rect(340, 220 + i * 70, 420, 46)
                    if rect.collidepoint(mouse):
                        opt["apply"](player)
                        state = EXPLORE

            elif state == PAUSE:
                if pause_save_rect().collidepoint(mouse):
                    slot_back_state = PAUSE
                    state = SLOT_SAVE
                elif pause_load_rect().collidepoint(mouse):
                    slot_back_state = PAUSE
                    state = SLOT_LOAD
                elif pause_exit_rect().collidepoint(mouse):
                    save_game(player, world, 1)
                    running = False

    if state == MENU:
        draw_menu(mouse)
        draw_toast()

    elif state == HOW_TO:
        draw_how_to(mouse)
        draw_toast()

    elif state == SLOT_SAVE:
        draw_slot_select(mouse, saving=True)
        draw_toast()

    elif state == SLOT_LOAD:
        draw_slot_select(mouse, saving=False)
        draw_toast()

    elif state == GAME_OVER:
        draw_game_over(mouse)
        game_over_tick += 1

    elif state == ENDING:
        draw_ending()

    elif state == DIALOGUE:
        dialogue.draw(screen)
        draw_toast()
        draw_item_popup()

    elif state == BOSS_DIALOGUE:
        dialogue.draw(screen)
        if boss:
            draw_boss_mood()
        draw_toast()
        draw_item_popup()

    elif state == EXPLORE:
        keys = pygame.key.get_pressed()
        player.move_world(keys, world.get_world_obstacles(), WORLD_WIDTH, WORLD_HEIGHT)

        playable_width = SCREEN_WIDTH - 240
        camera_x = player.x - playable_width // 2
        camera_y = player.y - SCREEN_HEIGHT // 2
        camera_x = max(0, min(camera_x, WORLD_WIDTH - playable_width))
        camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))

        world.draw(screen, player, camera_x, camera_y)
        player.draw_world(screen, camera_x, camera_y)

        draw_inventory(screen, player)
        draw_health_bar(screen, 18, 72, 200, 18, player.hp, player.max_hp)
        draw_region_header()
        draw_toast()
        draw_item_popup()

        npc = world.get_nearby_npc(player)
        if npc:
            pr = player.get_rect_world()
            draw_text("Click to interact", pr.x - camera_x, pr.y - camera_y - 25, (255, 255, 120), use_small=True)

        if world.can_interact_with_stump(player) and "Forest Map" not in player.story_items:
            stump = world.get_stump_rect()
            draw_text(
                "Click to inspect stump",
                stump.x - camera_x - 20,
                stump.y - camera_y - 25,
                (120, 220, 255),
                use_small=True
            )

        if (
            world.get_shrine_unlocked_flag() in player.flags and
            world.get_boss_defeated_flag() not in player.flags and
            player.get_rect_world().colliderect(world.get_shrine_rect())
        ):
            shrine = world.get_shrine_rect()
            draw_text(
                "Click to enter shrine",
                shrine.x - camera_x - 10,
                shrine.y - camera_y - 25,
                (140, 255, 140),
                use_small=True
            )

        if player.get_rect_world().colliderect(world.get_gate_rect()):
            gate = world.get_gate_rect()
            draw_text(
                "Click to inspect gate",
                gate.x - camera_x - 10,
                gate.y - camera_y - 25,
                (180, 220, 255),
                use_small=True
            )

    elif state == BOSS_COMBAT:
        screen.fill((22, 22, 30))
        combat_bounds = pygame.Rect(260, 90, 700, 540)
        player.update_boss_combat(bounds=combat_bounds)
        boss.update_survivor_style(player, combat_bounds)

        player.draw_boss_combat(screen)
        boss.draw(screen)

        draw_inventory(screen, player)
        draw_health_bar(screen, 18, 72, 200, 18, player.hp, player.max_hp)
        draw_text(f"Boss: {boss.name}", 270, 65)
        draw_text(f"Boss HP: {max(0, boss.hp)}/{boss.max_hp}", 270, 92)
        draw_text("Press SPACE to shoot pellets. Dodge the moss.", 270, 120, (220, 220, 180), use_small=True)
        draw_toast()
        draw_item_popup()

        if player.hp <= 0:
            state = GAME_OVER

        elif boss.hp <= 0:
            grant_boss_reward()

    elif state == BOSS_REWARD:
        draw_boss_reward(mouse)
        draw_item_popup()

    elif state == UPGRADE_DELAY:
        screen.fill((10, 12, 12))
        seconds = max(1, upgrade_delay_timer // 60 + 1)
        draw_text("The shrine's gift settles into your bones...", 390, 300, (240, 245, 220))
        draw_text(f"Choose an upgrade in {seconds}", 485, 350, (255, 255, 140), use_small=True)
        draw_item_popup()
        upgrade_delay_timer -= 1
        if upgrade_delay_timer <= 0:
            state = LEVELUP

    elif state == LEVELUP:
        screen.fill((16, 16, 20))
        draw_text("Choose an Upgrade", 460, 130)
        draw_toast()
        draw_item_popup()

        for i, opt in enumerate(upgrade_options):
            rect = pygame.Rect(340, 220 + i * 70, 420, 46)
            pygame.draw.rect(screen, (60, 60, 70), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            draw_text(opt["name"], rect.x + 14, rect.y + 10)

    elif state == PAUSE:
        draw_text("PAUSED", 545, 190)
        for rect, label in [
            (pause_save_rect(), "Save Game"),
            (pause_load_rect(), "Load Game"),
            (pause_exit_rect(), "Exit Game")
        ]:
            pygame.draw.rect(screen, (80, 80, 80), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            text = font.render(label, True, (255, 255, 255))
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
        draw_toast()
        draw_item_popup()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
