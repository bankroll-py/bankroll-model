from typing import Any, Callable, Dict, Sequence, TypeVar, cast

try:
    import pandas  # type: ignore
except ImportError:
    pandas = None

from .activity import Activity, Trade
from .position import Position

_ConvertibleModel = TypeVar("_ConvertibleModel", Position, Activity)


def dataframeForModelObjects(items: Sequence[_ConvertibleModel]) -> pandas.DataFrame:
    assert pandas, "Pandas needs to be installed to use this function"

    if len(items) > 0:
        rows = [[fn(i) for fn in _dataframeColumnFunctions(i).values()] for i in items]
        columns = _dataframeColumnFunctions(items[0]).keys()
        return pandas.DataFrame(rows, columns=columns)
    else:
        return pandas.DataFrame()


def _dataframeColumnFunctions(
    model: _ConvertibleModel
) -> Dict[str, Callable[[_ConvertibleModel], Any]]:
    if isinstance(model, Position):
        return {
            "Instrument": lambda p: str(p.instrument),
            "Quantity": lambda p: p.quantity.normalize(),
            "Avg Price": lambda p: p.averagePrice,
        }

    elif isinstance(model, Trade):
        return {
            "Date": lambda t: t.date.date(),
            "Action": lambda t: cast(Trade, t).action,
            "Quantity": lambda t: abs(cast(Trade, t).quantity),
            "Instrument": lambda t: str(cast(Trade, t).instrument),
            "Amount": lambda t: cast(Trade, t).amount,
            "Fees": lambda t: cast(Trade, t).fees,
        }
    else:
        return {}
