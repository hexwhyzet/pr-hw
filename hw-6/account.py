import datetime
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Transaction:
    time: datetime.datetime
    diff: int
    balance: int


class AccountDraft1:
    balance: int = 0
    transactions: List[Transaction] = []

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

    def statement(self):
        pass


def test_deposit_false():
    acc = AccountDraft1()
    acc.deposit(100)
    assert acc.balance == 100


class AccountDraft2:
    balance: int = 0
    transactions: List[Transaction] = []

    def deposit(self, amount):
        assert amount > 0
        self.balance += amount
        self.transactions.append(Transaction(datetime.datetime.now(), amount, self.balance))

    def withdraw(self, amount):
        pass

    def statement(self):
        pass


def test_deposit_correct():
    acc = AccountDraft2()
    acc.deposit(100)
    assert acc.balance == 100


def test_withdraw_false():
    acc = AccountDraft2()
    acc.deposit(100)
    acc.withdraw(100)
    assert acc.balance == 0


class AccountDraft3:
    balance: int = 0
    transactions: List[Transaction] = []

    def deposit(self, amount):
        assert amount > 0
        self.balance += amount
        self.transactions.append(Transaction(datetime.datetime.now(), amount, self.balance))

    def withdraw(self, amount):
        assert amount > 0
        assert self.balance >= amount
        self.balance -= amount
        self.transactions.append(Transaction(datetime.datetime.now(), -amount, self.balance))

    def statement(self) -> str:
        pass


def test_withdraw_true():
    acc = AccountDraft3()
    acc.deposit(100)
    acc.withdraw(100)
    assert acc.balance == 0


def test_statement_false():
    acc = AccountDraft3()
    acc.deposit(100)
    acc.withdraw(50)
    acc.withdraw(50)

    statement_regex = r"Time\sAmount\sBalance\n" \
                      r"\d+.\d+.\d+\s\d+:\d+:\d+\s\+100\s100\n" \
                      r"\d+.\d+.\d+\s\d+:\d+:\d+\s\-50\s50\n" \
                      r"\d+.\d+.\d+\s\d+:\d+:\d+\s\-50\s0"

    assert re.match(statement_regex, acc.statement())


class AccountDraft4:
    balance: int = 0
    transactions: List[Transaction] = []

    def deposit(self, amount):
        assert amount > 0
        self.balance += amount
        self.transactions.append(Transaction(datetime.datetime.now(), amount, self.balance))

    def withdraw(self, amount):
        assert amount > 0
        assert self.balance >= amount
        self.balance -= amount
        self.transactions.append(Transaction(datetime.datetime.now(), -amount, self.balance))

    def statement(self) -> str:
        result = "Time\tAmount\tBalance"
        for transaction in self.transactions:
            result += f"\n{transaction.time.strftime('%Y.%m.%d %H:%M:%S')}\t{'+' if transaction.diff > 0 else ''}{transaction.diff}\t{transaction.balance}"
        return result


def test_statement_true():
    acc = AccountDraft4()
    acc.deposit(100)
    acc.withdraw(50)
    acc.withdraw(50)

    statement_regex = r"Time\sAmount\sBalance\n" \
                      r"\d+.\d+.\d+\s\d+:\d+:\d+\s\+100\s100\n" \
                      r"\d+.\d+.\d+\s\d+:\d+:\d+\s\-50\s50\n" \
                      r"\d+.\d+.\d+\s\d+:\d+:\d+\s\-50\s0"

    assert re.match(statement_regex, acc.statement())
