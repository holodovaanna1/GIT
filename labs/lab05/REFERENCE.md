# Fraud: справка для ЛР5

Контекст содержит сумму, категорию магазина и число недавних попыток. Правила возвращают баллы; итоговый результат определяет ALLOW или DECLINE.

Здесь перечислены типы текущей работы. Что требуется реализовать и какие файлы можно менять, указано в [TASK.md](TASK.md).

## Предметные объекты и исполнители

| Тип и конструктор | Публичные действия и свойства | Файл |
|---|---|---|
| `LegacyRiskAdapter(legacy)` | `evaluate(context)` | `app/domain/adapters.py` |
| `FraudCheckContext(amount, merchant_category, recent_count=0)` | `amount`, `merchant_category`, `recent_count` | `app/domain/fraud.py` |
| `FraudResult(score, triggered_rules)` | `score`, `triggered_rules`, `decision` | `app/domain/fraud.py` |
| `FraudRule()` | `evaluate(context)` | `app/domain/risk_rules.py` |
| `LargeAmountRule()` | `evaluate(context)` | `app/domain/risk_rules.py` |
| `HighRiskMerchantRule()` | `evaluate(context)` | `app/domain/risk_rules.py` |

Свойства читаются без скобок. Поля объекта-значения не меняются присваиванием; результат операции создаётся отдельно. Для наследника без собственного конструктора показаны аргументы конструктора базового класса.

## Вызов сервиса

| Метод | Сигнатура |
|---|---|
| `__init__` | `FraudService(rules=())` |
| `check` | `check(context)` |
| `check_many` | `check_many(contexts)` |
| `highest_risk` | `highest_risk(contexts)` |

`app/api.py` — готовая внешняя граница; не изменяйте её. Вызов попадает в сервис из указанного модуля. Подробные примеры создания входных объектов находятся в открытых тестах текущей папки.

В `app/services/assembly.py` находятся стандартные конфигурации. Переданный объект сохраняется, а отсутствие обозначается `None`. Пустой список или словарь не равен отсутствию настройки. Копия контейнера не означает копирования исполнителей.

Сигнатура сборки: `build_service(rules=None)`.

## Готовые результаты и ошибки

`DomainError` находится в `app/support/errors.py`; код доступен через `error.code`. В разрешённых методах используйте готовые проверки, а не новую иерархию исключений.

`Money` хранит `Decimal` и валюту. Для учебных данных используются EUR и USD. Заданная сумма создаётся готовой `money("10", "EUR")`; арифметика выполняется готовыми методами Money. Курс и коэффициент не округляются как денежная сумма. В Account денежный модуль — `app/domain/money.py`, в остальных вариантах он предоставлен в `app/support/`.

## Проверка поведения

`tests/test_contract.py` и `tests/test_review_contract.py` проверяют предметные правила. `tests/test_progression.py` проверяет последовательности обращений и настройки текущей работы. Ни один результат теста не является командой менять защищённый API или тесты.

Ожидаемый стартовый результат — в [STARTER-STATE.md](STARTER-STATE.md). Проверка из корня проекта: `python check.py lab05`.
