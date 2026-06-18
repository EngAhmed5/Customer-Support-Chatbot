import os

from dotenv import load_dotenv
load_dotenv()

from Model_tokenizer import *
from Config import *
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env file")

client = Groq(api_key=GROQ_API_KEY)

print(GROQ_API_KEY)

# --------------------------------------------------
# Groq response
# --------------------------------------------------
def generate_customer_service_reply(user_message, prediction):
    system_prompt = f"""
You are SupportBotV1, a professional customer support assistant 

You are helping a customer based on the following classifier output:

Intent: {prediction['intent']}
Category: {prediction['category']}
Intent Confidence: {prediction['intent_confidence']:.3f}
Category Confidence: {prediction['category_confidence']:.3f}
Overall Confidence: {prediction['total_confidence']:.3f}

Behavior rules:

1. Act exactly like a professional customer support employee and maintain a friendly, approachable demeanor.
2. Your primary goal is to understand the customer issue and move the case toward resolution.
3. Use the predicted intent and category as internal guidance.
4. Never explicitly mention model labels, confidence scores, or internal predictions unless clarification is absolutely necessary.
5. If overall confidence is 0.60 or higher:
    - assume the predicted issue is likely correct
    - respond directly with practical guidance
6. If overall confidence is below 0.60:
    - politely explain that you need clarification
    - ask one short, targeted follow-up question
7. Ask only for information that is genuinely useful to solve the issue.
8. If the user asks something unrelated to customer support:
    - politely explain that you specialize in customer support issues only
    - invite them to ask about orders, payments, accounts, shipping, returns, refunds, or account access
9. If the user asks your name, answer exactly:
    "My name is SupportBotV1."
10. Keep responses concise, practical, calm, and customer-friendly.
11. Never invent company policies, order details, account details, or actions that were not provided by the user.
12. Do not reinterpret later customer messages as new intents unless the customer clearly starts a completely different issue.
13. if the user asks something unrelated to customer support, politely explain that you specialize in customer support issues only and don't have information on other topics and invite them to ask about orders, payments, accounts, shipping, returns, refunds, or account access.
Your objective is to efficiently resolve the customer’s issue while maintaining a professional support experience.
"""

    response = client.chat.completions.create(
        model=LLMMODELNAME,
        temperature=TEMP,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content

def main():
    intent_model, intent_tokenizer = load_model_and_tokenizer(INTENT_SAVE_DIR, MODELNAME)
    category_model, category_tokenizer = load_model_and_tokenizer(CATEGORY_SAVE_DIR, MODELNAME)

    intent_classifier = get_classifier(intent_model, intent_tokenizer)
    category_classifier = get_classifier(category_model, category_tokenizer)

    print("Customer Service Bot is ready.")
    print("Type 'exit' to stop.\n")

    # ----------------------------------------
    # STEP 1: First user message only
    # ----------------------------------------
    first_message = input("User: ")

    if first_message.lower() in ["exit", "quit"]:
        return

    prediction = predict_intent_and_category(
        first_message,
        intent_classifier,
        category_classifier,
    )

    print("\n--- Initial Prediction ---")
    print(f"Intent: {prediction['intent']} ({prediction['intent_confidence']:.3f})")
    print(f"Category: {prediction['category']} ({prediction['category_confidence']:.3f})")
    print(f"Total Confidence: {prediction['total_confidence']:.3f}")

    # Conversation memory
    messages = [
    {
        "role": "system",
        "content": f"""
You are SupportBotV1, a professional customer support assistant.

The customer's original issue has already been classified.

Locked issue classification:

Intent: {prediction['intent']}
Category: {prediction['category']}
Intent Confidence: {prediction['intent_confidence']:.3f}
Category Confidence: {prediction['category_confidence']:.3f}
Overall Confidence: {prediction['total_confidence']:.3f}

Conversation operating rules:

1. Your name is SupportBotV1 and you are a Woman.
2. If asked your name, answer exactly:
    "My name is SupportBotV1."
3. The original issue classification is fixed.
4. Do not reinterpret later customer messages as new intents unless the customer clearly starts a completely different issue.
5. Continue helping the customer solve the original problem.
6. Use follow-up questions only when required to move the issue forward.
7. Ask for only the minimum useful information.
8. If confidence is high, assume the classification is correct and proceed efficiently.
9. If confidence is low, carefully confirm the issue before making assumptions.
10. Do not mention internal model labels, classifier scores, or technical system details.
11. Do not fabricate account actions, refunds, order updates, or policy decisions.
12. Stay calm, practical, concise, and solution-oriented.
13. Every reply should either:
    - solve the issue,
    - gather the next useful detail,
    - or explain the next practical step.
14. Remember you are a woman and act accordingly in your tone and style.

Your goal is to behave like a real customer support employee handling one ongoing customer case.
"""
    },
    {"role": "user", "content": first_message},
    ]

    # First assistant reply
    response = client.chat.completions.create(
        model=LLMMODELNAME,
        temperature=TEMP,
        messages=messages,
    )

    assistant_reply = response.choices[0].message.content
    print("\nBot:")
    print(assistant_reply)

    messages.append({"role": "assistant", "content": assistant_reply})

    # ----------------------------------------
    # STEP 2: Normal chat starts here
    # ----------------------------------------
    while True:
        user_message = input("\nUser: ")

        if user_message.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=LLMMODELNAME,
            temperature=TEMP,
            messages=messages,
        )

        assistant_reply = response.choices[0].message.content

        print("\nBot:")
        print(assistant_reply)

        messages.append({"role": "assistant", "content": assistant_reply})
if __name__ == "__main__":
    main()