import random
import tkinter as tk
from tkinter import ttk

import questions
import styles
import theory


def center_window(window, width=None, height=None):
    """Центрирует окно на экране"""
    if width is None or height is None:
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y-25}')

def get_questions():
    return (random.sample(questions.easy, 5) + random.sample(questions.mid, 3)
            + random.sample(questions.hard, 2))
class NumberSystemsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обучающе-контролирующая программа 'Системы счисления'")
        self.root.geometry("1100x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#ffffff", relief="flat")
        self.test_questions = get_questions()

        # Настройка стилей
        styles.setup_styles()

        self.current_question = 0
        self.correct_answers = 0
        self.test_in_progress = False
        self.skipped_questions = []
        self.user_answers = [None] * len(self.test_questions)

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)

        # Вкладка "Теория"
        self.theory_tab = ttk.Frame(self.notebook)
        self.add_theory_content(self.theory_tab)

        # Вкладка "Практика"
        self.practice_tab = ttk.Frame(self.notebook)
        self.add_practice_content(self.practice_tab)

        # Вкладка "Тесты"
        self.tests_tab = ttk.Frame(self.notebook)
        self.add_tests_content(self.tests_tab)

        self.notebook.add(self.theory_tab, text="Теория")
        self.notebook.add(self.practice_tab, text="Калькулятор")
        self.notebook.add(self.tests_tab, text="Тесты")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Начинаем с вкладки теории
        self.notebook.select(0)

        self.status_bar = ttk.Label(self.root, text="Готово к работе", relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, padx=5, pady=5)

    def toggle_test_mode(self, active):
        """Блокирует или разблокирует вкладки теории и практики"""
        if not hasattr(self, 'notebook'):
            return

        self.test_in_progress = active

        if active:
            # Блокируем другие вкладки
            self.notebook.tab(0, state="disabled")
            self.notebook.tab(1, state="disabled")
            # Добавляем стиль заблокированных вкладок
            self.theory_tab.configure(style="Disabled.TFrame")
            self.practice_tab.configure(style="Disabled.TFrame")
        else:
            # Разблокируем вкладки
            self.notebook.tab(0, state="normal")
            self.notebook.tab(1, state="normal")
            # Возвращаем обычный стиль
            self.theory_tab.configure(style="Theory.TFrame")
            self.practice_tab.configure(style="TFrame")

    def add_theory_content(self, tab):
        # Главный контейнер с прокруткой
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_frame)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Привязываем прокрутку колесиком мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="top", fill="both", expand=True, anchor="center")

        # Содержимое теории
        th = theory.theory
        for block in th:
            self.add_section(title=block[0], content=block[1])

    def _on_mousewheel(self, event):
        """Обработчик прокрутки колесиком мыши"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_section(self, title, content):
        """Добавляет раздел теории с заголовком и содержанием"""
        frame = ttk.Frame(self.scrollable_frame, style="Theory.TFrame", padding=10, relief='groove')
        frame.pack(anchor="center")

        ttk.Label(frame, text=title, style="Subtitle.TLabel", background='#999999').pack(anchor="center")

        text = tk.Text(frame, wrap=tk.WORD, font=('Arial', 11),
                       padx=5, pady=5, height=content.count('\n') + 3)
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.X)

    def add_practice_content(self, tab):
        values = ['2', '8', '10', '16']

        frame = ttk.Frame(tab, relief="flat")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Калькулятор", style="Title.TLabel", padding=2, relief="flat").pack(padx=5, pady=5)

        # Создаем основной контейнер для разделения на левую и правую части
        main_container = ttk.Frame(frame)
        main_container.pack(fill=tk.BOTH, expand=True, pady=15)

        # Левый фрейм для перевода
        left_frame = ttk.Frame(main_container, relief="solid", borderwidth=1)
        left_frame.pack(side=tk.TOP, fill=tk.X, padx=20)

        # Поля ввода в левом фрейме
        input_frame = ttk.Frame(left_frame)
        input_frame.pack(pady=5)C:\Users\family\PycharmProjects\num_systems

        ttk.Label(input_frame, text="Число:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.number_entry = ttk.Entry(input_frame, width=20, font=('Arial', 11))
        self.number_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Из системы:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.from_base = ttk.Combobox(input_frame, values=values, width=5, font=('Arial', 11))
        self.from_base.grid(row=1, column=1, padx=5, pady=5)
        self.from_base.current(2)  # По умолчанию 10

        ttk.Label(input_frame, text="В систему:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
        self.to_base = ttk.Combobox(input_frame, values=values, width=5, font=('Arial', 11))
        self.to_base.grid(row=1, column=3, padx=5, pady=5)
        self.to_base.current(0)  # По умолчанию 2

        # Кнопка перевода в левом фрейме
        self.convert_button = ttk.Button(left_frame, text="Перевести", command=self.convert_number,
                                         style="TButton")
        self.convert_button.pack()

        # Кнопка случайного примера в левом фрейме
        self.random_button = ttk.Button(left_frame, text="Случайный пример", command=self.generate_random_example,
                                        style="TButton")
        self.random_button.pack(pady=5)

        # Правый фрейм для результата
        right_frame = ttk.Frame(main_container)
        right_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Фрейм результата в правом фрейме
        self.result_frame = ttk.Frame(right_frame)
        self.result_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(self.result_frame, text="Результат:", font=('Arial', 12)).pack(side=tk.LEFT)
        self.result_label = ttk.Label(self.result_frame, text="", font=('Arial', 12, 'bold'))
        self.result_label.pack(side=tk.LEFT, padx=5)

    def add_tests_content(self, tab):
        self.test_frame = ttk.Frame(tab, relief='solid', padding=10)
        self.test_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        self.test_question_var = tk.StringVar()
        self.test_answer_var = tk.StringVar()

        # Начальный экран теста
        ttk.Label(self.test_frame, text="Контрольный тест по системам счисления",
                  style="Title.TLabel").pack(pady=10)
        ttk.Label(self.test_frame, text="Тест содержит 10 вопросов по теме систем счисления",
                  font=('Arial', 11)).pack()
        ttk.Label(self.test_frame, text="Для начала теста нажмите кнопку ниже",
                  font=('Arial', 11)).pack()

        self.bt_frame = ttk.Frame(tab)
        self.bt_frame.pack(fill=tk.X, padx=10, pady=10)
        start_button = ttk.Button(self.bt_frame, text="Начать тест",
                                  command=self.start_test, style="B.TButton")
        start_button.pack(pady=20)

    def start_test(self):
        """Начинает тестирование"""

        self.current_question = 0
        self.correct_answers = 0
        self.skipped_questions = []
        self.user_answers = [None] * len(self.test_questions)
        self.toggle_test_mode(True)
        self.notebook.select(2)  # Переключаемся на вкладку тестов
        self.show_question(0)

    def show_question(self, question_num):
        for widget in self.test_frame.winfo_children():
            widget.destroy()

        if question_num >= len(self.test_questions):
            self.show_test_results()
            return

        self.current_question = question_num
        question_data = self.test_questions[question_num]

        # Показываем номер вопроса и прогресс
        progress_frame = ttk.Frame(self.test_frame)
        progress_frame.pack(fill=tk.X, pady=5)

        ttk.Label(progress_frame,
                  text=f"Вопрос {question_num + 1} из {len(self.test_questions)}",
                  style="Subtitle.TLabel").pack(side=tk.TOP)

        # Прогресс бар
        progress = ttk.Progressbar(progress_frame, orient="horizontal", length=200)
        progress.pack(side=tk.TOP)
        progress["value"] = f'{(question_num + 1) * 10.0}'

        # Показываем текст вопроса
        ttk.Label(self.test_frame, text=question_data["question"],
                  font=('Arial', 12), wraplength=800).pack(anchor=tk.W, pady=10)

        # Варианты ответов
        options_frame = ttk.Frame(self.test_frame, relief="solid")
        options_frame.pack(anchor=tk.W, padx=10, fill=tk.X)

        # Восстанавливаем предыдущий ответ, если он был
        if self.user_answers[question_num] is not None:
            self.test_answer_var.set(str(self.user_answers[question_num]))
        else:
            self.test_answer_var.set("")

        # варианты ответов
        for i, option in enumerate(question_data["options"]):
            ttk.Radiobutton(options_frame, text=option, variable=self.test_answer_var,
                            value=option).grid(row=i, column=0, sticky=tk.W, pady=3, padx=5)

        # Кнопки навигации
        button_frame = ttk.Frame(self.test_frame)
        button_frame.pack(pady=15)

        if question_num > 0:
            ttk.Button(button_frame, text="← Назад",
                       command=lambda: self.prev_question()).pack(side=tk.LEFT, padx=5)

        if question_num < len(self.test_questions) - 1:
            ttk.Button(button_frame, text="Пропустить →",
                       command=lambda: self.skip_question()).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Следующий →",
                       command=lambda: self.next_question()).pack(side=tk.RIGHT, padx=5)
        else:
            ttk.Button(button_frame, text="Завершить тест",
                       command=lambda: self.next_question()).pack(side=tk.RIGHT, padx=5)

    def prev_question(self):
        self.save_answer()
        self.show_question(self.current_question - 1)

    def next_question(self):
        self.save_answer()
        self.show_question(self.current_question + 1)

    def skip_question(self):
        self.save_answer()
        if self.current_question not in self.skipped_questions:
            self.skipped_questions.append(self.current_question)
        self.show_question(self.current_question + 1)

    def save_answer(self):
        """Сохраняет текущий ответ"""
        self.user_answers[self.current_question] = self.test_answer_var.get()

    def check_answer(self, question_idx):
        """Проверяет ответ на конкретный вопрос"""
        question_data = self.test_questions[question_idx]
        user_answer = self.user_answers[question_idx]

        if user_answer == question_data["answer"]:
            return True
        return False

    def calculate_grade(self, percentage):
        """Вычисляет оценку от 2 до 5 на основе процента правильных ответов"""
        if percentage >= 95:
            return 5
        elif percentage >= 75:
            return 4
        elif percentage >= 60:
            return 3
        else:
            return 2

    def show_test_results(self):
        for widget in self.test_frame.winfo_children():
            widget.destroy()

        # Проверяем все ответы
        self.correct_answers = 0
        for i in range(len(self.test_questions)):
            if self.check_answer(i):
                self.correct_answers += 1

        percentage = int(round(self.correct_answers / len(self.test_questions) * 100))
        grade = self.calculate_grade(percentage)

        # Показываем результаты
        ttk.Label(self.test_frame, text="Тест завершён!", style="Title.TLabel").pack(pady=10)

        ttk.Label(self.test_frame,
                  text=f"Результат: {percentage}% ({self.correct_answers} из {len(self.test_questions)})",
                  font=('Arial', 14, 'bold')).pack(pady=5)

        ttk.Label(self.test_frame,
                  text=f"Оценка: {grade}",
                  style="Grade.TLabel").pack(pady=10)

        if grade == 5:
            result_text = "Отлично! Вы прекрасно разбираетесь в системах счисления."
        elif grade == 4:
            result_text = "Хорошо! Есть небольшие пробелы в знаниях."
        elif grade == 3:
            result_text = "Удовлетворительно. Рекомендуется повторить теорию."
        else:
            result_text = "Неудовлетворительно. Вам нужно изучить тему заново."

        ttk.Label(self.test_frame, text=result_text, wraplength=800).pack(pady=10)

        # Показываем пропущенные вопросы, если они есть
        if self.skipped_questions:
            skipped_frame = ttk.Frame(self.test_frame)
            skipped_frame.pack(pady=10)

            ttk.Label(skipped_frame, text="Пропущенные вопросы:", style="Subtitle.TLabel").pack()

            for idx in self.skipped_questions:
                q_num = idx + 1
                ttk.Button(skipped_frame, text=f"Вопрос {q_num}",
                           command=lambda i=idx: self.return_to_question(i),
                           style="Skipped.TLabel").pack(side=tk.LEFT, padx=5)

        # Кнопки действий
        button_frame = ttk.Frame(self.test_frame)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Пройти тест снова",
                   command=self.restart_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Вернуться к теории",
                   command=self.return_to_theory).pack(side=tk.LEFT, padx=5)

        # Выключаем режим тестирования
        self.toggle_test_mode(False)

    def return_to_question(self, question_idx):
        """Возвращает к указанному вопросу"""
        self.toggle_test_mode(True)
        self.notebook.select(2)
        self.show_question(question_idx)

    def restart_test(self):
        """Перезапускает тест"""
        self.start_test()
        # новые вопросы
        self.test_questions = get_questions()

    def return_to_theory(self):
        """Возвращает к теории"""
        self.notebook.select(0)

    def convert_number(self):
        try:
            num = self.number_entry.get().strip().upper()
            from_base = int(self.from_base.get())
            to_base = int(self.to_base.get())

            if from_base != 10:
                decimal_num = int(num, from_base)
            else:
                decimal_num = int(num)

            if to_base == 10:
                result = str(decimal_num)
            else:
                digits = []
                n = decimal_num
                while n > 0:
                    n, remainder = divmod(n, to_base)
                    digits.append(hex(remainder)[2:].upper())
                result = ''.join(reversed(digits)) if digits else "0"

            self.result_label.config(text=result, foreground="green")
        except ValueError:
            self.result_label.config(text="Вы ввели неверное число!", foreground="red")
        except Exception as e:
            self.result_label.config(text="Ошибка вычисления", foreground="red")

    def generate_random_example(self):
        bases = [2, 8, 10, 16]
        from_base = random.choice(bases)
        to_base = random.choice([b for b in bases if b != from_base])

        if from_base == 10:
            num = str(random.randint(10, 100))
        else:
            digits = "0123456789ABCDEF"[:from_base]
            num = ''.join(random.choice(digits) for _ in range(random.randint(2, 4)))

        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, num)
        self.from_base.set(from_base)
        self.to_base.set(to_base)
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberSystemsApp(root)

    try:
        img = tk.PhotoImage(file="icon.png")
        root.iconphoto(True, img)
    except Exception as e:
        print(f"Не удалось загрузить иконку: {e}")

    center_window(root)
    root.mainloop()
    