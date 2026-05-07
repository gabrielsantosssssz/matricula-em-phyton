import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# ===== CORES =====
COR_FUNDO = "#1a1a3e"           # Azul muito escuro (Fundo principal)
COR_CAIXA = "#242456"            # Azul escuro (Fundo dos painéis/inputs)
COR_TEXTO = "#ffffff"            # Branco
COR_BOTAO_ROXO = "#5842c3"       # Roxo (Salvar)
COR_BOTAO_CINZA = "#4a4a75"      # Cinza (Limpar)
COR_BOTAO_VERMELHO = "#c0392b"   # Vermelho (Excluir)

# ===== FONTES =====
FONTE_TITULO = ("Segoe UI", 24, "bold")
FONTE_SUBTITULO = ("Segoe UI", 11, "bold")
FONTE_LABEL = ("Segoe UI", 10)
FONTE_ENTRADA = ("Segoe UI", 10)

# ===== CONEXÃO MONGODB =====
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

db = None
alunos_collection = None

if MONGO_URL:
    try:
        client = MongoClient(MONGO_URL)
        db = client["matricula_db"]
        alunos_collection = db["alunos"]
        print("✅ Conectado ao MongoDB com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao conectar no MongoDB: {e}")
else:
    print("❌ MONGO_URL não encontrado. Verifique seu arquivo .env")

# ===== INICIALIZAÇÃO DA JANELA =====
root = tk.Tk()
root.title("Matrícula de Alunos")
root.geometry("1200x850")
root.configure(bg=COR_FUNDO)

# Configuração de Estilos (Tabelas e Combobox)
style = ttk.Style()
style.theme_use("clam")

style.configure("TCombobox", fieldbackground=COR_CAIXA, background=COR_CAIXA, foreground=COR_TEXTO)
style.configure("Treeview", background=COR_CAIXA, foreground=COR_TEXTO, fieldbackground=COR_CAIXA, rowheight=25)
style.configure("Treeview.Heading", background="#2c2c63", foreground=COR_TEXTO, font=("Segoe UI", 10, "bold"))
style.map("Treeview", background=[("selected", COR_BOTAO_ROXO)])

# ╔═══════════════════════════════════════════════════════════╗
# ║   FUNÇÕES LÓGICAS (CRUD)                                  ║
# ╚═══════════════════════════════════════════════════════════╝

def salvar_aluno():
    if not alunos_collection is not None:
        messagebox.showerror("Erro", "Banco de dados não conectado!")
        return

    nome = entry_nome.get().strip()
    serie = combo_serie.get()
    
    if not nome or serie == "Selecione":
        messagebox.showwarning("Aviso", "Preencha pelo menos o Nome e a Série/Turma!")
        return
    
    aluno_dados = {
        "nome": nome,
        "data_nasc": entry_data_nasc.get(),
        "sexo": var_sexo.get(),
        "endereco": entry_endereco.get(),
        "telefone": entry_telefone.get(),
        "email": entry_email.get(),
        "serie": serie,
        "turno": var_turno.get(),
        "ano_letivo": combo_ano.get(),
        "data_matricula": entry_data_matricula.get(),
        "documentos": {
            "certidao": var_cert_nasc.get(),
            "historico": var_historico.get(),
            "comprovante": var_comprovante.get(),
            "foto": var_foto.get()
        },
        "responsavel": {
            "nome": entry_resp_nome.get(),
            "parentesco": entry_parentesco.get(),
            "telefone": entry_resp_tel.get(),
            "email": entry_resp_email.get()
        }
    }
    
    try:
        alunos_collection.insert_one(aluno_dados)
        messagebox.showinfo("Sucesso", "Aluno matriculado com sucesso!")
        limpar_campos()
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar: {e}")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    
    entry_data_nasc.delete(0, tk.END)
    entry_data_nasc.insert(0, "dd/mm/aaaa")
    
    entry_endereco.delete(0, tk.END)
    
    entry_telefone.delete(0, tk.END)
    entry_telefone.insert(0, "(00) 00000-0000")
    
    entry_email.delete(0, tk.END)
    entry_email.insert(0, "email@email.com")
    
    combo_serie.set("Selecione")
    combo_ano.set("2024")
    
    entry_data_matricula.delete(0, tk.END)
    entry_data_matricula.insert(0, "dd/mm/aaaa")
    
    entry_resp_nome.delete(0, tk.END)
    
    entry_parentesco.delete(0, tk.END)
    entry_parentesco.insert(0, "Ex: Pai, Mãe, Avó...")
    
    entry_resp_tel.delete(0, tk.END)
    entry_resp_tel.insert(0, "(00) 00000-0000")
    
    entry_resp_email.delete(0, tk.END)
    entry_resp_email.insert(0, "email@email.com")
    
    var_sexo.set("Masculino")
    var_turno.set("Manhã")
    var_cert_nasc.set(False)
    var_historico.set(False)
    var_comprovante.set(False)
    var_foto.set(False)

