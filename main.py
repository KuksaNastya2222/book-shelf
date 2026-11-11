import flet as ft
from supabase import create_client

# Ваши ключи (мы уже вставляли их сюда)
SUPABASE_URL = "https://qogokewwzovejmcvgzac.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFvZ29rZXd3em92ZWptY3ZnemFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQxMzEyMzksImV4cCI6MjEwOTcwNzIzOX0.jJzwtadFb1v7mRQNtURyG0SMLfesAZ7_5MXy-IOsV_Q"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def main(page: ft.Page):
    page.title = "Книжная полка"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Поле для ввода названия
    title_input = ft.TextField(label="Название книги", expand=True)
    # Поле для ввода автора
    author_input = ft.TextField(label="Автор", expand=True)
    
    # Контейнер для списка книг
    books_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    # Функция для загрузки книг из базы
    def load_books(e=None):
        books_list.controls.clear()
        try:
            response = supabase.table("books").select("*").order("id", desc=True).execute()
            for book in response.data:
                # Создаем карточку для каждой книги
                book_card = ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(book['title'], size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(book['author'], size=14, color="grey"),
                        ], expand=True),
                        
                        # Переключатель "Прочитано"
                        ft.Checkbox(
                            label="Прочитано", 
                            value=book['read'],
                            on_change=lambda e, book_id=book['id']: toggle_read(book_id, e.control.value)
                        ),
                        # Кнопка удаления
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE, 
                            icon_color="red",
                            on_click=lambda e, book_id=book['id']: delete_book(book_id)
                        )
                    ]),
                    padding=15,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
                )
                books_list.controls.append(book_card)
        except Exception as e:
            print("Ошибка загрузки:", e)
        
        page.update()

    # Функция добавления книги
    def add_book(e):
        if not title_input.value.strip() or not author_input.value.strip():
            return  # Не добавляем пустые поля
        
        try:
            data = {
                "title": title_input.value.strip(),
                "author": author_input.value.strip(),
                "read": False
            }
            supabase.table("books").insert(data).execute()
            
            title_input.value = ""
            author_input.value = ""
            load_books()  # Обновляем список
        except Exception as e:
            print("Ошибка добавления:", e)

    # Функция изменения статуса "Прочитано"
    def toggle_read(book_id, is_read):
        try:
            supabase.table("books").update({"read": is_read}).eq("id", book_id).execute()
        except Exception as e:
            print("Ошибка обновления:", e)

    # Функция удаления книги
    def delete_book(book_id):
        try:
            supabase.table("books").delete().eq("id", book_id).execute()
            load_books()  # Обновляем список
        except Exception as e:
            print("Ошибка удаления:", e)

    # Кнопка "Добавить"
    add_button = ft.ElevatedButton(
        text="Добавить книгу", 
        icon=ft.Icons.ADD, 
        on_click=add_book
    )

    # Собираем весь экран вместе
    page.add(
        ft.Text("Моя книжная полка", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([title_input, author_input]),
        ft.Row([add_button], alignment=ft.MainAxisAlignment.END),
        ft.Divider(),
        books_list
    )

    # Загружаем книги при запуске
    load_books()

ft.run(main)
