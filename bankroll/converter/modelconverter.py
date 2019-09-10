from typing import Any, Callable, Dict, List, TypeVar

try:
    import pandas  # type: ignore
except ImportError:
    pandas = None

from bankroll.model import Position, Trade

_ConvertibleModel = TypeVar("_ConvertibleModel", Position, Trade)
_ColumnFunctions = Dict[str, Callable[[_ConvertibleModel], Any]]


def dataframeForModelObjects(items: List[_ConvertibleModel]) -> pandas.DataFrame:
    if pandas and len(items) > 0:
        rows = [[fn(i) for fn in dataframeColumnFunctions(i).values()] for i in items]
        columns = dataframeColumnFunctions(items[0]).keys()
        return pandas.DataFrame(rows, columns=columns)
    else:
        return pandas.DataFrame()


def dataframeColumnFunctions(model: _ConvertibleModel) -> _ColumnFunctions:
    if isinstance(model, Position):
        return {
            "Instrument": lambda p: str(p.instrument),
            "Quantity": lambda p: p.quantity.normalize(),
            "Avg Price": lambda p: p.averagePrice,
        }

    elif isinstance(model, Trade):
        return {
            "Date": lambda t: t.date.date(),
            "Action": lambda t: t.action,
            "Quantity": lambda t: abs(t.quantity),
            "Instrument": lambda t: str(t.instrument),
            "Amount": lambda t: t.amount,
            "Fees": lambda t: t.fees,
        }
    else:
        return {}
