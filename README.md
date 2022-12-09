# Project2
`Roguelike` created with `PyGame`! You have sword, staff and bow. Collect upgrades for your charecter and weapond and defeat enemies to raise your score.

# Features
- Big preset of rooms that world generates with
- You can see a history of your runs on the scoreboard
- Many special upgrades for your weapons


# Gameplay
You get charecter upgrades after clearing a simple room and special upgrades after difficult rooms. Also you get money from defeated enemies.
Each floor has 6 rooms:
- 1 start room
- 1 boss room
- 1 shop
- 1 difficult rooms
- 2 simple rooms
There are 5 items in the shop. They can be upgrades, heals and keys. You can spend collected money on them.

# Player charecter
- Stats
    - HP (Hit points)
    - Stamina (Use it for dodjerolls and hits)
- Items
    - Backpack (It's your inventory)
    - Map
    - Basic weapon set

# Items, pickups and other stuff
- Weapons
    - Bow
    - Staff
    - Sword
- Upgrades
    - Charecther
        - +Atack
        - +AtackSpeed
        - +MoveSpeed
        - +MaxHP
        - +MaxMana
    - Special upgrades for weapons
        - Bow
            - +Arrows in a shot
        - Staff
            - -Mana Usage
            - +SpellCastSpeed
        - Sword
            - +SwingWidth
- PickUps
    - HpUps
        - Half heart
        - Full heart
        - Full HP
    - Treasures (money)
        - Coin (+1)
        - Ruby (+10)
        - Diamond (+50)
    - Keys for chests
        - Key 

# Elemental reactions
You can use different elements with your staff that are obtained during the run as spells you can switch. After combining them you can get special elemental reactions.
- Elements
    - Pyro
    - Hydro
    - Electro
    - Cryo
- Reactions

     ELEMENTS | Pyro | Hydro | Electro | Cryo 
    :----:|:----:|:-----:|:-------:|:----:
     Pyro | - | Vaporize | Overloaded | Melt 
     Hydro | Vaporize | - | Electro-Charged | Frozen 
     Electro | Overloaded | Electro-Charged | - | Super-conduct 
     Cryo | Melt | Frozen | Super-conduct | -

# Enemies
- Simple
    - Slimes
    - Zombies
    - Skeletons
        - Wariors
        - Archers
        - Mages (1 mage has 1 element)
    - Goblins
        - Wariors
        - Archers
        - Mages (1 mage has 1 element)
        - Assasins
        - Healers
- Elite
    - Elite enemies have increased resists to certain types of weapon.
- Bosses
    - Giant Slime
    - Angry Zombie
    - Ancient Skeleton
    - Hobgoblin
    - Grand Vampire

# Dependencies
- PyGame

# Authors
- [Biostev](https://github.com/Biostev)
