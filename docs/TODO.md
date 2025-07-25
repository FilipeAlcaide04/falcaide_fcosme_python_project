# TODO - Projeto Final PIV Eleições 

## ✅ Geração de resultados eleitorais simulados por freguesia
- [x] Script para fazer download dos dados (freguesias, municípios e distritos)
  - [x] Adicionar código a `1º-data_aquisition.py`
  - [x] Testar funcionalidade
- [x] Script para verificar consistência e limpar os dados se necessário (`2º-data_cleaning_etc.py`)
  - [x] Testar funcionalidade
    - [x] Guardar/processar dados recebidos no folder `data/processed`
- [x] Script para gerar simular/gerar dados por freguesia (`generate_data.py`)
  - [x] Testar funcionalidade

## 🔁 Comparação com os resultados reais de 2009
- [x] Alterar `1º-data_aquisition.py` para incluir download dos dados de 2009
  - [x] Testar funcionalidade
- [x] Criar script para processar e comparar com os simulados
  - [x] Testar funcionalidade

## 🌐 Servidor para recepção e processamento de dados
- [x] Implementar servidor (ex: `cne_server.py`)
  - [x] Receber dados e executar os cálculos necessário
    - [x] Testar funcionalidade

## 📊 Visualização de resultados
- [x] Script para visualização gráfica dos dados finais usando Flask (`cne_server.py`)
  - [x] Gráficos por Freguesia
  - [x] Comparação entre 2009 e 2024 (Selecionado pelo user)

## 🧪 Testes
- [x] Escrever testes automáticos (diretório `unit_tests/`)
  - [x] Testes unitários dos scripts principais

## 📄 Documentação
- [x] Atualizar `README.md`
  - [x] Instruções de instalação
  - [x] Como correr o projeto
- [x] Completar `relatorio.md`


