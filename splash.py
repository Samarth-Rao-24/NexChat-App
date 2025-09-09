import tkinter as tk
from PIL import Image, ImageTk

def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("400x300")
    splash.configure(bg="#1e1e1e")

    try:
        logo_raw = Image.open("assets/icons/logo.png")
        logo_raw = logo_raw.resize((180, 60), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_raw)
        tk.Label(splash, image=logo_img, bg="#1e1e1e").pack(pady=30)
    except:
        tk.Label(splash, text="NEXCHAT", font=("Segoe UI", 20, "bold"), fg="white", bg="#1e1e1e").pack(pady=30)

    tk.Label(splash, text="SmartChat", font=("Segoe UI", 18), fg="white", bg="#1e1e1e").pack()
    splash.after(2000, splash.destroy)
    splash.mainloop()