from piper.models.transactions import Transaction, Split, Category
from piper.api import blueprint, ModelView, register_model_view


@register_model_view(blueprint)
class TransactionView(ModelView):
    model = Transaction


@register_model_view(blueprint)
class CategoryView(ModelView):
    model = Category


@register_model_view(blueprint)
class SplitView(ModelView):
    model = Split
