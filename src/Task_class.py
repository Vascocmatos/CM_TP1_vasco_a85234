# Task_class.py
import flet as ft
import json
import asyncio
import time
from db_manager import save_to_db

# Lista global para gestão de estado em memória
save_data = []

class Task(ft.Column):
    """Componente visual e lógico para uma tarefa individual."""
    def __init__(self, task_name, completed, user_id, on_status_change, on_delete):
        super().__init__()

        self.completed = completed
        self.task_name = task_name
        self.user_id = user_id
        self.on_status_change = on_status_change
        self.on_delete = on_delete

        # Elementos da vista de visualização
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
                            tooltip="Editar Tarefa",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Eliminar Tarefa",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        # Elementos da vista de edição
        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Guardar Alterações",
                    on_click=self.save_clicked,
                ),
            ],
        )
        
        # Componente de animação (GIF de explosão)
        self.explosion_gif = ft.Image(
            src="/explosao.gif",
            visible=False,
            width=100,
            height=100,
        )

        # Stack permite sobrepor a animação à tarefa durante a eliminação
        self.controls = [
            ft.Stack(
                [
                    self.display_view,
                    self.edit_view,
                    ft.Row(
                        [self.explosion_gif],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            )
        ]

    def edit_clicked(self, e):
        """Alterna para o modo de edição."""
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        """Guarda as alterações do nome da tarefa."""
        for task in save_data:
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
        """Atualiza o estado de conclusão da tarefa."""
        self.completed = self.display_task.value

        for task in save_data:
            if task["name"] == self.task_name and task.get("user_id") == self.user_id:
                task["completed"] = self.completed
                break
                
        self.on_status_change()

    async def delete_clicked(self, e):
        """Executa a animação de explosão antes de remover a tarefa definitivamente."""
        global save_data
        
        # Força o recarregamento do GIF via timestamp para garantir que a animação começa do início
        self.explosion_gif.src = f"/explosao.gif?{time.time()}"
        self.display_view.visible = False
        self.explosion_gif.visible = True
        self.update()
        
        # Tempo de espera correspondente à duração visual da animação
        await asyncio.sleep(1)
        
        # Remoção lógica e persistência
        save_data = [t for t in save_data if not (t["name"] == self.task_name and t.get("user_id") == self.user_id)]
        self.on_delete(self)
        self.page.run_task(self.save_tasks)

    async def save_tasks(self):
        """Persiste o estado atualizado no armazenamento local do utilizador."""
        user_tasks = [t for t in save_data if t.get("user_id") == self.user_id]
        await self.page.shared_preferences.set(f"tasks_{self.user_id}", json.dumps(user_tasks))
        save_to_db(save_data)