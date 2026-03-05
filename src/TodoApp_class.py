from dataclasses import field
from typing import Callable
import flet as ft
from Task_class import Task, save_data

<<<<<<< HEAD

import duckdb 
import os 
import json



from Task_class import Task


class TodoApp(ft.Column):
    def __init__(self,page):
        super().__init__() # chama o construtor parente
        self.page = page
        # --- configuração da Base de dados e Storage ---

        self.db_file = "todo_data.duckdb"
        self.parquet_file = "tasks.parquet"

=======
import json

class TodoApp(ft.Column):
    def __init__(self):
        super().__init__() # Call parent constructor
>>>>>>> d9d18335b7b4043e33988fffc9773293220521da
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

<<<<<<< HEAD
        self.conn = duckdb.connect(self.db_file)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_name TEXT,
                completed BOOLEAN
            )
        """)

        self.load_from_database()

    def save_to_database(self):
        self.conn.execute("DELETE FROM tasks")

        for task in self.tasks.controls:
            self.conn.execute(
                "INSERT INTO tasks VALUES (?, ?)",
                (task.display_task.label, task.completed),
            )

        # exportar para parquet
        self.conn.execute(f"COPY tasks TO '{self.parquet_file}' (FORMAT PARQUET)")

    def load_from_database(self):
        result = self.conn.execute("SELECT * FROM tasks").fetchall()

        for row in result:
            data = {
                "task_name": row[0],
                "completed": row[1],
            }

            task = Task.from_dict(
                data,
                self.task_status_change,
                self.task_delete,
            )
            self.tasks.controls.append(task)


=======
        for task_name in save_data:  # Load tasks from save_data on initialization
            task = Task(
                task_name=task_name,
                on_status_change=self.task_status_change,
                on_delete=self.task_delete,
            )
            self.tasks.controls.append(task)

>>>>>>> d9d18335b7b4043e33988fffc9773293220521da
    def add_clicked(self, e):
        save_data.append(self.new_task.value)  # Save the new task name before adding
        print(f"Saved new task: {self.new_task.value}")  # Debug print
        print(f"Current save_data: {save_data}")  # Debug print

        task = Task(
            task_name=self.new_task.value,
            on_status_change=self.task_status_change,
            on_delete=self.task_delete,
        )
        #storage
        self.tasks.controls.append(task)
        self.page.run_task(self.save_tasks)

        self.new_task.value = ""
        self.update()

    def task_status_change(self):
        self.page.run_task(self.save_tasks)
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        #storage
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

    def tabs_changed(self, e):
        self.update()

    async def save_tasks(self):
        await self.page.shared_preferences.set("tasks", json.dumps(save_data))

