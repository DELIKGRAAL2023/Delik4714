# Reporting: справка для ЛР3

Записи операций превращаются в отчёт выбранной валюты. Строка отчёта может представлять одну операцию или группу операций.

Здесь перечислены типы текущей работы. Что требуется реализовать и какие файлы можно менять, указано в [TASK.md](TASK.md).

## Предметные объекты и исполнители

| Тип и конструктор | Публичные действия и свойства | Файл |
|---|---|---|
| `ReportBuilder()` | `build(records, currency)` | `app/domain/builders.py` |
| `TransactionHistoryReportBuilder()` | `build(records, currency)` | `app/domain/builders.py` |
| `DeclinedTransactionsReportBuilder()` | `build(records, currency)` | `app/domain/builders.py` |
| `TransactionRecord(transaction_id, customer_id, merchant_id, amount, status, timestamp)` | `transaction_id`, `customer_id`, `merchant_id`, `amount`, `status`, `timestamp` | `app/domain/reporting.py` |
| `Report(title, currency, rows)` | `title`, `currency`, `rows`, `approved_total` | `app/domain/reporting.py` |

Свойства читаются без скобок. Поля объекта-значения не меняются присваиванием; результат операции создаётся отдельно. Для наследника без собственного конструктора показаны аргументы конструктора базового класса.

## Вызов сервиса

| Метод | Сигнатура |
|---|---|
| `__init__` | `ReportingService(repository, builder)` |
| `record` | `record(record)` |
| `build` | `build(code)` |

`app/api.py` — готовая внешняя граница; не изменяйте её. Вызов попадает в сервис из указанного модуля. Подробные примеры создания входных объектов находятся в открытых тестах текущей папки.

Состав исполнителей в этой заготовке задан. Функция сборки уже готова; `app/services/assembly.py` не меняется. Задача — реализовать общий вызов и распределить поведение между указанными объектами.

## Готовые результаты и ошибки

`DomainError` находится в `app/support/errors.py`; код доступен через `error.code`. В разрешённых методах используйте готовые проверки, а не новую иерархию исключений.

`Money` хранит `Decimal` и валюту. Для учебных данных используются EUR и USD. Заданная сумма создаётся готовой `money("10", "EUR")`; арифметика выполняется готовыми методами Money. Курс и коэффициент не округляются как денежная сумма. В Account денежный модуль — `app/domain/money.py`, в остальных вариантах он предоставлен в `app/support/`.

## Проверка поведения

`tests/test_contract.py` и `tests/test_review_contract.py` проверяют предметные правила. `tests/test_progression.py` проверяет последовательности обращений и настройки текущей работы. Ни один результат теста не является командой менять защищённый API или тесты.

Ожидаемый стартовый результат — в [STARTER-STATE.md](STARTER-STATE.md). Проверка из корня проекта: `python check.py lab03`.
