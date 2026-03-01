import flet as ft
from TodoApp_class import TodoApp
from Task_class import Task, save_data


def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()



    app = TodoApp()

    page.add(app)

ft.app(target=main)