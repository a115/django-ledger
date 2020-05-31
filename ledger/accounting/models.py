from decimal import Decimal
# from django_extensions.db.models import TimeStampedModel
from django_pgviews import view as pg
from django.db import models


# TODO: create and move to utils folders
def validate_positive_amount(value: Decimal) -> bool:
    return value >= Decimal(0)

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
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    timestamp = models.DateTimeField()
    entry = models.ForeignKey(Entries, primary_key=True, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[validate_positive_amount])

    sql = VIEW_SQL_ACCOUNT_LEDGER

    class Meta:
        managed = False
        db_table = 'account_ledgers_view'
