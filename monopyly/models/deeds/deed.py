from typing import Optional

from monopyly.models.deeds.color_group import ColorGroup
from monopyly.models.player import Player



class PropertyDeed:
    ALLOWED_TYPES = [
        'street',
        'railroad',
        'utility'
    ]
    def __init__(
        self,
        color: 'ColorGroup',
        name: str,
        listed_price: int,
        base_rent: int,
        owner: Optional['Player'] = None,
        mortgaged: bool = False,
        mortgage_amount: int = 0,
        rent_history: Optional['RentHistory'] = None,
        development_allowed: bool = False,
        type_of_development_allowed: Optional[str] = None,
        immunity_tracker: Optional['ImmunityTracker'] = None
    ):
        self.__base_rent    = None
        self.__color        = None
        self.__listed_price = None
        self.__type         = None

        self.color = color
        self.name = name
        self.listed_price = listed_price
        self.owner = owner
        self.mortgaged = mortgaged
        self.mortgage_amount = mortgage_amount
        self._rent_history = rent_history or RentHistory()
        self.development_allowed = development_allowed
        self.type_of_development_allowed = type_of_development_allowed
        self.current_houses = 0
        self.current_hotels = 0
        self.immunity_tracker = immunity_tracker or ImmunityTracker()
        self.total_rent_collected_by_owner = 0
        self.total_rent_collected = 0
        self.total_revenue = 0
        self.last_purchase_price = 0

        self.base_rent = base_rent

    @property
    def base_rent(self):
        """
        Get the base rent for the property.

        Returns:
            int:
                The base rent for the property.
        """
        return self.__base_rent

    @base_rent.setter
    def base_rent(self, value: int):
        """
        Set the base rent for the property.

        Args:
            value (int): The base rent for the property.
        """
        if self.base_rent is not None:
            raise AttributeError("Base rent is already set and cannot be changed!")

        if not isinstance(value, int):
            raise ValueError("Base rent must be an integer.")

        self.__base_rent = value

    @property
    def development_allowed(self):
        """
        Check if development is allowed on the property.

        Returns:
            bool:
                - True:
                  Development is allowed on the property.
                - False:
                  Development is not allowed on the property.
        """
        return self.__development_allowed

    @property
    def mortgage_owed(self) -> int:
        """Calculate the mortgage owed (10% interest on mortgage amount)."""
        if not self.mortgage_amount:
            return 0
        return int(self.mortgage_amount + Decimal(self.mortgage_amount) * Decimal(0.1))

    @property
    def owner_has_monopoly(self) -> bool:
        """
        Check for monopoly ownership of the color group.

        Returns:
            bool:
                - True:
                  The owner owns all properties in the color group.
        """

    @property
    def rent_owed(self) -> int:
        """Calculate the rent owed based on development and immunity status."""
        if self.immunity_tracker.is_active():
            return 0
        base_rent = self._calculate_base_rent()
        self._rent_history.log(base_rent)
        return base_rent

    @property
    def deed_type(self) -> str:
        """Get the type of deed.

        Can be one of;
          - 'street',
          - 'railroad',
          - 'utility'

        """

    def _calculate_base_rent(self) -> int:
        """Private method to calculate the base rent."""
        base_rent = self.listed_price // 10  # Example calculation
        if self.current_houses > 0:
            base_rent += self.current_houses * (self.listed_price // 5)
        if self.current_hotels > 0:
            base_rent += self.current_hotels * (self.listed_price // 2)
        return base_rent

    def mortgage(self):
        """Mortgage the property."""
        if not self.mortgaged:
            self.mortgaged = True
            self.mortgage_amount = self.listed_price // 2

    def lift_mortgage(self):
        """Lift the mortgage on the property."""
        if self.mortgaged:
            self.mortgaged = False
            self.mortgage_amount = 0

    def collect_rent(self, amount: int):
        """Record rent collection."""
        self.total_rent_collected += amount
        if self.owner:
            self.total_rent_collected_by_owner += amount
        self.total_revenue += amount

    def develop(self, development_type: str):
        """Develop the property with houses or hotels."""
        if not self.development_allowed:
            raise ValueError("Development not allowed on this property.")
        if development_type not in ("house", "hotel"):
            raise ValueError("Invalid development type.")

        if development_type == "house" and self.type_of_development_allowed == "house":
            self.current_houses += 1
        elif development_type == "hotel" and self.type_of_development_allowed == "hotel":
            self.current_hotels += 1

    def transfer(self, new_owner: Player, price_paid: int = None):
        """Transfer ownership of the property."""

        if price_paid is None:
            price_paid = self.listed_price

        self.owner = new_owner
        self.last_purchase_price = self.listed_price

    def __str__(self):
        """String representation for debugging and display."""
        return (
            f"PropertyDeed(name={self.name}, owner={self.owner}, listed_price={self.listed_price}, "
            f"mortgaged={self.mortgaged}, rent_owed={self.rent_owed}, "
            f"houses={self.current_houses}, hotels={self.current_hotels})"
        )
