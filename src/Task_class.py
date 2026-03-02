from dataclasses import field
import json
from typing import Callable

import flet as ft
save_data = []  # This will hold the tasks to be saved

class Task(ft.Column):
    def __init__(self, task_name, on_status_change, on_delete):
        super().__init__()

        self.completed = False
        self.task_name = task_name
        self.on_status_change = on_status_change
        self.on_delete = on_delete

        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]


    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        print("edit clicked")  # Debug print
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        print("save clicked")  # Debug print

        save_data.remove(self.task_name)  # Remove the old task name from save_data
        self.task_name = self.edit_name.value  # Update the task name
        save_data.append(self.display_task.label)  # Add the new task name to save_data
        print(f"Updated save_data: {save_data}")  # Debug print
        self.page.run_task(self.save_tasks)  # Update local storage with the new save_data

        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.on_status_change()
        print("status changed")  # Debug print

    def delete_clicked(self, e):
        print("delete clicked")  # Debug print
        print(f"Deleted task: {self.task_name}")  # Debug print
        print(f"Current save_data after deletion: {save_data}")  # Debug print
        save_data.remove(self.task_name)  # Remove the task name from save_data
        self.on_delete(self)
        
        self.page.run_task(self.save_tasks)  # Update local storage with the new save_data

    async def save_tasks(self):
        await self.page.shared_preferences.set("tasks", json.dumps(save_data))