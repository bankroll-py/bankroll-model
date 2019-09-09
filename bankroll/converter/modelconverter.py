from typing import Any, Callable, cast, List, Optional, Sequence, Tuple, Union

try:
    import pandas as pd
except ImportError:
    pass

from bankroll.model import Position, Trade

ConvertibleModel = Union[Position, Trade]
ColumnFunctions = List[Tuple[str, Callable[[Any], Any]]]


def dataframeForModelObjects(
    items: Sequence[ConvertibleModel]
) -> Optional[pd.DataFrame]:
    df = None

    if module_exists("pandas"):
        rows: List[List[Any]] = []
        firstItem: Optional[ConvertibleModel] = None
        for i in items:
            if firstItem == None:
                firstItem = i
            else:
                assert type(firstItem) == type(i)

            rows.append([t[1](i) for t in dataframeColumnFunctions(i)])

        if firstItem is not None:
            actualFirstItem: ConvertibleModel = firstItem
            columns = [t[0] for t in dataframeColumnFunctions(actualFirstItem)]
            df = pd.DataFrame(rows, columns=columns)

    return df


def dataframeColumnFunctions(model: ConvertibleModel) -> ColumnFunctions:
    if isinstance(model, Position):
        posInstrument: Callable[[Position], Any] = lambda p: str(p.instrument)
        posQuantity: Callable[[Position], Any] = lambda p: p.quantity.normalize()
        posAveragePrice: Callable[[Position], Any] = lambda p: p.averagePrice
        return [
            ("Instrument", posInstrument),
            ("Quantity", posQuantity),
            ("Avg Price", posAveragePrice),
        ]

    elif isinstance(model, Trade):
        tradeDate: Callable[[Trade], Any] = lambda t: t.date.date()
        tradeAction: Callable[[Trade], Any] = lambda t: t.action
        tradeQuantity: Callable[[Trade], Any] = lambda t: abs(t.quantity)
        tradeInstrument: Callable[[Trade], Any] = lambda t: str(t.instrument)
        tradeAmount: Callable[[Trade], Any] = lambda t: t.amount
        tradeFees: Callable[[Trade], Any] = lambda t: t.fees
        return [
            ("Date", tradeDate),
            ("Action", tradeAction),
            ("Quantity", tradeQuantity),
            ("Instrument", tradeInstrument),
            ("Amount", tradeAmount),
            ("Fees", tradeFees),
        ]

    return []


def module_exists(module_name: str) -> bool:
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
