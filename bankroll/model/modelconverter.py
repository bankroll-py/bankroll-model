import pandas as pd
from typing import List

from bankroll.model import ConvertableModel, Position, Trade


class ModelConverter:
    @classmethod
    def dataframe(cls, items: List[ConvertableModel]) -> pd.DataFrame:
        if len(items) > 0:
            firstItem = items[0]
            assert all(isinstance(i, type(firstItem)) for i in items)
            rows = list(map(lambda t: t.dataframeValues(), items))
            return pd.DataFrame(rows, columns=firstItem.dataframeColumns())
        else:
            return pd.DataFrame()
