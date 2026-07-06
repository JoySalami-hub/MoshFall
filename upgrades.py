import random

def increase_max_hp(player):
    player.max_hp += 20
    player.hp = player.max_hp

def generate_upgrades():
    pool = [
        {"name": "Damage +10", "apply": lambda p: setattr(p, "damage", p.damage + 10)},
        {"name": "Speed +1", "apply": lambda p: setattr(p, "speed", p.speed + 1)},
        {"name": "Max HP +20", "apply": increase_max_hp},
    ]
    return random.sample(pool, 3)
