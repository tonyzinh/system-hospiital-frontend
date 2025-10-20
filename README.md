# Sistema Hospitalar - Frontend

## Sobre o Projeto

O Sistema de Gestão Hospitalar é uma aplicação web desenvolvida em Python utilizando Streamlit para o frontend. O sistema tem como objetivo facilitar a gestão de informações hospitalares, permitindo o cadastro e controle de pacientes, medicamentos, operações e incluindo um assistente de IA.

Este é o frontend da aplicação, que se comunica com uma API backend para gerenciar os dados do sistema hospitalar.

## Equipe

### Desenvolvedores
- **Bernardo Antônio Merlo Soares**
- **Bruno Emanuel Sales Rocha**
- **Entony Jovino dos Santos**
- **Kaio Barbosa Linhares**
- **Raphael Simões Gomes**
- **Rikelme Mindelo Biague**
- **Rafael Barcelos de Aquino Moura**

### Orientação Acadêmica
- **Prof. Howard Cruz Roatti** - *Orientador* - FAESA Centro Universitário

---
### Link do Vídeo
Youtube:
___
## Funcionalidades

### Funcionalidades Implementadas
- **Gestão de Pacientes**:
  - Cadastro de novos pacientes
  - Listagem de pacientes com busca
  - Edição de dados de pacientes
  - Exclusão de pacientes
  - Estatísticas de pacientes (total, por sexo)

### Em Desenvolvimento
- **Dashboard**: Página inicial com visão geral do sistema
- **Medicamentos**: Controle de medicamentos
- **Operações**: Gestão de procedimentos cirúrgicos
- **Assistente IA**: Assistente inteligente para apoio médico

## Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit**: Framework para criação de aplicações web
- **Requests**: Para comunicação com API REST
- **Python-dotenv**: Gerenciamento de variáveis de ambiente
- **Pandas**: Manipulação de dados
- **Plotly**: Visualização de dados
- **Tenacity**: Retry de requisições

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter:

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)
- API Backend do sistema rodando (padrão: `http://localhost:8000`)

## Como Executar o Projeto

### 1. Clone o Repositório
```bash
git clone https://github.com/tonyzinh/system-hospiital-frontend.git
cd system-hospiital-frontend
```

### 2. Crie um Ambiente Virtual (Recomendado)
```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente (Opcional)
Crie um arquivo `.env` na raiz do projeto para configurações personalizadas:
```env
API_BASE_URL=http://localhost:8000/api/v1
```

### 5. Execute a Aplicação
```bash
# Navegue até a pasta src
cd src

# Execute o Streamlit
streamlit run app.py
```

### 6. Acesse a Aplicação
Abra seu navegador e acesse: `http://localhost:8501`

## Estrutura do Projeto

```
system-hospiital-frontend/
├── .streamlit/                 # Configurações do Streamlit
│   ├── config.toml            # Configurações da aplicação
│   └── secrets.toml           # Configurações de segurança
├── src/                       # Código fonte principal
│   ├── app.py                 # Arquivo principal da aplicação
│   ├── config.py              # Configurações globais
│   ├── components/            # Componentes da interface
│   │   └── pages/             # Páginas do sistema
│   │       └── patients/      # Módulo de pacientes
│   │           ├── main.py           # Página principal de pacientes
│   │           ├── patient_forms.py  # Formulários de pacientes
│   │           ├── patient_list.py   # Lista de pacientes
│   │           ├── patient_actions.py # Ações de pacientes
│   │           └── utils/            # Utilitários
│   │               └── utils.py      # Funções auxiliares
│   └── services/              # Serviços de comunicação
│       └── patients_api.py    # API de pacientes
├── requirements.txt           # Dependências do projeto
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Documentação do projeto
```

## Configuração da API

O sistema está configurado para se comunicar com uma API REST. As configurações podem ser encontradas em:

- `src/config.py`: Configurações principais
- `.streamlit/secrets.toml`: Configurações de URL da API

### Endpoints Utilizados
- `GET /api/v1/patients/`: Lista todos os pacientes
- `GET /api/v1/patients/{id}/`: Busca um paciente específico
- `POST /api/v1/patients/`: Cria um novo paciente
- `PUT /api/v1/patients/{id}/`: Atualiza um paciente
- `DELETE /api/v1/patients/{id}/`: Remove um paciente

## Interface do Sistema

### Navegação
O sistema possui uma navegação superior com as seguintes páginas:
- **Dashboard**: Visão geral (Em desenvolvimento)
- **Pacientes**: Gestão completa de pacientes
- **Medicamentos**: (Em desenvolvimento)
- **Operações**: (Em desenvolvimento)
- **Assistente IA**: (Em desenvolvimento)

### Funcionalidades da Gestão de Pacientes
- **Busca**: Campo de busca por nome do paciente
- **Cadastro**: Modal para criar novos pacientes
- **Edição**: Modal para editar dados existentes
- **Exclusão**: Confirmação de exclusão com modal
- **Estatísticas**: Métricas de pacientes cadastrados

## Solução de Problemas

### Erro de Conexão com API
- Verifique se a API backend está rodando
- Confirme a URL da API em `src/config.py`
- Teste a conectividade: `curl http://localhost:8000/api/v1/patients/`

### Erro de Módulo Não Encontrado
- Certifique-se de que está na pasta `src` ao executar
- Verifique se todas as dependências foram instaladas: `pip install -r requirements.txt`

### Problemas de Porta
- Se a porta 8501 estiver ocupada, o Streamlit tentará usar a próxima disponível
- Você pode especificar uma porta: `streamlit run app.py --server.port 8502`

## Licença

Este projeto foi desenvolvido para fins acadêmicos.

___