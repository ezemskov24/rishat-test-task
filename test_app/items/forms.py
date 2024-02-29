from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Форма создания заказа
    """
    class Meta:
        model = Order
        fields = ['items', 'user']
        widgets = {"items": forms.CheckboxSelectMultiple}
