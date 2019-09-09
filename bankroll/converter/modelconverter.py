from typing import Any, Iterable, List, Optional, Sequence

try:
    import pandas as pd
except ImportError:
    pass

from bankroll.model import BRModel, Position, Trade


def dataframeForModelObjects(items: Sequence[BRModel]) -> Optional[pd.DataFrame]:
    df = None

    if module_exists("pandas"):
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
            df = pd.DataFrame(rows, columns=actualFirstItem.dataframeColumns())

    return df


def module_exists(module_name: str) -> bool:
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
