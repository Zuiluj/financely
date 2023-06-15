from django.contrib import admin

from finance.models import BankAccount, RecordType, Record

@admin.register(BankAccount)
class AccountAdmin(admin.ModelAdmin):
    model = BankAccount

    
@admin.register(RecordType)
class AccountAdmin(admin.ModelAdmin):
    model = RecordType

    
@admin.register(Record)
class AccountAdmin(admin.ModelAdmin):
    model = Record
