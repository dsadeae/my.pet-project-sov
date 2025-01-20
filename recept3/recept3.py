import requests # Импортирование библиотеки
import tkinter as tk # Импортирование библиотеки для графического оформления
from tkinter import messagebox, scrolledtext, font
from PIL import Image, ImageTk


def search_recipes_by_ingredients(api_key, ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": api_key,
        "ingredients": ingredients,
        "number": 5  # количество рецептов для возврата
    }

    response = requests.get(url, params=params) # Отправка GET-запроса к API

    if response.status_code == 200: # Код 200 - успешный запрос
        return response.json()
    else:
        messagebox.showerror("Ошибка", f"Ошибка API: {response.status_code}")
        return None # В случае ошибки возвращается None


def search_recipes():
    ingredients = entry_ingredients.get()
    if not ingredients:
        messagebox.showwarning("Внимание", "Пожалуйста, введите ингредиенты.")
        return

    recipes = search_recipes_by_ingredients(api_key, ingredients)

    if recipes:
        output_text.delete(1.0, tk.END)  # Очистить текстовое поле
        for recipe in recipes:
            output_text.insert(tk.END, f"Название рецепта: {recipe['title']}\n") # Выводим название рецепта
            output_text.insert(tk.END, f"ID рецепта: {recipe['id']}\n") # Выводим ID рецепта
            missed_ingredients = recipe.get('missedIngredients', []) # Получаем недостающие ингредиенты
            if missed_ingredients: # Если есть недостающие ингредиенты
                output_text.insert(tk.END,
                                   f"Недостающие ингредиенты: {', '.join([ingredient['name'] for ingredient in missed_ingredients])}\n")
            else:
                output_text.insert(tk.END, "Недостающих ингредиентов нет.\n")
            output_text.insert(tk.END, "-" * 40 + "\n")

api_key = "54da7e56bd9848478dd1c3c7b7fdd2c7" # Api ключ

# Создание окна
root = tk.Tk()
root.title("Поиск рецептов по ингредиентам")
root.geometry("600x400")

# Запрет на размеры окна
root.resizable(False, False)

# изображение
background_image = Image.open("C:\\Users\\Вадим\\Downloads\\images (1).jpg") # Открытие изображения
background_image = background_image.resize((600, 400), Image.LANCZOS) # Изменение размера изображения
background_photo = ImageTk.PhotoImage(background_image)

#метка фона
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Занять весь экран

# Создание шрифта
custom_font = font.Font(family="Helvetica", size=12)

# Создание виджетов
label_ingredients = tk.Label(root, text="Введите ингредиенты (через запятую):", bg='white', font=custom_font)
label_ingredients.pack(pady=10)  # Отступ сверху и снизу

entry_ingredients = tk.Entry(root, width=50, font=custom_font)
entry_ingredients.pack(pady=5)

button_search = tk.Button(root, text="Поиск рецептов", command=search_recipes, bg='#4CAF50', fg='white',
                          font=custom_font)
button_search.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=60, height=20, font=custom_font, bg='white', fg='black')
output_text.pack(pady=10)

# Запуск основного цикла приложения
root.mainloop()