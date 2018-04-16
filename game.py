#Created by Brady Kruse
#Guide from Phillip Johnson (www.letstalkdata.com)
#Help from stackoverflow.com
#ASCII Text from www.patorjk.com
#ASCII Art by Pranay Marella
#Inspired by Zork

import world
from items import *
import random
import time
import os
import shutil
import pygame

def credits():
    print("\n\nCreated by Brady Kruse")
    print("PLENTY of help from Phillip Johnson (www.letstalkdata.com)")
    print("ASCII Text from www.patorjk.com")
    print("ASCII Art from Pranay Marella")
    print("Inspiration from Zork")
    print("Sound Effects from Nintendo Corporation\n")
    return

def loadingscreen():
    progress = []
    for x in range(10): progress.append('-')
    for each in progress:
        time.sleep(0.5)
        progress.pop()
        progress.insert(0,'#')
        os.system('cls' if os.name == 'nt' else 'clear')
        print('LOADING...' + '\n' + ''.join(progress))

def ReadyPlayerOne():
    time.sleep(1)
    phrase = []
    RPO = 'READY PLAYER ONE'
    index = 0
    columns = shutil.get_terminal_size().columns
    for x in range(len(RPO)):
        time.sleep(0.2)
        phrase.append(RPO[index])
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'+''.join(phrase).center(columns))
        index += 1

def Sound():
    pygame.init()
    pygame.mixer.music.load("test.mp3")
    pygame.mixer.music.play()



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
        self.fire_shield = False
        self.Potion_Of_Life = False
        self.HealingPotions = 0
        self.beer = 0

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')
        print("=================\n{} is equipped\n=================\n".format(self.equipped_wep.name))

    def move(self,dx,dy):
        self.location_x += dx
        self.location_y += dy
        tile = world.tile_exists(self.location_x, self.location_y)
        print(tile.intro_text(self))

    def equip_wep(self):
        weapon = input("What would you like to equip? ")
        for item in self.inventory:
            if weapon.upper() == item.name.upper():
                self.equipped_wep = item
                print("{} equipped!\n".format(item.name))
                return
        print("You don't have that!")

    def pick_up_item(self):
        room.pick_up_item(self)

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
            self.twenty_percent = 0.2 * self.equipped_wep.damage
            self.hit_damage = random.randint(self.equipped_wep.damage - round(self.twenty_percent), self.equipped_wep.damage + round(self.twenty_percent))
            self.miss = random.randint(0,10)
            if self.miss == 5:
                print("You swing valiantly and miss epicly! Oof!")
                self.hit_damage = 0
            else:
                if enemy.name == 'Dragon':
                    if self.equipped_wep.name == 'Beer':
                        self.hit_damage = 1000000
                        print("The dragon seems to have an odd weakness to alcohol...lightweight.")
                enemy.hp -= self.hit_damage
            print('You do {} damage!'.format(self.hit_damage))
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
        for item in self.inventory:
            if item.name == 'Healing potion':
                if self.hp > 0:
                    if self.hp < 100:
                        self.hp += 30
                        if self.hp > 100:
                            self.hp = 100
                        self.inventory.pop(self.inventory.index(item))
                        self.HealingPotions -= 1
                        print('You gain 30 hitpoints!')
                        return
                    else:
                        print('Health already full!')
                        return
                else:
                    print("You are dead. You're going to need more than a healing potion to save you now...")
                    return


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
        print('As your blood seeps from your body, blackness fills your vision. Suddenly, a shining light surrounds you. A voice booms from above "Your journey is not over yet. Seek hope at an abandoned shop..." Your eyes shoot open. Your conscious has returned, but your body is still a swirly white. You are a ghost, unable to do damage to anything.')
        self.hp = -1
        return

    def check_hp(self):
        if self.hp <= 0:
            print('You are dead.')
        else:
            print('HP is {}'.format(self.hp))

    def sharpen(self):
        weapon = input('What would you like to sharpen? ')
        for item in self.inventory:
            if weapon.upper() == item.name.upper():
                dumbass = item.sharpen()
                if dumbass == True:
                    self.hp -= 1
                    return
                return
        print('You do not have that!')

    def drink(self):
        for item in self.inventory:
            if item.name == 'Beer':
                print("You drink the beer and feel quite ill. You lose a few hitpoints.")
                self.hp -= 5
                self.inventory.pop(self.inventory.index(item))
                self.beer -= 1
                return


def play():
    loadingscreen()
    ReadyPlayerOne()
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    Sound()
    time.sleep(0.75)
    print(" __          __  _                            _           _____      _           _  \n \ \        / / | |                          | |         / ____|    (_)         | | \n  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |     _ __ _ _ __ ___ | | \n   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | |    | '__| | '_ ` _ \| | \n    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |____| |  | | | | | | |_| \n     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \_____|_|  |_|_| |_| |_(_) \n\n")
    print('CRIM v1.3')
    print("Created by Brady Kruse\n\n")
    global room
    world.load_tiles()
    player = Player()
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text(player))
    while not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        if not player.victory:
            print("\nChoose an action:\n")
            available_actions = room.available_actions(player)
            for action in available_actions:
                print(action)
            action_input = input('\nAction: ')
            print()
            fail = 0
            for action in available_actions:
                if action_input.lower() == action.hotkey:
                    print("=============================================================================================")
                    player.do_action(action, **action.kwargs)
                    break
                else:
                    fail += 1
            if fail == len(available_actions):
                print("Invalid input!\n")

    credits()

play()
