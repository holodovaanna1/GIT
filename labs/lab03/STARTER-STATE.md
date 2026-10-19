# Исходные проверки ЛР3

Успешных проверок: **10**. Ожидаемых падений: **10**.

Не завершены общий интерфейс, алгоритмы исполнителей и основной метод сервиса. Поэтому один незаполненный метод может вызвать несколько падений — это не несколько независимых задач.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_risk_does_not_accumulate`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_abc_is_abstract`
- `tests.test_contract::test_existing_risk[100-GAMBLING-40-codes3]`
- `tests.test_contract::test_existing_risk[100-RESTAURANT-0-codes0]`
- `tests.test_contract::test_existing_risk[1000-RESTAURANT-0-codes1]`
- `tests.test_contract::test_existing_risk[1000.01-GAMBLING-80-codes4]`
- `tests.test_contract::test_existing_risk[1000.01-RESTAURANT-40-codes2]`
- `tests.test_contract::test_rule_contributions`
- `tests.test_contract::test_rules_used_in_real_path`
- `tests.test_contract::test_safe_after_risky_and_context_unchanged`

## Порядок проверки

Из корня проекта: `python check.py lab03`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
