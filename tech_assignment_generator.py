#!/usr/bin/env python3
"""Generate a typical technical assignment document in DOCX format."""

from __future__ import annotations

import argparse
import copy
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from xml.sax.saxutils import escape


DEFAULT_DATA: dict[str, Any] = {
    "project_name": "Информационная система учета заявок",
    "customer": "ООО \"Заказчик\"",
    "contractor": "ООО \"Исполнитель\"",
    "version": "1.0",
    "document_date": datetime.now().strftime("%d.%m.%Y"),
    "basis": "Договор на разработку программного обеспечения",
    "purpose": (
        "Автоматизация приема, обработки и контроля исполнения заявок "
        "пользователей."
    ),
    "scope": (
        "Разработка веб-приложения, пользовательской документации и "
        "комплекта эксплуатационных материалов."
    ),
    "platform": "Веб-приложение, доступное через современные браузеры",
    "support_period": "12 месяцев с даты приемки",
    "sections": {},
}


DEFAULT_SECTIONS: list[dict[str, Any]] = [
    {
        "id": "general",
        "title": "1. Общие сведения",
        "paragraphs": [
            "Наименование работ: разработка проекта \"{project_name}\".",
            "Заказчик: {customer}.",
            "Исполнитель: {contractor}.",
            "Основание для разработки: {basis}.",
        ],
    },
    {
        "id": "purpose",
        "title": "2. Назначение и цели создания",
        "paragraphs": [
            "Назначение системы: {purpose}",
            (
                "Целью работ является создание решения, которое снижает "
                "трудозатраты сотрудников, повышает прозрачность процессов "
                "и обеспечивает контроль сроков исполнения."
            ),
        ],
    },
    {
        "id": "scope",
        "title": "3. Состав и объем работ",
        "paragraphs": [
            "{scope}",
            "В состав работ входят обследование, проектирование, разработка, тестирование, внедрение и передача документации.",
        ],
    },
    {
        "id": "functional_requirements",
        "title": "4. Функциональные требования",
        "paragraphs": [
            "Система должна обеспечивать регистрацию и авторизацию пользователей.",
            "Система должна поддерживать создание, редактирование, поиск и закрытие заявок.",
            "Система должна предоставлять роли пользователей с разграничением прав доступа.",
            "Система должна формировать отчеты по статусам, исполнителям и срокам выполнения.",
        ],
    },
    {
        "id": "non_functional_requirements",
        "title": "5. Нефункциональные требования",
        "paragraphs": [
            "Интерфейс должен быть доступен через {platform}.",
            "Система должна сохранять работоспособность при типовой нагрузке, согласованной с заказчиком.",
            "Данные пользователей и заявок должны храниться с учетом требований конфиденциальности.",
            "Решение должно предусматривать резервное копирование и восстановление данных.",
        ],
    },
    {
        "id": "acceptance",
        "title": "6. Порядок контроля и приемки",
        "paragraphs": [
            "Приемка выполняется на основании демонстрации реализованных функций и результатов тестирования.",
            "Замечания фиксируются в реестре, согласуются сторонами и устраняются исполнителем.",
            "Результатом приемки является подписанный акт сдачи-приемки работ.",
        ],
    },
    {
        "id": "documentation",
        "title": "7. Документация",
        "paragraphs": [
            "Исполнитель передает заказчику руководство пользователя, инструкцию администратора и описание состава поставки.",
            "Документация предоставляется в электронном виде.",
        ],
    },
    {
        "id": "support",
        "title": "8. Гарантийное сопровождение",
        "paragraphs": [
            "Срок гарантийного сопровождения: {support_period}.",
            "В рамках сопровождения исполнитель устраняет ошибки, выявленные при штатной эксплуатации системы.",
        ],
    },
]


def xml_escape(value: Any) -> str:
    """Escape a value for XML text nodes and attributes."""
    return escape(str(value), {'"': "&quot;"})


class SafeFormatDict(dict[str, Any]):
    """Keep unknown placeholders visible instead of failing generation."""

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def normalize_paragraphs(value: Any, *, field_name: str) -> list[str]:
    if isinstance(value, str):
        return [value]

    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value

    raise ValueError(
        f"Field '{field_name}' must be a string or a list of strings."
    )


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as config_file:
        data = json.load(config_file)

    if not isinstance(data, dict):
        raise ValueError("Configuration root must be a JSON object.")

    return data


