import tkinter as tk

LIGHT_THEME = {
    "bg": "#ffffff",
    "fg": "#1f2937",
    "entry_bg": "#f9fafb",
    "entry_fg": "#111827",
    "button_bg": "#e5e7eb",
    "button_fg": "#111827",
    "button_active": "#3b82f6",
    "outgoing_bubble": "#dbeafe",
    "incoming_bubble": "#ede9fe",
    "bubble_text_fg": "#111827",
    "avatar_bg_self": "#3b82f6",
    "avatar_bg_other": "#9333ea",
    "avatar_text": "#ffffff",
    "canvas_bg": "#ffffff",
    "scrollbar_bg": "#d1d5db",
    "typing_fg": "#6b7280"
}

DARK_THEME = {
    "bg": "#0d1117",
    "fg": "#f9fafb",
    "entry_bg": "#161b22",
    "entry_fg": "#f9fafb",
    "button_bg": "#1f2937",
    "button_fg": "#f9fafb",
    "button_active": "#2563eb",
    "outgoing_bubble": "#2563eb",
    "incoming_bubble": "#7c3aed",
    "bubble_text_fg": "#ffffff",
    "avatar_bg_self": "#3b82f6",
    "avatar_bg_other": "#9333ea",
    "avatar_text": "#ffffff",
    "canvas_bg": "#0d1117",
    "scrollbar_bg": "#374151",
    "typing_fg": "#9ca3af"
}

def apply_theme(widget, theme):
    try:
        widget.configure(bg=theme.get("bg", "#ffffff"))
    except:
        pass

    for child in widget.winfo_children():
        try:
            if isinstance(child, tk.Frame):
                child.configure(bg=theme["bg"])
                apply_theme(child, theme)

            elif isinstance(child, tk.Label):
                child.configure(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    font=("Segoe UI", 10)
                )

            elif isinstance(child, tk.Text):
                child.configure(
                    bg=theme["entry_bg"],
                    fg=theme["entry_fg"],
                    insertbackground=theme["fg"],
                    relief="flat",
                    bd=1,
                    highlightthickness=1,
                    highlightbackground=theme["scrollbar_bg"]
                )

            elif isinstance(child, tk.Entry):
                child.configure(
                    bg=theme["entry_bg"],
                    fg=theme["entry_fg"],
                    insertbackground=theme["fg"],
                    relief="flat",
                    bd=1,
                    highlightthickness=1,
                    highlightbackground=theme["scrollbar_bg"],
                    highlightcolor=theme["button_active"]
                )

            elif isinstance(child, tk.Button):
                child.configure(
                    bg=theme["button_bg"],
                    fg=theme["button_fg"],
                    activebackground=theme["button_active"],
                    activeforeground="#ffffff",
                    relief="flat",
                    bd=0,
                    padx=12,
                    pady=6,
                    font=("Segoe UI", 10, "bold"),
                    cursor="hand2"
                )

            elif isinstance(child, tk.Canvas):
                child.configure(
                    bg=theme["canvas_bg"],
                    highlightthickness=0
                )

            elif isinstance(child, tk.Scrollbar):
                child.configure(
                    bg=theme["scrollbar_bg"],
                    troughcolor=theme["bg"]
                )

            elif isinstance(child, tk.Listbox):
                child.configure(
                    bg=theme["entry_bg"],
                    fg=theme["entry_fg"],
                    selectbackground=theme["button_active"],
                    bd=0
                )

            elif isinstance(child, tk.OptionMenu):
                child.configure(
                    bg=theme["button_bg"],
                    fg=theme["button_fg"]
                )

            elif isinstance(child, tk.Radiobutton):
                child.configure(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    selectcolor=theme["entry_bg"]
                )

        except:
            continue

def style_widget(widget, role, theme):
    if role == "chat_bubble_outgoing":
        widget.configure(
            bg=theme["outgoing_bubble"],
            fg=theme["bubble_text_fg"],
            bd=0,
            padx=12,
            pady=8,
            relief="flat",
            wraplength=360,
            justify="left",
            font=("Segoe UI", 10)
        )
        widget.master.configure(bg=theme["bg"])

    elif role == "chat_bubble_incoming":
        widget.configure(
            bg=theme["incoming_bubble"],
            fg=theme["bubble_text_fg"],
            bd=0,
            padx=12,
            pady=8,
            relief="flat",
            wraplength=360,
            justify="left",
            font=("Segoe UI", 10)
        )
        widget.master.configure(bg=theme["bg"])

    elif role == "avatar_self":
        widget.configure(bg=theme["avatar_bg_self"])

    elif role == "avatar_other":
        widget.configure(bg=theme["avatar_bg_other"])

    elif role == "typing":
        widget.configure(
            bg=theme["bg"],
            fg=theme["typing_fg"],
            font=("Segoe UI", 9, "italic")
        )