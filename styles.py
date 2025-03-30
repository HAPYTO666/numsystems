from number_systems import ttk

def setup_styles():
    style = ttk.Style()

    style.configure("TNotebook.Tab", font=('Arial', 10, 'bold'), padding=[10, 5])
    style.configure("Title.TLabel", font=('Arial', 14, 'bold'))
    style.configure("Subtitle.TLabel", font=('Arial', 12, 'bold'))
    style.configure("Theory.TFrame", background='#999999', relief="flat", anchor="center")
    style.configure("Correct.TLabel", foreground='green')
    style.configure("Incorrect.TLabel", foreground='red')
    style.configure("Disabled.TFrame", background='#f0f0f0')
    style.configure("Skipped.TLabel", foreground='blue')
    style.configure("Grade.TLabel", font=('Arial', 20, 'bold'))

    style.configure(
        'TButton',
        font=('Arial', 8, 'bold'),
        padding=2,
        relief='raised',
        background='#f0f0f0',
        foreground='#333333'
    )

    # Стиль при наведении
    style.map(
        'TButton',
        background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')],
        relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
    )

    # Для кнопки начать тест
    style.configure(
        'B.TButton',
        font=('Arial', 12, 'bold'),
        padding=5,
        relief='raised',
        background='#f0f0f0',
        foreground='#333333'
    )

    # Базовый стиль для всех полей ввода
    style.configure(
        'TEntry',
        font=('Arial', 11),
        padding=2,
        relief='solid',
        bordercolor='#cccccc',
        lightcolor='#ffffff',
        darkcolor='#f0f0f0',
        fieldbackground='#ffffff',
        foreground='#333333',
        insertcolor='#333333',
        insertwidth=2
    )

    # Стиль при фокусе
    style.map(
        'TEntry',
        bordercolor=[('focus', '#4CAF50'), ('!focus', '#cccccc')],
        lightcolor=[('focus', '#e8f5e9'), ('!focus', '#ffffff')],
        darkcolor=[('focus', '#e8f5e9'), ('!focus', '#f0f0f0')]
    )

    # Стиль для неактивного состояния
    style.configure(
        'Disabled.TEntry',
        fieldbackground='#f5f5f5',
        foreground='#999999'
    )