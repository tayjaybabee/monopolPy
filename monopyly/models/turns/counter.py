from monopyly.models.player import Player
from monopyly.utils.metaclass import Singleton
from monopyly.models.restrictions.development.base import DevelopmentRestriction


class TurnCounter(metaclass=Singleton):

    __players: list[Player]
    __development_restrictions: list[DevelopmentRestriction]


    def __init__(self, players: list[Player]):
        self.__bankrupt_players = {}
        self.__current_turn     = 0
        self.__players          = None
        self.__total_turns      = 0

        self.players = players

    @property
    def bankrupt_players(self):
        return self.__bankrupt_players

    @property
    def current_turn(self):
        return self.__current_turn

    @property
    def current_player(self):
        if not self.players:
            raise ValueError("Cannot get current player without players.")

        return self.players[self.current_turn]

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, new):
        if self.players:
            raise ValueError("Cannot reset players after they have been set.")

        self.__players = new

    @property
    def registered_restrictions(self) -> list[DevelopmentRestriction]:
        return self.__development_restrictions

    @property
    def total_turns(self):
        return self.__total_turns

    def bankrupt_player(self, player: Player):
        if player not in self.players:
            raise ValueError("Player is not in the game.")

        self.players.remove(player)
        self.__bankrupt_players[player.name] = self.total_turns

    def next_turn(self):
        if not self.players or len(self.players) <= 1:
            raise ValueError("Cannot proceed to next turn without two players or more.")

        for restriction in self.registered_restrictions:
            restriction.process_turn(self)

        self.__current_turn = (self.current_turn + 1) % len(self.players)
        if self.current_turn == 0:
            self.__total_turns += 1

    def register_restriction(self, restriction: DevelopmentRestriction):
        if restriction not in self.registered_restrictions:
            if not isinstance(restriction, DevelopmentRestriction):
                raise ValueError('Invalid restriction type.')

            self.__development_restrictions.append(restriction)


    def reset(self):
        self.__bankrupt_players = {}
        self.__current_turn     = 0
        self.__total_turns      = 0
