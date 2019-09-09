import pandas as pd
from typing import Any, Iterable, List, Optional, Sequence

from bankroll.model import BRModel, Position, Trade


def dataframeForModelObjects(items: Sequence[BRModel]) -> pd.DataFrame:
    rows: List[List[Any]] = []
    firstItem: Optional[BRModel] = None
    for i in items:
        if firstItem == None:
            firstItem = i
        else:
            assert type(firstItem) == type(i)

        rows.append(i.dataframeValues())

    if firstItem is not None:
        actualFirstItem: BRModel = firstItem
        return pd.DataFrame(rows, columns=actualFirstItem.dataframeColumns())
    else:
        return pd.DataFrame()
