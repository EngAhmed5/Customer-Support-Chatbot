import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Support Chatbot",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Söhne:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:         #0a0d14;
    --surface:    #111520;
    --surface2:   #181d2e;
    --border:     #1f2740;
    --accent:     #4f8ef7;
    --accent2:    #7c5af7;
    --text:       #e2e8f8;
    --muted:      #6b7a99;
    --danger:     #f75a5a;
    --success:    #00d4aa;
    --warning:    #f7a84f;
    --radius:     14px;
    --radius-sm:  8px;
}

html, body, [class*="css"] {
    font-family: 'Söhne', ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, var(--surface) 0%, #0d1526 60%, var(--bg) 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px 40px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(79,142,247,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute; bottom: -40px; left: 20%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(124,90,247,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(79,142,247,0.12);
    border: 1px solid rgba(79,142,247,0.3);
    border-radius: 99px;
    padding: 4px 14px;
    font-size: 11px; font-weight: 600; letter-spacing: 1.5px;
    color: var(--accent); text-transform: uppercase;
    margin-bottom: 14px;
}
.hero-title {
    font-size: 32px; font-weight: 700; line-height: 1.2;
    background: linear-gradient(135deg, #e2e8f8 30%, var(--accent) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 8px;
}
.hero-sub { font-size: 14px; color: var(--muted); font-weight: 400; margin: 0; }
.hero-dot {
    display: inline-block; width: 7px; height: 7px;
    background: var(--success); border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 8px var(--success);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: .5; transform: scale(1.4); }
}

/* ── Section label ── */
.section-label {
    font-size: 10px; font-weight: 600; letter-spacing: 2px;
    color: var(--muted); text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── Inputs ── */
textarea {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif !important;
    font-size: 14px !important;
    transition: border-color .2s;
}
textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(79,142,247,.12) !important; }

.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif !important;
    font-size: 13.5px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,.12) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 24px !important;
    transition: opacity .2s, transform .1s !important;
}
.stButton > button:hover { opacity: .88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

.reset-btn > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-size: 12px !important;
    padding: 6px 16px !important;
}
.reset-btn > button:hover { border-color: var(--danger) !important; color: var(--danger) !important; }

