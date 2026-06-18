from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from Config import *


def load_model_and_tokenizer(model_dir , ModelName):
    # Load the tokenizer from HuggingFace (roberta-base)
    tokenizer = AutoTokenizer.from_pretrained(ModelName)
    
    # Load the fine-tuned model weights from the local folder
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    
    return model, tokenizer


def get_classifier(model , tokenizer):
    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device= DEVICE ,
        truncation=True,
        max_length=MAX_LENGTH,
    )
    print("------- Classifier pipeline created successfully. -------")
    return classifier


def predict_intent_and_category(text, intent_classifier, category_classifier):
    
    intent_result = intent_classifier(text)[0]
    category_result = category_classifier(text)[0]
    
    intent_label = intent_result["label"]
    category_label = category_result["label"]
    
    intent_score = intent_result["score"]
    category_score = category_result["score"]
    
    intent_bar = "█" * int(intent_score * 20)
    category_bar = "█" * int(category_score * 20)
    
    total_confidence = (intent_score + category_score) / 2
    total_bar = "█" * int(total_confidence * 20)
    
    return {
        "intent": intent_label,
        "category": category_label,
        "intent_confidence": intent_score,
        "category_confidence": category_score,
        "total_confidence": total_confidence,
    }


if __name__ == "__main__":
    
    intent_model , intent_tokenizer = load_model_and_tokenizer(INTENT_SAVE_DIR , MODELNAME)
    category_model , category_tokenizer = load_model_and_tokenizer(CATEGORY_SAVE_DIR , MODELNAME)

    intent_classifier = get_classifier(intent_model , intent_tokenizer)
    category_classifier = get_classifier(category_model , category_tokenizer)
    
    examples = [
    "I need to cancel my order, I ordered the wrong item",
    "where is my package? it was supposed to arrive yesterday",
    "I was charged twice on my credit card this month",
    "how do i return this and get a refund?",
    "I forgot my password and can't log into my account",
    "can u change the shipping address for order 12345",
    "my account got hacked i think someone else is using it",
    "what payment methods do you accept?",
    "how is ronaldo ? " # for testing the model's behavior 
    ]
    
    
    for text in examples:
        results = predict_intent_and_category(text, intent_classifier, category_classifier)
        
        # Unpack the results
        i_label = results["intent"]
        i_score = results["intent_confidence"]
        i_bar = "█" * int(i_score * 20)
        c_label = results["category"]
        c_score = results["category_confidence"]
        c_bar = "█" * int(c_score * 20)
        t_score = results["total_confidence"]
        t_bar = "█" * int(t_score * 20) 
        
        # Formatted Output
        print(f"Text: \"{text}\"")
        print(f"  Intent   : {i_label:<15} [{i_bar:<20}] {i_score:.2%}")
        print(f"  Category : {c_label:<15}[{c_bar:<20}] {c_score:.2%}")
        print(f"  Overall  : {'Average Conf':<15}[{t_bar:<20}] {t_score:.2%}")
        print("=" * 80)
    