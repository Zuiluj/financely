from django.db import models
from django.utils import timezone
from crum import get_current_user
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        # alternative to `auto_now()`
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)


class BankAccount(BaseModel):
    DEBIT = 'debit'
    CASH = 'cash'
    CREDIT = 'credit'
    ACCOUNT_TYPES =[
        (DEBIT, "Debit"),
        (CASH, "Cash"),
        (CREDIT, "Credit")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=ACCOUNT_TYPES, default=DEBIT)
    desc = models.CharField(max_length=200, null=True, blank=True)

    @property
    def balance(self):
        all_income = self.account_records.aggregate(models.Sum('income')).get('income__sum') or 0
        all_spend = self.account_records.aggregate(models.Sum('spend')).get('spend__sum') or 0
        return all_income - all_spend


class RecordType(BaseModel):
    # Serves as "tag" for records
    name = models.CharField(max_length=200)
    color =  models.CharField(max_length=7) # hexadecimal

    def __str__(self):
        return self.name


class Record(BaseModel):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='account_records')
    name = models.CharField(max_length=200, default='Record')
    spend = models.FloatField(default=0, blank=True, null=True)
    income = models.FloatField(default=0, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    type = models.ManyToManyField(RecordType, blank=True)
    date = models.DateTimeField(default=timezone.now)
