from decimal import Decimal
from django_pgviews import view as pg
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db import models

# TODO: create and move to utils folders
def validate_positive_amount(value: Decimal) -> bool:
    return value > Decimal(0)

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=256, null=False)

class Entries(models.Model):
    description = models.CharField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[validate_positive_amount])
    credit = models.ForeignKey(Account, related_name='credit', on_delete=models.PROTECT)
    debit  = models.ForeignKey(Account, related_name='debit', on_delete=models.PROTECT)

    class Meta:
        indexes = [models.Index(fields=['credit', 'debit'])]


VIEW_SQL_ACCOUNT_LEDGER ="""
	SELECT
		accounting_entries.credit_id AS account_id,
        accounting_entries.timestamp,
		accounting_entries.id AS entry_id,
		accounting_entries.amount
	FROM
		accounting_entries
	UNION ALL
	SELECT
		accounting_entries.debit_id,
        accounting_entries.timestamp,
		accounting_entries.id,
		(0.0 - accounting_entries.amount)
	FROM
		accounting_entries;
    """


class AccountLedgers(pg.View):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()
    entry = models.ForeignKey(Entries, primary_key=True, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[validate_positive_amount])

    sql = VIEW_SQL_ACCOUNT_LEDGER

    class Meta:
        managed = False
        db_table = 'account_ledgers_view'

VIEW_SQL_ACCOUNT_BALANCE = """
    SELECT
        account_id,
        tdate AS timestamp,
        sum(day_end) over (partition by account_id order by tdate asc) AS balance
    FROM (
        SELECT
            accounting_account.id as account_id,
            account_ledgers_view.timestamp::date as tdate,
            COALESCE(sum(account_ledgers_view.amount), 0.0) as day_end
        FROM
            accounting_account
            LEFT OUTER JOIN
            account_ledgers_view
            ON accounting_account.id = account_ledgers_view.account_id
        GROUP BY accounting_account.id, account_ledgers_view.timestamp::date
    ) AS daily_balances;
    """

class AccountBalance(pg.MaterializedView):
    concurrent_index = 'account_id, timestamp'
    account = models.ForeignKey(Account, primary_key=True, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    sql = VIEW_SQL_ACCOUNT_BALANCE

    class Meta:
        managed = False
        db_table = 'account_balances'

@receiver(post_save, sender=Entries)
def trigger_fix_balance_entries_on_save(sender, action=None, instance=None, **kwargs):
    AccountBalance.refresh()

@receiver(post_delete, sender=Entries)
def trigger_fix_balance_entries_on_delete(sender, action=None, instance=None, **kwargs):
    AccountBalance.refresh()

@receiver(post_save, sender=Account)
def trigger_fix_balance_accounts_on_save(sender, action=None, instance=None, **kwargs):
    AccountBalance.refresh()

@receiver(post_delete, sender=Account)
def trigger_fix_balance_accounts_on_delete(sender, action=None, instance=None, **kwargs):
    AccountBalance.refresh()
