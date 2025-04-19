import tkinter as tk

from tkinter_client import TelegramSenderApp


if __name__ == '__main__':
    root = tk.Tk()
    app = TelegramSenderApp(root)
    root.mainloop()
