# Importing
from tkinter import Tk, Canvas
from random import randint, shuffle

# GUI set-up
root = Tk()
c = Canvas(root, width=1800, height=900)

# Variables
property_rents = \
    {
        "brown": [[2, 10, 30, 90, 160, 250], [4, 20, 60, 180, 320, 450]],
        "sky": [[6, 30, 90, 270, 400, 550], [6, 30, 90, 270, 400, 550], [8, 40, 100, 300, 450, 600]],
        "purple": [[10, 50, 150, 450, 625, 750], [10, 50, 150, 450, 625, 750], [12, 60, 180, 500, 700, 900]],
        "orange": [[14, 70, 200, 550, 750, 950], [14, 70, 200, 550, 750, 950], [16, 80, 220, 600, 800, 1000]],
        "red": [[18, 90, 250, 700, 875, 1050], [18, 90, 250, 700, 875, 1050], [20, 100, 300, 750, 925, 1200]],
        "yellow": [[22, 110, 330, 800, 975, 1275], [22, 110, 330, 800, 975, 1275], [24, 120, 360, 850, 1025, 1400]],
        "green": [[26, 130, 390, 900, 1100], [26, 130, 390, 900, 1100], [28, 150, 450, 1000, 1200]],
        "blue": [[35, 175, 500, 1100, 1300], [50, 200, 600, 1400, 1700]]
    }
place_list = []


# Functions

def player_acquisition_sequence(player, acquired_property, price):
    player.money -= price
    acquired_property.owner = player
    player.properties_list.append(acquired_property)


def move_players(player, index):
    player.index = index
    if player.index > 35:
        player.index -= 36
        player.money += 200
    place_list[player.index].visiting_sequence()


# Classes
class Player:
    def __init__(self):
        self.money = 1500
        self.properties_list = []
        self.railways_list = []
        self.utilities_list = []
        self.index = 0
        self.jail_time = 0
        self.latest_dice_roll = 0

    def go_to_jail(self):
        self.index = 10  # index for jail
        self.jail_time = 3

    def turn_sequence(self):
        self.index += randint(1, 6) + randint(1, 6)
        if self.jail_time > 0:
            self.jail_time -= 1
        else:
            turn__ = True
            double_rolls = 0
            while turn__:
                d1 = randint(1, 6)
                d2 = randint(1, 6)
                self.latest_dice_roll = d1 + d2
                if d1 == d2:
                    double_rolls += 1
                    if double_rolls == 3:
                        pass
                turn__ = False
                self.index += self.latest_dice_roll
                if self.index > 35:
                    self.index -= 36
                    self.money += 200
                place_list[self.index].visiting_sequence()


class Property:
    def __init__(self, name, price, rent, colour):
        self.name = name
        self.price = price
        self.colour = colour
        self.owner = None
        self.rent_list = rent
        self.rent = rent[0]
        self.houses = 0
        self.full_set = False

    def full_set_acquired(self):
        self.full_set = True
        self.update_rent()

    def update_rent(self):
        if self.full_set:
            if self.houses > 0:
                self.rent = self.rent_list[self.houses]
            else:
                self.rent = self.rent_list[0] * 2
        else:
            self.rent = self.rent_list[0]

    def acquired_by_player(self, player):
        player_acquisition_sequence(player, self, self.price)


class RailwayProperty:
    def __init__(self, name):
        self.name = name
        self.owner = None
        self.rent = 50

    def acquired_by_player(self, player):
        player_acquisition_sequence(player, self, 200)
        player.railways_list.append(self)
        self.update_rent()

    def update_rent(self):
        if not self.owner is None:
            self.rent = len(self.owner.railways_list) * 50


class UtilityProperty:
    def __init__(self, name):
        self.name = name
        self.rent_multiplier = 4
        self.rent_multiplier_list = [4, 10]
        self.rent = 0
        self.owner = None

    def acquired_by_player(self, player):
        player_acquisition_sequence(player, self, 150)
        player.utilities_list.append(self)
        self.update_rent()

    def update_rent(self):
        if not self.owner is None:
            self.rent_multiplier = self.rent_multiplier_list[len(self.owner.utilities_list)]


class PropertySet:
    def __init__(self, colour, length, property1, property2, property3=None):
        self.colour = colour
        self.property1 = property1
        self.property2 = property2
        self.property3 = property3
        self.length = length
        if length == 3:
            self.ownership_list = [property1.owner, property2.owner, property3.owner]
        else:
            self.ownership_list = [property1.owner, property2.owner]

    def check_ownership(self):
        if self.length == 3:
            if self.ownership_list[0] == self.ownership_list[1] and self.ownership_list[1] == self.ownership_list[2]:
                for x in self.ownership_list:
                    x.full_set_acquired()
        else:
            if self.ownership_list[0] == self.ownership_list[1]:
                for x in self.ownership_list:
                    x.full_set_acquired()


class Place:
    def __init__(self, index):
        self.index = index

    def visiting_sequence(self, player):
        raise NotImplementedError("Subclass must implement abstract method")


class TaxPlace(Place):
    def __init__(self, index, tax):
        super().__init__(index)
        self.tax = tax

    def visiting_sequence(self, player):
        player.money -= self.tax


class ChancePlace(Place):
    def __init__(self, index):
        super().__init__(index)
        self.chance_lists = [("", "am")]
        enumerate(self.chance_lists)
        shuffle(self.chance_lists)

    def visiting_sequence(self, player):
        picked_card = self.chance_lists.pop(0)
        self.chance_lists.append(picked_card)
        # card code stuff... will implement later


class PropertyPlace(Place):
    def __init__(self, index, linked_property):
        super().__init__(index)
        self.linked_property = linked_property

    def visiting_sequence(self, player):
        if self.linked_property.owner is None:
            acquire_property__ = None  # placeholder for figuring out whether player will buy or not... will implement with GUI
            if acquire_property__:
                self.linked_property.acquired_by_player(player)
            else:
                pass  # placeholder for auctions... will do later
        else:
            player.money -= self.linked_property.rent
            self.linked_property.owner.money += self.linked_property.rent


class UtilityPropertyPlace(Place):
    def __init__(self, index, linked_utility):
        super().__init__(index)
        self.linked_utility = linked_utility

    def visiting_sequence(self, player):
        if self.linked_utility.owner is None:
            acquire_property__ = None  # placeholder for figuring out whether player will buy or not... will implement with GUI
            if acquire_property__:
                self.linked_utility.acquired_by_player(player)
            else:
                pass  # placeholder for auctions... will do later
        else:
            player.money -= self.linked_utility.rent_multiplier * player.latest_dice_roll
            self.linked_utility.owner.money += self.linked_utility.rent_multiplier * player.latest_dice_roll


class GoToJailPlace(Place):
    def __init__(self, index):
        super().__init__(index)

    def visiting_sequence(self, player):
        player.go_to_jail()


class FreeParkingPlace(Place):
    def __init__(self, index):
        super().__init__(index)

    def visiting_sequence(self, player):
        pass  # This is not a placeholder... Nothing happens on free parking space! lol


class StartPlace(Place):
    def __init__(self, index):
        super().__init__(index)

    def visiting_sequence(self, player):
        pass  # No work needs to be done... the player glass gives the money itself


class JailPlace(Place):
    def __init__(self, index):
        super().__init__(index)

    def visiting_sequence(self, player):
        pass  # Nothing actually happens when you land on the jail space, it's just a place to keep tokens


c.pack()
root.mainloop()
