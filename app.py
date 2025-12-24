import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
import pandas as pd  # Needed for the Metadata Audit table
import sys

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Post Genius - LinkedIn Generator",
    page_icon="🤖",
    # Set layout to wide to enable the two-column structure
    layout="wide"
)

# --- 1. DESIGN & AESTHETICS (Custom CSS Overwrite) ---
st.markdown("""
<style>
/* Base Colors: Dark Background, Vibrant Accent */
:root {
    --bg-color: #1E2833; /* Deep professional navy/charcoal */
    --panel-color: #29394A; /* Slightly lighter container background */
    --accent-color: #00AEEF; /* Vibrant Cyan/Primary Button Color */
    --text-color: #FAFAFA;
    --card-shadow: rgba(0,0,0,0.3);
}

/* Global Body/Main Styles */
.stApp {
    background-color: var(--bg-color);
    color: var(--text-color);
}
h1 { 
    text-align:center; 
    font-weight:800; 
    font-size:48px; /* Slightly larger headline */
    color: var(--accent-color); 
}
h2 { color: var(--text-color); }

.subtitle { 
    text-align:center; 
    font-size:18px; 
    margin-top:5px; 
    margin-bottom:40px; 
    color: #AAAAAA; /* Gray subtitle text */
}

/* Navbar/Header Placeholder Style */
.st-emotion-cache-18ni3sq {
    padding-top: 1rem;
    padding-bottom: 1rem;
    background-color: var(--bg-color);
}

/* Main Generator Card Container */
.main-generator-card { 
    background-color: var(--panel-color); 
    padding:30px; 
    border-radius:15px; 
    box-shadow:0px 8px 25px var(--card-shadow); 
    margin-top:20px; 
}

/* Input Panel Headers */
.panel { 
    background-color: #4a5d73;
    padding:10px 15px; 
    border-radius:10px; 
    margin-bottom:10px; 
    color: var(--text-color); 
    font-weight: bold;
}

/* Button Styling (Primary Accent Color) */
.stButton>button { 
    width:100%; 
    background: var(--accent-color); 
    color: var(--bg-color); /* Dark text on bright button */
    font-weight:bold; 
    border-radius:10px; 
    padding:15px 0; 
    font-size:18px; 
    border: none;
    transition: background 0.3s;
}

/* Input Fields */
.stTextInput>div>div>input, .stTextArea>div>div>textarea { 
    background-color: #36495E;
    color: var(--text-color);
    border: 1px solid #005a73; 
    border-radius:10px; 
    padding:10px 15px; 
}
</style>
""", unsafe_allow_html=True)


# ---------------- CHROMA SETUP (Keep setup) ----------------
@st.cache_resource
def setup_chroma():
    try:
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        # Use PersistentClient to load data saved by preprocess.py
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(
            name="linkedin_styles",
            embedding_function=embedding_function
        )
        return collection
    except Exception:
        # Return None if the database setup fails
        return None


collection = setup_chroma()

# ---------------- HEADER & HERO SECTION ----------------

# 1. Header/Navbar Placeholder (Simulated using Markdown and Columns)
col_logo, col_nav = st.columns([1, 4])
with col_logo:
    st.markdown("## AI Post Genius", unsafe_allow_html=True)
with col_nav:
    # Simulating the right-aligned navigation items
    st.markdown(
        "<div style='text-align: right; margin-top: 15px;'>"
        "<span style='margin-right: 20px;'>Features</span>"
        "<span style='margin-right: 20px;'>Pricing</span>"
        "<span style='margin-right: 20px;'>Login</span>"
        "<span style='background-color: #00AEEF; color: #1E2833; padding: 8px 15px; border-radius: 5px; font-weight: bold;'>Try It Free</span>"
        "</div>", unsafe_allow_html=True
    )
st.markdown("---")

# 2. Hero Section (Headline)
st.markdown("<h1>Create High-Impact LinkedIn Posts with AI.</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Leverage Llama-powered RAG for Style-Consistent Content.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)  # Extra space

# ---------------- MAIN GENERATOR (TWO-COLUMN LAYOUT) ----------------

# Use a custom div to apply the 'card' styling to the entire two-column area
st.markdown("<div class='main-generator-card'>", unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1])

# --- LEFT COLUMN: INPUTS (The Control Panel) ---
with col_left:
    st.subheader("⚙️ Input & Style Control")

    # 1. Topic Input (Large, multi-line text area)
    st.markdown("<div class='panel'>📝 What is your post about?</div>", unsafe_allow_html=True)
    topic = st.text_area(
        "Topic Input",
        placeholder="Enter your core message, keywords, or idea (e.g., 'consistency is key to success')",
        height=150,
        label_visibility="collapsed"
    )

    # 2. Style Selectors (Dropdowns)
    col_tone, col_length = st.columns(2)
    with col_tone:
        st.markdown("<div class='panel'>🎭 Target Tone</div>", unsafe_allow_html=True)
        tone = st.selectbox("Tone", ["Professional 💼", "Motivational 🔥", "Emotional ❤️", "Funny 😄"],
                            label_visibility="collapsed")
    with col_length:
        st.markdown("<div class='panel'>📏 Post Length</div>", unsafe_allow_html=True)
        length = st.selectbox("Length", ["Short", "Medium", "Long"], label_visibility="collapsed")

    # 3. The Button
    generate = st.button("🚀 Generate My Post", key="generate_btn")

