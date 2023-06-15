from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json
import datetime
import pandas as pd

from finance.models import BankAccount, Record
from finance.forms import AccountForm, RecordForm, RecordTypeForm, DateRangeForm

@login_required
def dashboard_view(request):
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov',
        12: 'Dec'}
    total_earned = []
    total_spent = []
    total_months = []
    form = DateRangeForm(request.POST)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

    if start_date and end_date:
        dates = pd.date_range(start_date, end_date, freq='1M')
        index = 0
        for date in dates:
            if index == 0:
                month = start_date.month
                total_earned.append(Record.objects
                    .filter(date__date__range=(start_date, date))
                    .aggregate(Sum('income'))
                    .get('income__sum') 
                    or 0
                )
                total_spent.append(Record.objects
                    .filter(date__date__range=(start_date, date))
                    .aggregate(Sum('spend'))
                    .get('spend__sum') 
                    or 0
                )
            else:
                month = date.month
                total_earned.append(Record.objects
                    .filter(date__date__range=(last_end_date, date))
                    .aggregate(Sum('income'))
                    .get('income__sum') 
                    or 0
                )
                total_spent.append(Record.objects
                    .filter(date__date__range=(last_end_date, date))
                    .aggregate(Sum('spend'))
                    .get('spend__sum') 
                    or 0
                )
    
            index += 1
            last_end_date = date
            total_months.append(months.get(month))
        
            if index == len(dates):
                if not date.date() == end_date:
                    month = end_date.month
                    total_earned.append(Record.objects
                        .filter(date__date__range=(date, end_date))
                        .aggregate(Sum('income'))
                        .get('income__sum') 
                        or 0
                    )
                    total_spent.append(Record.objects
                        .filter(date__date__range=(date, end_date))
                        .aggregate(Sum('spend'))
                        .get('spend__sum') 
                        or 0
                    )
                    total_months.append(months.get(month))
            
        dashboard_data = {
            'labels': total_months,
            'datasets': [
                {
                    'label': 'Earned',
                    'backgroundColor': '#90CA77',
                    'data': total_earned
                },
                {
                    'label': 'Spent',
                    'backgroundColor': '#9E3B33',
                    'data': total_spent
                },
            ]
        }
    else:
        current_year = datetime.date.today().year
        for month_num, month in months.items():
            total_earned.append(Record.objects
                .filter(date__month=month_num, date__year=current_year)
                .aggregate(Sum('income'))
                .get('income__sum') 
                or 0
            )
            total_spent.append(Record.objects
                .filter(date__month=month_num, date__year=current_year)
                .aggregate(Sum('spend'))
                .get('spend__sum') 
                or 0
            )
            total_months.append(month)

        dashboard_data = {
            'labels': total_months,
            'datasets': [
                {
                    'label': 'Earned',
                    'backgroundColor': '#90CA77',
                    'data': total_earned
                },
                {
                    'label': 'Spent',
                    'backgroundColor': '#9E3B33',
                    'data': total_spent
                },
            ]
        }

    return render(request, 'finance/dashboard.html', context={
        'form': form,
        'dashboard_data': json.dumps(dashboard_data)
    })

@login_required
def accounts_view(request):
    accounts = BankAccount.objects.filter(user=request.user)
    context = {
        'accounts': accounts
    }
    if request.method == 'DELETE':
        # delete specified record
        print('delete account!')
    return render(request, 'finance/accounts.html', context=context)

@login_required 
def add_account_view(request):
    form = AccountForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        # context['form'] = AccountForm() # reset the form
        return redirect('/accounts')

    return render(request, 'finance/add_account.html', context={
        "form": form
    })

@login_required
def edit_account_view(request, acc_id):
    account = BankAccount.objects.get(id=acc_id)
    form = AccountForm(instance=account)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid(): 
            form.save()
            return redirect('/accounts')

    return render(request, 'finance/edit_account.html', context={
        "form": form,
        "error": form.errors
    })

@login_required
def account_records_view(request, acc_id):
    account = BankAccount.objects.get(id=acc_id)
    form = DateRangeForm(request.POST)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
    
    if start_date and end_date:
        records = Record.objects.filter(
            account=account,
            date__date__range=(start_date, end_date)
        ).order_by('-date')
    else:
        records = Record.objects.filter(account=account).order_by('-date')

    if request.method == 'DELETE':
        # delete specified record
        print('delete record!')

    return render(request, 'finance/account_records.html', context={
        "form": form,
        "account": account,
        "account_records": records
    })

@login_required
def add_record_view(request, acc_id):
    form = RecordForm(request.POST or None)
    account = BankAccount.objects.get(id=acc_id)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.account = account
        obj.save()
        # context['form'] = AccountForm() # reset the form
        return redirect(f'/accounts/{acc_id}/records')

    return render(request, 'finance/add_record.html', context={
        "form": form
    })

@login_required
def edit_record_view(request, acc_id, record_id):
    record = Record.objects.get(id=record_id)
    form = RecordForm(instance=record)
    
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect(f'/accounts/{acc_id}/records')

    return render(request, 'finance/edit_record.html', context={
        "form": form,
        "errors": form.errors
    })


@login_required
def add_record_type_view(request, acc_id):
    form = RecordTypeForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        # context['form'] = AccountForm() # reset the form
        return redirect(f'/accounts/{acc_id}/records')

    return render(request, 'finance/add_record_type.html', context={
        "form": form
    })
