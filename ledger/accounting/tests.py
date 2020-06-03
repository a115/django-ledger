from decimal import Decimal
from datetime import datetime
from django.test import TestCase
from accounting.models import Account, Entries, AccountLedgers, AccountBalance
# Create your tests here.
class TestAccountBalance(TestCase):
    fixtures = [
        "accounts",
        "entries"
    ]

    def setUp(self):
        self.account_one = Account.objects.get(name="Account one")

    def test_account_ledgers_has_debit_and_credit(self):
        # The AccountLedgers model should have a debit and credit object
        # for each entry.
        entry_one = Entries.objects.get(description="Entry one")
        entry_one_debit_credit = AccountLedgers.objects.filter(account=self.account_one,
                                                               entry=entry_one)
        self.assertEqual(entry_one_debit_credit.count(), 2)
        entry_one_with_positive_amount = entry_one_debit_credit.get(amount__gt = Decimal(0.0))
        entry_one_with_negative_amount = entry_one_debit_credit.get(amount__lt = Decimal(0.0))
        self.assertEqual(entry_one_with_positive_amount.amount, Decimal("10.12"))
        self.assertEqual(entry_one_with_negative_amount.amount, Decimal("-10.12"))

        entry_two = Entries.objects.get(description="Entry two")
        entry_two_debit_credit = AccountLedgers.objects.filter(account=self.account_one,
                                                               entry=entry_two)
        self.assertEqual(entry_two_debit_credit.count(), 2)
        entry_two_with_positive_amount = entry_two_debit_credit.get(amount__gt = Decimal(0.0))
        entry_two_with_negative_amount = entry_two_debit_credit.get(amount__lt = Decimal(0.0))
        self.assertEqual(entry_two_with_positive_amount.amount, Decimal("0.01"))
        self.assertEqual(entry_two_with_negative_amount.amount, Decimal("-0.01"))

    def test_account_balance_is_zero(self):
        account_one_balance = AccountBalance.objects.get(timestamp='2020-06-02', account=self.account_one)
        self.assertEqual(account_one_balance.balance, Decimal("0.00"))

    def test_acount_balance_refresh_on_create_update_delete_entry(self):
        entries = Entries.objects.all()
        self.assertEqual(entries.count(), 2)
        # create one entry should refresh account balance
        entry_three = Entries.objects.create(description="entry three",
                                             amount=Decimal("10.12"),
                                             debit=self.account_one,
                                             credit=self.account_one)
        timestamp = datetime.date(datetime.now())
        account_balance = AccountBalance.objects.get(account=self.account_one,
                                                     timestamp=timestamp)
        # The balance on today day should be 0
        self.assertEqual(account_balance.balance, Decimal("0.00"))

        # update entry amount
        entry_three.amount = Decimal("15.12")
        entry_three.save()
        account_balance = AccountBalance.objects.get(account=self.account_one,
                                                     timestamp=timestamp)
        self.assertEqual(account_balance.balance, Decimal("0.00"))

        # delete entry
        entry_three.delete()
        entries = Entries.objects.all()
        self.assertEqual(entries.count(), 2)
        account_balances = AccountBalance.objects.all()
        self.assertEqual(account_balances.count(), 1)
        account_balance = account_balances.first()
        self.assertEqual(account_balance.balance, Decimal("0.00"))


    def test_account_balance_refresh_on_create_delete_an_account(self):
        account_balances = AccountBalance.objects.all()
        self.assertEqual(account_balances.count(), 1)
        # create one account create an account balance
        account_two = Account.objects.create(name="Account two")
        account_balances = AccountBalance.objects.all()
        self.assertEqual(account_balances.count(), 2)

        # The balance on a new account is 0.00
        account_balance_on_account_two = account_balances.get(account=account_two)
        self.assertEqual(account_balance_on_account_two.balance, Decimal("0.00"))

        # delete one account deletes the correspond account balance
        account_two.delete()
        account_balances= AccountBalance.objects.all()
        self.assertEqual(account_balances.count(), 1)

    def test_credit_other_account(self):
        account_two = Account.objects.create(name="Account Two")
        account_balance_on_account_two = AccountBalance.objects.get(account=account_two)
        # account one send money to account two
        Entries.objects.create(description="send money to account two",
                               amount=Decimal("1.23"),
                               debit=self.account_one,
                               credit=account_two)
        timestamp = datetime.date(datetime.now())
        # today there should be a balance of 1.23 for account two balance
        account_balance = AccountBalance.objects.get(account=account_two, timestamp=timestamp)
        self.assertEqual(account_balance.balance, Decimal("1.23"))
        # today there should be a balance of -1.23 for account one balance
        account_balance = AccountBalance.objects.get(account=self.account_one, timestamp=timestamp)
        self.assertEqual(account_balance.balance, Decimal("-1.23"))

    def test_for_each_entry_account_ledgers_has_debit_and_credit(self):
        entry_one = Entries.objects.get(description="Entry one")
        account_ledger_on_entry_one = AccountLedgers.objects.filter(entry=entry_one)
        self.assertEqual(account_ledger_on_entry_one.count(), 2)
        account_ledger_positive = account_ledger_on_entry_one.get(amount__gt=Decimal(0.00))
        account_ledger_negative = account_ledger_on_entry_one.get(amount__lt=Decimal(0.00))
        sum_positive_negative_amount = account_ledger_positive.amount + account_ledger_negative.amount
        self.assertEqual(sum_positive_negative_amount, Decimal(0.00))
