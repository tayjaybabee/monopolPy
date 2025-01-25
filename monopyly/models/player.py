

class Player:
    def __init__(self):
        self.__name          = None
        self.__token         = None
        self.__cash          = 0
        self.__real_estate   = []
        self.__immunities    = []
        self.__debt          = 0
        self.__special_cards = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if self.__name is None:
            if isinstance(name, str):
                self.__name = name
            else:
                raise TypeError(f"Name must be a string, not '{type(name)}'!")

        else:
            raise AttributeError("Player name is already set and cannot be changed!")

    @property
    def token(self) -> str:
        return self.__token

