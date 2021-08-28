import datetime as dt


class Record:

    def __init__(self, amount: int, comment: str,
                 date: dt.date = None) -> None:
        self.amount = amount
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:

    def __init__(self, limit) -> None:
        self.records = []
        self.limit = limit

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> int:
        now = dt.datetime.now()
        amount: int = 0
        for i in self.records:
            if i.date == now.date():
                amount += i.amount
        return amount

    def get_week_stats(self) -> int:
        day_week_ago = dt.date.today() - dt.timedelta(days=7)
        today = dt.datetime.now().date()
        amount = 0
        for i in self.records:
            if day_week_ago <= i.date <= today:
                amount += i.amount
        return amount


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        result = self.limit - self.get_today_stats()
        if self.limit > self.get_today_stats():
            return f"Сегодня можно съесть что-нибудь ещё, \
но с общей калорийностью не более {result} кКал"
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE: float = 60.00
    EURO_RATE: float = 70.00

    def get_today_cash_remained(self, currency) -> str:
        day_result = 0
        local_limit = self.limit
        if currency == "usd":
            currency = "USD"
            local_limit = round(local_limit / self.USD_RATE, 2)
            day_result = round(self.get_today_stats() / self.USD_RATE, 2)
        elif currency == "eur":
            currency = "Euro"
            local_limit = round(local_limit / self.EURO_RATE, 2)
            print(local_limit)
            day_result = round(self.get_today_stats() / self.EURO_RATE, 2)
            print(day_result)
        elif currency == "rub":
            currency = "руб"
            day_result = round(self.get_today_stats(), 2)
        if (local_limit - day_result) == 0:
            return "Денег нет, держись"
        elif local_limit > day_result:
            return f"На сегодня осталось \
{local_limit - day_result} {currency}"
        elif local_limit < day_result:
            return f"Денег нет, держись: твой долг - \
{round(day_result - local_limit, 2)} {currency}"

# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('eur'))