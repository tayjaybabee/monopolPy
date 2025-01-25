from monopyly.models.player import Player
from monopyly.models.deeds.deed import PropertyDeed


class DevelopmentRestriction:
    """
    A restriction on the development of a property.

    This could be a restriction on building houses or hotels, or a restriction on both.

    Properties:
        TYPES_OF_BARRING (list):
            A list of the types of development that can be restricted.
                - 'houses';
                    Restricts the building of houses.
                - 'hotels';
                    Restricts the building of hotels.
                - 'all';
                    Restricts the building of both houses and hotels.

        target_property (PropertyDeed):
            The property that is being restricted.

        favored_player (Player):
            The player that is favored by the restriction.

        barring (str):
            The type of development that is being restricted.

        turns (int):
            The number of turns that the restriction will last.

        reason (str):
            The reason for the restriction.
    """
    TYPES_OF_BARRING = ['all', 'houses', 'hotels']

    def __init__(
            self,
            target_deed:    PropertyDeed,
            turns:          int,
            favored_player: Player,
            barring:        str = 'all',
            turn_counter:   'TurnCounter' = None
    ):
        self.__barring = None
        self.__favored_player  = None
        self.__target_property = None
        self.__turn_counter    = None
        self.__total_turns     = None
        self.__turns_remaining           = None
        self.__turns_passed    = None

        self.favored_player  = favored_player
        self.target_property = target_deed
        self.__total_turns           = turns
        self.barring       = barring


        barring:        str = 'all'  # Houses, hotels, all
        turns:          int = 0
        reason:         str = None

    @property
    def active(self) -> bool:
        """
        Returns whether the restriction is active.

        If the restriction has a turn count, and it's greater than zero, the restriction is active.

        Returns:
             bool:
                True if the restriction is active, False otherwise.
        """
        if self.turns is not None and self.turns > 0:
            return True

        return False

    @property
    def barring(self) -> str:
        return self.__barring

    @property
    def barred_player(self) -> Player:
        if not self.target_property:
            raise ValueError("Target property is not set.")

        return self.target_property.owner

    @property
    def favored_player(self) -> Player:

        return self.__favored_player

    @favored_player.setter
    def favored_player(self, new):
        if self.__favored_player is not None:
            raise ValueError("Favored player is already set.")

        if not isinstance(new, Player):
            raise ValueError("Favored player must be a Player instance.")

        self.__favored_player = new

    @property
    def target_property(self) -> PropertyDeed:
        return self.__target_property

    @target_property.setter
    def target_property(self, new):
        if self.target_property is not None:
            raise ValueError("Target property is already set.")

        if not isinstance(new, PropertyDeed):
            raise ValueError("Target property must be a PropertyDeed instance.")

        self.__target_property = new

    @property
    def turn_counter(self) -> 'TurnCounter':
        return self.__turn_counter

    @turn_counter.setter
    def turn_counter(self, new: 'TurnCounter'):
        if self.__turn_counter:
            raise ValueError("Turn counter is already set.")

        if not isinstance(new, 'TurnCounter'):
            raise ValueError("Turn counter must be a TurnCounter instance.")

        self.__turn_counter = new

        self.register_with_turn_counter()
        
    @property
    def total_turns(self) ->int:
        return self.__total_turns

    @property
    def turns_remaining(self) -> int:
        return self.__turns_remaining

    def __decrement_turn(self):
        if self.turns_remaining > 0 and self.active:
            self.__turns_remaining -= 1
            self.__turns_passed += 1
            
    def process_turn(self, turn_counter: 'TurnCounter'):
        from monopyly.models.turns.counter import TurnCounter

        if not isinstance(turn_counter, TurnCounter):
            raise ValueError('"turn_counter" myst be a TurnCounter object')

        tc = turn_counter
        
        if self.active and tc.current_player is self.favored_player:
            self.__decrement_turn()

    def register_with_turn_counter(self):
        if not self.turn_counter:
            raise ValueError("Turn counter is not set.")

        self.turn_counter.register_restriction(self)
