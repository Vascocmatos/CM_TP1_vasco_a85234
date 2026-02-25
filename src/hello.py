import flet as ft
from flet import Checkbox, FloatingActionButton, Icons, Page, TextField



def main(page: ft.Page):
    def add_clicked(e):
        page.add(Checkbox(label=new_task.value))
        new_task.value = ""
        view.update()

    new_task = TextField(hint_text="Whats needs to be done?", expand=True)
    tasks_view = ft.Column()
    view = ft.Column(
        width=600,
        controls=[
            ft.Row(
                controls=[
                    new_task,
                    FloatingActionButton(icon=Icons.ADD, on_click=add_clicked)
                ],
            ),
            tasks_view
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)

ft.run(main)