import tkinter as tk
from ui_utils import LIGHT_THEME, DARK_THEME

def create_reaction_bar(parent_frame, on_react, theme=DARK_THEME, reactions=None):
    if reactions is None:
        reactions = ["👍", "❤️", "😂", "🔥", "😮"]

    bar = tk.Frame(parent_frame, bg=theme.get("bg"))
    bar.pack(side=tk.BOTTOM, pady=4)

    def on_enter(btn):
        btn.config(bg=theme.get("button_active"))

    def on_leave(btn):
        btn.config(bg=theme.get("button_bg"), fg=theme.get("button_fg"))

    for emoji in reactions:
        btn = tk.Button(
            bar,
            text=emoji,
            font=("Segoe UI Emoji", 12),
            width=3,
            relief="flat",
            bd=0,
            bg=theme.get("button_bg"),
            fg=theme.get("button_fg"),
            activebackground=theme.get("button_active"),
            cursor="hand2",
            command=lambda e=emoji: on_react(e),
        )
        btn.pack(side=tk.LEFT, padx=2)
        btn.bind("<Enter>", lambda e, b=btn: on_enter(b))
        btn.bind("<Leave>", lambda e, b=btn: on_leave(b))

    return bar