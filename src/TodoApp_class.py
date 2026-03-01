from dataclasses import field
from typing import Callable

import flet as ft
from Task_class import Task, save_data, update_local_storage


class TodoApp(ft.Column):
    def __init__(self): # Changed from 'init' to '__init__'
        super().__init__() # Call parent constructor
        
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

    def add_clicked(self, e):
        save_data.append(self.new_task.value)  # Save the new task name before adding
        print(f"Saved new task: {self.new_task.value}")  # Debug print
        print(f"Current save_data: {save_data}")  # Debug print
        self.update_local_storage()  # Update local storage with the new save_data

        task = Task(
            task_name=self.new_task.value,
            on_status_change=self.task_status_change,
            on_delete=self.task_delete,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_status_change(self):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
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




    async def load_savedata_csstorage(self):
        # Implement loading data from storage
        await ft.SharedPreferences().set("my_key", "my_value")

        pass