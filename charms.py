from fun import spins
from fun import weight
from fun import Coin, Dice, Wheel, Card, Spinner
class Charm:
    def __init__(self, name, ability):
        self.name = name
        self.ability = ability
    def effect(self):
        return self.ability
def extra_spin():
    return spins + 1
Spare_Change = Charm("Spare Change", extra_spin)
def more_manifestation(Coin):
    return Coin(int(weight)) + 5
def more_manifestation(Wheel):
    return Wheel(int(weight)) + 5
def more_manifestation(Dice):
    return Dice(int(weight)) + 5
def more_manifestation(Card):
    return Card(int(weight)) + 5
def more_manifestation(Spinner):
    return Spinner(int(weight)) + 5
Money_Printer = Charm("Money Printer", more_manifestation(Coin))
Spare_Tires = Charm("Spare Tires", more_manifestation(Wheel))
Chancemaker = Charm("Chancemaker", more_manifestation(Dice))
Extra_Deck = Charm("Extra Deck", more_manifestation(Card))
ILoveTops = Charm("I Love Tops", more_manifestation(Spinner))