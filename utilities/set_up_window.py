import tkinter as tk

class SetupWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetr.io Agent Setup")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        tk.Label(
            self.root,
            text="Configura el juego en Chrome.\nCuando estés listo, presiona el botón.",
            font=("Arial", 11),
            pady=20,
            justify="center"
        ).pack()

        tk.Button(
            self.root,
            text="✅ Listo, comenzar agente",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self.root.destroy
        ).pack()

        self.root.mainloop()