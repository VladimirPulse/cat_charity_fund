from datetime import datetime
from typing import List

from app.models.base_model import BaseModelCatFund


def invest_in_project(
        target: BaseModelCatFund,
        sources: List[BaseModelCatFund]
) -> List[BaseModelCatFund]:
    updated = []
    for source in sources:
        if target.fully_invested:
            break
        remaining_source = source.full_amount - source.invested_amount
        available_target = target.full_amount - target.invested_amount
        investment_amount = min(remaining_source, available_target)
        for obj in (target, source):
            obj.invested_amount += investment_amount
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()
                updated.append(obj)
        updated.append(obj)
    return updated
