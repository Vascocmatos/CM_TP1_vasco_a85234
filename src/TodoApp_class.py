import flet as ft
import json
from Task_class import Task, save_data
from db_manager import save_to_db

class TodoApp(ft.Column):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

        # ====================== BOTÃO DE TEMA ======================
        self.theme_button = ft.IconButton(
            icon=ft.Icons.NIGHTS_STAY,
            tooltip="Alternar modo claro/escuro",
            on_click=self.toggle_theme,
        )

        self.header = ft.Row(
            controls=[
                ft.Text("Gestor de Tarefas", size=20, weight="bold"),
                ft.Row(
                    controls=[self.theme_button],
                    expand=True,
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        # ===========================================================

        self.filter = ft.TabBar(
            scrollable=False,
            tabs=[
                ft.Tab(label="Tudo"),
                ft.Tab(label="Ativas"),
                ft.Tab(label="Completadas"),
            ],
        )

        self.filter_tabs = ft.Tabs(
            length=3,
            selected_index=0,
            on_change=lambda e: self.update(),
            content=self.filter,
        )

        self.width = 600
        self.controls = [
            self.header,                    # ← título + botão de tema
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter_tabs,
                    self.tasks,
                ],
            ),
        ]

        # Carrega tarefas do utilizador atual
        for task_dict in save_data:
            if task_dict.get("user_id") == self.user_id:
                task = Task(
                    task_name=task_dict["name"],
                    completed=task_dict["completed"],
                    user_id=self.user_id,
                    on_status_change=self.task_status_change,
                    on_delete=self.task_delete,
                )
                self.tasks.controls.append(task)

    def toggle_theme(self, e):
        """Alterna claro/escuro e muda o ícone"""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.WB_SUNNY
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.NIGHTS_STAY
        self.page.update()

    def add_clicked(self, e):
        if not self.new_task.value:
            return

        new_task_dict = {"user_id": self.user_id, "name": self.new_task.value, "completadas": False}
        save_data.append(new_task_dict)

        task = Task(
            task_name=self.new_task.value,
            completed=False,
            user_id=self.user_id,
            on_status_change=self.task_status_change,
            on_delete=self.task_delete,
        )
        self.tasks.controls.append(task)
        self.page.run_task(self.save_tasks)

        self.new_task.value = ""
        self.update()

    def task_status_change(self):
        self.page.run_task(self.save_tasks)
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.page.run_task(self.save_tasks)
        self.update()

    def before_update(self):
        status = self.filter.tabs[self.filter_tabs.selected_index].label
        for task in self.tasks.controls:
            task.visible = (
                status == "Tudo"
                or (status == "Ativas" and not task.completed)
                or (status == "Completadas" and task.completed)
            )

    async def save_tasks(self):
        key = f"tasks_{self.user_id}" if self.user_id else "tasks"
        await self.page.shared_preferences.set(key, json.dumps(save_data))
        save_to_db(save_data)
        