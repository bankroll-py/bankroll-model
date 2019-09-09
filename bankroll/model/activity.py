from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Flag, auto
from typing import Any, Dict, List, Optional

from .cash import Cash
from .brmodel import BRModel
from .instrument import Instrument, Stock
from .position import Position


@dataclass(frozen=True)
class Activity(BRModel):
    date: datetime

    @staticmethod
    def dataframeColumns() -> List[str]:
        pass

    def dataframeValues(self) -> List[Any]:
        pass


# Represents a cash payment, such as a stock dividend or bond interest, whether
# or not it was cashed out or reinvested.
@dataclass(frozen=True)
class CashPayment(Activity):
    instrument: Optional[Instrument]
    proceeds: Cash

    def __str__(self) -> str:
        return f'{self.date.date()} Cash payment   {self.instrument or "":21} {self.proceeds.paddedString(padding=10)}'


class TradeFlags(Flag):
    NONE = 0
    OPEN = auto()
    CLOSE = auto()

    DRIP = auto()  # Dividend reinvestment

    EXPIRED = auto()
    ASSIGNED_OR_EXERCISED = auto()  # Sign of quantity will indicate which
    LIQUIDATED = auto()


@dataclass(frozen=True)
class Trade(Activity):
    instrument: Instrument
    quantity: Decimal
    amount: Cash
    fees: Cash
    flags: TradeFlags

    @classmethod
    def quantizeQuantity(cls, quantity: Decimal) -> Decimal:
        return Position.quantizeQuantity(quantity)

    def __post_init__(self) -> None:
        if not self.quantity.is_finite():
            raise ValueError(f"Trade quantity {self.quantity} is not a finite number")

        if self.flags not in [
            TradeFlags.OPEN,
            TradeFlags.CLOSE,
            TradeFlags.OPEN | TradeFlags.DRIP,
            TradeFlags.OPEN | TradeFlags.ASSIGNED_OR_EXERCISED,
            TradeFlags.CLOSE | TradeFlags.EXPIRED,
            TradeFlags.CLOSE | TradeFlags.ASSIGNED_OR_EXERCISED,
            TradeFlags.CLOSE | TradeFlags.LIQUIDATED,
        ]:
            raise ValueError(f"Invalid combination of flags: {self.flags}")

        super().__setattr__("quantity", self.quantizeQuantity(self.quantity))

    @property
    def price(self) -> Cash:
        if self.quantity >= 0:
            return -self.amount / self.instrument.multiplier
        else:
            return self.amount / self.instrument.multiplier

    @property
    def proceeds(self) -> Cash:
        return self.amount - self.fees

    @property
    def action(self) -> str:
        if self.quantity > 0:
            action = "Buy"
        elif TradeFlags.LIQUIDATED in self.flags:
            action = "Sell-L"
        else:
            action = "Sell"

        return action

    @staticmethod
    def dataframeColumns() -> List[str]:
        return ["Date", "Action", "Quantity", "Instrument", "Amount", "Fees"]

    def dataframeValues(self) -> List[Any]:
        return [
            self.date.date(),
            self.action,
            abs(self.quantity),
            self.instrument,
            self.amount,
            self.fees,
        ]

    def __str__(self) -> str:
        return f"{self.date.date()} {self.action:6} {abs(self.quantity):>9} {self.instrument:21} {self.amount.paddedString(padding=10)} (before {self.fees.paddedString(padding=5)} in fees)"
