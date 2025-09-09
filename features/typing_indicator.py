def bind_typing_indicator(entry_widget, label_widget, root, message="Typing...", delay=1500):
    state = {"after_id": None}

    def clear_label():
        label_widget.config(text="")
        state["after_id"] = None

    def on_typing(event):
        if state["after_id"] is not None:
            root.after_cancel(state["after_id"])
        label_widget.config(text=message)
        state["after_id"] = root.after(delay, clear_label)

    entry_widget.bind("<Key>", on_typing)