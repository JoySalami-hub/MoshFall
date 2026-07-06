def apply_relics(player):
    damage_bonus = 0
    speed_bonus = 0
    heal_bonus = 0

    for relic in player.relics:
        if relic["effect"] == "damage":
            damage_bonus += 5
        elif relic["effect"] == "speed":
            speed_bonus += 1
        elif relic["effect"] == "heal":
            heal_bonus += 20
        elif relic["effect"] == "knowledge":
            pass

    player.damage = 10 + damage_bonus
    player.speed = 4 + speed_bonus
    player.max_hp = 100 + heal_bonus
    player.hp = min(player.hp, player.max_hp)
