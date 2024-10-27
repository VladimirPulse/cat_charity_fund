from datetime import datetime


def invest_in_project(
        target=None,
        sources=None,
):
    in_db = []
    if not sources:
        return [target]
    if target.invested_amount is None:
        target.invested_amount = 0
    for source in sources:
        if source.full_amount <= target.full_amount:
            residual_amount = target.full_amount - source.full_amount
            target.full_amount = residual_amount
            source.invested_amount = source.full_amount
            target.invested_amount += source.full_amount
            source.full_amount = 0
            source.fully_invested = True
            source.close_date = datetime.utcnow()
            in_db.append(source)
        if target.full_amount == 0:
            target.fully_invested = True
            target.close_date = datetime.utcnow()
            in_db.append(target)
        else:
            residual_amount = source.full_amount - target.full_amount
            source.full_amount = residual_amount
            target.invested_amount = target.full_amount
            source.invested_amount += target.full_amount
            target.full_amount = 0
            target.fully_invested = True
            target.close_date = datetime.utcnow()
            in_db.append(source)
            in_db.append(target)
    return in_db