def atualizar_tabela():
    if alunos_collection is None:
        return

    for item in tree.get_children():
        tree.delete(item)
    
    try:
        alunos = list(alunos_collection.find())
        for idx, aluno in enumerate(alunos, 1):
            tree.insert("", "end", iid=str(aluno["_id"]), values=(
                idx,
                aluno.get("nome", "N/A"),
                aluno.get("data_nasc", "N/A"),
                aluno.get("serie", "N/A"),
                aluno.get("turno", "N/A"),
                aluno.get("responsavel", {}).get("nome", "N/A"),
                aluno.get("data_matricula", "N/A")
            ))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar tabela: {e}")

def excluir_aluno():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um aluno na tabela para excluir.")
        return
    
    resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este aluno?")
    if resposta:
        try:
            from bson.objectid import ObjectId
            aluno_id = selecionado[0] # O IID da linha é o _id do MongoDB
            alunos_collection.delete_one({"_id": ObjectId(aluno_id)})
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
            atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

# ╔═══════════════════════════════════════════════════════════╗
# ║   INTERFACE GRÁFICA (LAYOUT)                              ║
# ╚═══════════════════════════════════════════════════════════╝

# TÍTULO
tk.Label(root, text="MATRÍCULA DE ALUNOS", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=20)

# CONTAINER PRINCIPAL
main_container = tk.Frame(root, bg=COR_FUNDO)
main_container.pack(fill="both", expand=True, padx=30, pady=10)

# ----- LINHA 1: Dados do Aluno e Dados da Matrícula -----
row1 = tk.Frame(main_container, bg=COR_FUNDO)
row1.pack(fill="x", pady=5)

# DADOS DO ALUNO (Esquerda)
frame_aluno = tk.LabelFrame(row1, text="DADOS DO ALUNO", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO, bd=1, padx=15, pady=15)
frame_aluno.pack(side="left", fill="both", expand=True, padx=(0, 10))

