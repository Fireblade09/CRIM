import items
import random
class Enemy:
    def __init__(self, name, hp, damage, hostile = True):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.hostile = hostile

    def is_alive(self):
        return self.hp > 0

    def is_hostile(self):
        return self.hostile

    def become_hostile(self):
        self.hostile = True
        return

    def attack(self,player):
        if self.is_alive() and player.is_alive():
            self.twenty_percent = 0.2 * self.damage
            self.hit_damage = round(random.randint(self.damage - round(self.twenty_percent), self.damage + round(self.twenty_percent)))
            self.miss = random.randint(0,10)
            if self.miss == 5:
                print("The {} misses terribly! Lucky!".format(self.name))
                self.hit_damage = 0
            else:
                player.hp -= self.hit_damage
            if player.hp <= 0:
                player.hp = 0
            print("Enemy does {} damage! {} HP remaining!".format(self.hit_damage, player.hp))
            if player.hp == 0:
                player.player_death()
        elif not self.is_alive():
            print('Enemy is dead.')
        elif not player.is_alive():
            print('The enemy stares in confusion as it does no damage to you. You\'d probably laugh if you weren\'t, ya know, dead. Kinda a moodkiller.')

class Dragon(Enemy):
    def __init__(self):
        super().__init__(name = 'Dragon', hp = 200, damage = 30)

    def attack(self,player):
        if self.is_alive() and player.is_alive():
            self.twenty_percent = 0.2 * self.damage
            self.hit_damage = random.randint(self.damage - round(self.twenty_percent), self.damage + round(self.twenty_percent))
            if player.fire_shield == True:
                self.hit_damage = 2
            self.miss = random.randint(0,10)
            if self.miss == 5:
                print("The dragon has a momentary vision issue and completely misses you with the fire! Lucky!")
                self.hit_damage = 0
            else:
                player.hp -= self.hit_damage
            if player.hp <= 0:
                player.hp = 0
            print("Enemy does {} damage! {} HP remaining!".format(self.hit_damage, player.hp))
            if player.hp == 0:
                player.player_death()
        elif not self.is_alive():
            print('Enemy is dead.')
        elif not player.is_alive():
            print('The enemy stares in confusion as it does no damage to you. You\'d probably laugh if you weren\'t, ya know, dead. Kinda a moodkiller.')

class Skeleton(Enemy):
    def __init__(self):
        super().__init__(name="Skeleton", hp=20, damage=5)

class Rat(Enemy):
    def __init__(self):
        super().__init__(name= 'Rat', hp = 10, damage = 2)

class Dwarf(Enemy):
    def __init__(self):
        super().__init__(name = 'Dwarf', hp = 10, damage = 5, hostile = False)

class GoblinKing(Enemy):
    def __init__(self):
        super().__init__(name = 'Goblin King', hp = 50, damage = 20, hostile = False)
        self.key = True

    def money(self,player):
        print('The goblin king smiles at you. He says he knows you seek the green key, but he\'ll only give it to you for 100 gold! That asshole!')
        if player.coin.amount_coin >= 100:
            self.answer = input('Do you want to give it to him? (y/n) ').lower()
            while self.answer != 'y' and self.answer != 'n' and self.answer != 'yes' and self.answer != 'no':
                self.answer = input('Do you want to give it to him?(y/n) ')
            if self.answer == 'y' or self.answer == 'yes':
                print('You almost shed a tear as you hand over the coins.')
                player.coin.amount_coin -= 100
                player.keys += 1
                greenkey = items.GreenKey()
                player.inventory.append(greenkey)
                if player.keys > 1:
                    print('Congratulations! You now have {} keys!'.format(player.keys))
                else:
                    print("Congratulations! You now have {} key!".format(player.keys))
                return True
            if self.answer == 'n' or self.answer == 'no':
                print('The goblin calls you a Scrooge and resumes attempting to count past three.')
                return False
        else:
            print('You can\'t afford that!')
            return False

class Wizard(Enemy):
    def __init__(self):
        super().__init__(name = 'Wizard' , hp = 10, damage = 15)

class Sphinx(Enemy):
    def __init__(self):
        super().__init__(name = 'Sphinx', hp = 100, damage = 30, hostile = False)

    def become_hostile(self):
        self.hostile = True

    def riddle(self,player):
        self.hostile = False
        while not self.hostile:
            print('"Only a man of wisdom deserves this key. Solve my riddle and I grant you this key with no challenge. Guess incorrectly and you die."')
            yes_no = input('Would you like to try? (y/n) ').lower()
            while yes_no != 'y' and yes_no != 'yes' and yes_no != 'no' and yes_no != 'n':
                yes_no = input('Would you like to try? (y/n)')
            if yes_no == 'y' or yes_no  == 'yes':
                self.answer = input('This thing all things devours: birds, beasts, trees, flowers. Gnaws iron, bites steel. Grinds hard stones to meal. Slays king, ruins town, and beats high mountain down. \nWhat is it? ')
                if self.answer.upper() == 'TIME':
                    print('The sphinx gives a shocked look to you and calmly hands over a white key.')
                    player.keys += 1
                    WhiteKey = items.WhiteKey()
                    player.inventory.append(WhiteKey)
                    if player.keys > 1:
                        print('Congratulations! You now have {} keys!'.format(player.keys))
                    else:
                        print('Congratulations! You now have {} key!'.format(player.keys))
                    return True
                else:
                    print('The sphinx smiles evilly and lunges at you! You were wrong!')
                    self.become_hostile()
                    self.attack(player)
                    return False
            if yes_no == 'no' or yes_no == 'n':
                print('The sphinx looks slightly upset, then sits back.')
                return False
        self.attack()
