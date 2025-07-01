from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone

class Category(models.Model):
    """Model for user-specific transaction categories"""
    INCOME = 'IN'
    EXPENSE = 'EX'
    
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
        
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)],
        help_text="Category name (e.g. Salary, Rent, Food)"
    )
    transaction_type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        help_text="Income or Expense category"
    )
    is_default = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('user', 'name', 'transaction_type')
        ordering = ['transaction_type', 'name']

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def create_default_categories(cls, user):
        """Create default income and expense categories for a new user."""
        default_categories = [
            
            ("Food", cls.EXPENSE),
            ("Rent", cls.EXPENSE),
            ("Utilities", cls.EXPENSE),
            ("Travel", cls.EXPENSE),
            ("Borrowed", cls.INCOME),  # <- Special
            ('wage', cls.INCOME)
            ('salary', cls.INCOME)
            ("Lend", cls.EXPENSE),  
        ]

        for name, category_type in default_categories:
            cls.objects.create(user=user, name=name, transaction_type=category_type,is_default=True)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Transaction amount"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="Select or create a category"
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional transaction description"
    )
    date = models.DateTimeField(default=timezone.now)
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    @property
    def transaction_type(self):
        """Derived from the category to maintain consistency"""
        return self.category.transaction_type

    def __str__(self):
        return f"{self.category.name}: {self.amount} ({self.date.date()})"