/* ── Prediction panel ── */
.pred-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px 24px;
    margin-bottom: 20px;
    animation: fadeUp .35s ease;
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(12px); }
    to   { opacity:1; transform:translateY(0); }
}
.pred-row { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.pred-row:last-child { margin-bottom: 0; }
.pred-icon {
    width: 36px; height: 36px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.pred-icon.intent   { background: rgba(79,142,247,.15); }
.pred-icon.category { background: rgba(124,90,247,.15); }
.pred-icon.overall  { background: rgba(0,212,170,.15); }
.pred-info { flex: 1; min-width: 0; }
.pred-key {
    font-size: 10px; color: var(--muted); text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 600; margin-bottom: 3px;
}
.pred-val { font-size: 14px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pred-bar-wrap { height: 5px; background: var(--border); border-radius: 99px; margin-top: 5px; }
.pred-bar { height: 100%; border-radius: 99px; transition: width .6s cubic-bezier(.4,0,.2,1); }
.pred-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; font-weight: 500; color: var(--muted);
    flex-shrink: 0; min-width: 42px; text-align: right;
}
.conf-badge {
    display: inline-block; padding: 3px 10px; border-radius: 99px;
    font-size: 11px; font-weight: 600; letter-spacing: .5px;
}
.conf-high   { background: rgba(0,212,170,.15);  color: var(--success); }
.conf-medium { background: rgba(247,168,79,.15); color: var(--warning); }
.conf-low    { background: rgba(247,90,90,.15);  color: var(--danger);  }

/* ── Divider ── */
.divider { height: 1px; background: var(--border); margin: 24px 0; }

/* ── Chat area ── */
.chat-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 16px;
}
.chat-header {
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
    padding: 16px 24px;
    display: flex; align-items: center; gap: 12px;
}
.chat-avatar {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.chat-agent-name { font-weight: 600; font-size: 14px; }
.chat-agent-status { font-size: 11px; color: var(--success); display: flex; align-items: center; gap: 4px; }
.chat-messages {
    padding: 24px 32px;
    min-height: 200px;
    max-height: 600px;
    overflow-y: auto;
}
.msg-row { display: flex; gap: 10px; margin-bottom: 16px; align-items: flex-end; }
.msg-row.user { flex-direction: row-reverse; }
.msg-bubble {
    max-width: 82%; padding: 13px 18px; border-radius: 16px;
    font-size: 15px; line-height: 1.75; word-break: break-word;
}
.msg-bubble.bot {
    background: var(--surface2); border: 1px solid var(--border);
    border-bottom-left-radius: 4px; color: var(--text);
}
.msg-bubble.user {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    border-bottom-right-radius: 4px; color: #fff;
}
.msg-mini-avatar {
    width: 28px; height: 28px; border-radius: 50%;
    flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 13px;
}
.msg-mini-avatar.bot  { background: linear-gradient(135deg, var(--accent), var(--accent2)); }
.msg-mini-avatar.user { background: var(--surface2); border: 1px solid var(--border); }

/* ── Widen the centered content column ── */
section[data-testid="stMain"] > div:first-child,
.block-container {
    max-width: 860px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ── Misc ── */
.stSpinner > div { border-top-color: var(--accent) !important; }
label, .stMarkdown p { color: var(--text) !important; }
[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ───────────────────────────────────────────────────────────────
for key, val in {
    "messages":      [],
    "prediction":    None,
    "chat_active":   False,
    "first_message": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Model / API helpers (lazy-loaded, cached) ───────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_models():
    from Model_tokenizer import load_model_and_tokenizer, get_classifier
    from Config import INTENT_SAVE_DIR, CATEGORY_SAVE_DIR, MODELNAME
    intent_model,   intent_tok   = load_model_and_tokenizer(INTENT_SAVE_DIR,   MODELNAME)
    category_model, category_tok = load_model_and_tokenizer(CATEGORY_SAVE_DIR, MODELNAME)
    return (
        get_classifier(intent_model,   intent_tok),
        get_classifier(category_model, category_tok),
    )

def do_predict(text):
    from Model_tokenizer import predict_intent_and_category
    intent_clf, category_clf = load_models()
    return predict_intent_and_category(text, intent_clf, category_clf)

def get_groq_client():
    from groq import Groq
    key = os.getenv("GROQ_API_KEY")
    if not key:
        st.error("⚠️  GROQ_API_KEY not found in .env")
        st.stop()
    return Groq(api_key=key)

def groq_chat(messages):
    """Non-streaming — used for the very first bot reply on analyze."""
    from Config import LLMMODELNAME, TEMP
    client = get_groq_client()
    resp = client.chat.completions.create(
        model=LLMMODELNAME,
        temperature=TEMP,
        messages=messages,
    )
    return resp.choices[0].message.content

def groq_chat_stream(messages, placeholder):
    """
    Streaming — writes tokens into `placeholder` as they arrive.
    Returns the fully-assembled reply string when done.
    """
    from Config import LLMMODELNAME, TEMP
    client = get_groq_client()
    stream = client.chat.completions.create(
        model=LLMMODELNAME,
        temperature=TEMP,
        messages=messages,
        stream=True,
    )
    full_reply = ""
    for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        full_reply += token
        safe = full_reply.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        placeholder.markdown(f"""
<div class="msg-row">
  <div class="msg-mini-avatar bot">🤖</div>
  <div class="msg-bubble bot">{safe}<span style="opacity:.5;">▌</span></div>
</div>""", unsafe_allow_html=True)
    return full_reply

# ── System prompt — single source of truth, mirrors Chatbot.py exactly ─────────
def build_system_prompt(pred):
    """
    Identical to the system prompt used in Chatbot.py main() conversation loop.
    Any change to the bot's personality / rules must be made here only.
    """
    return f"""
You are SupportBotV1, a professional customer support assistant.

The customer's original issue has already been classified.

Locked issue classification:

Intent: {pred['intent']}
Category: {pred['category']}
Intent Confidence: {pred['intent_confidence']:.3f}
Category Confidence: {pred['category_confidence']:.3f}
Overall Confidence: {pred['total_confidence']:.3f}

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

# ── Confidence colour helper ────────────────────────────────────────────────────
def conf_class(score):
    if score >= 0.75: return "high",   "#00d4aa"
    if score >= 0.55: return "medium", "#f7a84f"
    return "low", "#f75a5a"

# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT  — single column, top-to-bottom
# ══════════════════════════════════════════════════════════════════════════════

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🎧 Customer Support Chatbot Using AI </div>
    <h1 class="hero-title">Customer Support Chatbot </h1>
    <p class="hero-sub">
        <span class="hero-dot"></span>
        Powered by RoBERTa intent classification &amp; Llama 3.3  (describe your issue to get started.)
    </p>
</div>
""", unsafe_allow_html=True)

# ── SECTION 1 : Issue input ────────────────────────────────────────────────────
st.markdown('<div class="section-label">📝 Describe Your Issue</div>', unsafe_allow_html=True)

user_input = st.text_area(
    label="issue",
    placeholder="e.g. I was charged twice on my credit card this month…",
    height=110,
    label_visibility="collapsed",
    key="main_input",
)

btn_col1, btn_col2 = st.columns([3, 1])
with btn_col1:
    analyze_clicked = st.button("⚡  Analyze & Start Chat", use_container_width=True)
with btn_col2:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    reset_clicked = st.button("↺  Reset", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Reset handler
if reset_clicked:
    for k in ["messages", "prediction", "chat_active", "first_message"]:
        st.session_state[k] = (
            []    if k == "messages"      else
            None  if k == "prediction"    else
            False if k == "chat_active"   else
            ""
        )
    st.rerun()

# Analyze handler
if analyze_clicked and user_input.strip():
    with st.spinner("Running classifiers, Please wait…"):
        pred = do_predict(user_input.strip())

    st.session_state.prediction    = pred
    st.session_state.first_message = user_input.strip()
    st.session_state.chat_active   = True

    system_msg = {"role": "system", "content": build_system_prompt(pred)}
    user_msg   = {"role": "user",   "content": user_input.strip()}

    with st.spinner("SupportBotV1 is responding…"):
        reply = groq_chat([system_msg, user_msg])

    st.session_state.messages = [system_msg, user_msg, {"role": "assistant", "content": reply}]
    st.rerun()

# ── SECTION 2 : Classification results (only after analysis) ───────────────────
if st.session_state.prediction:
    pred = st.session_state.prediction
    i_cls, i_col = conf_class(pred["intent_confidence"])
    c_cls, c_col = conf_class(pred["category_confidence"])
    o_cls, o_col = conf_class(pred["total_confidence"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🔍 Classification Results</div>', unsafe_allow_html=True)

    st.markdown(f"""
<div class="pred-panel">

  <div class="pred-row">
    <div class="pred-icon intent">🎯</div>
    <div class="pred-info">
      <div class="pred-key">Intent</div>
      <div class="pred-val">{pred['intent']}</div>
      <div class="pred-bar-wrap">
        <div class="pred-bar" style="width:{pred['intent_confidence']*100:.1f}%;background:{i_col};"></div>
      </div>
    </div>
    <div class="pred-pct">{pred['intent_confidence']*100:.1f}%</div>
  </div>

  <div class="pred-row">
    <div class="pred-icon category">🗂️</div>
    <div class="pred-info">
      <div class="pred-key">Category</div>
      <div class="pred-val">{pred['category']}</div>
      <div class="pred-bar-wrap">
        <div class="pred-bar" style="width:{pred['category_confidence']*100:.1f}%;background:{c_col};"></div>
      </div>
    </div>
    <div class="pred-pct">{pred['category_confidence']*100:.1f}%</div>
  </div>

  <div class="pred-row">
    <div class="pred-icon overall">📊</div>
    <div class="pred-info">
      <div class="pred-key">Overall Confidence</div>
      <div class="pred-val">
        <span class="conf-badge conf-{o_cls}">{o_cls.upper()}</span>
      </div>
      <div class="pred-bar-wrap">
        <div class="pred-bar" style="width:{pred['total_confidence']*100:.1f}%;background:{o_col};"></div>
      </div>
    </div>
    <div class="pred-pct">{pred['total_confidence']*100:.1f}%</div>
  </div>

</div>
""", unsafe_allow_html=True)

# ── SECTION 3 : Chat (only after analysis, user scrolls down to reach it) ──────
if st.session_state.chat_active:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">💬 Live Support Chat</div>', unsafe_allow_html=True)

    # Build chat bubbles HTML
    msgs = [m for m in st.session_state.messages if m["role"] != "system"]
    bubbles_html = ""
    for m in msgs:
        is_user      = m["role"] == "user"
        avatar_emoji = "👤" if is_user else "🤖"
        text         = m["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        row_cls      = "msg-row user" if is_user else "msg-row"
        avatar_cls   = "msg-mini-avatar user" if is_user else "msg-mini-avatar bot"
        bubble_cls   = "msg-bubble user" if is_user else "msg-bubble bot"
        bubbles_html += f"""
<div class="{row_cls}">
  <div class="{avatar_cls}">{avatar_emoji}</div>
  <div class="{bubble_cls}">{text}</div>
</div>"""

    st.markdown(f"""
<div class="chat-container">
  <div class="chat-header">
    <div class="chat-avatar">🤖</div>
    <div>
      <div class="chat-agent-name">SupportBotV1</div>
      <div class="chat-agent-status">
        <span class="hero-dot" style="width:6px;height:6px;"></span> Online &amp; Ready
      </div>
    </div>
  </div>
  <div class="chat-messages" id="chat-scroll">
    {bubbles_html}
  </div>
</div>
<script>
  const el = document.getElementById('chat-scroll');
  if (el) el.scrollTop = el.scrollHeight;
</script>
""", unsafe_allow_html=True)

    # Reply input — form so Enter key submits AND field clears automatically
    with st.form(key="chat_form", clear_on_submit=True):
        inp_col, btn_col = st.columns([5, 1])
        with inp_col:
            follow_up = st.text_input(
                "reply",
                placeholder="Type your reply and press Enter…",
                label_visibility="collapsed",
            )
        with btn_col:
            send_clicked = st.form_submit_button("Send →", use_container_width=True)

    if send_clicked and follow_up.strip():
        st.session_state.messages.append({"role": "user", "content": follow_up.strip()})
        stream_placeholder = st.empty()
        reply = groq_chat_stream(st.session_state.messages, stream_placeholder)
        stream_placeholder.empty()
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:40px;padding-top:16px;border-top:1px solid #1f2740;">
  <span style="font-size:11px;color:#3d4d6a;letter-spacing:.5px;">
    SupportBotV1 · RoBERTa + Llama 3.3 · Built for customer excellence
  </span>
</div>
""", unsafe_allow_html=True)