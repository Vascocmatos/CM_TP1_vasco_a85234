import flet as ft
import os
import json
import Task_class
from TodoApp_class import TodoApp
from db_manager import load_from_db
from dotenv import load_dotenv

# Carregamento das variáveis de ambiente para OAuth e chaves de encriptação
load_dotenv()

# Configuração do provedor de autenticação GitHub
provider = ft.auth.providers.GitHubOAuthProvider(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    redirect_url="http://127.0.0.1:8550/oauth_callback"
)

async def main(page: ft.Page):
    page.title = "To-Do App - Gestão de Tarefas"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    async def load_app_for_user(user_id):
        """Inicializa a interface principal após autenticação bem-sucedida."""
        page.controls.clear()
        page.vertical_alignment = ft.MainAxisAlignment.START

        # Definição do tema padrão
        if page.theme_mode is None:
            page.theme_mode = ft.ThemeMode.LIGHT

        # Sincronização de dados: Base de Dados (DuckDB) + Cache Local (Shared Preferences)
        db_tasks = load_from_db()
        user_tasks = [t for t in db_tasks if t.get("user_id") == user_id]

        saved_tasks_str = await page.shared_preferences.get(f"tasks_{user_id}")
        client_tasks = json.loads(saved_tasks_str) if saved_tasks_str else []

        # Limpa e reconstrói a lista global de tarefas em memória
        Task_class.save_data.clear()
        if user_tasks:
            Task_class.save_data.extend(user_tasks)
        elif client_tasks:
            Task_class.save_data.extend(client_tasks)

        # Instanciação da aplicação principal injetando o ID do utilizador autenticado
        todo_app = TodoApp(user_id=user_id)

        # Sincronização visual do ícone de tema com o estado atual da página
        if hasattr(todo_app, "theme_button"):
            if page.theme_mode == ft.ThemeMode.LIGHT:
                todo_app.theme_button.icon = ft.Icons.NIGHTS_STAY
            else:
                todo_app.theme_button.icon = ft.Icons.WB_SUNNY

        page.add(ft.SafeArea(content=todo_app))
        page.update()

    async def on_login(e):
        """Callback executado após o fluxo de OAuth do GitHub."""
        if e.error:
            print(f"Erro na autenticação: {e.error}")
            return
        
        user_id = str(page.auth.user.id)
        await load_app_for_user(user_id)

    page.on_login = on_login

    async def login_click(e):
        """Inicia o processo de login via browser."""
        await page.login(provider)

    # Interface de Login inicial
    login_view = ft.Column(
        controls=[
            ft.Icon(ft.Icons.LOCK_OUTLINE, size=60),
            ft.Text("Gestor de Tarefas", size=30, weight="bold"),
            ft.FilledButton(
                content=ft.Text("Login com GitHub"),
                on_click=login_click,
                icon=ft.Icons.LOGIN
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Verificação de persistência de sessão
    if page.auth:
        user_id = str(page.auth.user.id)
        await load_app_for_user(user_id)
    else:
        page.add(login_view)

    page.update()

if __name__ == "__main__":
    # Inicialização da app com suporte a assets locais (GIFs, imagens)
    ft.app(target=main, port=8550, assets_dir="assets")