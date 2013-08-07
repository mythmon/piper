from piper.models.budgets import Budget
from piper.api import blueprint, ModelView, register_model_view


@register_model_view(blueprint)
class BudgetView(ModelView):
    model = Budget
