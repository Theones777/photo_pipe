import tkinter as tk
from tkinter import filedialog, messagebox
from config import Config
from exceptions import UserNotFoundError
from tg import TGClient


class TelegramSenderApp:
    def __init__(self, root):
        self.tg_client = TGClient(Config.BOT_TOKEN)
        self.root = root
        self.root.title("Отправка фото в Telegram")

        self.username_var = tk.StringVar()
        self.photo_dir = None

        # Поле ввода Telegram username
        tk.Label(root, text="Telegram username (без @):").pack(pady=(10, 0))
        tk.Entry(root, textvariable=self.username_var, width=40).pack(pady=5)

        # Кнопка выбора папки
        tk.Button(root, text="Выбрать папку с фото", command=self.select_folder).pack(pady=5)

        # Метка с выбранной папкой
        self.folder_label = tk.Label(root, text="Папка не выбрана", fg="gray")
        self.folder_label.pack()

        # Кнопка отправки
        tk.Button(root, text="Отправить", command=self.send_to_telegram).pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Выберите папку с фото")
        if folder:
            self.photo_dir = folder
            self.folder_label.config(text=folder, fg="black")
        else:
            self.folder_label.config(text="Папка не выбрана", fg="gray")

    def send_to_telegram(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Введите Telegram username")
            return

        if not self.photo_dir:
            messagebox.showerror("Ошибка", "Выберите папку с фото")
            return

        try:
            chat_id = self.tg_client.get_user_chat_id(f"@{username}")
            if not chat_id:
                raise UserNotFoundError()

            self.tg_client.send_to_telegram(chat_id, self.photo_dir)
            messagebox.showinfo("Успех", "Фото успешно отправлены!")

        except UserNotFoundError:
            messagebox.showerror("Ошибка", "Пользователь не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")
