"""SQLite catalog of typical solution templates for technical assignments."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_DB_PATH = Path("tech_assignment_solutions.db")


@dataclass(frozen=True)
class SolutionOption:
    id: str
    name: str
    description: str
    payload: dict[str, Any]


DEFAULT_SOLUTIONS: list[SolutionOption] = [
    SolutionOption(
        id="request-management",
        name="Система учета заявок",
        description="Прием, назначение, контроль и закрытие пользовательских заявок.",
        payload={
            "purpose": "Автоматизация приема, обработки и контроля исполнения заявок пользователей.",
            "scope": (
                "Разработка веб-приложения для регистрации заявок, назначения "
                "исполнителей, контроля сроков и формирования отчетности."
            ),
            "platform": "Веб-приложение, доступное через современные браузеры",
            "sections": {
                "functional_requirements": [
                    "Пользователь должен иметь возможность создать заявку с темой, описанием, приоритетом и вложениями.",
                    "Руководитель должен назначать исполнителя и контролировать срок выполнения заявки.",
                    "Исполнитель должен изменять статус заявки и фиксировать результат работ.",
                    "Система должна отправлять уведомления при изменении статуса заявки.",
                    "Система должна формировать отчеты по статусам, исполнителям и срокам выполнения.",
                ],
                "non_functional_requirements": [
                    "Интерфейс должен быть доступен через современные браузеры без установки дополнительного ПО.",
                    "Система должна хранить историю изменений заявок.",
                    "Доступ к данным должен разграничиваться ролями пользователей.",
                    "Решение должно предусматривать резервное копирование базы данных.",
                ],
            },
        },
    ),
    SolutionOption(
        id="crm",
        name="CRM для отдела продаж",
        description="Учет клиентов, сделок, задач менеджеров и отчетов по продажам.",
        payload={
            "purpose": "Автоматизация работы отдела продаж с клиентами, сделками и задачами.",
            "scope": (
                "Разработка CRM-системы с карточками клиентов, воронкой продаж, "
                "задачами менеджеров и аналитическими отчетами."
            ),
            "platform": "Веб-приложение с адаптивным интерфейсом для рабочих станций и планшетов",
            "sections": {
                "functional_requirements": [
                    "Система должна вести карточки клиентов с контактами, историей взаимодействий и ответственным менеджером.",
                    "Система должна поддерживать этапы воронки продаж и перемещение сделок между этапами.",
                    "Менеджер должен создавать задачи, напоминания и комментарии по клиентам и сделкам.",
                    "Система должна формировать отчеты по сумме сделок, конверсии и активности менеджеров.",
                ],
                "non_functional_requirements": [
                    "Система должна поддерживать одновременную работу нескольких менеджеров.",
                    "Доступ к клиентской базе должен ограничиваться ролями и правами пользователей.",
                    "Интерфейс должен корректно отображаться на экранах ноутбуков и планшетов.",
                ],
            },
        },
    ),
    SolutionOption(
        id="online-store",
        name="Интернет-магазин",
        description="Каталог товаров, корзина, оформление заказов и управление оплатой.",
        payload={
            "purpose": "Организация онлайн-продаж товаров и автоматизация обработки заказов.",
            "scope": (
                "Разработка интернет-магазина с каталогом, карточками товаров, "
                "корзиной, оформлением заказов и административной панелью."
            ),
            "platform": "Веб-сайт с публичной частью и административным интерфейсом",
            "sections": {
                "functional_requirements": [
                    "Покупатель должен просматривать каталог товаров, выполнять поиск и фильтрацию.",
                    "Покупатель должен добавлять товары в корзину и оформлять заказ.",
                    "Администратор должен управлять товарами, категориями, ценами и остатками.",
                    "Система должна фиксировать статусы заказов и историю их изменения.",
                    "Система должна поддерживать выгрузку заказов для последующей обработки.",
                ],
                "non_functional_requirements": [
                    "Публичные страницы должны быть адаптированы для мобильных устройств.",
                    "Система должна обеспечивать защиту персональных данных покупателей.",
                    "Административный интерфейс должен быть доступен только авторизованным пользователям.",
                ],
            },
        },
    ),
    SolutionOption(
        id="document-workflow",
        name="Электронный документооборот",
        description="Создание, согласование, хранение и поиск внутренних документов.",
        payload={
            "purpose": "Автоматизация жизненного цикла внутренних документов организации.",
            "scope": (
                "Разработка системы электронного документооборота с маршрутами "
                "согласования, хранилищем документов и журналом действий."
            ),
            "platform": "Веб-приложение для сотрудников и администраторов организации",
            "sections": {
                "functional_requirements": [
                    "Пользователь должен создавать карточку документа и прикладывать файлы.",
                    "Система должна поддерживать маршруты согласования с несколькими участниками.",
                    "Согласующий должен утверждать документ, возвращать его на доработку или оставлять комментарий.",
                    "Система должна хранить версии документов и журнал действий пользователей.",
                    "Система должна обеспечивать поиск документов по реквизитам и текстовым атрибутам.",
                ],
                "non_functional_requirements": [
                    "Доступ к документам должен ограничиваться ролями, подразделениями и участием в маршруте.",
                    "Система должна сохранять историю согласования и изменения версий.",
                    "Решение должно предусматривать архивное хранение закрытых документов.",
                ],
            },
        },
    ),
    SolutionOption(
        id="analytics-dashboard",
        name="Аналитическая панель",
        description="Сбор показателей, визуализация данных и регулярная отчетность.",
        payload={
            "purpose": "Предоставление руководителям и специалистам актуальной аналитики по ключевым показателям.",
            "scope": (
                "Разработка аналитической панели с загрузкой данных, виджетами, "
                "фильтрами, экспортом отчетов и настройкой прав доступа."
            ),
            "platform": "Веб-приложение с интерактивными графиками и таблицами",
            "sections": {
                "functional_requirements": [
                    "Система должна загружать данные из согласованных источников.",
                    "Пользователь должен фильтровать показатели по периоду, подразделению и другим параметрам.",
                    "Система должна отображать графики, таблицы и сводные карточки показателей.",
                    "Пользователь должен экспортировать отчеты в распространенные офисные форматы.",
                    "Администратор должен управлять наборами данных и доступом пользователей.",
                ],
                "non_functional_requirements": [
                    "Панели должны обновляться с периодичностью, согласованной с заказчиком.",
                    "Система должна корректно обрабатывать отсутствие или неполноту входных данных.",
                    "Доступ к аналитическим данным должен разграничиваться ролями пользователей.",
                ],
            },
        },
    ),
]


def connect(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def ensure_database(db_path: Path = DEFAULT_DB_PATH, *, reset: bool = False) -> None:
    """Create the catalog database and seed it with default solutions."""
    with connect(db_path) as connection:
        if reset:
            connection.execute("DROP TABLE IF EXISTS solutions")

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS solutions (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                payload_json TEXT NOT NULL
            )
            """
        )

        for solution in DEFAULT_SOLUTIONS:
            connection.execute(
                """
                INSERT OR IGNORE INTO solutions (
                    id,
                    name,
                    description,
                    payload_json
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    solution.id,
                    solution.name,
                    solution.description,
                    json.dumps(solution.payload, ensure_ascii=False),
                ),
            )


def list_solutions(db_path: Path = DEFAULT_DB_PATH) -> list[SolutionOption]:
    ensure_database(db_path)
    with connect(db_path) as connection:
        rows = connection.execute(
            "SELECT id, name, description, payload_json FROM solutions ORDER BY name"
        ).fetchall()

    return [
        SolutionOption(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            payload=json.loads(row["payload_json"]),
        )
        for row in rows
    ]


def get_solution(db_path: Path, solution_id: str) -> SolutionOption:
    ensure_database(db_path)
    with connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT id, name, description, payload_json
            FROM solutions
            WHERE id = ?
            """,
            (solution_id,),
        ).fetchone()

    if row is None:
        raise KeyError(f"Solution '{solution_id}' was not found in {db_path}.")

    return SolutionOption(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        payload=json.loads(row["payload_json"]),
    )
