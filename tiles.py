import items, enemies, actions, world
import random
import pictures

class MapTile:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def intro_text(self,player):
        return

    def modify_player(self,player):
        return

    def adjacent_moves(self):
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self,player):
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.CheckHP())
        moves.append(actions.EquipWep())
        if player.Potion_Of_Life:
            moves.append(actions.Undead())
        if player.HealingPotions > 0:
            moves.append(actions.Heal())
        if player.beer > 0:
            moves.append(actions.Drink())
        return moves

class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        self.item_name = 'nothing'
        self.item = False
        super().__init__(x, y)

    def modify_player(self, player):
        if self.enemy.is_alive():
            self.enemy.attack(player)
        else:
            print(self.enemy_death(self.enemy.name, self.item_name))

    def enemy_death(self, enemy, item):
        return "The {} is dead and dropped {}".format(enemy,item)

    def available_actions(self,player):
        if self.enemy.is_alive() and player.is_alive():
            moves = [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
            if player.HealingPotions > 0:
                moves.append(actions.Heal())
            return moves
        else:
            moves = self.adjacent_moves()
            moves.append(actions.ViewInventory())
            moves.append(actions.CheckHP())
            moves.append(actions.EquipWep())
            if self.item and not self.enemy.is_alive():
                moves.append(actions.PickUpItem())
            if player.Potion_Of_Life:
                moves.append(actions.Undead())
            if player.HealingPotions > 0:
                moves.append(actions.Heal())
            if player.beer > 0:
                moves.append(actions.Drink())
            return moves

class SpawnRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "You're in a damp dungeon room. Chains and other nefarious-looking objects hang on the wall. A poster on the wall advertises for 'Shabazz's Famous Life Potions! Now touchable by the dead! On sale now!' To the west, a heavy metal door is locked with a very oversized padlock with 4 different key holes, each a different color: blue, white, black, and green. Paths lead to the north and south."

class RatRoom(EnemyRoom):
    def __init__(self,x, y):
        super().__init__(x,y, enemies.Rat())
        self.taken = False
        self.item = self.enemy.is_alive()
        self.item_name = 'sword'

    def intro_text(self,player):
        if self.enemy.is_alive():
            return 'A rat sits on the floor, attempting to look menacing. A dull sword that it is apparently guarding sits in the corner. Paths lead to the north and east.'
        elif self.item:
            return 'A now slain rat lies on the floor. What a mighty hero you must be to defeat this awful vermin! A now unguarded sword lies in the corner. Paths lead to the north and east.'
        else:
            return 'A now slain rat lies on the floor. What a mighty hero you must be to defeat this awful vermin! You have already taken the sword. Paths lead to the north and east.'


    def pick_up_item(self, player):
        if not self.taken:
            if player.is_alive():
                sword = items.Sword()
                player.inventory.append(sword)
                self.taken = True
                self.item = False
                print('Sword taken!')
            else:
                print("You try to grab the sword, but your hand passes right through.")

class FallenKnightRoom(MapTile):

    def __init__(self,x,y):
        super().__init__(x,y)
        self.taken = False

    def intro_text(self,player):
        if not self.taken:
            return "A slain knight slumps against the wall. Scorch marks cover his armor. Claw marks mar the walls. A once-mighty sword lays next to the deceased knight, although it now appears to be quite dull. Paths lead south and east."
        else:
            return "A slain knight slumps against the wall. Scorch marks cover his armor. Claw marks mar the walls. The sword that was once here now belongs to you. Paths lead south and east."
        return


    def pick_up_item(self,player):
        if not self.taken:
            if player.is_alive():
                GreatSword = items.GreatSword()
                self.taken = True
                print("You pick up the sword and feel a certain energy flow through your body.")
                player.inventory.append(GreatSword)
            else:
                print("You try to pick up the sword, but, due to being dead, fail terribly.")

    def available_actions(self,player):
        moves = super().available_actions(player)
        if not self.taken:
            moves.append(actions.PickUpItem())
        return moves

class AbandonAllHopeRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "You stand in a stone hallway. Burn and scratch marks cover all the walls. To the west, a path with a sign above it warns 'Abandon All Hope Ye Who Enter Here.' Another, much safer-looking path leads south. Someone has scratched something on the wall. They almost look like arrows: ^ > > v v v v v > v > v v >"

    def modify_player(self,player):
        return

class HallRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "You stand in a standard hallway. Not much else to see here. It's pretty miserable actually."

    def modify_player(self,player):
        return

class GoingWrongWayRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "You stand in a hall. Along the wall, huge letters tell you 'You are going the wrong way!' Paths lead to the north, or, if you are particulalry ignorant of warnings, to the south."

    def modify_player(self,player):
        return

    def available_actions(self,player):
        moves = []
        moves.append(actions.MoveNorth())
        moves.append(actions.MoveSouth())
        moves.append(actions.ViewInventory())
        moves.append(actions.CheckHP())
        moves.append(actions.EquipWep())
        if player.Potion_Of_Life:
            moves.append(actions.Undead())
        if player.HealingPotions > 0:
            moves.append(actions.Heal())
        if player.beer > 0:
            moves.append(actions.Drink())
        return moves

class DoNotGoSouthRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "A voice booms from the heavens: 'DO NOT GO SOUTH.' Paths lead north or south."

    def modify_player(self,player):
        return

class SeriouslyNoSouthRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "In large, flaming, OBVIOUS letters, someone has written: 'Are you stupid? Seriously. No south.' Paths lead north or south."

    def modify_player(self,player):
        return

class DeathRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return ''

    def modify_player(self,player):
        if player.hp > 0:
            print("Spikes shoot from the walls, killing you instantly. You have nobody but yourself to blame.")
        elif player.hp < 0:
            print("Spikes shoot from the walls, passing right through your ghostly body.")
        if player.hp != -1:
            player.player_death()
        return

class BigCoinRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.taken = False
        self.item = True
        self.item_name = 'coins'

    def intro_text(self,player):
        return ''

    def modify_player(self,player):
        if player.is_alive():
            print("Wait, how did you get here? While ALIVE?")
        elif not player.is_alive() and not self.taken:
            print("You stand in stone room full of MONEY and - Wait, how did you get here? Oh, you're dead already. Guess you can't be double dead. Enjoy your coins.")
        else:
            print("You stand in a stone room NO LONGER full of money. What? You thought I was dumb enough to give you money twice?")


    def pick_up_item(self, player):
        player.coin.add_coin(500)
        self.taken = True
        self.item = True

    def available_actions(self,player):
        moves = super().available_actions(player)
        if not self.taken:
            moves.append(actions.PickUpItem())
        return moves

class CaveRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "You stand in a gross cave. It smells. Ew."

    def modify_player(self,player):
        return

class RandomRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "You stand in a room that appears to be spinning. You quickly lose your bearings. This is otherwise known as becoming zorked."

    def modify_player(self,player):
        return

    def available_actions(self,player):
        moves = []
        moves.append(actions.StumbleThroughDoor(self))
        return moves

class SkeletonRoom(EnemyRoom):
    def __init__(self,x, y):
        super().__init__(x,y, enemies.Skeleton())
        self.taken = False
        self.item = self.enemy.is_alive()
        self.item_name = 'coins'

    def intro_text(self,player):
        if self.enemy.is_alive():
            pictures.SkeletonTwo()
            return 'A skeleton warrior swings at you as you walk in!'
        elif self.item:
            return 'The skeleton has been slain and leaves a few coins behind.'
        else:
            return 'The skeleton has been slain and you have already taken the coins.'


    def pick_up_item(self, player):
        if not self.taken:
            if player.is_alive():
                player.coin.add_coin(20)
                self.taken = True
                self.item = False
                print('Coins taken!')
            else:
                print('You are dead! How are you supposed to pick up money?')

class DragonRoom(EnemyRoom):
    def __init__(self,x, y):
        dragon = enemies.Dragon()
        super().__init__(x,y, dragon)
        self.key_taken = False

    def intro_text(self,player):
        if self.enemy.is_alive():
            if player.fire_shield == True:
                pictures.DragonTwo()
                return 'A mighty black dragon shoots fire at you as you walk in! But, thanks to your fire shield, it tickles more than anything else. '
            pictures.DragonTwo()
            return 'A mighty black dragon shoots fire at you as you walk in!'
        else:
            return 'The black dragon has been slain. You are truly a warrior.'

    def modify_player(self,player):
        self.enemy.attack(player)
        if not self.enemy.is_alive() and not self.key_taken:
            player.keys += 1
            BlackKey = items.BlackKey()
            player.inventory.append(BlackKey)
            if player.keys > 1:
                print("As the life seeps from the dragon's body, he stumbles to reveal a black key behind him. You pick it up. Congratulations! You now have {} keys!".format(player.keys))
            else:
                print("As the life seeps from the dragon's body, he stumbles to reveal a black key behind him. You pick it up. Congratulations! You now have {} key!".format(player.keys))
            self.key_taken = True

class WizardRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.key_taken = False

    def intro_text(self,player):
        if player.is_alive() and not self.key_taken:
            return 'You see a wizard standing behind a forcefield of some sort. You try to get through but cannot. The wizard happily exclaims that you will never get his key, and that no living mortal could ever get through his shield!'
        if not player.is_alive() and not self.key_taken:
            player.keys += 1
            BlueKey = items.BlueKey()
            player.inventory.append(BlueKey)
            self.key_taken = True
            if player.keys > 1:
                return 'The wizard stares in shock as your cold, ghastly, dead body passes through his forcefield. Terrified, he hands you a white key. Congratulations! You now have {} keys!'.format(player.keys)
            else:
                return 'The wizard stares in shock as your cold, ghastly, dead body passes through his forcefield. Terrified, he hands you a white key. Congratulations! You now have {} key!'.format(player.keys)
        else:
            return 'The wizard is still huddled in the corner, mourning the loss of his key.'

    def modify_player(self,player):
        return

class UndeadRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.taken = False

    def intro_text(self,player):
        if self.taken and player.keys < 4 and not player.is_alive() and player.Potion_Of_Life == False:
            print("Your ghostly form sprints through the door into the room, but, alas, the Potion of Life is gone and used. You realize that there is no hope left for you and slowly ascend into the next world. You have failed. ")
            player.victory = 'Loss'
            return ''
        if not self.taken:
            return "You stand in a abandoned store of some sort, although a dungeon seems like an odd place for it. Posters plaster the wall, advertising the magical healing benefits of Shabazz's Potions of Life! On a lit podium in the middle of the store sits one of the famous potions. How lucky that no thieves have yet taken it!"
        else:
            return "You stand in a abandoned store of some sort, although a dungeon seems like an odd place for it. Posters plaster the wall, advertising the magical healing benefits of Shabazz's Potions of Life! A now-empty podium sits in the middle of the store."
        return


    def pick_up_item(self,player):
        if not self.taken:
            PotionOfLife = items.PotionOfLife()
            self.taken = True
            print("You take the potion")
            player.inventory.append(PotionOfLife)
            player.Potion_Of_Life = True
        else:
            print("Nothing to pick up!")

    def available_actions(self,player):
        moves = super().available_actions(player)
        if not self.taken:
            moves.append(actions.PickUpItem())
        return moves

class SphinxRoom(EnemyRoom):
    def __init__(self,x, y):
        self.sphinx = enemies.Sphinx()
        super().__init__(x,y, self.sphinx)
        self.key_taken = False

    def intro_text(self,player):
        self.enemy.hostile = False
        if self.enemy.is_alive() and not self.key_taken:
            return 'You stumble through a door and, in an instant, you seem to have been teleported to ancient Egypt. A massive sphinx sits in the middle of the room.'
        elif not self.enemy.is_alive():
            return 'The sphinx carcass lies motionless on the floor.'
        else:
            return 'The sphinx sits calmly on the floor, happy that the key has found such an intelligent owner.'

    def modify_player(self,player):
        if self.enemy.is_alive():
            if self.enemy.is_hostile():
                self.enemy.attack(player)
            elif not self.key_taken:
                if player.is_alive():
                    self.key_taken = self.enemy.riddle(player)
                else:
                    print('The sphinx looks at you quizzically. "My mortal is only for LIVING beings," it says.')
            if self.key_taken:
                return
        elif not self.enemy.is_alive() and not self.key_taken:
            print('The sphinx is dead. You pry the white key from it\'s cold dead hands.')
            player.keys += 1
            WhiteKey = items.WhiteKey()
            player.inventory.append(WhiteKey)
            if player.keys > 1:
                print('Congratulations! You now have {} keys!'.format(player.keys))
            else:
                print("Congratulations! You now have {} key!".format(player.keys))
            self.key_taken = True
            return
        else:
            return


    def available_actions(self,player):
        moves = self.adjacent_moves()
        if self.item:
            moves.append(actions.PickUpItem())
        if self.enemy.is_alive():
            moves.append(actions.Attack(enemy=self.enemy))
        if player.Potion_Of_Life:
            moves.append(actions.Undead())
        moves.append(actions.ViewInventory())
        moves.append(actions.CheckHP())
        moves.append(actions.EquipWep())
        if player.HealingPotions > 0:
            moves.append(actions.Heal())
        if player.beer > 0:
            moves.append(actions.Drink())
        return moves

class DwarfRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        beer = items.Beer()
        if player.is_alive():
            player.inventory.append(beer)
            player.beer += 1
            return "You walk under a short doorway into a bar full of very drunk dwarves. They look at you quizzically for a few seconds, then hand you a drink with a cheer. A grindstone sits in the corner."
        else:
            return "You glide under a short doorway into a bar full of very drunk dwarves. They look at you quizzically for a few seconds. You are, after all, a ghost. One particularly rowdy dwarf in the corner yells something about not discriminating against ghosts and tries to hand you a beer. Alas, it falls through your hands, but nobody notices. The dwarves are back to partying."

    def modify_player(self,player):
        return

    def available_actions(self,player):
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.CheckHP())
        moves.append(actions.EquipWep())
        if player.is_alive():
            moves.append(actions.Sharpen())
        if player.Potion_Of_Life:
            moves.append(actions.Undead())
        if player.HealingPotions > 0:
            moves.append(actions.Heal())
        if player.beer > 0:
            moves.append(actions.Drink())
        return moves

class VendorRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return "You enter a surprisngly non-abandoned store. A vendor behind the counter offers you healing potions for 10 gold."


    def modify_player(self,player):
        if player.is_alive():
            answer = input('Would you like to buy a potion?(y/n) ')
            while answer != 'y' and answer != 'n':
                answer = input('Would you like to buy a potion?(y/n) ')
            if answer == 'y':
                number = input("How many? ")
                while True:
                    try:
                        number = round(int(number))
                        break
                    except:
                        number = input("How many? (Must be an integer)")
                count = 0
                for x in range(number):
                    if player.coin.amount_coin >= 10:
                        player.HealingPotions += 1
                        HealingPotion = items.HealingPotion()
                        player.inventory.append(HealingPotion)
                        player.coin.amount_coin -= 10
                        count += 1
                    else:
                        print('You do not have enough money!')
                        break
                print("{} potions added!".format(count))
            if answer == 'n':
                print('The store vendor looks a little sad.')
        else:
            print('The vendor shakes his head at you sadly. You\'re going to need more than healing potions now.')

class GoblinRoom(EnemyRoom):
    def __init__(self,x, y):
        GoblinKing = enemies.GoblinKing()
        super().__init__(x,y, GoblinKing)
        self.key_taken = False

    def intro_text(self,player):
        if self.enemy.is_alive() and not self.key_taken:
            return 'You step into a massive ballroom, decorated tastefully with heads on spikes and torches on the wall. Dozens of goblins are milling around. The ugliest and fattest sits on a throne with a crown on his head.'
        elif not self.enemy.is_alive():
            return 'The goblin king lies dead on the floor. Women goblins weep over him.'
        else:
            return 'The goblin king is counting his money and doesn\'t pay you a second thought.'

    def modify_player(self,player):
        if self.enemy.is_alive():
            if self.enemy.is_hostile():
                self.enemy.attack(player)
            elif not self.key_taken:
                if player.is_alive():
                    self.key_taken = self.enemy.money(player)
                else:
                    print('The goblin king jumps up, frightened, then begins yelling about a ghost. You best be leaving.')
            if self.key_taken:
                return
        elif not self.enemy.is_alive() and not self.key_taken:
            print('The goblin king is dead. You pry the green key from his greedy hands.')
            player.keys += 1
            GreenKey = items.GreenKey()
            player.inventory.append(GreenKey)
            if player.keys > 1:
                print('Congratulations! You now have {} keys!'.format(player.keys))
            else:
                print('Congratulations! You now have {} key!'.format(player.keys))
            self.key_taken = True
            return
        else:
            return

    def available_actions(self,player):
        moves = self.adjacent_moves()
        if self.item:
            moves.append(actions.PickUpItem())
        if self.enemy.is_alive():
            moves.append(actions.Attack(enemy=self.enemy))
        if player.Potion_Of_Life:
            moves.append(actions.Undead())
        moves.append(actions.ViewInventory())
        moves.append(actions.CheckHP())
        moves.append(actions.EquipWep())
        if player.HealingPotions > 0:
            moves.append(actions.Heal())
        if player.beer > 0:
            moves.append(actions.Drink())
        if player.Potion_Of_Life:
            moves.append(actions.Undead())
        return moves

class TreasureRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)

    def intro_text(self,player):
        return ''

    def modify_player(self,player):
        if not player.is_alive():
            print("Dead people can't unlock doors!")
            return
        elif player.keys >= 4:
            print("You slowly put each key into the corresponding lock. The padlock falls off and the door slowly creaks open...Before you sits more riches than you'll ever be able to spend. You are rich for life and fulfilled your quest! A winner is you!\n\n")
            print( "  ______   ______   .__   __.   _______ .______          ___   .___________. __    __   __          ___   .___________. __    ______   .__   __.      _______. __  \n /      | /  __  \  |  \ |  |  /  _____||   _  \        /   \  |           ||  |  |  | |  |        /   \  |           ||  |  /  __  \  |  \ |  |     /       ||  | \n|  ,----'|  |  |  | |   \|  | |  |  __  |  |_)  |      /  ^  \ `---|  |----`|  |  |  | |  |       /  ^  \ `---|  |----`|  | |  |  |  | |   \|  |    |   (----`|  | \n|  |     |  |  |  | |  . `  | |  | |_ | |      /      /  /_\  \    |  |     |  |  |  | |  |      /  /_\  \    |  |     |  | |  |  |  | |  . `  |     \   \    |  | \n|  `----.|  `--'  | |  |\   | |  |__| | |  |\  \----./  _____  \   |  |     |  `--'  | |  `----./  _____  \   |  |     |  | |  `--'  | |  |\   | .----)   |   |__| \n \______| \______/  |__| \__|  \______| | _| `._____/__/     \__\  |__|      \______/  |_______/__/     \__\  |__|     |__|  \______/  |__| \__| |_____   /" , end = '')
            print("   (__)")
            player.victory = True
        else:
            print("The padlock still looms in front of you, unmoving no matter how hard you stare at it. Your initial attempts at telekinesis have failed. Guess you better start looking for keys...\n")
            return

    def available_actions(self,player):
        moves = []
        moves.append(actions.MoveEast())
        moves.append(actions.ViewInventory())
        moves.append(actions.CheckHP())
        moves.append(actions.EquipWep())
        if player.Potion_Of_Life:
            moves.append(actions.Undead())
        if player.HealingPotions > 0:
            moves.append(actions.Heal())
        if player.beer > 0:
            moves.append(actions.Drink())
        return moves

class FireShieldRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.taken = False

    def intro_text(self,player):
        if not self.taken:
            return 'You walk into a fairly dark room, save for a glowing orange shield propped against the wall. A majestic flame has been painted on front. Obviously this shield is magic of some sort.'
        if self.taken:
            return "You walk into a fairly dark room. The orange shield has been taken."

    def modify_player(self,player):
        return


    def pick_up_item(self, player):
        if player.is_alive():
            fire_shield = items.FireShield()
            player.fire_shield = True
            player.inventory.append(fire_shield)
            self.taken = True
            print('Shield taken!')
        else:
            print("You are dead! You cannot grab it!")

    def available_actions(self,player):
        moves = super().available_actions(player)
        if not self.taken:
            moves.append(actions.PickUpItem())
        return moves

class CoinRoom(MapTile):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.taken = False

    def intro_text(self,player):
        if not self.taken:
            return 'You walk into a cave and notice someone has dropped a few coins! How lucky!'
        if self.taken:
            return "Now that the coins are gone, the cave is just dull."

    def modify_player(self,player):
        return


    def pick_up_item(self, player):
        if player.is_alive():
            coin_amount = random.randint(15,35)
            player.coin.add_coin(coin_amount)
            self.taken = True
            print('{} Coins added!'.format(str(coin_amount)))
        else:
            print("You are dead, what good is money to you now? Besides, you can't grab it.")

    def available_actions(self,player):
        moves = super().available_actions(player)
        if not self.taken:
            moves.append(actions.PickUpItem())
        return moves
