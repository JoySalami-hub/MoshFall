import pygame
import random

class NPC:
    def __init__(self, x, y, name, color, dialogue_id, solid=True):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.dialogue_id = dialogue_id
        self.solid = solid
        self.rect = pygame.Rect(x, y, 28, 28)

    def draw(self, screen, player, camera_x, camera_y):
        color = self.color
        if self.rect.colliderect(player.get_rect_world().inflate(70, 70)):
            color = (255, 255, 140)
        pygame.draw.rect(screen, color, (self.x - camera_x, self.y - camera_y, 28, 28))

class World:
    def __init__(self):
        self.region = "Forest"

        self.regions = {
            "Forest": (34, 88, 46),
            "Village": (112, 96, 78),
            "Caverns": (54, 54, 82),
            "Citadel": (92, 28, 28)
        }

        self.npcs = [
            NPC(620, 540, "Elder Rowan", (220, 200, 80), "elder_blocked"),
            NPC(930, 700, "Forager Lysa", (130, 220, 120), "forager_intro"),
            NPC(1400, 580, "Hunter Brann", (200, 110, 90), "hunter_intro"),
            NPC(1180, 1200, "Lost Child", (150, 190, 255), "child_intro"),
            NPC(520, 980, "Lantern Keeper", (235, 205, 120), "knowledge_lantern"),
            NPC(1530, 1160, "Root Scholar", (170, 230, 170), "knowledge_roots"),
            NPC(1770, 430, "Stone Reader", (185, 185, 220), "knowledge_stones"),
            NPC(2260, 760, "Moss Singer", (120, 220, 180), "knowledge_song"),
            NPC(2420, 1280, "Quiet Scout", (210, 160, 120), "knowledge_scout"),
            NPC(690, 1680, "Old Cartographer", (180, 210, 240), "knowledge_cartographer"),
            NPC(2920, 520, "Gate Watcher", (190, 190, 150), "knowledge_gate")
        ]

        self.static_obstacles = [
            pygame.Rect(780, 420, 160, 60),
            pygame.Rect(1100, 900, 180, 60),
            pygame.Rect(1600, 760, 80, 240),
            pygame.Rect(860, 1480, 220, 80),
            pygame.Rect(1900, 500, 120, 120),
            pygame.Rect(2100, 1020, 140, 200),
            pygame.Rect(2600, 700, 180, 70),
        ]

        self.gate_rect = pygame.Rect(2860, 900, 90, 220)
        self.shrine_rect = pygame.Rect(2480, 320, 100, 100)
        self.stump_rect = pygame.Rect(980, 1540, 80, 80)

        self.dialogues = {
            "intro_1": {
                "text": "You wake under a wet canopy of leaves. Pale moss covers the trees, the path, and your broken stick. Something in the forest is breathing with you.",
                "choices": [{"text": "Sit up", "effect": "dialogue:intro_2"}]
            },
            "intro_2": {
                "text": "A trail of lantern posts leads inward. Someone has kept this path alive, even as the Verdant Blight spreads through the roots.",
                "choices": [{"text": "Follow the path", "effect": "dialogue:intro_3"}]
            },
            "intro_3": {
                "text": "If you want to survive here, you will need trust, knowledge, and whatever scraps the forest is willing to surrender.",
                "choices": [{"text": "Enter the forest", "effect": "next:explore"}]
            },
            "elder_blocked": {
                "text": "Elder Rowan glances at you once, then away. 'Bring me proof that you understand this forest. Seven lessons at least. I will not send ignorance to the shrine.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "elder_neutral": {
                "text": "Elder Rowan folds his arms. 'You are learning, but not enough. Speak with the people who still remember what the moss was before it became hunger.'",
                "choices": [{"text": "I understand", "effect": "stay"}]
            },
            "elder_trust": {
                "text": "Elder Rowan studies the map in your hands and the quiet in your posture. 'Good. You listened. You helped. The shrine lies far to the east, past the split roots and black stones. The Moss Bear keeps the key there.'",
                "choices": [{"text": "Ask him to mark the shrine", "effect": "unlock:shrine"}]
            },
            "forager_intro": {
                "text": "Forager Lysa kneels beside a tangle of roots. 'Do you know what the worst part is? People think gathering is just taking. They never stay for the remembering. If you want what I found, then hear all of it.'",
                "choices": [
                    {"text": "Listen to her story", "effect": "quest:forager_accept"},
                    {"text": "I don't have time", "effect": "quest:forager_reject"}
                ]
            },
            "forager_story_2": {
                "text": "Lysa exhales slowly. 'When the blight reached my family's grove, the moss didn't kill the old trees. It held them together. My mother called it a grave. I called it mercy. Down by the hollow stump, I found a lens covered in green veins. I kept waiting for someone patient enough to carry it.'",
                "choices": [{"text": "Accept the lens", "effect": "find:moss_lens"}]
            },
            "forager_reward": {
                "text": "Lysa nods as you take the moss lens. 'Good. Then maybe the forest chose better this time. It reveals patterns in living growth. Don't waste that on fear.'",
                "choices": [{"text": "Thank her", "effect": "stay"}]
            },
            "forager_refused": {
                "text": "Lysa turns away. 'Then don't ask again. If you can't spare a minute for the living, you don't deserve what the roots remember.'",
                "choices": [{"text": "Leave her be", "effect": "stay"}]
            },
            "forager_done": {
                "text": "Lysa nods at the moss lens hanging from your belt. 'Use it well. The forest shows more to people who stop trying to conquer it.'",
                "choices": [{"text": "Step back", "effect": "stay"}]
            },
            "hunter_intro": {
                "text": "Hunter Brann grips a chipped spear so hard his knuckles pale. 'My brother vanished near the eastern shrine. If the moss speaks, I don't care what it says. I care what it took.'",
                "choices": [
                    {"text": "Feed his anger", "effect": "gain:power"},
                    {"text": "Tell him rage will blind him", "effect": "gain:mercy"}
                ]
            },
            "hunter_done": {
                "text": "Brann stares into the trees. 'Maybe you're right. Or maybe mercy is just what people say when they are too weak to finish a job.'",
                "choices": [{"text": "Leave him to his thoughts", "effect": "stay"}]
            },
            "child_intro": {
                "text": "A child sits beside a stone marker, trying not to cry. 'I lost the forest map. Elder Rowan said never to bring it outside the village path, but I dropped it near the glowing stump in the south. If I go back empty-handed, he'll never trust me again.'",
                "choices": [
                    {"text": "I'll look for it", "effect": "quest:child_accept"},
                    {"text": "You're on your own", "effect": "stay"}
                ]
            },
            "child_quest_accepted": {
                "text": "The child wipes their eyes. 'The stump glows blue at night, green by day. Please don't let the moss swallow the map before you reach it.'",
                "choices": [{"text": "Go search", "effect": "stay"}]
            },
            "child_return_complete": {
                "text": "The child stares as you unfold the map. 'You really found it... No, keep it. Rowan should see that you were the one who brought it back. Take this charm too. My mother said it keeps old roots kind.'",
                "choices": [{"text": "Accept the charm", "effect": "find:root_charm"}]
            },
            "child_has_map": {
                "text": "The child gasps when they see the muddy map in your hands. 'You found it? Please, show me. I need to know it wasn't swallowed.'",
                "choices": [
                    {"text": "Give him the map", "effect": "quest:child_turn_in"},
                    {"text": "Not yet", "effect": "stay"}
                ]
            },
            "child_done": {
                "text": "The child gives a small, relieved smile. 'If Rowan still won't trust you after this, then he trusts no one.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "knowledge_lantern": {
                "text": "The Lantern Keeper taps ash from an old wick. 'Blue moss means memory. Green moss means hunger. If it shines both ways, do not touch it with bare fear.'",
                "choices": [{"text": "Remember the lesson", "effect": "learn:lantern"}]
            },
            "knowledge_lantern_done": {
                "text": "The Lantern Keeper smiles. 'You remember. Good. Memory is a path you can relight.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "knowledge_roots": {
                "text": "The Root Scholar kneels by a split trunk. 'Roots share warnings faster than people share kindness. Watch the leaves when the ground is silent.'",
                "choices": [{"text": "Study the roots", "effect": "learn:roots"}]
            },
            "knowledge_roots_done": {
                "text": "The Root Scholar pats the soil. 'You have heard this lesson already. Now listen for it underfoot.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "knowledge_stones": {
                "text": "The Stone Reader traces lichen on a marker. 'The old paths curve away from blight. Straight roads are for people who have forgotten danger.'",
                "choices": [{"text": "Read the marker", "effect": "learn:stones"}]
            },
            "knowledge_stones_done": {
                "text": "The Stone Reader nods. 'The marker has said all it can.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "knowledge_song": {
                "text": "The Moss Singer hums softly. 'The bear listens for rhythm. Speak in patience, not panic, and it may remember sleep.'",
                "choices": [{"text": "Learn the rhythm", "effect": "learn:song"}]
            },
            "knowledge_song_done": {
                "text": "The Moss Singer hums the same phrase, quieter now.",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "knowledge_scout": {
                "text": "The Quiet Scout points east. 'The shrine wakes when watched. Approach when your hands know why they are empty.'",
                "choices": [{"text": "Mark the warning", "effect": "learn:scout"}]
            },
            "knowledge_scout_done": {
                "text": "The Quiet Scout has no more words, only a careful look toward the shrine.",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "knowledge_cartographer": {
                "text": "The Old Cartographer dusts off a cracked compass. 'Maps are promises, not truth. When the forest moves, trust landmarks that remember you.'",
                "choices": [{"text": "Compare the map", "effect": "learn:cartographer"}]
            },
            "knowledge_cartographer_done": {
                "text": "The Old Cartographer squints at your path. 'You have enough ink from me.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "knowledge_gate": {
                "text": "The Gate Watcher taps the old lock. 'Keys open iron. Trust opens exits. You will need both before the village lets you leave the forest behind.'",
                "choices": [{"text": "Listen closely", "effect": "learn:gate"}]
            },
            "knowledge_gate_done": {
                "text": "The Gate Watcher folds their hands. 'The lock remembers you now.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "forest_gate_locked": {
                "text": "Thorned roots choke the old village gate. A metal lock hangs beneath them, half-swallowed by bark.",
                "choices": [{"text": "Step back", "effect": "stay"}]
            },
            "forest_gate_open": {
                "text": "The Forest Gate Key turns with a deep iron groan. Beyond it lies the Sunken Village, drowned in roots and rain.",
                "choices": [
                    {"text": "Proceed to the village", "effect": "region:village"},
                    {"text": "Stay in the forest", "effect": "stay"}
                ]
            },
            "village_warden": {
                "text": "The Village Warden studies the mud on your boots. 'You steadied the square and listened to the rain. The drowned shrine is yours to face.'",
                "choices": [{"text": "Ask for the shrine path", "effect": "unlock:shrine"}]
            },
            "village_warden_intro": {
                "text": "The Village Warden plants a staff in the wet boards. 'Before I mark our shrine, prove you can help a place that is still drowning. Speak to the Rain Listener, the Bell Diver, and the Root Medic.'",
                "choices": [{"text": "Take the village tasks", "effect": "region_tasks:start"}]
            },
            "village_warden_wait": {
                "text": "The Village Warden shakes their head. 'Not yet. Learn what the rain knows, return the drowned bell, and help the root medic before I mark the shrine.'",
                "choices": [{"text": "I will help first", "effect": "stay"}]
            },
            "village_listener": {
                "text": "The Rain Listener cups one hand to the sky. 'The water repeats every secret. Do you want the warning or the comfort?'",
                "choices": [
                    {"text": "Hear the warning", "effect": "learn:village"},
                    {"text": "Ask for comfort", "effect": "gain:mercy"},
                    {"text": "Step back", "effect": "stay"}
                ]
            },
            "knowledge_village_done": {
                "text": "The Rain Listener nods. 'You already heard what the rain would say.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "village_bell": {
                "text": "A Bell Diver wrings water from their sleeve. 'The shrine bell sank near the old well. If you find it, the village will hear itself again.'",
                "choices": [
                    {"text": "Search for the bell", "effect": "quest:village_bell"},
                    {"text": "Ask why it matters", "effect": "learn:village"},
                    {"text": "Leave", "effect": "stay"}
                ]
            },
            "village_bell_done": {
                "text": "The Bell Diver taps the restored bell. Its note rolls through the flooded street.",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "village_medic": {
                "text": "The Root Medic presses moss to a cracked beam. 'I need clean root-fiber from the dry bridge. Bring it, and I can bind this house before it sinks.'",
                "choices": [
                    {"text": "Find root-fiber", "effect": "quest:village_medic"},
                    {"text": "Ask about the house", "effect": "gain:mercy"},
                    {"text": "Leave", "effect": "stay"}
                ]
            },
            "village_medic_done": {
                "text": "The Root Medic nods. 'The roots will hold for now.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "village_gate_locked": {
                "text": "A waterlogged gate blocks the road into the caverns. Its lock is packed with wet moss.",
                "choices": [{"text": "Step back", "effect": "stay"}]
            },
            "village_gate_open": {
                "text": "The Village Gate Key turns. Beneath the village, old stone stairs descend into cold dark.",
                "choices": [
                    {"text": "Proceed to the caverns", "effect": "region:caverns"},
                    {"text": "Stay here", "effect": "stay"}
                ]
            },
            "cavern_warden": {
                "text": "The Echo Keeper raises a lantern. 'The cavern shrine answers movement, not words. Find it before the dark finds your name.'",
                "choices": [{"text": "Ask for the shrine path", "effect": "unlock:shrine"}]
            },
            "cavern_warden_intro": {
                "text": "The Echo Keeper raises a lantern but does not hand it over. 'Bring proof that you can listen in the dark: learn the echo, find the blue crystal, and guide the lost miner home.'",
                "choices": [{"text": "Take the cavern tasks", "effect": "region_tasks:start"}]
            },
            "cavern_warden_wait": {
                "text": "The Echo Keeper keeps the lantern low. 'Bring back a living echo, find the blue crystal, and guide the lost miner. Then I will show you the shrine.'",
                "choices": [{"text": "Into the dark, then", "effect": "stay"}]
            },
            "knowledge_cavern": {
                "text": "A Miner of the Deep taps the wall twice, then waits for three answers. 'Stone remembers every footstep. What do you hear back?'",
                "choices": [
                    {"text": "A warning", "effect": "learn:cavern"},
                    {"text": "A challenge", "effect": "gain:power"},
                    {"text": "Only stone", "effect": "stay"}
                ]
            },
            "knowledge_cavern_done": {
                "text": "The Miner of the Deep listens to the same echo again.",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "cavern_crystal": {
                "text": "A Crystal Child points into the dark. 'The blue crystal rolled under the black arch. It sings when kind hands touch it. Can you bring it back?'",
                "choices": [
                    {"text": "Search for the crystal", "effect": "quest:cavern_crystal"},
                    {"text": "Ask about its song", "effect": "learn:cavern"},
                    {"text": "Leave", "effect": "stay"}
                ]
            },
            "cavern_crystal_done": {
                "text": "The Crystal Child listens to the quiet place where the crystal used to sing.",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "cavern_miner": {
                "text": "A Lost Miner grips a broken lamp. 'My guide-stone fell near the rail bend. Without it, every tunnel sounds like home.'",
                "choices": [
                    {"text": "Find the guide-stone", "effect": "quest:cavern_miner"},
                    {"text": "Tell him to stay calm", "effect": "gain:mercy"},
                    {"text": "Leave", "effect": "stay"}
                ]
            },
            "cavern_miner_done": {
                "text": "The Lost Miner breathes easier beside the lit path.",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "cavern_gate_locked": {
                "text": "A black iron lift refuses to rise toward the citadel. It waits for the Cavern Gate Key.",
                "choices": [{"text": "Step back", "effect": "stay"}]
            },
            "cavern_gate_open": {
                "text": "The Cavern Gate Key wakes the old lift. Chains groan upward toward the red citadel.",
                "choices": [
                    {"text": "Proceed to the citadel", "effect": "region:citadel"},
                    {"text": "Stay here", "effect": "stay"}
                ]
            },
            "citadel_warden": {
                "text": "The Ash Sentinel lowers their blade. 'The final shrine burns behind the broken court. End what followed you from the forest.'",
                "choices": [{"text": "Ask for the shrine path", "effect": "unlock:shrine"}]
            },
            "citadel_warden_intro": {
                "text": "The Ash Sentinel bars the court. 'No one enters the final shrine on courage alone. Read the red page, gather cold embers, and mend the banner first.'",
                "choices": [{"text": "Take the citadel tasks", "effect": "region_tasks:start"}]
            },
            "citadel_warden_wait": {
                "text": "The Ash Sentinel bars the court. 'Read the red page, gather the cold embers, and mend the torn banner. Then the last shrine opens.'",
                "choices": [{"text": "I will return", "effect": "stay"}]
            },
            "knowledge_citadel": {
                "text": "The Red Archivist opens a scorched book. 'Power without memory becomes blight wearing a crown. Which line do you follow?'",
                "choices": [
                    {"text": "The line about memory", "effect": "learn:citadel"},
                    {"text": "The line about power", "effect": "gain:power"},
                    {"text": "Close the book", "effect": "stay"}
                ]
            },
            "knowledge_citadel_done": {
                "text": "The Red Archivist closes the book. 'That page has already marked you.'",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "citadel_embers": {
                "text": "An Ember Keeper kneels beside ash that refuses to cool. 'The cold embers scattered near the broken court. The hot ones remember teeth.'",
                "choices": [
                    {"text": "Gather cold embers", "effect": "quest:citadel_embers"},
                    {"text": "Ask about the fire", "effect": "learn:citadel"},
                    {"text": "Leave", "effect": "stay"}
                ]
            },
            "citadel_embers_done": {
                "text": "The Ember Keeper sifts the harmless ash through one hand.",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "citadel_banner": {
                "text": "A Banner Keeper holds torn cloth against the wind. 'The silver thread blew into the lower court. Find it, and the citadel may remember it was built to protect.'",
                "choices": [
                    {"text": "Find silver thread", "effect": "quest:citadel_banner"},
                    {"text": "Ask what the banner means", "effect": "gain:mercy"},
                    {"text": "Leave", "effect": "stay"}
                ]
            },
            "citadel_banner_done": {
                "text": "The mended banner snaps once, bright against the ash.",
                "choices": [{"text": "Step away", "effect": "stay"}]
            },
            "citadel_gate_locked": {
                "text": "The last gate is ceremonial and sealed. Something beyond it waits for the Citadel Gate Key.",
                "choices": [{"text": "Step back", "effect": "stay"}]
            },
            "citadel_gate_open": {
                "text": "The Citadel Gate Key turns. Your relics answer in a chorus of root, stone, rain, and ash.",
                "choices": [
                    {"text": "Offer the relics", "effect": "ending:relics"},
                    {"text": "Remain in the citadel", "effect": "stay"}
                ]
            },
            "regional_lore": {
                "text": "They share a local truth, something ordinary enough to survive the blight. It sounds different in every mouth, but it points toward the same lesson.",
                "choices": [
                    {"text": "Ask about the shrine", "effect": "gain:knowledge"},
                    {"text": "Ask how people endure", "effect": "gain:mercy"},
                    {"text": "Ask what threatens them", "effect": "gain:power"},
                    {"text": "Move on", "effect": "stay"}
                ]
            },
            "regional_locked": {
                "text": "They glance toward the local elder. 'Speak to the one who keeps this place first. The work starts there.'",
                "choices": [{"text": "Find the elder", "effect": "stay"}]
            }
        }

    def get_color(self):
        return self.regions[self.region]

    def get_region_key(self):
        keys = {
            "Forest": "forest",
            "Village": "village",
            "Caverns": "cavern",
            "Citadel": "citadel"
        }
        return keys.get(self.region, self.region.lower())

    def get_region_index(self):
        return list(self.regions.keys()).index(self.region)

    def get_region_key_item(self):
        names = {
            "Forest": "Forest Gate Key",
            "Village": "Village Gate Key",
            "Caverns": "Cavern Gate Key",
            "Citadel": "Citadel Gate Key"
        }
        return names.get(self.region, f"{self.region} Gate Key")

    def get_shrine_unlocked_flag(self):
        return f"{self.get_region_key()}_shrine_unlocked"

    def get_boss_defeated_flag(self):
        return f"{self.get_region_key()}_boss_defeated"

    def get_gate_locked_dialogue_id(self):
        return f"{self.get_region_key()}_gate_locked"

    def get_gate_open_dialogue_id(self):
        return f"{self.get_region_key()}_gate_open"

    def get_region_task_flags(self):
        tasks = {
            "Village": ["learned_village", "village_bell_returned", "village_medic_helped"],
            "Caverns": ["learned_cavern", "cavern_crystal_found", "cavern_miner_found"],
            "Citadel": ["learned_citadel", "citadel_embers_gathered", "citadel_banner_mended"]
        }
        return tasks.get(self.region, [])

    def get_region_tasks_started_flag(self):
        return f"{self.get_region_key()}_tasks_started"

    def has_region_tasks_started(self, player):
        return self.get_region_tasks_started_flag() in player.flags

    def has_region_tasks_complete(self, player):
        return all(flag in player.flags for flag in self.get_region_task_flags())

    def get_collectibles(self):
        return {
            "Village": [
                {"start": "started_village_bell", "done": "village_bell_returned", "label": "Drowned Bell", "rect": pygame.Rect(760, 500, 80, 80), "prompt": "Click to haul up bell"},
                {"start": "started_village_medic", "done": "village_medic_helped", "label": "Root-Fiber", "rect": pygame.Rect(1510, 430, 90, 70), "prompt": "Click to gather root-fiber"}
            ],
            "Caverns": [
                {"start": "started_cavern_crystal", "done": "cavern_crystal_found", "label": "Blue Crystal", "rect": pygame.Rect(2260, 520, 80, 80), "prompt": "Click to take crystal"},
                {"start": "started_cavern_miner", "done": "cavern_miner_found", "label": "Guide-Stone", "rect": pygame.Rect(1380, 1180, 80, 80), "prompt": "Click to recover guide-stone"}
            ],
            "Citadel": [
                {"start": "started_citadel_embers", "done": "citadel_embers_gathered", "label": "Cold Embers", "rect": pygame.Rect(1840, 520, 90, 80), "prompt": "Click to gather embers"},
                {"start": "started_citadel_banner", "done": "citadel_banner_mended", "label": "Silver Thread", "rect": pygame.Rect(2260, 980, 90, 80), "prompt": "Click to take silver thread"}
            ]
        }.get(self.region, [])

    def get_nearby_collectible(self, player):
        player_rect = player.get_rect_world()
        for collectible in self.get_collectibles():
            if (
                collectible["start"] in player.flags and
                collectible["done"] not in player.flags and
                player_rect.colliderect(collectible["rect"].inflate(50, 50))
            ):
                return collectible
        return None

    def draw(self, screen, player, camera_x, camera_y):
        self.draw_ground(screen, camera_x, camera_y)
        self.draw_points_of_interest(screen, camera_x, camera_y, player)
        self.draw_obstacles(screen, camera_x, camera_y)

        for npc in self.npcs:
            npc.draw(screen, player, camera_x, camera_y)

    def draw_ground(self, screen, camera_x, camera_y):
        base = self.get_color()
        for x in range(240, 3200, 80):
            for y in range(0, 2200, 80):
                shade = ((x + y) // 80) % 2 * 8
                color = (
                    min(255, base[0] + shade),
                    min(255, base[1] + ((x // 80) % 3)),
                    min(255, base[2] + shade // 2)
                )
                pygame.draw.rect(screen, color, (x - camera_x, y - camera_y, 80, 80))

    def draw_points_of_interest(self, screen, camera_x, camera_y, player):
        if self.region != "Forest":
            square = pygame.Rect(620, 420, 360, 260).move(-camera_x, -camera_y)
            well = pygame.Rect(760, 500, 80, 80).move(-camera_x, -camera_y)
            pygame.draw.rect(screen, (120, 105, 90), square)
            pygame.draw.rect(screen, (170, 170, 190), well)
            pygame.draw.rect(screen, (235, 235, 220), well, 2)
            for collectible in self.get_collectibles():
                if collectible["start"] in player.flags and collectible["done"] not in player.flags:
                    rect = collectible["rect"].move(-camera_x, -camera_y)
                    pygame.draw.rect(screen, (210, 190, 90), rect)
                    pygame.draw.rect(screen, (255, 245, 180), rect, 2)
        else:
            stump_screen = self.stump_rect.move(-camera_x, -camera_y)
            pygame.draw.rect(screen, (90, 130, 220), stump_screen)
            pygame.draw.rect(screen, (180, 220, 255), stump_screen, 2)

        gate_screen = self.gate_rect.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, (110, 120, 140), gate_screen)
        pygame.draw.rect(screen, (180, 220, 255), gate_screen, 2)

        if self.get_shrine_unlocked_flag() in player.flags:
            shrine = self.shrine_rect.move(-camera_x, -camera_y)
            pygame.draw.rect(screen, (140, 220, 140), shrine)
            pygame.draw.rect(screen, (255, 255, 255), shrine, 2)

    def draw_obstacles(self, screen, camera_x, camera_y):
        for rect in self.static_obstacles:
            pygame.draw.rect(screen, (70, 50, 28), rect.move(-camera_x, -camera_y))

    def get_world_obstacles(self):
        npc_rects = [npc.rect for npc in self.npcs if npc.solid]
        return self.static_obstacles + npc_rects

    def get_nearby_npc(self, player):
        for npc in self.npcs:
            if npc.rect.colliderect(player.get_rect_world().inflate(60, 60)):
                return npc
        return None

    def can_interact_with_stump(self, player):
        return (
            "child_quest_started" in player.flags and
            "child_quest_complete" not in player.flags and
            player.get_rect_world().colliderect(self.stump_rect.inflate(30, 30))
        )

    def get_dialogue(self, dialogue_id, player):
        if dialogue_id == "elder_blocked":
            if self.can_elder_trust(player):
                return self.dialogues["elder_trust"]
            if self.has_any_progress(player):
                return self.dialogues["elder_neutral"]
            return self.dialogues["elder_blocked"]

        if dialogue_id == "forager_intro":
            if "forager_refused" in player.flags:
                return self.dialogues["forager_refused"]
            if "forager_quest_complete" in player.flags:
                return self.dialogues["forager_done"]
            return self.dialogues["forager_intro"]

        if dialogue_id == "hunter_intro":
            if "hunter_resolved" in player.flags:
                return self.dialogues["hunter_done"]
            return self.dialogues["hunter_intro"]

        if dialogue_id == "child_intro":
            if "child_quest_complete" in player.flags:
                if "child_reward_taken" in player.flags:
                    return self.dialogues["child_done"]
                return self.dialogues["child_return_complete"]
            if "Forest Map" in player.story_items:
                return self.dialogues["child_has_map"]
            if "child_quest_started" in player.flags:
                return self.dialogues["child_quest_accepted"]
            return self.dialogues["child_intro"]

        if dialogue_id.startswith("knowledge_"):
            lesson = dialogue_id.split("_", 1)[1]
            if f"learned_{lesson}" in player.flags:
                return self.dialogues[f"{dialogue_id}_done"]
            return self.dialogues[dialogue_id]

        if dialogue_id == "village_listener":
            if not self.has_region_tasks_started(player):
                return self.dialogues["regional_locked"]
            if "learned_village" in player.flags:
                return self.dialogues["knowledge_village_done"]
            return self.dialogues["village_listener"]

        if dialogue_id in ("village_warden", "cavern_warden", "citadel_warden"):
            if not self.has_region_tasks_started(player):
                return self.dialogues[f"{dialogue_id}_intro"]
            if self.has_region_tasks_complete(player):
                return self.dialogues[dialogue_id]
            return self.dialogues[f"{dialogue_id}_wait"]

        task_dialogues = {
            "village_bell": "village_bell_returned",
            "village_medic": "village_medic_helped",
            "cavern_crystal": "cavern_crystal_found",
            "cavern_miner": "cavern_miner_found",
            "citadel_embers": "citadel_embers_gathered",
            "citadel_banner": "citadel_banner_mended"
        }
        if dialogue_id in task_dialogues:
            if not self.has_region_tasks_started(player):
                return self.dialogues["regional_locked"]
            if task_dialogues[dialogue_id] in player.flags:
                return self.dialogues[f"{dialogue_id}_done"]
            return self.dialogues[dialogue_id]

        if dialogue_id == "regional_lore":
            if not self.has_region_tasks_started(player):
                return self.dialogues["regional_locked"]
            return self.dialogues["regional_lore"]

        return self.dialogues.get(dialogue_id)

    def has_any_progress(self, player):
        return (
            "forager_listened" in player.flags or
            "forager_quest_complete" in player.flags or
            "forager_refused" in player.flags or
            "child_quest_started" in player.flags or
            "child_quest_complete" in player.flags or
            "hunter_resolved" in player.flags
        )

    def has_met_forest_requirements(self, player):
        return (
            "child_quest_complete" in player.flags and
            "hunter_resolved" in player.flags and
            player.knowledge >= 7
        )

    def can_elder_trust(self, player):
        return self.has_met_forest_requirements(player)

    def region_goal_text(self, player):
        return self.region_goal_texts(player)[0]

    def region_goal_texts(self, player):
        goals = []
        if self.region == "Forest":
            if self.get_region_key_item() in player.story_items:
                goals.append("The gate is ready. Leave for the Sunken Village when you choose.")
                return goals
            if self.get_shrine_unlocked_flag() in player.flags:
                goals.append("Find the marked shrine in the east and confront the Moss Bear.")
                return goals
            if self.can_elder_trust(player):
                goals.append("Return to Elder Rowan. He will reveal the shrine.")
                return goals
            goals.append("Speak to the forest dwellers and earn the elder's trust.")
            if "Forest Map" in player.story_items and "child_quest_complete" not in player.flags:
                goals.append("Return the lost map to the child.")
            elif "child_quest_started" in player.flags and "child_quest_complete" not in player.flags:
                goals.append("Find the lost map near the glowing stump in the south.")
            if player.knowledge < 7:
                goals.append(f"Learn the forest's lessons. Knowledge: {player.knowledge}/7.")
            if "hunter_resolved" not in player.flags:
                goals.append("Resolve Hunter Brann's anger.")
            return goals

        if self.get_region_key_item() in player.story_items:
            return [f"The {self.get_region_key_item()} is ready. Find the gate onward."]
        if self.get_shrine_unlocked_flag() in player.flags:
            return [f"Find the marked {self.region} shrine and confront its guardian."]

        if not self.has_region_tasks_started(player):
            return [f"Speak to the {self.region} elder to learn what must be done."]

        goals.append(f"Help the people of the {self.region} to earn the shrine path.")
        done = sum(1 for flag in self.get_region_task_flags() if flag in player.flags)
        total = len(self.get_region_task_flags())
        goals.append(f"Region tasks: {done}/{total}.")
        task_names = {
            "learned_village": "Listen to the Rain Listener.",
            "village_bell_returned": "Return the drowned bell.",
            "village_medic_helped": "Help the Root Medic.",
            "learned_cavern": "Learn the cavern echo.",
            "cavern_crystal_found": "Find the blue crystal.",
            "cavern_miner_found": "Guide the lost miner.",
            "learned_citadel": "Read the red page.",
            "citadel_embers_gathered": "Gather the cold embers.",
            "citadel_banner_mended": "Mend the torn banner."
        }
        for flag in self.get_region_task_flags():
            if flag not in player.flags:
                goals.append(task_names.get(flag, flag))
        return goals

    def next_region(self):
        regions = list(self.regions.keys())
        i = regions.index(self.region)
        if i < len(regions) - 1:
            self.region = regions[i + 1]
            self.setup_region()

    def setup_region(self):
        if self.region == "Village":
            self.npcs = [
                NPC(650, 520, "Village Warden", (210, 190, 150), "village_warden"),
                NPC(900, 640, "Rain Listener", (150, 190, 230), "village_listener"),
                NPC(1280, 760, "Bell Diver", (120, 180, 210), "village_bell"),
                NPC(1780, 560, "Root Medic", (130, 220, 150), "village_medic"),
                NPC(520, 980, "Canal Mason", (180, 170, 140), "regional_lore"),
                NPC(820, 1180, "Net Mender", (160, 210, 210), "regional_lore"),
                NPC(1120, 980, "Moss Baker", (210, 180, 130), "regional_lore"),
                NPC(1500, 1080, "Flood Scribe", (190, 190, 230), "regional_lore"),
                NPC(2050, 760, "Lantern Nurse", (230, 210, 140), "regional_lore"),
                NPC(2480, 1120, "Bridge Child", (160, 190, 230), "regional_lore")
            ]
            self.static_obstacles = [
                pygame.Rect(540, 360, 140, 70),
                pygame.Rect(1040, 500, 100, 220),
                pygame.Rect(760, 820, 260, 70),
                pygame.Rect(1320, 620, 160, 160)
            ]
            self.gate_rect = pygame.Rect(2860, 900, 90, 220)
            self.shrine_rect = pygame.Rect(2300, 420, 100, 100)
        elif self.region == "Caverns":
            self.npcs = [
                NPC(620, 560, "Echo Keeper", (175, 175, 225), "cavern_warden"),
                NPC(1160, 840, "Miner of the Deep", (160, 150, 120), "knowledge_cavern"),
                NPC(1580, 660, "Crystal Child", (100, 190, 230), "cavern_crystal"),
                NPC(2100, 1120, "Lost Miner", (180, 170, 120), "cavern_miner"),
                NPC(520, 1080, "Glowcap Tender", (120, 210, 160), "regional_lore"),
                NPC(860, 1320, "Rail Keeper", (180, 160, 120), "regional_lore"),
                NPC(1360, 1220, "Deep Cartographer", (150, 190, 220), "regional_lore"),
                NPC(1840, 900, "Quiet Prospector", (170, 150, 110), "regional_lore"),
                NPC(2380, 700, "Water Seer", (120, 170, 210), "regional_lore"),
                NPC(2680, 1240, "Stone Singer", (190, 180, 230), "regional_lore")
            ]
            self.static_obstacles = [
                pygame.Rect(700, 420, 220, 90),
                pygame.Rect(1120, 1040, 260, 80),
                pygame.Rect(1760, 620, 90, 340),
                pygame.Rect(2280, 1180, 300, 90)
            ]
            self.gate_rect = pygame.Rect(2860, 860, 90, 240)
            self.shrine_rect = pygame.Rect(2380, 340, 110, 110)
        elif self.region == "Citadel":
            self.npcs = [
                NPC(680, 560, "Ash Sentinel", (230, 120, 100), "citadel_warden"),
                NPC(1240, 760, "Red Archivist", (210, 170, 150), "knowledge_citadel"),
                NPC(1640, 900, "Ember Keeper", (230, 150, 90), "citadel_embers"),
                NPC(2140, 620, "Banner Keeper", (200, 120, 150), "citadel_banner"),
                NPC(520, 980, "Wall Mason", (190, 150, 130), "regional_lore"),
                NPC(900, 1160, "Glass Knight", (220, 190, 180), "regional_lore"),
                NPC(1380, 1180, "Ash Gardener", (180, 130, 110), "regional_lore"),
                NPC(1840, 1180, "Court Page", (210, 150, 160), "regional_lore"),
                NPC(2460, 760, "Oath Keeper", (230, 180, 120), "regional_lore"),
                NPC(2700, 1160, "Last Watch", (180, 180, 190), "regional_lore")
            ]
            self.static_obstacles = [
                pygame.Rect(620, 360, 260, 80),
                pygame.Rect(1060, 900, 160, 260),
                pygame.Rect(1640, 520, 320, 90),
                pygame.Rect(2260, 980, 260, 180)
            ]
            self.gate_rect = pygame.Rect(2860, 840, 90, 260)
            self.shrine_rect = pygame.Rect(2380, 360, 120, 120)

    def get_gate_rect(self):
        return self.gate_rect

    def get_shrine_rect(self):
        return self.shrine_rect

    def get_stump_rect(self):
        return self.stump_rect

    def get_random_relic(self):
        return random.choice([
            {"name": "Ancient Acorn", "effect": "heal"},
            {"name": "Moss Crown", "effect": "damage"},
            {"name": "Broken Compass", "effect": "speed"}
        ])
