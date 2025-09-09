import ctypes
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from firebase_config import login_user, send_message, fetch_messages
from ui_utils import apply_theme
from features.typing_indicator import bind_typing_indicator
from features.offline_queue import queue_message, flush_queue
from splash import show_splash

LIGHT_THEME = {
    "bg": "#FFFDEB",
    "fg": "#3F7A9C",
    "entry_bg": "#FFFFFF",
    "entry_fg": "#3F7A9C",
    "button_bg": "#9ED2EC",
    "button_fg": "#3F7A9C",
    "button_active": "#6B91B6",
    "outgoing_bubble": "#9ED2EC",
    "incoming_bubble": "#6B91B6",
    "typing_fg": "#3F7A9C",
    "avatar_bg_self": "#3F7A9C",
    "avatar_bg_other": "#6B91B6",
    "avatar_text": "#FFFDEB",
    "bubble_text_fg": "#FFFDEB",
    "canvas_bg": "#FFFDEB"
}

DARK_THEME = {
    "bg": "#3F7A9C",
    "fg": "#FFFDEB",
    "entry_bg": "#6B91B6",
    "entry_fg": "#FFFDEB",
    "button_bg": "#6B91B6",
    "button_fg": "#FFFDEB",
    "button_active": "#9ED2EC",
    "outgoing_bubble": "#9ED2EC",
    "incoming_bubble": "#6B91B6",
    "typing_fg": "#FFFDEB",
    "avatar_bg_self": "#9ED2EC",
    "avatar_bg_other": "#6B91B6",
    "avatar_text": "#3F7A9C",
    "bubble_text_fg": "#FFFDEB",
    "canvas_bg": "#3F7A9C"
}

current_user = None
current_theme = DARK_THEME
selected_server = "general"
REFRESH_INTERVAL_MS = 3000
FLUSH_QUEUE_INTERVAL_MS = 5000
_refresh_after_id = None
_flush_after_id = None
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

