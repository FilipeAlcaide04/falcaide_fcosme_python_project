# TODO - Projeto Final PIV Eleições 

## ✅ Geração de resultados eleitorais simulados por freguesia
- [x] Script para fazer download dos dados (freguesias, municípios e distritos)
  - [x] Adicionar código a `1º-data_aquisition.py`
  - [ ] Testar funcionalidade
- [ ] Script para verificar consistência e limpar os dados se necessário (`2º-data_cleaning_etc.py`)
- [ ] Script para gerar simular/gerar dados por freguesia (`generate_data.py`)

## 🔁 Comparação com os resultados reais de 2009
- [ ] Alterar `1º-data_aquisition.py` para incluir download dos dados de 2009
- [ ] Criar script para processar e comparar com os simulados

## 🌐 Servidor para recepção e processamento de dados
- [ ] Implementar servidor (ex: `cne_server.py`, `data_processor.py`)
  - [ ] Receber dados e executar os cálculos necessário
  - [ ] Guardar/processar dados recebidos no folder `data/processed`

## 📊 Visualização de resultados
- [ ] Script para visualização gráfica dos dados finais (`visualization.py`)
  - [ ] Gráficos por distrito
  - [ ] Gráficos por município
  - [ ] Comparação entre simulado vs real

## 🧪 Testes
- [ ] Escrever testes automáticos (diretório `tests/`)
  - [ ] Validação de dados (`data_validation.py`)
  - [ ] Testes unitários dos scripts principais

## 📄 Documentação
- [ ] Atualizar `README.md`
  - [ ] Instruções de instalação
  - [ ] Como correr o projeto
  - [ ] Explicação dos ficheiros principais
- [ ] Completar `relatorio.md`
  - [ ] Metodologia
  - [ ] Resultados
  - [ ] Discussão

