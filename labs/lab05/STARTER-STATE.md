# Исходные проверки ЛР5

Успешных проверок: **12**. Ожидаемых падений: **17**.

Не завершены использование переданных зависимостей, сборка и основной путь операции. Проверки вызывают разные конфигурации и ошибающегося исполнителя; ошибка не должна превращаться в успешный результат или повторную операцию.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_dependency_error_then_success_does_not_accumulate`
- `tests.test_progression::test_progression_extra_lab05`
- `tests.test_progression::test_progression_risk_does_not_accumulate`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_dependency_error_not_allow`
- `tests.test_contract::test_existing_risk[100-GAMBLING-40-codes3]`
- `tests.test_contract::test_existing_risk[100-RESTAURANT-0-codes0]`
- `tests.test_contract::test_existing_risk[1000-RESTAURANT-0-codes1]`
- `tests.test_contract::test_existing_risk[1000.01-GAMBLING-80-codes4]`
- `tests.test_contract::test_existing_risk[1000.01-RESTAURANT-40-codes2]`
- `tests.test_contract::test_injection_copy_empty_and_capped_sum`
- `tests.test_contract::test_invalid_rule_result[-1]`
- `tests.test_contract::test_invalid_rule_result[1.5]`
- `tests.test_contract::test_invalid_rule_result[101]`
- `tests.test_contract::test_invalid_rule_result[True]`
- `tests.test_contract::test_rules_used_in_real_path`
- `tests.test_contract::test_safe_after_risky_and_context_unchanged`
- `tests.test_review_contract::test_review_all_contributions_are_evaluated_even_at_cap`

## Порядок проверки

Из корня проекта: `python check.py lab05`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
