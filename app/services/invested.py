from datetime import datetime


def invest_in_project(target, sources):
    in_db = []
    for source in sources:
        investment_amount = min(source.full_amount, target.full_amount)
        if investment_amount > 0:
            for obj, _ in [(target, source), (source, target)]:
                obj.invested_amount += investment_amount
                obj.full_amount -= investment_amount
                if obj.full_amount == 0:
                    obj.fully_invested = True
                    obj.close_date = datetime.utcnow()
                    in_db.append(obj)
    return in_db
