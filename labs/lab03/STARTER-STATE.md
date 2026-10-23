# Исходные проверки ЛР3

Успешных проверок: **4**. Ожидаемых падений: **7**.

Не завершены общий интерфейс, алгоритмы исполнителей и основной метод сервиса. Поэтому один незаполненный метод может вызвать несколько падений — это не несколько независимых задач.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_report_currency_and_snapshot`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_abc_is_abstract`
- `tests.test_contract::test_duplicate_record_is_not_new_spending`
- `tests.test_contract::test_history_ignores_declines_in_total_and_other_currency`
- `tests.test_contract::test_new_repository_empty_with_explicit_currency`
- `tests.test_contract::test_two_builders_preserve_shape_and_order`
- `tests.test_review_contract::test_review_service_uses_builder_in_lab3`

## Порядок проверки

Из корня проекта: `python check.py lab03`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
