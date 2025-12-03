# Geração de Dados Sintéticos - CEMA

Pipeline de geração de documentos organizacionais sintéticos para empresas de consultoria ESG, utilizando LLMs locais via Ollama.

## 🎯 Objetivo

Gerar documentos realistas de empresas brasileiras de consultoria ESG para uso no sistema CEMA, preservando confidencialidade de dados reais.

## 📊 Documentos Gerados

Para cada empresa sintética, são gerados 5 documentos:

1. **doc1_mission_vision_values.md** - Missão, Visão e Valores
2. **doc2_dre.csv** - Demonstração do Resultado do Exercício
3. **doc3_social_impact_report.md** - Relatório de Impacto Social
4. **doc4_business_model_canvas.md** - Business Model Canvas
5. **doc5_swot_analysis.md** - Análise SWOT

## 🚀 Setup

### 1. Pré-requisitos

- Python 3.10+
- [Ollama](https://ollama.com/download) instalado
- uv (gerenciador de pacotes) - recomendado

### 2. Instalar Ollama

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
- Baixe e instale de [ollama.com/download](https://ollama.com/download)

### 3. Baixar modelo GAIA
```bash
ollama pull brunoconterato/Gemma-3-Gaia-PT-BR-4b-it:f16
```

**Modelo:** Gemma-3-Gaia-PT-BR-4b-it (ajustado para português brasileiro)  
**Tamanho:** ~4GB  
**Tempo de download:** ~5-10 minutos (depende da conexão)

### 4. Instalar dependências Python

**Com uv (recomendado):**
```bash
cd synthetic-data-generation
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync
```

**Com pip:**
```bash
cd synthetic-data-generation
python -m venv .venv
source .venv/bin/activate
pip install jupyter pandas python-dotenv ollama
```

### 5. Verificar setup
```bash
# Verificar se Ollama está rodando
ollama list

# Deve aparecer: brunoconterato/Gemma-3-Gaia-PT-BR-4b-it:f16
```

## 🔬 Executando a Pipeline

### 1. Abrir Jupyter Notebook
```bash
jupyter notebook synth_data_gen.ipynb
```

Ou use VS Code com extensão Jupyter.

### 2. Executar células sequencialmente

O notebook contém:

**Estágio 1:** Geração do Perfil Organizacional
- Define características da empresa (porte, localização, receita, funcionários)
- Output: JSON estruturado

**Estágio 2:** Geração da DRE (baseada em regras)
- Calcula demonstrativo financeiro com precisão contábil
- Usa benchmarks da indústria de consultoria
- Output: CSV

**Estágio 3:** Geração de Documentos Narrativos
- Gera 4 documentos Markdown usando LLM
- Condicionado ao perfil + DRE (contexto consistente)
- Output: 4 arquivos .md

### 3. Validar outputs

Documentos gerados estarão em:
```
synthetic_documents/PEQUENA/
├── doc1_mission_vision_values.md
├── doc2_dre.csv
├── doc3_social_impact_report.md
├── doc4_business_model_canvas.md
└── doc5_swot_analysis.md
```

## ⚙️ Configuração

### Parâmetros do Modelo (no notebook)
```python
# Ajuste criatividade vs determinismo
temperature = 0.7  # Padrão: 0.7 (0.0 = determinístico, 1.0 = criativo)

# Ajuste comprimento máximo dos documentos
max_tokens = 2048  # Padrão: 2048

# Núcleo de amostragem
top_p = 0.9  # Padrão: 0.9
```

### Porte da Empresa

Modifique no notebook para gerar outros portes:
```python
org_size = "PEQUENA"  # Opções: MICROEMPRESA, PEQUENA, MEDIA, GRANDE
```

## 📚 Metodologia

### Abordagem: Example-Guided Generation

1. **Exemplos Semente:** 6 empresas reais certificadas Sistema B
2. **In-Context Learning:** LLM aprende padrões dos exemplos
3. **Multi-Stage Pipeline:** Garante consistência entre documentos
4. **Rule-Based DRE:** Precisão matemática para dados financeiros

**Referências acadêmicas:**
- Long et al. (2024). "LLMs for Synthetic Data Generation"
- Gaia (2025). "Gemma-3-Gaia-PT-BR Model"

### Validação Automática

O notebook inclui validações:
- ✅ Consistência de porte organizacional
- ✅ Alinhamento geográfico
- ✅ Estrutura de documentos (SPS = 100%)
- ✅ Precisão financeira (DRE)

## 🐛 Troubleshooting

**Erro: "Ollama connection refused"**
- Inicie Ollama: `ollama serve`
- Verifique se está rodando: `ollama list`

**Erro: "Model not found"**
- Baixe o modelo: `ollama pull brunoconterato/Gemma-3-Gaia-PT-BR-4b-it:f16`

**Geração lenta**
- Normal para primeira execução (carregamento do modelo)
- Modelo f16 é pesado (~4GB) mas mais preciso
- Para GPU: Ollama usa automaticamente se disponível

**Documentos inconsistentes**
- Ajuste `temperature` para 0.5 (mais determinístico)
- Re-execute pipeline completa (não só uma célula)

**Memória insuficiente**
- Modelo requer ~8GB RAM
- Use modelo quantizado menor se necessário: `Gemma-3-Gaia-PT-BR-4b-it:q4_0`

## 🔄 Gerando Múltiplas Empresas

Para gerar mais de uma empresa:

1. Execute notebook completo
2. Mova outputs de `synthetic_documents/PEQUENA/` para backup
3. Modifique `random_seed` no notebook
4. Re-execute

**Exemplo:**
```python
random_seed = 42  # Empresa 1
random_seed = 123  # Empresa 2
random_seed = 999  # Empresa 3
```

## 📊 Outputs para CEMA

Copie documentos gerados para o backend:
```bash
cp -r synthetic_documents/PEQUENA/* ../backend/cema_system/knowledge_base/PEQUENA/
```

## 📚 Referências

- [Ollama Documentation](https://ollama.com/docs)
- [Gemma Model Card](https://ai.google.dev/gemma)
- [GAIA-PT-BR Paper](https://arxiv.org/abs/GAIA-reference)
- Long et al. (2024). "LLMs as Synthetic Data Generators"

---

**Nota:** Documentos sintéticos são para fins de teste e validação acadêmica. Não representam empresas reais.
