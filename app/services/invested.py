from datetime import datetime

from app.models.base_model import BaseModelCatFund


def invest_in_project(
        target: BaseModelCatFund,
        sources: list[BaseModelCatFund]
) -> list[BaseModelCatFund]:
    updated = []
    for source in sources:
        investment_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += investment_amount
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()
        updated.append(source)
        if target.fully_invested:
            break
    return updated
