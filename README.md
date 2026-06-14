# Генератор технического задания

Небольшая программа для формирования типового технического задания в формате
Microsoft Word (`.docx`). Генератор работает на стандартной библиотеке Python и
не требует установки внешних зависимостей.

## Быстрый старт

Открыть пользовательское окно:

```bash
python3 tech_assignment_gui.py
```

Для окна нужен стандартный модуль Tkinter. В Windows и macOS он обычно входит в
Python. В некоторых Linux-системах его нужно установить отдельным системным
пакетом, например `python3-tk` для Debian/Ubuntu.

В окне можно:

1. выбрать типовое решение из SQLite-базы;
2. заполнить данные проекта, заказчика и исполнителя;
3. отредактировать разделы технического задания;
4. выбрать путь сохранения и сформировать Word-файл.

Командная строка также остается доступной.

Создать документ с данными по умолчанию:

```bash
python3 tech_assignment_generator.py --output technical_assignment.docx
```

Создать пример JSON-конфигурации:

```bash
python3 tech_assignment_generator.py --init-sample examples/project_data.json
```

Сформировать Word-файл из JSON-конфигурации:

```bash
python3 tech_assignment_generator.py \
  --config examples/project_data.json \
  --output examples/technical_assignment_example.docx
```

## База типовых решений

Типовые решения хранятся в SQLite-базе. По умолчанию используется файл
`tech_assignment_solutions.db` в текущем каталоге. Если файла нет, программа
создаст его автоматически и заполнит начальными вариантами.

Создать или обновить базу решений:

```bash
python3 tech_assignment_generator.py --init-db
```

Пересоздать базу решений с начальными данными:

```bash
python3 tech_assignment_generator.py --reset-db
```

Посмотреть доступные решения:

```bash
python3 tech_assignment_generator.py --list-solutions
```

Сформировать ТЗ по выбранному решению:

```bash
python3 tech_assignment_generator.py \
  --solution-id crm \
  --output crm_technical_assignment.docx
```

Можно указать свой путь к базе:

```bash
python3 tech_assignment_generator.py \
  --db data/solutions.db \
  --list-solutions
```

Предзаполненные решения:

- `request-management` — система учета заявок;
- `crm` — CRM для отдела продаж;
- `online-store` — интернет-магазин;
- `document-workflow` — электронный документооборот;
- `analytics-dashboard` — аналитическая панель.

Если одновременно указаны `--solution-id` и `--config`, данные из JSON-файла
переопределяют значения выбранного типового решения.

## Настройка данных

В JSON-файле можно переопределить основные поля:

- `project_name` — название проекта;
- `customer` — заказчик;
- `contractor` — исполнитель;
- `version` — версия документа;
- `document_date` — дата документа;
- `basis` — основание для разработки;
- `purpose` — назначение системы;
- `scope` — состав и объем работ;
- `platform` — целевая платформа;
- `support_period` — срок гарантийного сопровождения.

Раздел `sections` позволяет заменить текст стандартных разделов. Значение
каждого раздела может быть строкой или списком строк:

```json
{
  "project_name": "CRM для отдела продаж",
  "sections": {
    "functional_requirements": [
      "Система должна вести карточки клиентов.",
      "Система должна формировать отчет по сделкам."
    ]
  }
}
```

Доступные идентификаторы разделов:

- `general`
- `purpose`
- `scope`
- `functional_requirements`
- `non_functional_requirements`
- `acceptance`
- `documentation`
- `support`

## Пример

В каталоге `examples/` находится пример входных данных
`project_data.json` и сгенерированный Word-файл
`technical_assignment_example.docx`.

## Файлы проекта

- `tech_assignment_gui.py` — окно пользователя для ввода данных и генерации ТЗ;
- `tech_assignment_generator.py` — CLI и DOCX-генератор;
- `solution_catalog.py` — SQLite-каталог типовых решений;
- `examples/project_data.json` — пример входных данных;
- `examples/technical_assignment_example.docx` — пример готового Word-файла.
