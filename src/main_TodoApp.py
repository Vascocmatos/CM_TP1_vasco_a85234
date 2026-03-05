import flet as ft
import os
import json
import Task_class
from TodoApp_class import TodoApp
from db_manager import load_from_db
from dotenv import load_dotenv

load_dotenv()

provider = ft.auth.providers.GitHubOAuthProvider(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    redirect_url="http://127.0.0.1:8550/oauth_callback"  # ← obrigatório
)

async def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    async def load_app_for_user(user_id):
        page.controls.clear()
        page.vertical_alignment = ft.MainAxisAlignment.START
        
        # Carregar tarefas da base de dados
        db_tasks = load_from_db()

        # Filtrar apenas tarefas do utilizador atual
        user_tasks = [t for t in db_tasks if t.get("user_id") == user_id]

        saved_tasks_str = await page.shared_preferences.get(f"tasks_{user_id}")
        client_tasks = json.loads(saved_tasks_str) if saved_tasks_str else []

        Task_class.save_data.clear()

        if user_tasks:
            Task_class.save_data.extend(user_tasks)
        elif client_tasks:
            Task_class.save_data.extend(client_tasks)

        page.add(ft.SafeArea(content=TodoApp(user_id=user_id)))
        page.update()

    # Quando o login termina
    async def on_login(e):
        if e.error:
            print(f"Erro no login: {e.error}")
            return
        
        user_id = str(page.auth.user.id)
        await load_app_for_user(user_id)

    page.on_login = on_login

    async def login_click(e):
        await page.login(provider)  # ← Isto é a forma correta agora!

    # Vista de login (igual)
    login_view = ft.Column(
        controls=[
            ft.Icon(ft.Icons.LOCK_OUTLINE, size=60),
            ft.Text("Gestor de Tarefas", size=30, weight="bold"),
            ft.ElevatedButton(
                content=ft.Text("Login com GitHub"),
                on_click=login_click,
                icon=ft.Icons.LOGIN
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Se já estiver autenticado (após redirect do GitHub)
    if page.auth:
        user_id = str(page.auth.user.id)
        await load_app_for_user(user_id)
    else:
        page.add(login_view)

    page.update()

if __name__ == "__main__":
    ft.run(main, port=8550)