import json

import streamlit as st

from app.analyzer import summarize_text

st.set_page_config(
    page_title="AI Text Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 25px;
    }

    .result-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    .sentiment {
        font-size: 24px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🤖 AI Text Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze long documents using Google Gemini AI'
    '</div>',
    unsafe_allow_html=True
)

with st.sidebar:

    st.header("⚙️ Settings")

    summary_type = st.selectbox(
        "Summary Length",
        [
            "short",
            "medium",
            "detailed"
        ],
        format_func=lambda x: x.capitalize()
    )

    st.divider()

    st.subheader("📌 Supported Analysis")

    st.markdown(
        """
        - 📝 Summary
        - 🔑 Key Points
        - 🏷️ Keywords
        - 😊 Sentiment
        - 🏢 Entities
        - ✅ Action Items
        """
    )

    st.divider()

    st.caption(
        "Powered by Google Gemini"
    )

st.header("📄 Input Document")

uploaded_file = st.file_uploader(
    "Upload a TXT file",
    type=["txt"]
)


text_input = st.text_area(
    "Or paste your text below",
    height=280,
    placeholder=(
        "Paste your document here..."
    )
)

text = text_input


if uploaded_file is not None:

    try:

        file_text = uploaded_file.read().decode(
            "utf-8"
        )

        text = file_text

        st.success(
            f"📄 Loaded: {uploaded_file.name}"
        )

    except UnicodeDecodeError:

        st.error(
            "Unable to read this file. "
            "Please upload a UTF-8 encoded TXT file."
        )

        text = ""

if text.strip():

    words = len(
        text.split()
    )

    characters = len(text)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Characters",
            f"{characters:,}"
        )

    with col2:

        st.metric(
            "Words",
            f"{words:,}"
        )

col1, col2 = st.columns([3, 1])


with col1:

    analyze_button = st.button(
        "🔍 Analyze Document",
        type="primary",
        use_container_width=True
    )


with col2:

    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


if clear_button:

    st.session_state.pop(
        "result",
        None
    )

    st.rerun()

if analyze_button:

    if not text.strip():

        st.warning(
            "⚠️ Please enter text or upload a TXT file."
        )

    else:

        try:

            with st.spinner(
                "🤖 Gemini is analyzing your document..."
            ):

                result = summarize_text(
                    text,
                    summary_type
                )

            if isinstance(result, str):

                result = json.loads(result)

            if not isinstance(result, dict):

                raise ValueError(
                    "Gemini returned an unexpected response format."
                )

            st.session_state["result"] = result

            st.success(
                "✅ Analysis completed successfully!"
            )

        except json.JSONDecodeError:

            st.error(
                "❌ Gemini returned invalid JSON. "
                "Please try again."
            )

        except Exception as e:

            st.error(
                "❌ Analysis failed."
            )

            st.info(
                "Please check your API configuration, "
                "internet connection, and API quota."
            )

            with st.expander(
                "Technical details"
            ):

                st.code(
                    str(e)
                )

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.header("📊 Analysis Results")

    st.subheader("📝 Summary")

    summary = result.get(
        "summary",
        "No summary available."
    )

    st.info(summary)

    st.subheader("🔑 Key Points")

    key_points = result.get(
        "key_points",
        []
    )

    if key_points:

        for point in key_points:

            st.markdown(
                f"- {point}"
            )

    else:

        st.write(
            "No key points found."
        )

    st.subheader("🏷️ Keywords")

    keywords = result.get(
        "keywords",
        []
    )

    if keywords:

        keyword_text = " • ".join(
            str(keyword)
            for keyword in keywords
        )

        st.markdown(
            f"**{keyword_text}**"
        )

    else:

        st.write(
            "No keywords found."
        )

    st.subheader("😊 Sentiment")

    sentiment = str(
        result.get(
            "sentiment",
            "Unknown"
        )
    )

    sentiment_lower = sentiment.lower()

    if sentiment_lower == "positive":

        st.success(
            "😊 Positive"
        )

    elif sentiment_lower == "negative":

        st.error(
            "😞 Negative"
        )

    else:

        st.info(
            "😐 Neutral"
        )

    st.subheader("🏢 Named Entities")

    entities = result.get(
        "entities",
        []
    )

    if entities:

        for entity in entities:

            st.markdown(
                f"- **{entity}**"
            )

    else:

        st.write(
            "No named entities found."
        )

    st.subheader("✅ Action Items")

    action_items = result.get(
        "action_items",
        []
    )

    if action_items:

        for action in action_items:

            st.checkbox(
                action,
                key=f"action_{action}"
            )

    else:

        st.write(
            "No action items found."
        )