import os
import flet as ft
from supabase import create_client


SUPABASE_URL = "https://qogokewwzovejmcvgzac.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFvZ29rZXd3em92ZWptY3ZnemFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQxMzEyMzksImV4cCI6MjEwOTcwNzIzOX0.jJzwtadFb1v7mRQNtURyG0SMLfesAZ7_5MXy-IOsV_Q"

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
