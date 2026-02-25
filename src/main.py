import flet as ft

def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)

    def decrement_click(e):
        counter.data -= 1
        counter.value = str(counter.data)

    botao_diminuir = ft.Button(
        content=ft.Text("- Diminuir"),
        on_click=decrement_click,
        bgcolor="red",
        color="white",
    )

    botao_aumentar = ft.Button(
        content=ft.Text("+ Aumentar"),
        on_click=increment_click,
        bgcolor="green",
        color="white",
    )

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    counter,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[botao_diminuir, botao_aumentar]
                    )
                ]
            )
        )
    )

ft.run(main)