# --- RIGHT COLUMN: OUTPUT / RETRIEVAL REPORT ---
with col_right:
    st.subheader("✨ RAG Content Audit & Output")

    # Placeholder for Generated Text (Placeholder Title: "✨ Generated Content.")
    output_container = st.container(border=True)
    output_placeholder = output_container.empty()
    output_placeholder.markdown(
        "*Output will appear here. The system retrieves style examples for consistent generation.*")

    # 3. Actions (Small buttons below the output box)
    col_copy, col_regen = st.columns(2)
    with col_copy:
        st.button("📋 Copy Text", use_container_width=True, key="copy_btn")
    with col_regen:
        st.button("🔁 Generate Again", use_container_width=True, key="regen_btn")

st.markdown("</div>", unsafe_allow_html=True)  # Close main-generator-card

# ---------------- GENERATION/RETRIEVAL LOGIC ----------------
# ---------------- GENERATION ----------------
def generate_post(topic, context, tone, length):
    topic_l = topic.lower()

    if length == "Short":
        if "Emotional" in tone:
            return f"❤️ {topic.title()} taught me lessons I will never forget.\n{context}"
        elif "Funny" in tone:
            return f"😄 {topic.title()}… we all ignore it until it's gone 😅\n{context}"
        elif "Motivational" in tone:
            return f"🔥 {topic.title()} is the key to success.\n{context}"
        else:
            return f"💼 {topic.title()} is important in the professional world.\n{context}"

    elif length == "Medium":
        if "Emotional" in tone:
            return f"❤️ **{topic.title()}**\n\nThere was a moment I underestimated *{topic_l}*.\n{context}\nGrowth happens quietly, behind the scenes. Keep pushing forward."
        elif "Funny" in tone:
            return f"😄 **{topic.title()}**\n\nNobody talks enough about *{topic_l}*… until it disappears 😅\n{context}\nPatience and persistence beat instant gratification every time."
        elif "Motivational" in tone:
            return f"🔥 **{topic.title()}**\n\nSuccess isn’t accidental. *{topic_l}* makes all the difference.\n{context}\nSmall consistent efforts compound into great results."
        else:
            return f"💼 **{topic.title()}**\n\nIn today’s competitive landscape, *{topic_l}* is a differentiator.\n{context}\nConsistency and learning drive sustainable growth."

    else:  # Long
        if "Emotional" in tone:
            return f"❤️ **{topic.title()}**\n\nThere was a time I underestimated the power of *{topic_l}*.\n{context}\nGrowth isn’t loud—it’s quiet, consistent, and deeply personal.\nEvery lesson stays with you long after the noise fades.\nKeep going. ❤️"
        elif "Funny" in tone:
            return f"😄 **{topic.title()}**\n\nNobody talks enough about *{topic_l}*… until it disappears 😅\n{context}\nSuccess needs patience, practice, and fewer excuses.\nShow up, even when motivation disappears."
        elif "Motivational" in tone:
            return f"🔥 **{topic.title()}**\n\nSuccess doesn’t happen by accident. *{topic_l}* builds it.\n{context}\nEvery small step matters. Every effort compounds.\nStay focused and disciplined.\nYour future self will thank you. 🚀"
        else:
            return f"💼 **{topic.title()}**\n\nIn today’s professional world, *{topic_l}* is critical.\n{context}\nSustainable success comes from deliberate effort, continuous learning, and consistency."


# ---------------- GENERATE & SHOW ----------------
if generate:
    if not topic.strip():
        st.warning("Please enter a topic before generating.")
    else:
        # Retrieve context from Chroma DB if possible
        context = "Consistency and learning drive long-term professional success."
        if collection:
            try:
                results = collection.query(query_texts=[topic], n_results=3, include=["documents"])
                docs = results.get("documents", [[]])[0]
                if docs:
                    context = docs[0]  # Use first document as context
            except Exception as e:
                st.warning(f"Could not retrieve context from DB: {e}")

        # Generate post
        post = generate_post(topic, context, tone, length)

        # Display in a card
        st.markdown(
            f"<div style='background-color:white; padding:30px; border-radius:20px; box-shadow:0px 8px 25px rgba(0,0,0,0.15); color:black;'>"
            f"<h3>✨ Generated LinkedIn Post</h3>"
            f"<p>{post.replace(chr(10), '<br>')}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:12px; color:#AAAAAA;'>Copyright 2024 AI Post Genius | Terms of Service | Privacy Policy</p>",
    unsafe_allow_html=True)