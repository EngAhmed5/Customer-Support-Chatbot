import torch

# ----------- Model Path and Configurations -----------
INTENT_SAVE_DIR = r"D:\Ahmed\Study\NLP\Practical Project final version\Saved Models\best_model_intent"
CATEGORY_SAVE_DIR = r"D:\Ahmed\Study\NLP\Practical Project final version\Saved Models\best_model_category"

MAX_LENGTH = 64
LABEL_MODE = "category"


# ----------- Device Configuration -----------
DEVICE = 0 if torch.cuda.is_available() else -1

#------------- Model Name -------------
MODELNAME = "roberta-base"

#------------- LLM Configurations -------------

LLMMODELNAME="llama-3.3-70b-versatile"
TEMP = 0.3