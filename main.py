
# Importing
from tkinter import Tk, Canvas

# GUI set-up
root = Tk()
c = Canvas(root, width=1800, height=900)
c.pack()
root.mainloop()


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


# Classes
class Player:
    def __init__(self):
        self.money = 0
        self.properties_list = []



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
        self.owner = player
        player.properties_list.append(self)
        player.money -= self.price



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
    