def set_fixed_window(window: tk.Tk, title: str = "NexChat") -> None:
    window.title(title)
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    window.resizable(False, False)
    window.update_idletasks()
    sw, sh = window.winfo_screenwidth(), window.winfo_screenheight()
    x, y = (sw // 2) - (WINDOW_WIDTH // 2), (sh // 2) - (WINDOW_HEIGHT // 2)
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

def toggle_theme() -> None:
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme(root, current_theme)

def handle_login() -> None:
    global current_user
    email = email_entry.get().strip()
    password = password_entry.get()
    if not email or not password:
        messagebox.showwarning("Missing credentials", "Please enter both email and password.")
        return
    user = login_user(email, password)
    if user:
        current_user = user
        login_frame.destroy()
        show_server_selector()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials or network error.")

def get_initials(sender: str) -> str:
    if not sender:
        return "??"
    try:
        base = sender.split("@")[0]
        parts = base.replace(".", " ").split()
        return (parts[0][0] + parts[1][0]).upper() if len(parts) >= 2 else parts[0][:2].upper()
    except:
        return sender[:2].upper()

def safe_fetch_messages():
    try:
        data = fetch_messages(selected_server) or {}
        return [msg for msg in data.values() if isinstance(msg, dict) and msg.get("message")]
    except Exception as e:
        print("⚠️ Fetch error:", e)
        return []

def show_chat_window():
    global _refresh_after_id, _flush_after_id
    set_fixed_window(root, f"NexChat – {selected_server.capitalize()}")
    for w in root.winfo_children():
        w.destroy()
    chat_frame = tk.Frame(root, bg=current_theme["bg"])
    chat_frame.pack(fill="both", expand=True)
    canvas = tk.Canvas(chat_frame, bg=current_theme["bg"], highlightthickness=0)
    vsb = tk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    messages_frame = tk.Frame(canvas, bg=current_theme["bg"])
    window_id = canvas.create_window((0, 0), window=messages_frame, anchor="nw")
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window_id, width=event.width)
    messages_frame.bind("<Configure>", on_configure)
    typing_label = tk.Label(chat_frame, text="", font=("Segoe UI", 9),
                            bg=current_theme["bg"], fg=current_theme["typing_fg"])
    typing_label.pack(side=tk.BOTTOM, anchor="w", padx=16, pady=(0, 6))
    input_holder = tk.Frame(chat_frame, bg=current_theme["bg"])
    input_holder.pack(side=tk.BOTTOM, fill="x", padx=20, pady=14)
    message_entry = tk.Entry(input_holder, font=("Segoe UI", 13),
                             bg=current_theme["entry_bg"], fg=current_theme["entry_fg"],
                             relief="flat", bd=2, highlightthickness=1,
                             highlightbackground=current_theme["bg"],
                             highlightcolor=current_theme["button_active"])
    message_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10), ipady=14)
    message_entry.focus_set()
    def send_message_from_entry(entry_widget: tk.Entry):
        text = entry_widget.get().strip()
        if not text or not current_user:
            return
        if send_message(current_user["localId"], text, selected_server):
            entry_widget.delete(0, tk.END)
            refresh_messages()
        else:
            queue_message(current_user["localId"], text)
            messagebox.showinfo("Offline Mode", "Message queued. Will send when online.")
            entry_widget.delete(0, tk.END)
    send_btn = tk.Button(input_holder, text="➤",
                         command=lambda: send_message_from_entry(message_entry),
                         bg=current_theme["button_bg"], fg=current_theme["button_fg"],
                         relief="flat", font=("Segoe UI", 12, "bold"),
                         padx=16, pady=10)
    send_btn.pack(side=tk.LEFT)
    message_entry.bind("<Return>", lambda ev: send_message_from_entry(message_entry))
    bind_typing_indicator(message_entry, typing_label, root)
    emoji_frame = tk.Frame(chat_frame, bg=current_theme["bg"])
    emoji_frame.pack(side=tk.BOTTOM, pady=(0, 8))
    def insert_emoji(emoji: str):
        message_entry.insert(tk.END, emoji)
        message_entry.focus_set()
    for e in ["😀", "😂", "❤️", "👍", "🔥"]:
        tk.Button(emoji_frame, text=e, command=lambda e=e: insert_emoji(e),
                  relief="flat", bg=current_theme["button_bg"], fg=current_theme["fg"],
                  font=("Segoe UI", 12), padx=8, pady=6).pack(side=tk.LEFT, padx=4)
    def refresh_messages():
        global _refresh_after_id
        for child in messages_frame.winfo_children():
            child.destroy()

        messages = safe_fetch_messages()
        messages.sort(key=lambda m: m.get("timestamp", ""), reverse=True)  # newest first

        if not messages:
            tk.Label(messages_frame, text="No messages yet. Say hello 👋",
                 bg=current_theme["bg"], fg=current_theme["fg"],
                 font=("Segoe UI", 10, "italic")).pack(pady=12)
        else:
            for msg in messages:
                sender = msg.get("sender", "Unknown")
                text = msg.get("message", "")
                timestamp = msg.get("timestamp", "")
                is_self = current_user and (
                    sender == current_user.get("localId") or
                    sender == current_user.get("email") or
                    sender == current_user.get("displayName")
                )

                row = tk.Frame(messages_frame, bg=current_theme["bg"])
                row.pack(fill="x", pady=6, padx=12)

                avatar = tk.Canvas(row, width=36, height=36,
                                bg=current_theme.get("canvas_bg"), highlightthickness=0)
                avatar_color = current_theme.get("avatar_bg_self") if is_self else current_theme.get("avatar_bg_other")
                avatar.create_oval(2, 2, 34, 34, fill=avatar_color, outline="")
                avatar.create_text(18, 18, text=get_initials(sender),
                               fill=current_theme.get("avatar_text"), font=("Segoe UI", 9, "bold"))

                bubble_bg = current_theme.get("outgoing_bubble") if is_self else current_theme.get("incoming_bubble")
                bubble_fg = current_theme.get("bubble_text_fg", current_theme["fg"])
                bubble = tk.Label(row, text=f"{timestamp}\n{text}", bg=bubble_bg, fg=bubble_fg,
                              wraplength=700, justify="left", font=("Segoe UI", 11),
                              padx=14, pady=10, bd=0, relief="flat")

                if is_self:
                    tk.Frame(row, bg=current_theme["bg"]).pack(side=tk.LEFT, fill="x", expand=True)
                    bubble.pack(side=tk.RIGHT, anchor="e", padx=(4, 0))
                    avatar.pack(side=tk.RIGHT, padx=(4, 8))
                else:
                    avatar.pack(side=tk.LEFT, padx=(0, 8))
                    bubble.pack(side=tk.LEFT, anchor="w")

        canvas.yview_moveto(0.0)  # stay at the newest (top)
        _refresh_after_id = root.after(REFRESH_INTERVAL_MS, refresh_messages)
    apply_theme(chat_frame, current_theme)
    refresh_messages()
    def periodic_flush():
        global _flush_after_id
        try:
            flush_queue(root)
        except Exception as e:
            print("⚠️ flush_queue error:", e)
        _flush_after_id = root.after(FLUSH_QUEUE_INTERVAL_MS, periodic_flush)
    periodic_flush()

