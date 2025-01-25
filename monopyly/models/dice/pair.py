from monopyly.models.dice.die import Die


class Pair:
    """
    A pair of dice.
    """
    def __init__(self, die_1: Die, die_2: Die):
        self.__die_1 = None
        self.__die_2 = None

        self.die_1 = die_1
        self.die_2 = die_2

        self.__roll_history = []

    @property
    def die_1(self) -> Die:
        return self.__die_1

    @die_1.setter
    def die_1(self, new: Die):

        if not isinstance(new, Die):
            raise ValueError('The die must be an instance of the Die class!')

        if self.die_2:
            if new.sides != self.die_2.sides:
                raise ValueError('Both dice must have the same number of sides!')

        self.__die_1 = new

    @property
    def die_2(self) -> Die:
        return self.__die_2

    @die_2.setter
    def die_2(self, new: Die):
        if not isinstance(new, Die):
            raise ValueError('The die must be an instance of the Die class!')

        if self.die_1:
            if new.sides != self.die_1.sides:
                raise ValueError('Both dice must have the same number of sides!')

        self.__die_2 = new

    @property
    def roll_count(self) -> int:
        return len(self.__roll_history)

    @property
    def roll_history(self) -> list[tuple[int, int]]:
        return self.__roll_history

    def roll(self):
        """
        Rolls the dice and records the result.

        Returns:
            tuple[int, tuple[int, int], bool]:
                The result comes in three parts:
                    - The total of the two dice.
                    - The individual results of the two dice.
                    - Whether the two dice are the same.

        Example:
            >>> pair = Pair(Die(), Die())
            >>> pair.roll()
            (7, (3, 4), False)
        """
        if not self.die_1 or not self.die_2:
            missing = []
            if not self.die_1:
                missing.append('die_1')
            if not self.die_2:
                missing.append('die_2')

            raise ValueError(f'Both dice must be set before rolling! Missing dice: {", ".join(missing)}')

        res_1 = self.die_1.roll()
        res_2 = self.die_2.roll()
        double = res_1 == res_2
        result = (res_1 + res_2, (res_1, res_2), double)
        self.__roll_history.append(result)

        return result

