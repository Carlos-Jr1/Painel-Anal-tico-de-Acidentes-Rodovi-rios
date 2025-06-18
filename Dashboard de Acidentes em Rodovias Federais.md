# Dashboard de Acidentes em Rodovias Federais

## Descrição do Projeto

Este projeto consiste em um dashboard interativo desenvolvido em Python usando Dash e Plotly para análise de acidentes em rodovias federais brasileiras. O sistema permite visualizar e analisar dados de acidentes de forma interativa, identificando padrões temporais, geográficos e correlações com a frota de veículos.

## Funcionalidades Implementadas

### ✅ Análises Estatísticas
- Total de acidentes por rodovia, trecho e município
- Análise temporal: acidentes por dia da semana e faixa de horário
- Distribuição por tipo de acidente
- Correlação entre frota de veículos e número de acidentes

### ✅ Dashboard Interativo
- **Mapa de Acidentes**: Visualização geográfica dos pontos de acidentes
- **Gráfico de Pizza**: Distribuição por tipo de acidente
- **Gráficos de Barras**: Acidentes por dia da semana e faixa de horário
- **Gráfico de Dispersão**: Correlação frota vs acidentes
- **Tabela Interativa**: Ranking dos trechos mais críticos

### ✅ Filtros Interativos
- Filtro por Estado (UF)
- Filtro por Rodovia
- Filtro por Tipo de Acidente
- Filtro por Faixa de Horário

### ✅ Funcionalidades de Exportação
- Exportação de gráficos em formato PNG
- Exportação de tabelas em formato PDF

## Estrutura dos Arquivos

```
├── acidentes2025_estruturado.csv    # Dados de acidentes (exemplo)
├── frotas_veiculos_2023.csv         # Dados de frota de veículos (exemplo)
├── etl_data.py                      # Script de ETL e transformação de dados
├── statistical_analysis.py          # Script de análises estatísticas
├── dashboard.py                     # Aplicação principal do dashboard
├── export_functions.py              # Funções de exportação
├── exports/                         # Pasta com arquivos exportados
│   ├── grafico_tipos_acidente.png
│   ├── grafico_dia_semana.png
│   ├── grafico_faixa_horario.png
│   ├── grafico_correlacao.png
│   └── ranking_trechos_criticos.pdf
└── todo.md                          # Lista de tarefas do projeto
```

## Como Usar

### 1. Preparação dos Dados
```bash
python3 etl_data.py
```
Este script carrega os dados CSV, realiza limpeza e transformações, criando colunas derivadas como dia da semana e faixa de horário.

### 2. Análises Estatísticas
```bash
python3 statistical_analysis.py
```
Executa análises exploratórias e gera estatísticas descritivas dos dados.

### 3. Executar o Dashboard
```bash
python3 dashboard.py
```
Inicia o servidor do dashboard em `http://localhost:8050`

### 4. Exportar Resultados
```bash
python3 export_functions.py
```
Gera arquivos PNG dos gráficos e PDF da tabela de trechos críticos.

## Dependências

```bash
pip3 install pandas dash plotly dash-bootstrap-components kaleido reportlab
```

## Características Técnicas

- **Framework**: Dash (Flask-based)
- **Visualizações**: Plotly
- **Processamento de Dados**: Pandas
- **Estilo**: Bootstrap (dash-bootstrap-components)
- **Exportação**: Kaleido (PNG) e ReportLab (PDF)

## Adaptação para Dados Reais

Para usar com seus dados reais:

1. Substitua os arquivos CSV pelos seus dados reais
2. Ajuste as colunas no script `etl_data.py` conforme necessário
3. Modifique os filtros e análises no `dashboard.py` se necessário
4. Execute novamente o pipeline completo

## Melhorias Futuras

- Implementação de cache para melhor performance
- Adição de mais tipos de visualizações
- Integração com APIs de dados em tempo real
- Funcionalidades de machine learning para predição de acidentes
- Deploy em produção com Docker

## Observações

Este projeto foi desenvolvido com dados simulados para demonstração. Para uso em produção, certifique-se de:
- Validar a qualidade dos dados reais
- Implementar tratamento de erros robusto
- Configurar adequadamente a segurança
- Otimizar para grandes volumes de dados