def show_server_selector():
    set_fixed_window(root, "Select Server")
    for w in root.winfo_children():
        w.destroy()
    selector_frame = tk.Frame(root, bg=current_theme["bg"])
    selector_frame.pack(fill="both", expand=True)
    tk.Label(selector_frame, text="Choose a Server", font=("Segoe UI", 14, "bold"),
             bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=30)
    servers = ["General", "projectX", "teamchat"]
    for name in servers:
        tk.Button(selector_frame, text=name.capitalize(),
                  command=lambda n=name: enter_server(n),
                  width=20, font=("Segoe UI", 11, "bold"),
                  bg=current_theme["button_bg"], fg=current_theme["button_fg"],
                  activebackground=current_theme["button_active"]).pack(pady=10)
    tk.Button(selector_frame, text="Toggle Theme", command=toggle_theme,
              font=("Segoe UI", 10), bg=current_theme["button_bg"], fg=current_theme["button_fg"]).pack(pady=20)

def enter_server(name):
    global selected_server
    selected_server = name
    show_chat_window()

show_splash()
root = tk.Tk()
set_fixed_window(root, "NexChat Login")
try:
    root.iconphoto(False, tk.PhotoImage(file="assets/icons/logo.png"))
except:
    pass
try:
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
    style &= ~0x00020000
    style &= ~0x00010000
    ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
except:
    pass
login_frame = tk.Frame(root, bg=current_theme["bg"])
login_frame.pack(fill="both", expand=True)
try:
    logo_raw = Image.open("assets/icons/logo.png")
    logo_raw = logo_raw.resize((200, 70), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo_raw)
    tk.Label(login_frame, image=logo_img, bg=current_theme["bg"]).pack(pady=(20, 10))
except Exception as e:
    print("⚠️ Logo load failed:", e)
    tk.Label(login_frame, text="NEXCHAT", font=("Segoe UI", 22, "bold"),
             bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=(30, 12))
tk.Label(login_frame, text="Email", bg=current_theme["bg"], fg=current_theme["fg"],
         font=("Segoe UI", 11)).pack(pady=(6, 0))
email_entry = tk.Entry(login_frame, width=40, font=("Segoe UI", 11),
                       bg=current_theme["entry_bg"], fg=current_theme["entry_fg"])
email_entry.pack(pady=6, ipady=6)
tk.Label(login_frame, text="Password", bg=current_theme["bg"], fg=current_theme["fg"],
         font=("Segoe UI", 11)).pack(pady=(6, 0))
password_entry = tk.Entry(login_frame, show="*", width=40, font=("Segoe UI", 11),
                          bg=current_theme["entry_bg"], fg=current_theme["entry_fg"])
password_entry.pack(pady=6, ipady=6)
tk.Button(login_frame, text="Login", command=handle_login, width=18,
          font=("Segoe UI", 11, "bold"), bg=current_theme["button_bg"], fg=current_theme["button_fg"]).pack(pady=(16, 8))
tk.Button(login_frame, text="Toggle Theme", command=toggle_theme, width=18,
          font=("Segoe UI", 10), bg=current_theme["button_bg"], fg=current_theme["button_fg"]).pack()
tips = [
    "Tip: Use emojis to express yourself 🔥",
    "Did you know? NexChat supports offline messaging 📦",
    "Toggle between light and dark themes for the perfect vibe 🌗",
    "Your messages are timestamped in UTC for global clarity 🌍",
    "Tip: Mention someone with @ to grab their attention instantly 📣",
    "Fun Fact: NexChat syncs across all your devices — magic in the cloud ☁️",
    "Did you know? You can pin important messages for easy access 📌",
    "Power Users Love: Slash commands make things faster ⚡",
    "Keep it clean: Messages auto-expire in secret mode 🕵️‍♂️",
    "Keyboard Ninja? Shortcuts are your best friend ⌨️💨",
    "No Wi-Fi? No problem. Messages queue and send later 🚀"
]
tk.Label(login_frame, text=random.choice(tips),
         font=("Segoe UI", 12, "italic"),
         fg=current_theme["typing_fg"],
         bg=current_theme["bg"]).pack(pady=(12, 0))
apply_theme(root, current_theme)
root.mainloop()
