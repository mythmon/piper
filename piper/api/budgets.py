from collections import defaultdict

from sqlalchemy.orm import joinedload

from piper import utils
from piper.api import blueprint, ModelView, register_model_view
from piper.models.budgets import Budget
from piper.models.transactions import Split, Transaction


@register_model_view(blueprint)
class BudgetView(ModelView):
    model = Budget


import q


@blueprint.route('/budget/audit')
@utils.with_db
def budget_audit(db):
    budgets = db.query(Budget).all()
    splits = (db.query(Split)
                .options(joinedload(Split.transaction))
                .all())

    matches = defaultdict(list)

    for b in budgets:
        for t in b.transactions:
            for s in t['splits']:
                matches[s['id']].append(b)

    results = {}
    for s in splits:
        if len(matches[s.id]) != 1:
            t = results.get(s.transaction.id)
            if t is None:
                results[s.transaction.id] = s.transaction.for_json()
                results[s.transaction.id]['splits'] = []
                t = results[s.transaction.id]
            serialized = s.for_json()
            serialized['budget_match'] = matches[s.id]
            t['splits'].append(serialized)

    return utils.json_response(results.values())