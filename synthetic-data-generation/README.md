# Synthetic Data Generation - CEMA

Pipeline for generating synthetic organizational documents for ESG consulting firms, utilizing local LLMs via Ollama.

## 🎯 Objective

Generate realistic documents for Brazilian ESG consulting firms for use in the CEMA system, preserving the confidentiality of real data.

## 📊 Generated Documents

For each synthetic company, 5 documents are generated:

1. **doc1_mission_vision_values.md** - Mission, Vision, and Values
2. **doc2_dre.csv** - Income Statement (DRE)
3. **doc3_social_impact_report.md** - Social Impact Report
4. **doc4_business_model_canvas.md** - Business Model Canvas
5. **doc5_swot_analysis.md** - SWOT Analysis

## 🚀 Setup

### 1. Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed
- uv (package manager) - recommended

### 2. Install Ollama

**Linux/Mac:**
```bash
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
````

**Windows:**

  - Download and install from [ollama.com/download](https://ollama.com/download)

### 3\. Download GAIA model

```bash
ollama pull brunoconterato/Gemma-3-Gaia-PT-BR-4b-it:f16
```

**Model:** Gemma-3-Gaia-PT-BR-4b-it (fine-tuned for Brazilian Portuguese)  
**Size:** \~4GB  
**Download time:** \~5-10 minutes (depends on connection)

### 4\. Install Python dependencies

**With uv (recommended):**

```bash
cd synthetic-data-generation
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync
```

**With pip:**

```bash
cd synthetic-data-generation
python -m venv .venv
source .venv/bin/activate
pip install jupyter pandas python-dotenv ollama
```

### 5\. Verify setup

```bash
# Check if Ollama is running
ollama list

# Should appear: brunoconterato/Gemma-3-Gaia-PT-BR-4b-it:f16
```

## 🔬 Running the Pipeline

### 1\. Open Jupyter Notebook

```bash
jupyter notebook synth_data_gen.ipynb
```

Or use VS Code with Jupyter extension.

### 2\. Execute cells sequentially

The notebook contains:

**Stage 1:** Organizational Profile Generation

  - Defines company characteristics (size, location, revenue, employees)
  - Output: Structured JSON

**Stage 2:** Income Statement Generation (Rule-Based)

  - Calculates financial statement with accounting precision
  - Uses consulting industry benchmarks
  - Output: CSV

**Stage 3:** Narrative Document Generation

  - Generates 4 Markdown documents using LLM
  - Conditioned on profile + Income Statement (consistent context)
  - Output: 4 .md files

### 3\. Validate outputs

Generated documents will be at:

```
synthetic_documents/PEQUENA/
├── doc1_mission_vision_values.md
├── doc2_dre.csv
├── doc3_social_impact_report.md
├── doc4_business_model_canvas.md
└── doc5_swot_analysis.md
```

## ⚙️ Configuration

### Model Parameters (in notebook)

```python
# Adjust creativity vs determinism
temperature = 0.7  # Default: 0.7 (0.0 = deterministic, 1.0 = creative)

# Adjust maximum document length
max_tokens = 2048  # Default: 2048

# Sampling nucleus
top_p = 0.9  # Default: 0.9
```

### Company Size

Modify in the notebook to generate other sizes:

```python
org_size = "PEQUENA"  # Options: MICROEMPRESA, PEQUENA, MEDIA, GRANDE
```

## 📚 Methodology

### Approach: Example-Guided Generation

1.  **Seed Examples:** 6 real B-Corp certified companies
2.  **In-Context Learning:** LLM learns patterns from examples
3.  **Multi-Stage Pipeline:** Ensures consistency between documents
4.  **Rule-Based DRE:** Mathematical precision for financial data

**Academic references:**

  - Long et al. (2024). "LLMs for Synthetic Data Generation"
  - Gaia (2025). "Gemma-3-Gaia-PT-BR Model"

### Automatic Validation

The notebook includes validations:

  - ✅ Organizational size consistency
  - ✅ Geographic alignment
  - ✅ Document structure (SPS = 100%)
  - ✅ Financial precision (Income Statement)

## 🐛 Troubleshooting

**Error: "Ollama connection refused"**

  - Start Ollama: `ollama serve`
  - Verify it is running: `ollama list`

**Error: "Model not found"**

  - Download the model: `ollama pull brunoconterato/Gemma-3-Gaia-PT-BR-4b-it:f16`

**Slow generation**

  - Normal for the first run (model loading)
  - The f16 model is heavy (\~4GB) but more accurate
  - For GPU: Ollama automatically uses it if available

**Inconsistent documents**

  - Adjust `temperature` to 0.5 (more deterministic)
  - Re-run the complete pipeline (not just one cell)

**Insufficient memory**

  - Model requires \~8GB RAM
  - Use a smaller quantized model if necessary: `Gemma-3-Gaia-PT-BR-4b-it:q4_0`

## 🔄 Generating Multiple Companies

To generate more than one company:

1.  Run the complete notebook
2.  Move outputs from `synthetic_documents/PEQUENA/` to backup
3.  Modify `random_seed` in the notebook
4.  Re-run

**Example:**

```python
random_seed = 42   # Company 1
random_seed = 123  # Company 2
random_seed = 999  # Company 3
```

## 📊 Outputs for CEMA

Copy generated documents to the backend:

```bash
cp -r synthetic_documents/PEQUENA/* ../backend/cema_system/knowledge_base/PEQUENA/
```

## 📚 References

  - [Ollama Documentation](https://ollama.com/docs)
  - [Gemma Model Card](https://ai.google.dev/gemma)
  - [GAIA-PT-BR Paper](https://arxiv.org/abs/GAIA-reference)
  - Long et al. (2024). "LLMs as Synthetic Data Generators"

-----

**Note:** Synthetic documents are for testing and academic validation purposes. They do not represent real companies.
