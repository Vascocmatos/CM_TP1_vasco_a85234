import flet as ft
import Task_class
from TodoApp_class import TodoApp

from db_manager import load_from_db
import json

# define a função assíncrona principal que será chamada pelo Flet
async def main(page: ft.Page):
    # configura o título da janela
    page.title = "To-Do App"
    # alinha os conteúdos horizontalmente no centro da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # tenta carregar tarefas guardadas numa base de dados local (parquet)
    db_tasks = load_from_db()
    
    # lê as tarefas guardadas nas preferências do cliente (shared_preferences)
    saved_tasks_str = await page.shared_preferences.get("tasks")
    client_tasks = json.loads(saved_tasks_str) if saved_tasks_str else []

    # limpa a lista de tarefas em Task_class antes de sincronizar
    Task_class.save_data.clear()
    # se existirem tarefas na base de dados, usa‑as
    if db_tasks:
        Task_class.save_data.extend(db_tasks)
        print("Sincronizado via Base de Dados Parquet.")
    # caso contrário, se houver tarefas no armazenamento do cliente, usa‑as
    elif client_tasks:
        Task_class.save_data.extend(client_tasks)
        print("Sincronizado via Client Storage.")
    
    # força a atualização da página para refletir os dados carregados
    page.update()
    # adiciona o componente principal ao layout dentro de uma SafeArea
    page.add(
        ft.SafeArea(
            content=TodoApp(),
        )
    )

# inicia a aplicação Flet, passando a função main como alvo
ft.app(target=main)