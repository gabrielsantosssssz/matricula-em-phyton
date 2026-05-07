# 📚 Sistema de Matrícula de Alunos

Sistema de matrícula escolar com **Python**, **Tkinter** e **MongoDB**.

---

## ✨ O que tem?

- ✅ Interface gráfica profissional
- ✅ Banco de dados MongoDB
- ✅ Busca automática de CEP (API ViaCEP)
- ✅ CRUD completo (Criar, Ler, Atualizar, Deletar)
- ✅ Validação de dados
- ✅ Tabela dinâmica

---

## 🚀 Instalação Rápida

### 1. Instalar dependências
```bash
pip install pymongo requests python-dotenv
```

### 2. Configurar MongoDB Atlas
1. Criar conta em: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Criar cluster (M0 Free)
3. Criar usuário e pegar connection string

### 3. Criar arquivo `.env`
```env
MONGO_URL=mongodb+srv://usuario:senha@cluster0.mongodb.net/matricula_db?retryWrites=true&w=majority
```

### 4. Executar
```bash
python main.py
```

---

## 📋 Campos do Formulário

**Aluno:**
- Nome, Email, Data de Nascimento, Sexo, Endereço, Telefone

**Matrícula:**
- Série/Turma, Turno, Ano Letivo, Data da Matrícula, Documentos

**Responsável:**
- Nome, Parentesco, Telefone, Email

---

## 🎯 Como Usar

1. **Preencha os campos** do formulário
2. **Clique "Buscar"** no CEP para auto-preencher endereço
3. **Clique "Salvar"** para registrar aluno
4. **Veja na tabela** abaixo todos os alunos cadastrados

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|-----------|-----|
| Python | Linguagem |
| Tkinter | Interface gráfica |
| MongoDB | Banco de dados |
| PyMongo | Driver MongoDB |
| Requests | Consumir APIs |
| ViaCEP | Buscar CEP |

---

## 📂 Estrutura

```
projeto/
├── main.py
├── requirements.txt
├── .env
└── docs/
    └── guias e exemplos
```

---

## 🐛 Erros Comuns

**Erro: "ServerSelectionTimeoutError"**
- Verifique se a senha em `.env` está correta
- Verifique internet

**Erro: "No such module 'tkinter'"**
```bash
pip install tk
```

**Erro: "No such file '.env'"**
- Crie arquivo `.env` com sua MONGO_URL

---

## 📚 Documentação

Veja a pasta `/docs/` para guias completos:
- `guia_completo_detalhado.md` - Tutorial passo a passo
- `mongodb_setup_detalhado.md` - Setup MongoDB
- `exemplos_simples.md` - Código testável

---

## 🎯 Próximos Passos

1. Instale e configure
2. Execute o programa
3. Teste registrando um aluno
4. Leia os guias para aprender mais

---

## 📝 Exemplo de Dados

```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "data_nasc": "15/03/2010",
  "sexo": "M",
  "endereco": "Avenida Paulista, Bela Vista, São Paulo",
  "telefone": "(11) 99999-9999",
  "serie": "7º Ano A",
  "turno": "Manhã",
  "ano_letivo": "2024",
  "data_matricula": "20/05/2024"
}
```

---

## ✅ Pronto!

Instale, configure e comece a usar! 🚀

Para dúvidas, leia os guias em `/docs/`.
