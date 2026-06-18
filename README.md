# Customer Support Chatbot - AI-Powered Intent Classification & Conversational Agent

> **customer support automation: Dual RoBERTa classifiers meet LLaMA 3.3 70B to understand, route, and resolve customer queries with near-perfect accuracy.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org)
[![RoBERTa](https://img.shields.io/badge/RoBERTa-base-orange)](https://huggingface.co/roberta-base)
[![LLaMA](https://img.shields.io/badge/LLaMA_3.3-70B-purple)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)](https://streamlit.io)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)](https://huggingface.co)
[![Accuracy](https://img.shields.io/badge/Test_Accuracy-99.98%25-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## Overview

The **Customer Support Chatbot** is a production-grade NLP pipeline that automates the full customer support lifecycle - from understanding what a customer wants, to generating a professional, context-aware response - with **no human routing required**.

At its core, the system runs two fine-tuned **RoBERTa-base** classifiers in parallel to simultaneously predict the **intent** (27 fine-grained classes) and **category** (11 high-level topics) of any customer message. These predictions are passed as structured context to **LLaMA 3.3 70B** (via Groq Cloud), which generates professional customer service responses grounded in the classifier's routing output.

The result: a stateful, multi-turn support agent that achieves **99.98% accuracy** on the held-out test set, with only **1 misclassification out of 4,031 samples**.

---

## Demo

### Live Chat Interface

> *([Add your demo video here](https://github.com/user-attachments/assets/d5921c3e-dba4-4974-86df-6b96d9ad5106))*

```
https://github.com/user-attachments/assets/d5921c3e-dba4-4974-86df-6b96d9ad5106
```

---

## How It Works - System Pipeline

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────────────┐
│      User Input      │────▶│    Text Cleaning      │────▶│  RoBERTa Classifier #1  │
│  Customer describes  │     │  URL/HTML removal,    │     │  Intent Model (27 cls)  │
│  problem in natural  │     │  whitespace normalize │     │  Fine-grained prediction│
│      language        │     └──────────────────────┘     └─────────────────────────┘
└─────────────────────┘                                               │
                                                                      ▼
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────────────┐
│   Chat Interface     │◀────│  LLaMA 3.3 70B        │◀────│  Confidence Routing     │
│  User ↔ SupportBot  │     │  (Groq Cloud API)     │     │  ≥ 0.60 → direct reply  │
│  multi-turn dialogue │     │  Professional response│     │  < 0.60 → clarify first │
└─────────────────────┘     └──────────────────────┘     └─────────────────────────┘
                                       ▲
                         ┌─────────────────────────┐
                         │  RoBERTa Classifier #2   │
                         │  Category Model (11 cls) │
                         │  High-level topic routing│
                         └─────────────────────────┘
```

---

## Key Results

| Metric | Value |
|--------|-------|
| Test Set Accuracy | **99.98%** |
| Macro F1 Score | **0.9996** |
| Weighted F1 Score | **0.9998** |
| Test Loss | **0.0017** |
| Total Misclassifications | **1 out of 4,031 samples** |
| Training Time | ~5 minutes (4 epochs, early stopping) |
| Throughput | 635 samples/second |

---

## Features

- **Dual Parallel Classification** - Intent (27 classes) and Category (11 classes) predicted simultaneously on the first user message, then locked into context for the entire session
- **Class-Weighted Loss** - Handles dataset imbalance (6.3× between most/least frequent classes) by penalizing minority-class errors more heavily
- **Confidence-Based Routing** - Automatically asks a clarifying question when overall confidence falls below 0.60
- **Stateful Conversation Memory** - Full conversation history passed to LLaMA on every turn; no topic drift
- **Zero-Code Interface** - Streamlit UI with visual confidence bars, live chat, and reset functionality; no technical knowledge required
- **Dynamic Padding** - Per-batch padding (not global max length), reducing GPU memory waste for short-text inputs

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Classifier | RoBERTa-base (HuggingFace Transformers) - fine-tuned twice |
| LLM Backend | LLaMA 3.3 70B Versatile via Groq Cloud API |
| UI Framework | Streamlit |
| Training Framework | HuggingFace `Trainer` with custom weighted loss |
| Hardware | NVIDIA GPU (CUDA-enabled) |
| Language | Python 3.10+ |

---

## Dataset

The model is trained on the **[Bitext Customer Support LLM Chatbot Training Dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset)** - a professionally curated dataset of 26,872 customer utterances covering 11 support categories and 27 fine-grained intents.

### Category Distribution

| Category | Samples | Share |
|----------|---------|-------|
| ACCOUNT | 5,986 | 22.3% |
| ORDER | 3,988 | 14.8% |
| REFUND | 2,992 | 11.1% |
| CONTACT | 1,999 | 7.4% |
| INVOICE | 1,999 | 7.4% |
| PAYMENT | 1,998 | 7.4% |
| FEEDBACK | 1,997 | 7.4% |
| DELIVERY | 1,994 | 7.4% |
| SHIPPING | 1,970 | 7.3% |
| SUBSCRIPTION | 999 | 3.7% |
| CANCEL | 950 | 3.5% |

**Imbalance ratio: 6.30×** (ACCOUNT vs. CANCEL) - addressed via class-weighted cross-entropy loss during training.

### Data Split

| Split | Samples | Share |
|-------|---------|-------|
| Train | 18,810 | 70% |
| Validation | 4,031 | 15% |
| Test | 4,031 | 15% |

Stratified splitting applied across all splits. Random seed: 42.

---

## Model Architecture

### RoBERTa-base

| Parameter | Value |
|-----------|-------|
| Architecture | Transformer Encoder (12 layers, 12 attention heads) |
| Hidden Size | 768 dimensions |
| Total Parameters | 124,654,091 (full fine-tuning) |
| Classification Head | Dense(768 → 27) for intent; Dense(768 → 11) for category |
| Tokenizer | Byte-Pair Encoding (BPE), vocab size 50,265 |
| Max Sequence Length | 64 tokens |

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Learning Rate | 2e-5 |
| Batch Size | 32 (train) / 64 (eval) |
| Max Epochs | 10 (early stopping, patience=3) |
| LR Scheduler | Cosine decay |
| Weight Decay | 0.01 (L2 regularization) |
| Mixed Precision | FP16 (when CUDA available) |
| Model Selection | Best Macro F1 checkpoint |
| Seed | 42 |

---

## Repository Structure

```bash
customer-support-chatbot/
│   How to run.txt                          # Quick-start instructions
│
├───Customer Service ChatBot/               # Core application
│       .env                                # Environment variables (API keys)
│       app.py                              # Streamlit web application
│       Chatbot.py                          # Conversational loop & Groq LLM integration
│       Config.py                           # Model paths, LLM & app configuration
│       Model_tokenizer.py                  # RoBERTa model & tokenizer loading utilities
│
├───Documentation/
│       Customer Support Chatbot Documentation Github.pdf   # Full technical documentation
│
├───Results/
│   ├───category results/
│   │       classification report category.txt              # Per-class precision/recall/F1
│   │       Screenshot 2026-05-04 035753.png                # Confusion matrix (category)
│   │       training_curves_category.png                    # Loss & accuracy curves
│   │
│   └───intent results/
│           confusion_matrix_intent.png                     # Confusion matrix (intent)
│           intent classification results.txt               # Per-class metrics (27 intents)
│           training_curves_intent.png                      # Loss & accuracy curves
│
├───Saved Models/
│   ├───best_model_category/                # Fine-tuned RoBERTa — Category (11 classes)
│   │       config.json
│   │       model.safetensors
│   │       tokenizer.json
│   │       tokenizer_config.json
│   │       training_args.bin
│   │
│   └───best_model_intent/                  # Fine-tuned RoBERTa — Intent (27 classes)
│           config.json
│           model.safetensors
│           tokenizer.json
│           tokenizer_config.json
│           training_args.bin
│
├───Test_Scripts/
│       Config.py                           # Test environment configuration
│       Testing_models_together.py          # Dual-model inference testing script
│
└───Trainig Notebooks/
        Bitext Customer Support Category Intent Final One.ipynb   # Full training pipeline
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/customer-support-chatbot.git
cd customer-support-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Open `Customer Service ChatBot/.env` and set your credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 4. (Optional) Re-train the Models

Open and run the training notebook end-to-end:

```
Training Notebooks/Bitext Customer Support Category Intent Final One.ipynb
```

> Pre-trained model weights are already included in `Saved Models/` — you can skip this step and run the app directly.

### 5. Launch the App

```bash
cd "Customer Service ChatBot"
streamlit run app.py
```

> See `How to run.txt` in the root directory for additional environment-specific notes.

---

## Usage

1. Open the Streamlit interface in your browser (default: `http://localhost:8501`)
2. Type your customer support issue in the text area (e.g., *"I can't remember my account password"*)
3. Click **Analyze & Start Chat**
4. The system displays:
   - Predicted **Intent** (e.g., `recover_password`) with confidence score
   - Predicted **Category** (e.g., `ACCOUNT`) with confidence score
   - Overall confidence level (HIGH / LOW)
5. The LLM immediately begins a professional support conversation based on the classification results
6. Continue chatting — the bot maintains full session memory
7. Click **Reset** to start a new session

---

## Per-Class Performance (Test Set)

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| ACCOUNT | 1.00 | 1.00 | 1.00 | 898 |
| CANCEL | 1.00 | 1.00 | 1.00 | 142 |
| CONTACT | 1.00 | 1.00 | 1.00 | 300 |
| DELIVERY | 1.00 | 1.00 | 1.00 | 299 |
| FEEDBACK | 1.00 | 1.00 | 1.00 | 300 |
| INVOICE | 1.00 | 1.00 | 1.00 | 300 |
| ORDER | 1.00 | 1.00 | 1.00 | 598 |
| PAYMENT | 1.00 | 1.00 | 1.00 | 300 |
| REFUND | 1.00 | 1.00 | 1.00 | 449 |
| SHIPPING | 1.00 | 1.00 | 1.00 | 295 |
| SUBSCRIPTION | 1.00 | 0.99 | 1.00 | 150 |
| **Macro Avg** | **1.00** | **1.00** | **1.00** | **4031** |

> The single misclassification was a SUBSCRIPTION utterance predicted as ORDER — a semantically adjacent edge case where subscription language overlaps with order language.

---

## LLM Configuration

| Parameter | Value |
|-----------|-------|
| Model | LLaMA 3.3 70B Versatile |
| Provider | Groq Cloud API |
| Temperature | 0.3 (controlled, professional tone) |
| Persona | SupportBotV1 — professional female customer support agent |
| Memory | Full conversation history per session |
| Confidence Threshold | ≥ 0.60: direct response / < 0.60: clarifying question |

---

## Acknowledgments

This project was developed by **Eng. Ahmed Mohamed Hussein** as a complete end-to-end NLP system demonstrating transformer-based intent classification integrated with conversational AI.

Special thanks to **[Bitext Innovations](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset)** for the high-quality training dataset, and to the **Groq Cloud** team for ultra-fast LLM inference.

---

**License:** MIT License
