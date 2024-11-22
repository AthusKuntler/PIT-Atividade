import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass, asdict
from PIL import Image, ImageTk
import json
import re

# Constants for UI
class UIConstants:
    BG_COLOR = "#f8f8f8"
    BUTTON_COLOR_GREEN = "#4CAF50"
    BUTTON_COLOR_BLUE = "#2196F3"
    BUTTON_COLOR_ORANGE = "#FF9800"
    FONT_TITLE = ("Arial", 18, "bold")
    FONT_LABEL = ("Arial", 12)

@dataclass
class Cupcake:
    name: str
    price: float
    image: str

@dataclass
class User:
    name: str
    password: str

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Vendas de Cupcakes")
        self.root.geometry("400x600")
        self.current_frame = None
        self.users = {}  # Dictionary to store users
        self.cart = []  # List to store cart items
        self.image_references = []  # Initialize image references here
        self.logged_in_user = None # Track do Usuario   
        self.load_users()  # Load users from file if exists
        self.show_home_screen()

    def load_users(self):
        # Load users from a JSON file if it exists
        try:
            with open('users.json', 'r') as f:
                user_data = json.load(f)
                self.users = {email: User(**data) for email, data in user_data.items()}
        except FileNotFoundError:
            self.users = {}

    def save_users(self):
        # Convert users to JSON serializable format
        user_data = {email: asdict(user) for email, user in self.users.items()}
        with open('users.json', 'w') as f:
            json.dump(user_data, f)

    def create_label(self, parent, text, font=None, bg=None):
        label = tk.Label(parent , text=text, font=font, bg=bg)
        label.pack(pady=5)
        return label

    def show_home_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=UIConstants.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_label(self.current_frame, "Bem-vindo ao Sistema de Vendas de Cupcakes", font=UIConstants.FONT_TITLE, bg=UIConstants.BG_COLOR)
        tk.Button(self.current_frame, text="Registrar", command=self.show_registration_screen, bg=UIConstants.BUTTON_COLOR_GREEN, fg="white", width=20).pack(pady=10)
        tk.Button(self.current_frame, text="Login", command=self.show_login_screen, bg=UIConstants.BUTTON_COLOR_BLUE, fg="white", width=20).pack(pady=10)
        tk.Button(self.current_frame, text="Ver Catálogo", command=self.show_catalog_screen, bg=UIConstants.BUTTON_COLOR_ORANGE, fg="white", width=20).pack(pady=10)

    def show_registration_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=UIConstants.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_label(self.current_frame, "Registro de Cliente", font=UIConstants.FONT_TITLE, bg=UIConstants.BG_COLOR)
        self.create_label(self.current_frame, "Nome:", bg=UIConstants.BG_COLOR)
        self.name_entry = tk.Entry(self.current_frame)
        self.name_entry.pack(pady=5)

        self.create_label(self.current_frame, "E-mail:", bg=UIConstants.BG_COLOR)
        self.email_entry = tk.Entry(self.current_frame)
        self.email_entry.pack(pady=5)

        self.create_label(self.current_frame, "Senha:", bg=UIConstants.BG_COLOR)
        self.password_entry = tk.Entry(self.current_frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.current_frame, text="Voltar", command=self.show_home_screen,bg=UIConstants.BUTTON_COLOR_GREEN,fg="white").pack(pady=20)
        tk.Button(self.current_frame, text="Registrar", command=self.register_user, bg=UIConstants.BUTTON_COLOR_GREEN, fg="white").pack(pady=20)

    def show_login_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=UIConstants.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_label(self.current_frame, "Login de Cliente", font=UIConstants.FONT_TITLE, bg=UIConstants.BG_COLOR)
        self.create_label(self.current_frame, "E-mail:", bg=UIConstants.BG_COLOR)
        self.email_entry = tk.Entry(self.current_frame)
        self.email_entry.pack(pady=5)

        self.create_label(self.current_frame, "Senha:", bg=UIConstants.BG_COLOR)
        self.password_entry = tk.Entry(self.current_frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.current_frame, text="Entrar", command=self.login_user, bg=UIConstants.BUTTON_COLOR_BLUE, fg="white").pack(pady=20)
        tk.Button(self.current_frame, text="Voltar", command=self.show_home_screen, bg=UIConstants.BUTTON_COLOR_GREEN, fg="white").pack(pady=10)

    def show_catalog_screen(self):
        if self.logged_in_user is None: 
            messagebox.showwarning("Acesso Negado", "Você precisa estar logado para acessar o catálogo.")
            self.show_login_screen()
            return
        
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=UIConstants.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_label(self.current_frame, "Catálogo de Cupcakes", font=UIConstants.FONT_TITLE, bg=UIConstants.BG_COLOR)

        self.cupcakes = [
            Cupcake("Cupcake de Chocolate", 5.00, "CupcakeChocolate.png"),
            Cupcake("Cupcake de Baunilha", 4.50, "CupcakeBaunilha.png"),
            Cupcake("Cupcake de Red Velvet", 6.00, "CupcakeRedVelvet.png")
        ]

        # Store references to the images
        self.image_references = []

        for cupcake in self.cupcakes:
            frame = tk.Frame(self.current_frame, bg=UIConstants.BG_COLOR)
            frame.pack(pady=10)

            try:
                # Open the image using Pillow
                pil_image = Image.open(cupcake.image)
                pil_image = pil_image.resize((100, 100), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(pil_image)
                self.image_references.append(tk_image)
                image_label = tk.Label(frame, image=tk_image, bg=UIConstants.BG_COLOR)
                image_label.pack(side=tk.LEFT )
            except Exception as e:
                print(f"Error loading image {cupcake.image}: {e}")

            self.create_label(frame, f"{cupcake.name} - R$ {cupcake.price:.2f}", bg=UIConstants.BG_COLOR)
            tk.Button(frame, text="Adicionar ao Carrinho", command=lambda c=cupcake: self.add_to_cart(c), bg=UIConstants.BUTTON_COLOR_ORANGE, fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(self.current_frame, text="Voltar", command=self.show_home_screen, bg=UIConstants.BUTTON_COLOR_GREEN, fg="white").pack(pady=10)

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in self.users:
            messagebox.showerror("Erro", "E-mail já cadastrado!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Erro", "E-mail inválido!")
            return

        self.users[email] = User(name, password)
        self.save_users()
        messagebox.showinfo("Registro", "Usuário registrado com sucesso!")
        self.show_home_screen()

    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        user = self.users.get(email)
        if user is None or user.password != password:
            messagebox.showerror("Erro", "E-mail ou senha inválidos!")
            return
        self.logged_in_user = user
        messagebox.showinfo("Login", "Login bem-sucedido!")
        self.show_catalog_screen()

    def add_to_cart(self, cupcake):
        self.cart.append(cupcake)
        messagebox.showinfo("Carrinho", "Cupcake adicionado ao carrinho!")
        self.show_payment_screen()  # Redireciona para a tela de pagamento

    def show_payment_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=UIConstants.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_label(self.current_frame, "Tela de Pagamento", font=UIConstants.FONT_TITLE, bg=UIConstants.BG_COLOR)

        self.create_label(self.current_frame, "Total a Pagar: R$ {:.2f}".format(sum(cupcake.price for cupcake in self.cart)), bg=UIConstants.BG_COLOR)

        self.create_label(self.current_frame, "Nome no Cartão:", bg=UIConstants.BG_COLOR)
        self.card_name_entry = tk.Entry(self.current_frame)
        self.card_name_entry.pack(pady=5)

        self.create_label(self.current_frame, "Número do Cartão:", bg=UIConstants.BG_COLOR)
        self.card_number_entry = tk.Entry(self.current_frame)
        self.card_number_entry.pack(pady=5)

        self.create_label(self.current_frame, "Data de Vencimento (MM/AA):", bg=UIConstants.BG_COLOR)
        self.expiration_date_entry = tk.Entry(self.current_frame)
        self.expiration_date_entry.pack(pady=5)

        self.create_label(self.current_frame, "CVV:", bg=UIConstants.BG_COLOR)
        self.cvv_entry = tk.Entry(self.current_frame, show="*")
        self.cvv_entry.pack(pady=5)

        tk.Button(self.current_frame, text="Finalizar Pagamento", command=self.finalize_payment, bg=UIConstants.BUTTON_COLOR_ORANGE, fg="white").pack(pady=20)
        tk.Button(self.current_frame, text="Voltar ao Catálogo", command=self.show_catalog_screen, bg=UIConstants.BUTTON_COLOR_GREEN, fg="white").pack(pady=10)

    def finalize_payment(self):
        card_name = self.card_name_entry.get()
        card_number = self.card_number_entry.get()
        expiration_date = self.expiration_date_entry.get()
        cvv = self.cvv_entry.get()

        if not (card_name and card_number and expiration_date and cvv):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        messagebox.showinfo("Pagamento", "Pagamento realizado com sucesso!")
        self.cart = []  # Limpa o carrinho após o pagamento
        self.show_catalog_screen()

    def show_cart_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()

        self.create_label(self.current_frame, "Carrinho de Compras", font=UIConstants.FONT_TITLE)

        for i, cupcake in enumerate(self.cart):
            self.create_label(self.current_frame, f"{cupcake.name} - R$ {cupcake.price:.2f }")
            tk.Button(self.current_frame, text="Remover", command=lambda i=i: self.remove_from_cart(i)).pack(pady=5)

        tk.Button(self.current_frame, text="Finalizar Pedido", command=self.checkout).pack(pady=10)
        tk.Button(self.current_frame, text="Voltar", command=self.show_catalog_screen).pack(pady=10)

    def remove_from_cart(self, index):
        del self.cart[index]
        messagebox.showinfo("Carrinho", "Item removido do carrinho!")
        self.show_cart_screen()

    def checkout(self):
        total = sum(cupcake.price for cupcake in self.cart)
        confirm = messagebox.askyesno("Confirmar Pedido", f"Confirmar pedido? Total: R$ {total:.2f}")
        if confirm:
            messagebox.showinfo("Pedido", f"Pedido finalizado! Total: R$ {total:.2f}")
            self.cart = []
            self.show_catalog_screen()

    def validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()