def merge_data(custom_data: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(DEFAULT_DATA)
    custom_sections = custom_data.pop("sections", None)
    data.update(custom_data)

    if custom_sections is not None:
        if not isinstance(custom_sections, dict):
            raise ValueError("Field 'sections' must be a JSON object.")
        data["sections"] = custom_sections

    return data


def render_template(text: str, data: dict[str, Any]) -> str:
    return text.format_map(SafeFormatDict(data))


def paragraph(
    text: str = "",
    *,
    style: str | None = None,
    align: str | None = None,
    bold: bool = False,
) -> str:
    if text == "":
        return "<w:p/>"

    properties: list[str] = []
    if style:
        properties.append(f'<w:pStyle w:val="{xml_escape(style)}"/>')
    if align:
        properties.append(f'<w:jc w:val="{xml_escape(align)}"/>')

    paragraph_properties = (
        f"<w:pPr>{''.join(properties)}</w:pPr>" if properties else ""
    )
    run_properties = "<w:rPr><w:b/></w:rPr>" if bold else ""
    text_node = f'<w:t xml:space="preserve">{xml_escape(text)}</w:t>'

    return f"<w:p>{paragraph_properties}<w:r>{run_properties}{text_node}</w:r></w:p>"


def cell(text: str) -> str:
    return (
        '<w:tc><w:tcPr><w:tcW w:w="4500" w:type="dxa"/></w:tcPr>'
        f"{paragraph(text)}</w:tc>"
    )


def metadata_table(rows: Iterable[tuple[str, str]]) -> str:
    table_rows = []
    for label, value in rows:
        table_rows.append(f"<w:tr>{cell(label)}{cell(value)}</w:tr>")

    return (
        "<w:tbl>"
        "<w:tblPr>"
        '<w:tblW w:w="0" w:type="auto"/>'
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        "</w:tblBorders>"
        "</w:tblPr>"
        f"{''.join(table_rows)}"
        "</w:tbl>"
    )


def section_paragraphs(section: dict[str, Any], data: dict[str, Any]) -> list[str]:
    section_id = section["id"]
    override = data.get("sections", {}).get(section_id)
    paragraphs = (
        normalize_paragraphs(override, field_name=f"sections.{section_id}")
        if override is not None
        else section["paragraphs"]
    )
    return [render_template(item, data) for item in paragraphs]


def build_document_xml(data: dict[str, Any]) -> str:
    body_parts = [
        paragraph("Техническое задание", style="Title", align="center", bold=True),
        paragraph(
            f'на создание проекта "{data["project_name"]}"',
            style="Subtitle",
            align="center",
        ),
        paragraph(),
        metadata_table(
            [
                ("Проект", str(data["project_name"])),
                ("Заказчик", str(data["customer"])),
                ("Исполнитель", str(data["contractor"])),
                ("Версия документа", str(data["version"])),
                ("Дата", str(data["document_date"])),
            ]
        ),
        paragraph(),
    ]

    for section in DEFAULT_SECTIONS:
        body_parts.append(paragraph(section["title"], style="Heading1"))
        for item in section_paragraphs(section, data):
            body_parts.append(paragraph(item))

    body_parts.extend(
        [
            paragraph(),
            paragraph("Согласование", style="Heading1"),
            metadata_table(
                [
                    ("От заказчика", "________________ / __________________"),
                    ("От исполнителя", "________________ / __________________"),
                ]
            ),
        ]
    )

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'mc:Ignorable="w14 wp14">'
        f"<w:body>{''.join(body_parts)}"
        "<w:sectPr>"
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:cols w:space="708"/>'
        '<w:docGrid w:linePitch="360"/>'
        "</w:sectPr>"
        "</w:body></w:document>"
    )


def styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        '<w:name w:val="Normal"/>'
        '<w:qFormat/>'
        '<w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
        "</w:style>"
        '<w:style w:type="paragraph" w:styleId="Title">'
        '<w:name w:val="Title"/>'
        '<w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/>'
        '<w:qFormat/>'
        '<w:pPr><w:spacing w:after="240"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>'
        "</w:style>"
        '<w:style w:type="paragraph" w:styleId="Subtitle">'
        '<w:name w:val="Subtitle"/>'
        '<w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/>'
        '<w:qFormat/>'
        '<w:pPr><w:spacing w:after="240"/></w:pPr>'
        '<w:rPr><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
        "</w:style>"
        '<w:style w:type="paragraph" w:styleId="Heading1">'
        '<w:name w:val="heading 1"/>'
        '<w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/>'
        '<w:qFormat/>'
        '<w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
        "</w:style>"
        "</w:styles>"
    )


def content_types_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        "</Types>"
    )


def relationships_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )


def document_relationships_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        "</Relationships>"
    )


def core_properties_xml(title: str) -> str:
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f"<dc:title>{xml_escape(title)}</dc:title>"
        "<dc:creator>tech_assignment_generator.py</dc:creator>"
        "<cp:lastModifiedBy>tech_assignment_generator.py</cp:lastModifiedBy>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>'
        "</cp:coreProperties>"
    )


def app_properties_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>Tech Assignment Generator</Application>"
        "</Properties>"
    )


def write_docx(output_path: Path, data: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document_title = f'Техническое задание: {data["project_name"]}'

    parts = {
        "[Content_Types].xml": content_types_xml(),
        "_rels/.rels": relationships_xml(),
        "docProps/core.xml": core_properties_xml(document_title),
        "docProps/app.xml": app_properties_xml(),
        "word/_rels/document.xml.rels": document_relationships_xml(),
        "word/document.xml": build_document_xml(data),
        "word/styles.xml": styles_xml(),
    }

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as docx_file:
        for name, content in parts.items():
            docx_file.writestr(name, content.encode("utf-8"))


def write_sample_config(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample = copy.deepcopy(DEFAULT_DATA)
    sample["sections"] = {
        "functional_requirements": [
            "Пользователь должен иметь возможность создать заявку с темой, описанием, приоритетом и вложениями.",
            "Руководитель должен назначать исполнителя и контролировать срок выполнения заявки.",
            "Система должна отправлять уведомления при изменении статуса заявки.",
        ],
        "acceptance": [
            "Приемочные испытания проводятся на тестовом стенде заказчика.",
            "Критерием приемки является успешное прохождение согласованных тестовых сценариев.",
        ],
    }
    with output_path.open("w", encoding="utf-8") as config_file:
        json.dump(sample, config_file, ensure_ascii=False, indent=2)
        config_file.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a typical technical assignment in DOCX format."
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        help="Path to a JSON file with project data.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("technical_assignment.docx"),
        help="Path to the generated DOCX file.",
    )
    parser.add_argument(
        "--init-sample",
        type=Path,
        help="Write a sample JSON config to the given path and exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.init_sample:
        write_sample_config(args.init_sample)
        print(f"Sample config written to {args.init_sample}")
        return

    custom_data = load_config(args.config) if args.config else {}
    data = merge_data(custom_data)
    write_docx(args.output, data)
    print(f"Technical assignment written to {args.output}")


if __name__ == "__main__":
    main()
