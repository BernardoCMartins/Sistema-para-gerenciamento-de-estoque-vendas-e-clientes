import customtkinter as ctk
from tkinter import ttk, messagebox
import json

estoque_produtos = "estoque.json"

def analisar_estoque():
    try:
        with open(estoque_produtos, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def escrever_estoque(estoque):
    with open(estoque_produtos, "w") as file:
        json.dump(estoque, file, indent=4)

class ControleEstoqueApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Controle de Estoque")
        self.centralizar_janela(self,900,500)
        self.configure(fg_color="#06141e")
        self._set_appearance_mode("dark")
        self.resizable(width=False, height=False)
        self.estoque = analisar_estoque()  # Carrega o estoque inicial
        self.tela_principal()
        
        
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
        for widget in self.winfo_children():
            widget.destroy()

    def tela_principal(self):
        self.limpar_tela()

        # Menu principal
        frame_menu = ctk.CTkFrame(self, width=200, fg_color="#1e2b34")
        frame_menu.pack(side="left", fill="y")

        ctk.CTkButton(
            frame_menu, font=("Arial Bold",14), text="Adicionar Item", command=self.adicionar_item, hover_color="#32CD32"
        ).pack(pady=10)
        ctk.CTkButton(
            frame_menu, font=("Arial Bold",14), text="Editar Item", command=self.editar_item, hover_color="#DAA520" 
        ).pack(pady=10) 
        ctk.CTkButton(
            frame_menu, font=("Arial Bold",14), text="Remover Item", command=self.remover_item,  hover_color="#FF0000"
        ).pack(pady=10)
       
        

        # Área de exibição
        self.frame_exibicao = ctk.CTkFrame(self, fg_color="#06141e")
        self.frame_exibicao.pack(side="right", fill="both", expand=True)

        # Inicia com a exibição do estoque
        self.visualizar_estoque()


    def visualizar_estoque(self):
        for widget in self.frame_exibicao.winfo_children():
            widget.destroy()


        if self.estoque:
            style = ttk.Style()
            style.theme_use("clam") 
            style.configure("Treeview.Heading", font=("Arial Bold", 14), foreground="black", relief="flat")
            style.configure("Treeview", font=("Arial", 14,),rowheight=30,foreground="white", background="#4f4f4f",fieldbackground="4f4f4f",)  
            style.map("Treeview",background=[("selected", "#0d6efd")],foreground=[("selected", "white")])
            self.iconbitmap("shoes.ico")

            
            

            tree = ttk.Treeview(self.frame_exibicao,  columns=("nome", "quantidade", "preco"), show="headings")
            tree.heading("nome", text="Nome" )
            tree.heading("quantidade", text="Quantidade")
            tree.heading("preco", text="Preço")
            tree.pack(fill="both", expand=True)
            scrollbar_vertical = ttk.Scrollbar(self.frame_exibicao, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar_vertical.set)
           
         

            for nome, dados in self.estoque.items():
                tree.insert("", "end", values=(nome, dados["quantidade"], f"R$ {dados['preco']:.2f}"))
        else:
            ctk.CTkLabel(self.frame_exibicao, text="Estoque vazio!", font=("Arial ", 18)).pack(pady=20)

    def adicionar_item(self):
        def salvar_item():
            nome = entry_nome.get().lower()
            preco = float(entry_preco.get())
            quantidade = int(entry_quantidade.get())

            if nome in self.estoque:
                self.estoque[nome]["quantidade"] += quantidade
            else:
                self.estoque[nome] = {"quantidade": quantidade, "preco": preco}

            escrever_estoque(self.estoque)
            messagebox.showinfo("Sucesso", f"O item '{nome}' foi adicionado ao estoque.")
            janela.destroy()
            self.visualizar_estoque()

        janela = ctk.CTkToplevel(self)
        janela.title("Adicionar Item")
        self.centralizar_janela(janela, 300, 300)
        janela.resizable(width=False, height=False)
        
        janela.transient(self)  # Torna a janela filha da janela principal
        janela.grab_set()       # Desativa interação com a janela principal
        janela.focus_set()
        

        ctk.CTkLabel(janela, text="Nome:").pack()
        entry_nome = ctk.CTkEntry(janela)
        entry_nome.pack()

        ctk.CTkLabel(janela, text="Preço:").pack()
        entry_preco = ctk.CTkEntry(janela)
        entry_preco.pack()

        ctk.CTkLabel(janela, text="Quantidade:").pack()
        entry_quantidade = ctk.CTkEntry(janela)
        entry_quantidade.pack()

        ctk.CTkButton(janela, text="Salvar", command=salvar_item).pack(pady=10)

    def remover_item(self):
        def confirmar_remocao():
            nome = entry_nome.get().lower()

            if nome in self.estoque:
                
                del self.estoque[nome]
                escrever_estoque(self.estoque)
                messagebox.showinfo("Sucesso", f"O item '{nome}' foi removido do estoque.")
                janela.destroy()
                self.visualizar_estoque()
            else:
                messagebox.showerror("Erro", f"O item '{nome}' não está no estoque.")

        janela = ctk.CTkToplevel(self)
        janela.title("Remover Item")
        self.centralizar_janela(janela,300,300)
        janela.resizable(width=False, height=False)
        
        janela.transient(self)  # Torna a janela filha da janela principal
        janela.grab_set()       # Desativa interação com a janela principal
        janela.focus_set()

        ctk.CTkLabel(janela, text="Nome do Item:").pack()
        entry_nome = ctk.CTkEntry(janela)
        entry_nome.pack()

        ctk.CTkButton(janela, text="Remover", command=confirmar_remocao).pack(pady=10)
        
    def editar_item(self):
        def salvar_alteracoes():
            nome = entry_nome.get().lower()
            novo_preco = entry_preco.get()
            nova_quantidade = entry_quantidade.get()

            if nome in self.estoque:
                try:
                    # Atualizando os dados do item no estoque
                    self.estoque[nome]["preco"] = float(novo_preco)
                    self.estoque[nome]["quantidade"] = int(nova_quantidade)

                    escrever_estoque(self.estoque)  # Atualizando o arquivo JSON
                    messagebox.showinfo("Sucesso", f"O item '{nome}' foi atualizado.")
                    janela.destroy()
                    self.visualizar_estoque()  # Atualiza a exibição na Treeview
                except ValueError:
                 messagebox.showerror("Erro", "Insira valores válidos para preço e quantidade.")
            else:
             messagebox.showerror("Erro", f"O item '{nome}' não está no estoque.")

        def carregar_item():
            nome = entry_nome.get().lower()
            if nome in self.estoque:
                entry_preco.delete(0, "end")
                entry_preco.insert(0, self.estoque[nome]["preco"])

                entry_quantidade.delete(0, "end")
                entry_quantidade.insert(0, self.estoque[nome]["quantidade"])
            else:
                messagebox.showerror("Erro", f"O item '{nome}' não está no estoque.")

        # Criando a janela para edição
        janela = ctk.CTkToplevel(self)
        janela.title("Editar Item")
        self.centralizar_janela(janela,350,350)
        janela.resizable(width=False, height=False)
        
        janela.transient(self)  # Torna a janela filha da janela principal
        janela.grab_set()       # Desativa interação com a janela principal
        janela.focus_set()

        # Campos de entrada
        ctk.CTkLabel(janela, text="Nome do Item:").pack(pady=5)
        entry_nome = ctk.CTkEntry(janela)
        entry_nome.pack(pady=5)

        ctk.CTkButton(janela, text="Carregar Dados", command=carregar_item).pack(pady=5)

        ctk.CTkLabel(janela, text="Novo Preço:").pack(pady=5)
        entry_preco = ctk.CTkEntry(janela)
        entry_preco.pack(pady=5)

        ctk.CTkLabel(janela, text="Nova Quantidade:").pack(pady=5)
        entry_quantidade = ctk.CTkEntry(janela)
        entry_quantidade.pack(pady=5)

        # Botão para salvar alterações
        ctk.CTkButton(janela, text="Salvar Alterações", command=salvar_alteracoes).pack(pady=10)

    

    
              
if __name__ == "__main__":
    app = ControleEstoqueApp()
    app.mainloop()
