import os
import flet as ft
from dotenv import load_dotenv
from supabase import create_client

# Загружаем ключи из файла .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Подключаемся к Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def main(page: ft.Page):
    page.title = "Книжная полка"
    
    try:
        # Пытаемся получить данные из базы
        response = supabase.table("books").select("*").execute()
        books = response.data
        
        print("Успешное подключение! Данные из базы:", books)
        page.add(ft.Text(f"Книг в базе: {len(books)}"))
        
    except Exception as e:
        print("Ошибка:", e)
        page.add(ft.Text(f"Ошибка подключения: {e}", color="red"))

ft.run(main)