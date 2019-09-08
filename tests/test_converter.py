from hypothesis import assume, given, reproduce_failure, seed
from hypothesis.strategies import from_type, lists
from typing import List
from tests import helpers

from bankroll.model import ConvertableModel, ModelConverter, Position, Trade

import unittest


class TestModelConverter(unittest.TestCase):
    @given(lists(from_type(Trade), min_size=3, max_size=3))
    def test_convertTrades(self, trades: List[Trade]) -> None:
        df = ModelConverter.dataframe(trades)
        self.assertEqual(len(df.index), len(trades))

        for i in range(len(trades)):
            self.assertEqual(df.at[i, "Date"], trades[i].date.date())
            self.assertEqual(df.at[i, "Action"], trades[i].action)
            self.assertEqual(df.at[i, "Quantity"], abs(trades[i].quantity))
            self.assertEqual(df.at[i, "Instrument"], trades[i].instrument)
            self.assertEqual(df.at[i, "Amount"], trades[i].amount)
            self.assertEqual(df.at[i, "Fees"], trades[i].fees)

    @given(lists(from_type(Position), min_size=3, max_size=3))
    def test_convertPositions(self, positions: List[Position]) -> None:
        df = ModelConverter.dataframe(positions)
        self.assertEqual(len(df.index), len(positions))

        for i in range(len(positions)):
            self.assertEqual(df.at[i, "Instrument"], positions[i].instrument)
            self.assertEqual(df.at[i, "Quantity"], positions[i].quantity.normalize())
            self.assertEqual(df.at[i, "Avg Price"], positions[i].averagePrice)


if __name__ == "__main__":
    unittest.main()
