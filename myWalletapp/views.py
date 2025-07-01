from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm
from django.utils import timezone
from .forms import CustomUserCreationForm


@login_required
def wallet_view(request):
    income = Transaction.objects.filter(
        user=request.user,
        category__transaction_type='IN'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    expense = Transaction.objects.filter(
        user=request.user,
        category__transaction_type='EX'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance = income - expense

    return render(request, 'wallet.html', {
        'balance': balance,
        'username': request.user.username,
    })



@login_required
def transaction_list(request):
    filter_type = request.GET.get('type')  # IN or EX
    transactions = Transaction.objects.filter(user=request.user).order_by('date')

    if filter_type in ['IN', 'EX']:
        transactions = transactions.filter(category__transaction_type=filter_type).order_by('-date')
        total = sum(t.amount for t in transactions)
        return render(request, 'transactions.html', {
            'transactions': transactions,
            'filter_type': filter_type,
            'total': total
        })
    else:
        balance = 0
        transactions_with_balance = []
        for txn in transactions:
            if txn.category.transaction_type == 'IN':
                balance += txn.amount
            else:
                balance -= txn.amount

            transactions_with_balance.append({
                'transaction': txn,
                'balance': balance
            })

        return render(request, 'transactions.html', {
            'transactions_with_balance': transactions_with_balance,
            'filter_type': None,
            'total': None
        })
def signup(request):
    if request.user.is_authenticated:
        return redirect('myWalletapp:wallet')  # already logged in, no duplicate signup

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Category.create_default_categories(user)
            return redirect('myWalletapp:wallet')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def add_transaction(request, *args, **kwargs):
    transaction_type = kwargs.get('transaction_type')  # IN or EX

    if request.method == 'POST':
        post_data = request.POST.copy()
        form = TransactionForm(request.user, transaction_type, post_data)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('myWalletapp:wallet')
        else:
            print("Form Errors:", form.errors)
    else:
        form = TransactionForm(request.user, transaction_type)

    return render(request, 'add_transaction.html', {
        'form': form,
        'transaction_type': transaction_type,
    })


@login_required
def add_category(request):
    transaction_type = request.GET.get('type')  # should be 'IN' or 'EX'

    if transaction_type not in ['IN', 'EX']:
        return redirect('myWalletapp:wallet')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            # Check for existing category with same name for same user and type
            exists = Category.objects.filter(
                user=request.user,
                name__iexact=name.strip(),  # case-insensitive
                transaction_type=transaction_type
            ).exists()
            if exists:
                form.add_error('name', 'This category already exists.')
            else:
                category = form.save(commit=False)
                category.user = request.user
                category.transaction_type = transaction_type
                category.save()
                if transaction_type == 'IN':
                    return redirect('myWalletapp:add_income')
                else:
                    return redirect('myWalletapp:add_expense')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {
        'form': form,
        'transaction_type': transaction_type,
    })



@login_required
def category_transactions(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    transactions = Transaction.objects.filter(
        user=request.user,
        category=category
    ).order_by('-date')
    
    return render(request, 'category_transactions.html', {
        'category': category,
        'transactions': transactions,
    })


@login_required
def credit_view(request):
    credit_categories = Category.objects.filter(user=request.user, name__in=['Borrowed', 'Lend'])
    credits = Transaction.objects.filter(user=request.user, category__in=credit_categories)

    return render(request, 'credit_view.html', {
        'credits': credits
    })

@login_required
def mark_as_returned(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if not txn.returned:
        txn.returned = True
        txn.return_date = timezone.now()
        txn.save()

        # Now auto-create opposite transaction
        auto_category_type = 'EX' if txn.category.transaction_type == 'IN' else 'IN'
        auto_category_name = f"Returned"

        auto_category, created = Category.objects.get_or_create(
            user=request.user,
            name=auto_category_name,
            transaction_type=auto_category_type
        )
        returned_description = f"{txn.description}"

        # Create the automatic transaction
        Transaction.objects.create(
            user=request.user,
            amount=txn.amount,
            category=auto_category,
            description=returned_description,
        )
    
    return redirect('myWalletapp:credit_view')