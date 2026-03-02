import flet as ft
from TodoApp_class import TodoApp
from Task_class import Task, save_data

import json

async def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    saved_tasks = await page.shared_preferences.get("tasks")
    if saved_tasks:
        global save_data
        save_data = json.loads(saved_tasks)

    
    page.update()
    page.add(
        ft.SafeArea(
            content=TodoApp(),
        )
    )


ft.app(target=main)


