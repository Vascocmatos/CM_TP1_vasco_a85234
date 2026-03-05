# TodoApp_class.py
import flet as ft
import json
from Task_class import Task, save_data
from db_manager import save_to_db
from Task_class import Task, save_data

class TodoApp(ft.Column):
    def __init__(self, user_id=None): # Adicionado user_id
        super().__init__()
        self.user_id = user_id
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

        self.filter = ft.TabBar(
            scrollable=False,
            tabs=[
                ft.Tab(label="all"),
                ft.Tab(label="active"),
                ft.Tab(label="completed"),
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

        # Carrega APENAS as tarefas deste utilizador na interface
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

    def add_clicked(self, e):
        if not self.new_task.value:
            return

        # Associa a nova tarefa ao utilizador
        new_task_dict = {"user_id": self.user_id, "name": self.new_task.value, "completed": False}
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
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )

    async def save_tasks(self):
        # Grava as tarefas com uma chave única por utilizador
        key = f"tasks_{self.user_id}" if self.user_id else "tasks"
        
        # IMPORTANTE: Usamos o save_data que veio do Task_class
        await self.page.shared_preferences.set(key, json.dumps(save_data))
        save_to_db(save_data)