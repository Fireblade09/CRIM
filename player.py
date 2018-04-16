import world
from items import *
import random

class Player():
    def __init__(self):
        self.coin = Coin()
        self.fists = Fist()
        self.inventory = [self.coin, self.fists]
        self.hp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False
        self.equipped_wep = self.fists
        self.keys = 0
        self.fire_shield = True
        self.Potion_Of_Life = False

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')
        print("{} is equipped\n".format(self.equipped_wep))

    def move(self,dx,dy):
        self.location_x += dx
        self.location_y += dy
        tile = world.tile_exists(self.location_x, self.location_y)
        print(tile.intro_text(self))

    def equip_wep(self):
        weapon = input("What would you like to equip?")
        if weapon in inventory:
            self.equipped_wep = weapon
        else:
            print('You don\'t have that!')

    def pick_up_item(self):
        game.room.pick_up_item(self)

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        if self.is_alive():
            enemy.hp -= self.equipped_wep.damage
            print('You do {} damage!'.format(self.equipped_wep.damage))
            enemy.become_hostile()
            if not enemy.is_alive():
                print("You killed {}!".format(enemy.name))
            else:
                print("{} HP is {}.".format(enemy.name, enemy.hp))
        else:
            print('You swing ferociously, but, despite your best efforts, your weapon passes harmlessly through the enemy. ')

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def flee(self, tile):
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

    def heal(self):
        if HealingPotion in self.inventory:
            if self.hp > 0:
                if self.hp < 100:
                    self.hp += 50
                    if self.hp > 100:
                        self.hp = 100
                    self.inventory.pop(self.inventory.index(HealingPotion))
                    print('You gain 30 hitpoints!')
                    print('Hitpoints:', self.hp)
                else:
                    print('Health already full!')
            else:
                print("You are dead. You're going to need more than a healing potion to save you now...")
        else:
            print('You have no potions!')

    def raise_from_dead(self):
        if self.Potion_Of_Life:
            if self.hp > 0:
                print("You're already alive, no point for that!")
            else:
                print('You feel life once again course through your veins. Try not to die this time.')
                self.hp = 100
                self.Potion_Of_Life = False
        else:
            print('You have no Potions of Life!')

    def player_death(self):
        print('As your blood seeps from your body, blackness fills your vision. Suddenly, a shining light surrounds you. A voice booms from above "Your journey is not over yet. Seek hope at an abandoned shop..." Your eyes shoot open. Your conscious has returned, but your body is still a swirly white. You are a ghost, unable to interact with the world.')
        self.hp = -1
        return

    def check_hp(self):
        if self.hp <= 0:
            print('You are dead.')
        else:
            print('HP is {}'.format(self.hp))

    def sharpen(self):
        for weapon in self.inventory:
            try:
                weapon.sharpen()
            except:
                pass

    def drink(self):
        return
