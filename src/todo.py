import flet as ft
import Task_class
from TodoApp_class import TodoApp


import json

async def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    saved_tasks = await page.shared_preferences.get("tasks")
    if saved_tasks:
        print(f"Loaded tasks from storage: {saved_tasks}")  # Debug print
        Task_class.save_data.clear()  # Clear existing save_data before loading
        Task_class.save_data.extend(json.loads(saved_tasks))
        print("RAW STORAGE:", saved_tasks)
    
    page.update()
<<<<<<< HEAD
    
    # criação da instacia atual
    app = TodoApp(page)

    page.add(app)
=======
    page.add(
        ft.SafeArea(
            content=TodoApp(),
        )
    )


ft.app(target=main)

>>>>>>> d9d18335b7b4043e33988fffc9773293220521da

