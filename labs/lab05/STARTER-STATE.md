# Исходные проверки ЛР5

Успешных проверок: **6**. Ожидаемых падений: **9**.

Не завершены использование переданных зависимостей, сборка и основной путь операции. Проверки вызывают разные конфигурации и ошибающегося исполнителя; ошибка не должна превращаться в успешный результат или повторную операцию.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_extra_lab05`
- `tests.test_progression::test_progression_false_builder_error_preserves_records`
- `tests.test_progression::test_progression_report_currency_and_snapshot`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_builder_errors_do_not_change_records`
- `tests.test_contract::test_builder_is_used_and_results_do_not_accumulate`
- `tests.test_contract::test_duplicate_record_is_not_new_spending`
- `tests.test_contract::test_history_ignores_declines_in_total_and_other_currency`
- `tests.test_contract::test_new_repository_empty_with_explicit_currency`
- `tests.test_review_contract::test_review_builder_wrong_currency_is_not_accepted`

## Порядок проверки

Из корня проекта: `python check.py lab05`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
