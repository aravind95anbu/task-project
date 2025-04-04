from django.shortcuts import render, redirect
from .models import Account, Transaction
from decimal import Decimal
from django.contrib import messages


def home(request):
    accounts = Account.objects.all()
    return render(request, 'home.html', {'accounts': accounts})

def add_account(request):
    if request.method == 'POST':
        account_holder = request.POST['account_holder']
        account_number = request.POST['account_number']
        #address = request.POST['address']
        Account.objects.create(account_holder=account_holder, account_number=account_number)
        return redirect('home')
    return render(request, 'add_account.html')

def deposit(request):
    if request.method == 'POST':
        account_id = request.POST['account_id']
        amount = Decimal(request.POST['amount'])  
        account = Account.objects.get(id=account_id)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, transaction_type='Deposit', amount=amount)
        return redirect('home')
    accounts = Account.objects.all()
    return render(request, 'deposit.html', {'accounts': accounts})


def withdraw(request):
    if request.method == 'POST':
        account_id = request.POST['account_id']
        amount = Decimal(request.POST['amount'])  
        account = Account.objects.get(id=account_id)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, transaction_type='Withdrawal', amount=amount)
        return redirect('home')
    accounts = Account.objects.all()
    return render(request, 'withdraw.html', {'accounts': accounts})
'''

def transfer(request):
    if request.method == 'POST':
        from_account_id = request.POST['from_account_id']
        to_account_id = request.POST['to_account_id']
        amount = Decimal(request.POST['amount'])  

        from_account = Account.objects.get(id=from_account_id)
        to_account = Account.objects.get(id=to_account_id)

        if from_account.balance >= amount:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, transaction_type='Transfer', amount=amount, related_account=to_account)

        return redirect('home')
    
    accounts = Account.objects.all()
    return render(request, 'transfer.html', {'accounts': accounts})
'''

def transaction_history(request):
    transactions = Transaction.objects.all().order_by('-timestamp')
    return render(request, 'transaction_history.html', {'transactions': transactions})

def transfer(request):
    if request.method == 'POST':
        from_account_id = request.POST['from_account_id']
        to_account_id = request.POST['to_account_id']
        amount = Decimal(request.POST['amount'])

        if from_account_id == to_account_id:
            messages.error(request, "You cannot transfer money to the same account.")
            return redirect('transfer')

        from_account = Account.objects.get(id=from_account_id)
        to_account = Account.objects.get(id=to_account_id)

        if from_account.balance >= amount:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, transaction_type='Transfer', amount=amount, related_account=to_account)
        else:
            messages.error(request, "Insufficient balance for this transfer.")
        return redirect('home')

    accounts = Account.objects.all()
    return render(request, 'transfer.html', {'accounts': accounts})
