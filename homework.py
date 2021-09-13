import datetime as dt
from typing import Union


class Record:

    def __init__(
            self,
            amount: int,
            comment: str,
            date: Union[str, None] = None
    ) -> None:
        self.amount = amount
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:

    def __init__(self, limit) -> None:
        self.records = []
        self.limit = limit

    def result_limit_get_today_status(self):
        result = self.limit - self.get_today_stats()
        return result

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> int:
        now = dt.datetime.now().date()
        amount: int = 0
        for record in self.records:
            if record.date == now:
                amount += record.amount
        return amount

    def get_week_stats(self) -> int:
        day_week_ago = dt.date.today() - dt.timedelta(days=7)
        today = dt.datetime.now().date()
        amount = 0
        for record in self.records:
            if day_week_ago <= record.date <= today:
                amount += record.amount
        return amount


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        result = self.result_limit_get_today_status()
        if result > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, "
                    f"но с общей калорийностью не более "
                    f"{result} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE: float = 60.00
    EURO_RATE: float = 70.00
    RUB_RATE: float = 1.00
    money_dict = {
        "usd": ["USD", USD_RATE],
        "eur": ["Euro", EURO_RATE],
        "rub": ["руб", RUB_RATE],
    }

    def currency_is(self, currency):
        local_limit = round(self.limit / self.money_dict[currency][1], 2)
        day_result = round(self.get_today_stats() / self.money_dict[currency][1], 2)
        currency = self.money_dict[currency][0]
        result = (currency, local_limit, day_result)
        return result

    def get_today_cash_remained(self, currency) -> str:
        check_zero = round(self.result_limit_get_today_status(), 2)
        if check_zero == 0:
            return "Денег нет, держись"
        if currency == "usd":
            result = self.currency_is(currency)
        if currency == "eur":
            result = self.currency_is(currency)
        if currency == "rub":
            result = self.currency_is(currency)

        if result[1] > result[2]:
            remains = round(result[1] - result[2], 2)
            return (f"На сегодня осталось "
                    f"{remains} {result[0]}")
        if result[1] < result[2]:
            debt = round(result[2] - result[1], 2)
            return (f"Денег нет, держись: твой долг - "
                    f"{debt} {result[0]}")
