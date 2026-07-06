import json
import os

def save_filename(slot=1):
    return f"save_slot{slot}.json"

def save_game(player, world=None, slot=1):
    data = {
        "x": player.x,
        "y": player.y,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "damage": player.damage,
        "speed": player.speed,
        "relics": player.relics,
        "story_items": list(player.story_items),
        "flags": list(player.flags),
        "mercy": player.mercy,
        "power": player.power,
        "knowledge": player.knowledge
    }
    if world:
        data["region"] = world.region

    with open(save_filename(slot), "w") as f:
        json.dump(data, f, indent=2)

def load_game(player, slot=1):
    filename = save_filename(slot)
    if not os.path.exists(filename):
        if slot == 1 and os.path.exists("save.json"):
            filename = "save.json"
        else:
            return None

    with open(filename, "r") as f:
        data = json.load(f)

    player.x = data.get("x", player.x)
    player.y = data.get("y", player.y)
    player.hp = data.get("hp", player.hp)
    player.max_hp = data.get("max_hp", player.max_hp)
    player.damage = data.get("damage", player.damage)
    player.speed = data.get("speed", player.speed)
    player.relics = data.get("relics", [])
    player.story_items = set(data.get("story_items", []))
    player.flags = set(data.get("flags", []))
    player.mercy = data.get("mercy", player.mercy)
    player.power = data.get("power", player.power)
    player.knowledge = data.get("knowledge", player.knowledge)
    return data

def slot_has_save(slot):
    return os.path.exists(save_filename(slot)) or (slot == 1 and os.path.exists("save.json"))

def slot_label(slot):
    if not slot_has_save(slot):
        return f"Slot {slot}: Empty"

    filename = save_filename(slot)
    if not os.path.exists(filename) and slot == 1 and os.path.exists("save.json"):
        filename = "save.json"

    try:
        with open(filename, "r") as f:
            data = json.load(f)
        region = data.get("region", "Forest")
    except (OSError, json.JSONDecodeError):
        region = "Unknown"

    return f"Slot {slot}: {region}"
