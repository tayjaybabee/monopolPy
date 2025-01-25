from typing import Optional

from monopyly.models.ledger.transactions.transaction import Transaction


class RentTransaction(Transaction):
    """Class representing a rent transaction."""
    def __init__(self,
                 amount: int,
                 source: Optional['Player'],
                 destination: Optional['Player'],
                 property_name: str,
                 description: str = "Rent Payment"):
        super().__init__(amount, source, destination, description)
        self.property_name = property_name

    def __str__(self):
        return f"{super().__str__()} for property: {self.property_name}"
