# Генератор технического задания

Небольшая программа для формирования типового технического задания в формате
Microsoft Word (`.docx`). Генератор работает на стандартной библиотеке Python и
не требует установки внешних зависимостей.

## Быстрый старт

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
