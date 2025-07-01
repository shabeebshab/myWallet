from django import forms
from .models import Transaction, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TransactionForm(forms.ModelForm):
    def __init__(self, user, transaction_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = Category.objects.filter(user=user).exclude(name__startswith="Returned -")

        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type).exclude(name__startswith="Returned")

        self.fields['category'].queryset = queryset

    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Amount',
                'class': 'form-control'
            }),
            'description': forms.TextInput(attrs={
                'placeholder': 'Description',
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Category Name',
                'class': 'form-control'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-select'
            })
        }
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = ''
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {field_name.replace("1", "").replace("2", " again").capitalize()}'
            })

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']