# Aplicação de Busca de Veículos

Uma aplicação Python que permite buscar veículos usando linguagem natural em português. Este projeto demonstra desenvolvimento Python moderno com FastAPI, SQLAlchemy, MCP (Model Context Protocol) e processamento de linguagem natural.

Esta aplicação implementa um MCP customizado para comunicação entre cliente e servidor.

- **Comunicação Cliente-Servidor**: O agente conversa com o servidor usando o protocolo MCP customizado
- **Estrutura Padronizada**: Requisições e respostas seguem um formato JSON consistente definido pelo protocolo
- **Separação de Responsabilidades**: Cliente processa linguagem natural, servidor gerencia dados
- **Escalabilidade**: Facilita futuras expansões e integrações
- **Flexibilidade**: Protocolo adaptado às necessidades específicas da aplicação

## O Que Esta Aplicação Faz

Você pode conversar com a aplicação em português e ela entenderá o que você está procurando. Por exemplo:

- "quero um Honda"
- "carro até 150mil reais a partir de 2018"
- "BMW automático com teto solar"
- "veículo elétrico até 50mil km"

## Como Funciona

A aplicação tem três partes principais:

1. **Agente** - Entende sua entrada/mensagem e converte em filtros de busca
2. **Servidor MCP** - Gerencia as solicitações de busca usando o MCP
3. **Banco de Dados** - Armazena 400 veículos com dados fictícios

## Início Rápido

**Passo 1: Clonar o Repositório**
git clone https://github.com/tomrodww/python-vehicle-search.git
cd python-vehicle-search

**Passo 2: Verificar Versão do Python**
python --version# Deve mostrar Python 3.17 ou superior

**Passo 3: Instalar Dependências**
pip install -r requirements.txt

**Passo 4: Criar o Banco de Dados**
python -m src.database.populate_db

**Passo 5: Iniciar o Servidor MCP** 
python run_server.py

**Passo 6: Executar a Aplicação Principal** (em um novo terminal)
python main.py

**Passo 7: Começar a Buscar!**

- "quero um Honda"
- "carro até 150mil reais"
- "BMW automático com teto solar"


## Testes

O projeto inclui alguns testes para garantir o funcionamento:

# Executar todos os testes
python run_tests.py

Há 22 testes cobrindo:

- Processamento de linguagem natural
- Funcionalidade do servidor MCP
- Casos especificos e tratamento de erros
- Combinações de filtros

## Estrutura do Projeto


python-vehicle-search/
├── src/
│   ├── agent/              
│   │   └── agent.py        # Lógica do agente
│   ├── mcp_server/         
│   │   └── mcp_server.py   # Servidor MCP
│   ├── database/           
│   │   ├── populate_db.py  # Geração de dados
│   │   └── utils.py        # Conexão com banco
│   ├── models/             
│   │   └── models.py       # Modelo de veículo
│   └── constants/          
│       └── constants.py    # Valores válidos
├── tests/                  
│   ├── test_agent.py       # Testes do agente
│   └── test_mcp_server.py  # Testes do servidor
├── main.py                 # Ponto de entrada da aplicação
├── run_server.py           # Inicialização do servidor
├── run_tests.py            # Executor de testes
└── requirements.txt        # Dependências


## Principais Recursos

### Processamento de Linguagem Natural

- Entende entrada em português com acentos
- Lida com consultas complexas com múltiplos filtros
- Suporta faixas de preço ("até 150mil reais")
- Suporta faixas de quilometragem ("até 50mil km a partir de 30mil km")
- Análise contextual (distingue ano de faixas de preço)

### Protocolo MCP

- Implementa o MCP para comunicação cliente-servidor
- Sem acesso direto ao banco de dados pelo cliente

### Banco de Dados

- 400 veículos com dados fictícios
- 10+ atributos por veículo (marca, modelo, ano, preço, etc.)
- Gerado usando o módulo random do Python com dados predefinidos (opcional usar Faker para gerar dados mais realistas)
- SQLAlchemy 2.0

### Testes

- 22 testes
- Cobre toda a funcionalidade principal
- Testa casos específicos e cenários de erro
- Garante conformidade com o protocolo MCP

## Detalhes Técnicos

### Dependências

- **FastAPI** - Framework web para o servidor MCP
- **SQLAlchemy 2.0** - ORM moderno para operações de banco
- **Pytest** - Framework de testes
- **Random** - Módulo random nativo do Python para geração de dados
- **Requests** - Cliente HTTP para comunicação MCP

### Esquema do Banco de Dados

Cada veículo tem estes atributos:

- id, 
- marca, 
- modelo, 
- ano
- preço_centavos, 
- cor, 
- quilometragem
- motor, 
- transmissão, 
- tipo_combustível
- categoria, teto_solar

### Protocolo MCP

O servidor espera requisições neste formato:

json
{
  "action": "search_vehicles",
  "filters": {
    "brand": "honda",
    "year": 2020,
    "price_max": 15000000,
    ...
  }
}

E retorna respostas como:

json
{
  "success": true,
  "data": [...],
  "total": 5,
  "message": "Encontrei 5 veículos"
}
