# TODO - Projeto Final PIV Eleições 

## ✅ Geração de resultados eleitorais simulados por freguesia
- [x] Script para fazer download dos dados (freguesias, municípios e distritos)
  - [x] Adicionar código a `1º-data_aquisition.py`
  - [ ] Testar funcionalidade
- [x] Script para verificar consistência e limpar os dados se necessário (`2º-data_cleaning_etc.py`)
  - [ ] Testar funcionalidade
- [ ] Script para gerar simular/gerar dados por freguesia (`generate_data.py`)
  - [ ] Testar funcionalidade

## 🔁 Comparação com os resultados reais de 2009
- [ ] Alterar `1º-data_aquisition.py` para incluir download dos dados de 2009
  - [ ] Testar funcionalidade
- [ ] Criar script para processar e comparar com os simulados
  - [ ] Testar funcionalidade

## 🌐 Servidor para recepção e processamento de dados
- [ ] Implementar servidor (ex: `cne_server.py`, `data_processor.py`)
  - [ ] Receber dados e executar os cálculos necessário
    - [ ] Testar funcionalidade
  - [ ] Guardar/processar dados recebidos no folder `data/processed`
  * python -m http.server 8000 // Para iniciar o server (remove later)

## 📊 Visualização de resultados
- [ ] Script para visualização gráfica dos dados finais (`visualization.py`)
  - [ ] Gráficos por distrito
  - [ ] Gráficos por município
  - [ ] Comparação entre simulado vs real

## 🧪 Testes
- [ ] Escrever testes automáticos (diretório `tests/`)
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

