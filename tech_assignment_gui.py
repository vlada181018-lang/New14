#!/usr/bin/env python3
"""Desktop window for generating technical assignment DOCX files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from solution_catalog import DEFAULT_DB_PATH, SolutionOption, ensure_database, list_solutions
from tech_assignment_generator import DEFAULT_DATA, merge_data, write_docx

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ModuleNotFoundError:  # pragma: no cover - depends on OS packages
    tk = None  # type: ignore[assignment]
    filedialog = None  # type: ignore[assignment]
    messagebox = None  # type: ignore[assignment]
    ttk = None  # type: ignore[assignment]


FIELD_DEFINITIONS = [
    ("project_name", "Название проекта"),
    ("customer", "Заказчик"),
    ("contractor", "Исполнитель"),
    ("version", "Версия документа"),
    ("document_date", "Дата документа"),
    ("basis", "Основание для разработки"),
    ("purpose", "Назначение системы"),
    ("scope", "Состав и объем работ"),
    ("platform", "Платформа"),
    ("support_period", "Гарантийное сопровождение"),
]


SECTION_DEFINITIONS = [
    ("functional_requirements", "Функциональные требования"),
    ("non_functional_requirements", "Нефункциональные требования"),
    ("acceptance", "Порядок контроля и приемки"),
    ("documentation", "Документация"),
    ("support", "Гарантийное сопровождение"),
]


NO_SOLUTION_LABEL = "Без типового решения"


class TechnicalAssignmentApp:
    def __init__(self, root: tk.Tk, db_path: Path = DEFAULT_DB_PATH) -> None:
        self.root = root
        self.db_path = db_path
        self.root.title("Генератор технического задания")
        self.root.geometry("980x760")
        self.root.minsize(860, 640)

        ensure_database(self.db_path)
        self.solutions = list_solutions(self.db_path)
        self.solution_labels = self.build_solution_labels(self.solutions)

        self.field_vars: dict[str, tk.StringVar] = {
            key: tk.StringVar(value=str(DEFAULT_DATA.get(key, "")))
            for key, _label in FIELD_DEFINITIONS
        }
        self.output_var = tk.StringVar(value="technical_assignment.docx")
        self.solution_var = tk.StringVar(value=NO_SOLUTION_LABEL)
        self.description_var = tk.StringVar(value="Выберите типовое решение из базы данных.")
        self.section_widgets: dict[str, tk.Text] = {}

        self.build_layout()

    @staticmethod
    def build_solution_labels(
        solutions: list[SolutionOption],
    ) -> dict[str, SolutionOption]:
        return {f"{solution.name} ({solution.id})": solution for solution in solutions}

    def build_layout(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        main_tab = ttk.Frame(notebook)
        sections_tab = ttk.Frame(notebook)
        output_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="Основные данные")
        notebook.add(sections_tab, text="Разделы ТЗ")
        notebook.add(output_tab, text="Файл и генерация")

        self.build_main_tab(main_tab)
        self.build_sections_tab(sections_tab)
        self.build_output_tab(output_tab)

    def build_main_tab(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(1, weight=1)

        ttk.Label(parent, text="Типовое решение из базы данных").grid(
            row=0, column=0, sticky=tk.W, padx=8, pady=(10, 4)
        )
        self.solution_combo = ttk.Combobox(
            parent,
            textvariable=self.solution_var,
            values=[NO_SOLUTION_LABEL, *self.solution_labels.keys()],
            state="readonly",
        )
        self.solution_combo.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=(10, 4))
        self.solution_combo.bind("<<ComboboxSelected>>", self.on_solution_selected)

        ttk.Label(parent, textvariable=self.description_var, wraplength=760).grid(
            row=1, column=0, columnspan=2, sticky=tk.EW, padx=8, pady=(0, 12)
        )

        for row_index, (key, label) in enumerate(FIELD_DEFINITIONS, start=2):
            ttk.Label(parent, text=label).grid(
                row=row_index, column=0, sticky=tk.W, padx=8, pady=5
            )
            entry = ttk.Entry(parent, textvariable=self.field_vars[key])
            entry.grid(row=row_index, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Button(
            parent,
            text="Обновить список решений из базы",
            command=self.reload_solutions,
        ).grid(row=len(FIELD_DEFINITIONS) + 2, column=1, sticky=tk.E, padx=8, pady=12)

    def build_sections_tab(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=1)

        hint = (
            "Каждая непустая строка будет добавлена в выбранный раздел ТЗ "
            "отдельным пунктом."
        )
        ttk.Label(parent, text=hint, wraplength=820).grid(
            row=0, column=0, sticky=tk.EW, padx=8, pady=(10, 4)
        )

        for row_index, (key, label) in enumerate(SECTION_DEFINITIONS, start=1):
            frame = ttk.LabelFrame(parent, text=label)
            frame.grid(row=row_index, column=0, sticky=tk.NSEW, padx=8, pady=6)
            frame.columnconfigure(0, weight=1)

            text = tk.Text(frame, height=5, wrap=tk.WORD)
            text.grid(row=0, column=0, sticky=tk.NSEW, padx=(6, 0), pady=6)
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text.yview)
            scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=(0, 6), pady=6)
            text.configure(yscrollcommand=scrollbar.set)
            self.section_widgets[key] = text

    def build_output_tab(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(1, weight=1)

        ttk.Label(parent, text="Файл Word для сохранения").grid(
            row=0, column=0, sticky=tk.W, padx=8, pady=(18, 6)
        )
        ttk.Entry(parent, textvariable=self.output_var).grid(
            row=0, column=1, sticky=tk.EW, padx=8, pady=(18, 6)
        )
        ttk.Button(parent, text="Выбрать...", command=self.choose_output_file).grid(
            row=0, column=2, sticky=tk.E, padx=8, pady=(18, 6)
        )

        ttk.Label(
            parent,
            text=f"База решений: {self.db_path}",
            wraplength=820,
        ).grid(row=1, column=0, columnspan=3, sticky=tk.EW, padx=8, pady=8)

        ttk.Button(
            parent,
            text="Сформировать техническое задание",
            command=self.generate_document,
        ).grid(row=2, column=1, sticky=tk.E, padx=8, pady=18)

    def reload_solutions(self) -> None:
        ensure_database(self.db_path)
        self.solutions = list_solutions(self.db_path)
        self.solution_labels = self.build_solution_labels(self.solutions)
        self.solution_combo.configure(values=[NO_SOLUTION_LABEL, *self.solution_labels.keys()])
        self.solution_var.set(NO_SOLUTION_LABEL)
        self.description_var.set("Список решений обновлен из базы данных.")

    def on_solution_selected(self, _event: tk.Event[Any] | None = None) -> None:
        label = self.solution_var.get()
        if label == NO_SOLUTION_LABEL:
            self.description_var.set("Поля можно заполнить вручную без типового решения.")
            return

        solution = self.solution_labels.get(label)
        if solution is None:
            return

        self.description_var.set(solution.description)
        self.apply_solution_payload(solution.payload)

    def apply_solution_payload(self, payload: dict[str, Any]) -> None:
        for key in ("purpose", "scope", "platform"):
            if key in payload:
                self.field_vars[key].set(str(payload[key]))

        sections = payload.get("sections", {})
        if isinstance(sections, dict):
            for key, value in sections.items():
                if key in self.section_widgets:
                    self.set_text_value(key, self.format_section_value(value))

    @staticmethod
    def format_section_value(value: Any) -> str:
        if isinstance(value, list):
            return "\n".join(str(item) for item in value)
        return str(value)

    def set_text_value(self, key: str, value: str) -> None:
        widget = self.section_widgets[key]
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)

    def choose_output_file(self) -> None:
        output_path = filedialog.asksaveasfilename(
            title="Сохранить техническое задание",
            defaultextension=".docx",
            filetypes=[("Word document", "*.docx"), ("All files", "*.*")],
        )
        if output_path:
            self.output_var.set(output_path)

    def collect_data(self) -> dict[str, Any]:
        field_data = {
            key: value.get().strip()
            for key, value in self.field_vars.items()
            if value.get().strip()
        }
        sections: dict[str, list[str]] = {}
        for key, widget in self.section_widgets.items():
            lines = [
                line.strip()
                for line in widget.get("1.0", tk.END).splitlines()
                if line.strip()
            ]
            if lines:
                sections[key] = lines

        if sections:
            field_data["sections"] = sections

        return merge_data(field_data)

    def generate_document(self) -> None:
        output_value = self.output_var.get().strip()
        if not output_value:
            messagebox.showerror("Ошибка", "Укажите путь для сохранения Word-файла.")
            return

        try:
            output_path = Path(output_value)
            data = self.collect_data()
            write_docx(output_path, data)
        except Exception as error:  # pragma: no cover - GUI feedback path
            messagebox.showerror("Ошибка", f"Не удалось сформировать документ:\n{error}")
            return

        messagebox.showinfo(
            "Готово",
            f"Техническое задание сохранено:\n{output_path}",
        )


def main() -> None:
    if tk is None:
        raise SystemExit(
            "Tkinter is not installed. Install the OS package for Tkinter "
            "(for example, python3-tk on Debian/Ubuntu) and run again."
        )

    root = tk.Tk()
    app = TechnicalAssignmentApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
