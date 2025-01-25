import random
import numpy as np


class Die:
    def __init__(self, sides=6):
        self.__roll_history = []
        self.__sides = None

        self.sides = sides

    @property
    def average_roll(self):
        return sum(self.__roll_history) / len(self.__roll_history)

    @property
    def most_common_roll(self):
        return max(set(self.__roll_history), key=self.__roll_history.count)

    @property
    def roll_count(self):
        return len(self.__roll_history)

    @property
    def roll_history(self):
        return self.__roll_history

    @property
    def sides(self):
        return self.__sides

    @sides.setter
    def sides(self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except ValueError:
                raise TypeError('The number of sides must be an integer!')

        if value < 2:
            raise ValueError('A die must have at least two sides!')

        self.__sides = value

    def roll(self):
        #roll = random.randint(1, self.sides)
        roll = np.random.randint(1, 7)
        self.__roll_history.append(roll)

        return roll

    def number_of_rolls_with_value(self, value):
        return self.__roll_history.count(value)
