class Item():
    #Base class for all items
    def __init__(self,name,description, damage = 0):
        self.name = name
        self.description = description
        self.damage = damage

    def __str__(self):
        return "{}\n=====\n{}\nDamage: {}".format(self.name, self.description, self.damage)

    def sharpen(self):
        print("Can't be sharpened.")

class Sword(Item):
    def __init__(self):
        super().__init__(name = 'Sword', description = 'A standard short sword, not particularly sharp though...', damage = 10)

    def sharpen(self):
        print("{} sharpened!".format(self.name))
        self.name = "Sharp Sword"
        self.description = "A much sharper sword now"
        self.damage = 20
        super().__init__(self.name,self.description,self.damage)

class GreatSword(Item):
    def __init__(self):
        super().__init__(name = 'Great Sword', description = 'A heavy, tall sword, meant only for the strongest of warriors. Not particularly sharp though...', damage = 20)

    def sharpen(self):
        print("{} sharpened!".format(self.name))
        self.name = 'Sharp Great Sword'
        self.description = 'A much sharper great sword now.'
        self.damage = 30
        super().__init__(self.name,self.description,self.damage)

class Coin(Item):
    def __init__(self):
        self.amount_coin = 0
        super().__init__(name = 'Coins', description = 'The most powerful force in the world: money. Currently have ' + str(self.amount_coin), damage = 0)


    def add_coin(self, number):
        self.amount_coin = self.amount_coin + number
        super().__init__(name = 'Coins', description = 'The most powerful force in the world: money. Currently have ' + str(self.amount_coin), damage = 0)

    def __str__(self):
        super().__init__(name = 'Coins', description = 'The most powerful force in the world: money. Currently have ' + str(self.amount_coin), damage = 0)
        return "{}\n=====\n{}\nDamage: {}".format(self.name, self.description, self.damage)

class Fist(Item):
    def __init__(self):
        super().__init__(name = 'Fists', description = 'Your cold, bare hands.', damage = 3)

    def sharpen(self):
        print('Remind me again why you would want to sharpen your fists? Nonetheless, you try it, cut yourself, and lose a hitpoint.')
        return True

class HealingPotion(Item):
    def __init__(self):
        super().__init__(name = 'Healing potion', description = 'A potion that restores 50 health!' , damage = 1)

class PotionOfLife(Item):
    def __init__(self):
        super().__init__(name = 'Potion of Life', description = 'A potion that can do the impossible - bring the dead to life.' , damage = 1)

class WhiteKey(Item):
    def __init__(self):
        super().__init__(name = 'White Key', description = 'A dazzling white key used to unlock the Treasure Room' , damage = 1)

class GreenKey(Item):
    def __init__(self):
        super().__init__(name = 'Green Key', description = 'A gross green key that still has grease stains on it from its previous owner.' , damage = 1)

class Beer(Item):
    def __init__(self):
        super().__init__(name = 'Beer', description = 'A very, very, VERY stout drink meant for dwarves' , damage = 1)

class BlackKey(Item):
    def __init__(self):
        super().__init__(name = 'Black Key', description = 'A glossy black key that constantly softly vibrates. Something about it is very evil and powerful.' , damage = 1)

class BlueKey(Item):
    def __init__(self):
        super().__init__(name = 'Blue Key', description = 'A magical blue key that occasionally shoots a random bolt of lightning. Interesting.' , damage = 1)

class FireShield(Item):
    def __init__(self):
        super().__init__(name = 'Fire Shield', description = 'A magical shield that prevents damage from fire.' , damage = 1)
