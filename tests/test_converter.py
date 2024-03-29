from hypothesis import assume, given, reproduce_failure, seed
from hypothesis.strategies import from_type, lists
import pandas as pd  # type: ignore
from typing import Iterable, List, Sequence
from tests import helpers

from bankroll.model import Position, Trade
from bankroll.model.converter import dataframeForModelObjects

import unittest


class TestModelConverter(unittest.TestCase):
    @given(lists(from_type(Trade)))
    def test_convertTrades(self, trades: List[Trade]) -> None:
        df: pd.DataFrame = dataframeForModelObjects(trades)
        self.assertEqual(len(df.index), len(trades))

        for i in range(len(trades)):
            self.assertEqual(df.at[i, "Date"], trades[i].date.date())
            self.assertEqual(df.at[i, "Action"], trades[i].action)
            self.assertEqual(df.at[i, "Quantity"], abs(trades[i].quantity))
            self.assertEqual(df.at[i, "Instrument"], str(trades[i].instrument))
            self.assertEqual(df.at[i, "Amount"], trades[i].amount)
            self.assertEqual(df.at[i, "Fees"], trades[i].fees)

    @given(lists(from_type(Position)))
    def test_convertPositions(self, positions: List[Position]) -> None:
        df: pd.DataFrame = dataframeForModelObjects(positions)
        self.assertEqual(len(df.index), len(positions))

        for i in range(len(positions)):
            self.assertEqual(df.at[i, "Instrument"], str(positions[i].instrument))
            self.assertEqual(df.at[i, "Quantity"], positions[i].quantity.normalize())
            self.assertEqual(df.at[i, "Avg Price"], positions[i].averagePrice)


if __name__ == "__main__":
    unittest.main()
