import customtkinter as ctk
from PIL import Image
import sqlite3
from tkinter import messagebox
from interface_menu import ControleEstoqueApp

class App(ctk.CTk):
    def conecta_db(self):
        self.conn = sqlite3.connect("Bestshoes_system.db")
        self.cursor = self.conn.cursor()
        print("Bd sucess")
       
    def desconecta_db(self):
        self.conn.close()
        print("Bd desconectado")
            
    def cria_tabela(self):
        self.conecta_db()
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );             
        """)
        self.conn.commit()
        print("Tabela criada com sucesso!")
        self.desconecta_db()
        
    def cadastrar_usuario(self):
        try:
            self.conecta_db()  # Conectando ao banco de dados
            
            #  lógica de inserção e validação 
            usuario = self.txt_usuario.get()
            senha = self.txt_senha.get()
            confirmar_senha = self.txt_confirmar_senha.get()

            # Validações
            if not usuario or not senha or not confirmar_senha:
                messagebox.showerror(title="Sistema cadastro", message="Por favor preencha todos os campos.")
                return

            if len(senha) < 4:
                messagebox.showerror(title="Sistema cadastro", message="Por favor utilize uma senha com mais de 4 caracteres para sua segurança.")
                return

            if senha != confirmar_senha:
                messagebox.showerror(title="Sistema cadastro", message="As senhas não coincidem.")
                return
 

            self.cursor.execute("SELECT Username FROM Usuarios WHERE Username = ?", (usuario,))
            usuario_existente = self.cursor.fetchone()
            
            if usuario_existente:
                messagebox.showerror(title="Sistema cadastro", message="   Usuário ja cadastrado\n Escolha outro nome por favor! ")
                self.desconecta_db
                return
            
            else:
             self.cursor.execute("""
                INSERT INTO Usuarios (Username, Senha, Confirma_Senha)
                VALUES (?, ?, ?)
            """, (usuario, senha, confirmar_senha))
             self.conn.commit() 

            messagebox.showinfo(title="Sistema cadastro", message="Usuário cadastrado com sucesso!")
            print("Usuário cadastrado no sistema.")
        except sqlite3.Error as e:
            messagebox.showerror(title="Erro no cadastro", message=f"Ocorreu um erro ao cadastrar o usuário: {e}")
        finally:
            self.desconecta_db() # Fechando a conexão com o banco
            self.limpar_tela()
            self.tela_login()
            
    def verifica_login(self):
        usuario = self.txt_usuario.get()
        senha= self.txt_senha.get()
        
        self.conecta_db()
        
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username =? AND Senha = ?) """, (usuario, senha)) 
        self.verifica_dados = self.cursor.fetchone() #Verificando se o usuario existe no banco de dados
        
        
        if self.verifica_dados:
                messagebox.showinfo(title="Login", message="Login efetuado com sucesso")
                self.after(100, self.abrir_menu)
                     
        else:
              messagebox.showerror(title="Login", message="Usuário ou senha inválidos")
        
        
        
    def abrir_menu(self): 
        self.quit()     
        self.destroy()
        menu = ControleEstoqueApp()
        menu.mainloop()
        
        


    def __init__(self):
        super().__init__()
        self.cria_tabela()  # Cria a tabela ao inicializar a aplicação
        self.janela_principal()  # Configurações da janela
        self.tela_login()  # Inicia com a tela de login


    def janela_principal(self):
        # Configurações da janela principal
        self.title("Sistema Best Shoes")
        self.centralizar_janela(self,900,500)
        self.resizable(width=False, height=False)
        self._set_appearance_mode("dark")
        self.configure(fg_color="#06141e")
        self.iconbitmap("shoes.ico")
        
        
    def centralizar_janela(self, janela, largura, altura):
        # Atualiza a geometria da janela
        janela.update_idletasks()
    
        # Obtém as dimensões da tela
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
    
        # Calcula a posição da janela
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
    
        # Define a geometria da janela
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def limpar_tela(self):
        # Remove todos os widgets da janela
        for widget in self.winfo_children():
            widget.destroy()

    def tela_login(self):
        self.limpar_tela()  # Limpa a tela antes de exibir a tela de login

        # Frame principal
        self.frame = ctk.CTkFrame(master=self, width=285, height=415, fg_color="#1e2b34")
        self.frame.place(x=596, y=43)

        # Título
        self.txt_titulo = ctk.CTkLabel(self, text="Best Shoes", font=("arial bold", 48))
        self.txt_titulo.pack(pady=0, padx=0)

        # Elementos da tela de login
        self.txt_login = ctk.CTkLabel(self, text="Login", font=("arial", 24), bg_color="#1e2b34")
        self.txt_login.place(x=612, y=106)
        self.txt_usuario = ctk.CTkEntry(self, width=242, placeholder_text="Seu login", bg_color="#1e2b34")
        self.txt_usuario.place(x=618, y=155)
        self.txt_senha = ctk.CTkEntry(self, width=242, placeholder_text="Sua senha", show="*", bg_color="#1e2b34")
        self.txt_senha.place(x=618, y=200)
        
        # Checkbox
        self.check_mostrar = ctk.CTkCheckBox(self, text="Lembrar senha", font=("arial", 12), width=0, height=0, border_width=2, bg_color="#1e2b34")
        self.check_mostrar.place(x=618, y=238)
        self.check_lembrar = ctk.CTkCheckBox(self, text="Clique aqui para ver a senha.", font=("arial", 12), width=0, height=0, border_width=2, bg_color="#1e2b34")
        self.check_lembrar.place(x=618, y=270)

        # Botões
        self.btn_login = ctk.CTkButton(self, width=242, text="Entrar", bg_color="#1e2b34", command=self.verifica_login)
        self.btn_login.place(x=618, y=305)
        self.btn_cadastrar = ctk.CTkButton(
            self, width=242, text="Cadastre-se", fg_color="#97c98d", bg_color="#1e2b34", command=self.tela_cadastro
        )
        self.btn_cadastrar.place(x=618, y=345)

        # Imagem
        self.img = ctk.CTkImage(Image.open("tenis.png"), size=(350, 350))
        self.label_img = ctk.CTkLabel(self, image=self.img, text="")
        self.label_img.place(x=50, y=80)

    def tela_cadastro(self):
        self.limpar_tela()  # Limpa a tela antes de exibir a tela de cadastro

        # Frame principal
        self.frame = ctk.CTkFrame(master=self, width=285, height=415, fg_color="#1e2b34")
        self.frame.place(x=596, y=43)
        
        self.img = ctk.CTkImage(Image.open("tenis.png"), size=(350, 350))
        self.label_img = ctk.CTkLabel(self, image=self.img, text="")
        self.label_img.place(x=50, y=80)

        # Título
        self.txt_titulo = ctk.CTkLabel(self, text="Cadastro", font=("arial bold", 48))
        self.txt_titulo.pack(pady=0, padx=0)

        # Elementos da tela de cadastro
        self.txt_usuario = ctk.CTkEntry(self, width=242, placeholder_text="Crie seu login", bg_color="#1e2b34")
        self.txt_usuario.place(x=618, y=155)
        self.txt_senha = ctk.CTkEntry(self, width=242, placeholder_text="Crie sua senha", show="*", bg_color="#1e2b34")
        self.txt_senha.place(x=618, y=200)
        self.txt_confirmar_senha = ctk.CTkEntry(
            self, width=242, placeholder_text="Confirme sua senha", show="*", bg_color="#1e2b34"
        )
        self.txt_confirmar_senha.place(x=618, y=245)

        # Botões
        self.btn_voltar = ctk.CTkButton(
            self, width=242, text="Voltar", fg_color="#97c98d", bg_color="#1e2b34", command=self.tela_login
        )
        self.btn_voltar.place(x=618, y=305)
        self.btn_cadastrar = ctk.CTkButton(self, width=242, text="Confirmar", bg_color="#1e2b34", command=self.cadastrar_usuario)
        self.btn_cadastrar.place(x=618, y=345)


if __name__ == "__main__":
    app = App()
    app.mainloop()
