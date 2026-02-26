import flet as ft
from TodoApp_class import TodoApp
from Task_class import Task

def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    app = TodoApp()

    # add application's root control to the page
    # DO NOT manually assign app.page = page
    page.add(app)

ft.app(target=main)