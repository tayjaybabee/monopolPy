from datetime import datetime
from typing import Optional

from monopyly.models.player import Player


class Transaction:
    """Class representing a single financial transaction."""
    def __init__(self,
                 amount: int,
                 source: Optional['Player'],
                 destination: Optional['Player'],
                 description: str = ""):
        self.__settled_at = None

        self.amount = amount
        self.source = source
        self.destination = destination
        self.description = description
        self.__invoice_created_at = datetime.now()

    @property
    def description(self):
        return self.__description

    @property
    def invoice_created_at(self):
        return self.__invoice_created_at

    @property
    def pending(self):
        return not self.settled

    @property
    def settled(self):
        return self.settled_at is not None

    @property
    def settled_at(self):
        return self.__settled_at

    def commit(self):
        if self.amount and isinstance(self.destination, Player):
            self.source.cash -= self.amount
            self.destination.cash += self.amount
            self.__settled_at = datetime.now()

    def __str__(self):
        source_name = self.source.name if self.source else "Bank"
        destination_name = self.destination.name if self.destination else "Bank"
        return (
            f"[{self.timestamp}] {source_name} -> {destination_name}: {self.amount} ({self.description})"
        )