tk.Label(frame_aluno, text="Nome:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=0, column=0, sticky="w", pady=5)
entry_nome = tk.Entry(frame_aluno, width=45, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_nome.grid(row=0, column=1, columnspan=2, sticky="w", pady=5, ipady=3)

tk.Label(frame_aluno, text="Data Nasc.:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=1, column=0, sticky="w", pady=5)
entry_data_nasc = tk.Entry(frame_aluno, width=20, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_data_nasc.insert(0, "dd/mm/aaaa")
entry_data_nasc.grid(row=1, column=1, sticky="w", pady=5, ipady=3)

tk.Label(frame_aluno, text="Sexo:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=2, column=0, sticky="w", pady=5)
var_sexo = tk.StringVar(value="Masculino")
frame_sexo = tk.Frame(frame_aluno, bg=COR_FUNDO)
frame_sexo.grid(row=2, column=1, columnspan=2, sticky="w")
tk.Radiobutton(frame_sexo, text="Masculino", variable=var_sexo, value="Masculino", bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).pack(side="left")
tk.Radiobutton(frame_sexo, text="Feminino", variable=var_sexo, value="Feminino", bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).pack(side="left", padx=10)

tk.Label(frame_aluno, text="Endereço:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=3, column=0, sticky="w", pady=5)
entry_endereco = tk.Entry(frame_aluno, width=45, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_endereco.grid(row=3, column=1, columnspan=2, sticky="w", pady=5, ipady=3)

tk.Label(frame_aluno, text="Telefone:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=4, column=0, sticky="w", pady=5)
entry_telefone = tk.Entry(frame_aluno, width=20, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_telefone.insert(0, "(00) 00000-0000")
entry_telefone.grid(row=4, column=1, sticky="w", pady=5, ipady=3)

tk.Label(frame_aluno, text="Email:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=5, column=0, sticky="w", pady=5)
entry_email = tk.Entry(frame_aluno, width=45, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_email.insert(0, "email@email.com")
entry_email.grid(row=5, column=1, columnspan=2, sticky="w", pady=5, ipady=3)

# DADOS DA MATRÍCULA (Direita)
frame_matricula = tk.LabelFrame(row1, text="DADOS DA MATRÍCULA", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO, bd=1, padx=15, pady=15)
frame_matricula.pack(side="right", fill="both", expand=True, padx=(10, 0))

tk.Label(frame_matricula, text="Série / Turma:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=0, column=0, sticky="w", pady=5)
combo_serie = ttk.Combobox(frame_matricula, values=["6º Ano A", "7º Ano B", "8º Ano A"], width=25, font=FONTE_ENTRADA)
combo_serie.set("Selecione")
combo_serie.grid(row=0, column=1, sticky="w", pady=5)

tk.Label(frame_matricula, text="Turno:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=1, column=0, sticky="w", pady=5)
var_turno = tk.StringVar(value="Manhã")
frame_turno = tk.Frame(frame_matricula, bg=COR_FUNDO)
frame_turno.grid(row=1, column=1, sticky="w")
tk.Radiobutton(frame_turno, text="Manhã", variable=var_turno, value="Manhã", bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).pack(side="left")
tk.Radiobutton(frame_turno, text="Tarde", variable=var_turno, value="Tarde", bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).pack(side="left")
tk.Radiobutton(frame_turno, text="Noite", variable=var_turno, value="Noite", bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).pack(side="left")

tk.Label(frame_matricula, text="Ano Letivo:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=2, column=0, sticky="w", pady=5)
combo_ano = ttk.Combobox(frame_matricula, values=["2024", "2025", "2026"], width=10, font=FONTE_ENTRADA)
combo_ano.set("2024")
combo_ano.grid(row=2, column=1, sticky="w", pady=5)

tk.Label(frame_matricula, text="Data da Matrícula:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=3, column=0, sticky="w", pady=5)
entry_data_matricula = tk.Entry(frame_matricula, width=20, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_data_matricula.insert(0, "dd/mm/aaaa")
entry_data_matricula.grid(row=3, column=1, sticky="w", pady=5, ipady=3)

tk.Label(frame_matricula, text="Documentos:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=4, column=0, sticky="nw", pady=5)
frame_docs = tk.Frame(frame_matricula, bg=COR_FUNDO)
frame_docs.grid(row=4, column=1, sticky="w", pady=5)

var_cert_nasc = tk.BooleanVar()
var_historico = tk.BooleanVar()
var_comprovante = tk.BooleanVar()
var_foto = tk.BooleanVar()

tk.Checkbutton(frame_docs, text="Certidão de Nascimento", variable=var_cert_nasc, bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).grid(row=0, column=0, sticky="w")
tk.Checkbutton(frame_docs, text="Histórico Escolar", variable=var_historico, bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).grid(row=0, column=1, sticky="w", padx=10)
tk.Checkbutton(frame_docs, text="Comprovante de Residência", variable=var_comprovante, bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame_docs, text="Foto 3x4", variable=var_foto, bg=COR_FUNDO, fg=COR_TEXTO, selectcolor=COR_CAIXA, activebackground=COR_FUNDO, activeforeground=COR_TEXTO).grid(row=1, column=1, sticky="w", padx=10)


# ----- LINHA 2: Responsável e Ações -----
row2 = tk.Frame(main_container, bg=COR_FUNDO)
row2.pack(fill="x", pady=10)

# RESPONSÁVEL (Esquerda)
frame_resp = tk.LabelFrame(row2, text="RESPONSÁVEL", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO, bd=1, padx=15, pady=15)
frame_resp.pack(side="left", fill="both", expand=True, padx=(0, 10))

tk.Label(frame_resp, text="Nome do Responsável:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=0, column=0, sticky="w", pady=5)
entry_resp_nome = tk.Entry(frame_resp, width=45, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_resp_nome.grid(row=0, column=1, columnspan=3, sticky="w", pady=5, ipady=3)

tk.Label(frame_resp, text="Parentesco:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=1, column=0, sticky="w", pady=5)
entry_parentesco = tk.Entry(frame_resp, width=20, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_parentesco.insert(0, "Ex: Pai, Mãe, Avó...")
entry_parentesco.grid(row=1, column=1, sticky="w", pady=5, ipady=3)

tk.Label(frame_resp, text="Telefone:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=2, column=0, sticky="w", pady=5)
entry_resp_tel = tk.Entry(frame_resp, width=20, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_resp_tel.insert(0, "(00) 00000-0000")
entry_resp_tel.grid(row=2, column=1, sticky="w", pady=5, ipady=3)

tk.Label(frame_resp, text="Email:", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_LABEL).grid(row=2, column=2, sticky="e", padx=(10,5), pady=5)
entry_resp_email = tk.Entry(frame_resp, width=25, bg=COR_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, font=FONTE_ENTRADA, relief="flat")
entry_resp_email.insert(0, "email@email.com")
entry_resp_email.grid(row=2, column=3, sticky="w", pady=5, ipady=3)

# AÇÕES (Direita)
frame_acoes = tk.LabelFrame(row2, text="AÇÕES", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO, bd=1, padx=15, pady=15)
frame_acoes.pack(side="right", fill="both", expand=True, padx=(10, 0))

# Centralizar os botões dentro do frame de ações
frame_botoes = tk.Frame(frame_acoes, bg=COR_FUNDO)
frame_botoes.pack(expand=True)

btn_salvar = tk.Button(frame_botoes, text="💾 Salvar", font=FONTE_SUBTITULO, bg=COR_BOTAO_ROXO, fg=COR_TEXTO, relief="flat", padx=20, pady=5, cursor="hand2", command=salvar_aluno)
btn_salvar.grid(row=0, column=0, padx=10)

btn_limpar = tk.Button(frame_botoes, text="🔄 Limpar", font=FONTE_SUBTITULO, bg=COR_BOTAO_CINZA, fg=COR_TEXTO, relief="flat", padx=20, pady=5, cursor="hand2", command=limpar_campos)
btn_limpar.grid(row=0, column=1, padx=10)

btn_excluir = tk.Button(frame_botoes, text="🗑️ Excluir", font=FONTE_SUBTITULO, bg=COR_BOTAO_VERMELHO, fg=COR_TEXTO, relief="flat", padx=20, pady=5, cursor="hand2", command=excluir_aluno)
btn_excluir.grid(row=0, column=2, padx=10)


# ----- LINHA 3: Tabela -----
frame_tabela_container = tk.LabelFrame(main_container, text="ALUNOS MATRICULADOS", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO, bd=1)
frame_tabela_container.pack(fill="both", expand=True, pady=10)

colunas = ("ID", "Nome do Aluno", "Data Nasc.", "Série / Turma", "Turno", "Responsável", "Data Matrícula")
tree = ttk.Treeview(frame_tabela_container, columns=colunas, show="headings", height=8)

tree.heading("ID", text="ID")
tree.heading("Nome do Aluno", text="Nome do Aluno")
tree.heading("Data Nasc.", text="Data Nasc.")
tree.heading("Série / Turma", text="Série / Turma")
tree.heading("Turno", text="Turno")
tree.heading("Responsável", text="Responsável")
tree.heading("Data Matrícula", text="Data Matrícula")

tree.column("ID", width=40, anchor="center")
tree.column("Nome do Aluno", width=250)
tree.column("Data Nasc.", width=100, anchor="center")
tree.column("Série / Turma", width=120, anchor="center")
tree.column("Turno", width=80, anchor="center")
tree.column("Responsável", width=200)
tree.column("Data Matrícula", width=120, anchor="center")

tree.pack(fill="both", expand=True, padx=2, pady=2)

# Popula a tabela ao iniciar
atualizar_tabela()

root.mainloop()