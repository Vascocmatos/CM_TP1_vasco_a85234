# Task_class.py
import flet as ft
import json
from db_manager import save_to_db

save_data = []  

class Task(ft.Column):
    def __init__(self, task_name, completed, user_id, on_status_change, on_delete):
        super().__init__()

        self.completed = completed
        self.task_name = task_name
        self.user_id = user_id  # Novo atributo
        self.on_status_change = on_status_change
        self.on_delete = on_delete

        self.display_task = ft.Checkbox(
            value=self.completed, label=self.task_name, on_change=self.status_changed
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
        self.update()

    def save_clicked(self, e):
        for task in save_data:
            # Garante que só edita a tarefa correspondente ao utilizador atual
            if task["name"] == self.task_name and task.get("user_id") == self.user_id:
                task["name"] = self.edit_name.value
                break

        self.display_task.label = self.edit_name.value
        self.task_name = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        
        self.page.run_task(self.save_tasks)
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value

        for task in save_data:
            if task["name"] == self.task_name and task.get("user_id") == self.user_id:
                task["completed"] = self.completed
                break
                
        self.on_status_change()

    def delete_clicked(self, e):
        global save_data
        # Remove a tarefa correta deste utilizador específico
        save_data = [t for t in save_data if not (t["name"] == self.task_name and t.get("user_id") == self.user_id)]
        self.on_delete(self)
        self.page.run_task(self.save_tasks)

    async def save_tasks(self):
        # O armazenamento local fica isolado por utilizador
        user_tasks = [t for t in save_data if t.get("user_id") == self.user_id]
        await self.page.shared_preferences.set(f"tasks_{self.user_id}", json.dumps(user_tasks))
        save_to_db(save_data)