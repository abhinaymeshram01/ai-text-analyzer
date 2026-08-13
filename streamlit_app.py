import json

import streamlit as st

from app.analyzer import summarize_text

st.set_page_config(
    page_title="AI Text Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    .main-title {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 0;
        letter-spacing: -1px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    .card {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.20);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
    }


    .keyword-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .keyword-chip {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 20px;
        background-color: rgba(70, 130, 180, 0.12);
        border: 1px solid rgba(70, 130, 180, 0.25);
        font-size: 14px;
    }


    .entity-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .entity-chip {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 20px;
        background-color: rgba(128, 128, 128, 0.10);
        border: 1px solid rgba(128, 128, 128, 0.25);
        font-size: 14px;
    }


    .sentiment-positive {
        font-size: 24px;
        font-weight: 700;
    }

    .sentiment-negative {
        font-size: 24px;
        font-weight: 700;
    }

    .sentiment-neutral {
        font-size: 24px;
        font-weight: 700;
    }


    .footer {
        text-align: center;
        color: #888;
        font-size: 13px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid rgba(128, 128, 128, 0.20);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">🤖 AI Text Analyzer</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Analyze documents with Google Gemini AI — summaries,
        key points, keywords, sentiment, entities, and action items.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:

    st.header("⚙️ Settings")

    summary_type = st.selectbox(
        "Summary Length",
        ["short", "medium", "detailed"],
        index=1,
        format_func=lambda value: value.capitalize(),
    )

    st.divider()

    st.subheader("📌 Analysis Features")

    st.markdown(
        """
        📝 **Summary**

        🔑 **Key Points**

        🏷️ **Keywords**

        😊 **Sentiment**

        🏢 **Named Entities**

        ✅ **Action Items**
        """
    )

    st.divider()

    st.subheader("🧠 Processing")

    st.caption(
        "Short documents are analyzed directly. "
        "Long documents are automatically split into "
        "manageable chunks before Gemini analysis."
    )

    st.divider()

    st.caption("Powered by Google Gemini")

st.header("📄 Input Document")

uploaded_file = st.file_uploader(
    "Upload a TXT file",
    type=["txt"],
    help="Upload a UTF-8 encoded text file.",
)


text_input = st.text_area(
    "Or paste your text below",
    height=260,
    placeholder=(
        "Paste your document here...\n\n"
        "Example:\n"
        "The company is preparing to launch a new "
        "product in September."
    ),
)

text = text_input.strip()

uploaded_file_name = None

if uploaded_file is not None:

    try:

        uploaded_text = uploaded_file.read().decode("utf-8")

        if uploaded_text.strip():

            text = uploaded_text.strip()
            uploaded_file_name = uploaded_file.name

            st.success(
                f"📄 Loaded: **{uploaded_file.name}**"
            )

    except UnicodeDecodeError:

        st.error(
            "❌ Unable to read this file. "
            "Please upload a UTF-8 encoded TXT file."
        )

        text = ""

if text:

    characters = len(text)

    words = len(text.split())

    lines = len(text.splitlines())

    paragraphs = len(
        [
            paragraph
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]
    )

    st.subheader("📊 Document Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Characters",
            f"{characters:,}",
        )

    with col2:

        st.metric(
            "Words",
            f"{words:,}",
        )

    with col3:

        st.metric(
            "Lines",
            f"{lines:,}",
        )

    with col4:

        st.metric(
            "Paragraphs",
            f"{paragraphs:,}",
        )

if text:

    if len(text) > 12000:

        st.info(
            "📚 **Long document detected.** "
            "The analyzer will automatically split the document "
            "into chunks and combine the results."
        )

    else:

        st.success(
            "⚡ **Short document detected.** "
            "The document can be analyzed directly."
        )

st.divider()

button_col1, button_col2, button_col3 = st.columns(
    [3, 1, 1]
)


with button_col1:

    analyze_button = st.button(
        "🔍 Analyze Document",
        type="primary",
        use_container_width=True,
    )


with button_col2:

    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True,
    )


with button_col3:

    if "result" in st.session_state:

        download_button_placeholder = True

    else:

        download_button_placeholder = False

if clear_button:

    st.session_state.pop("result", None)

    st.rerun()

if analyze_button:

    if not text.strip():

        st.warning(
            "⚠️ Please enter some text or upload a TXT file."
        )

    else:

        try:

            with st.spinner(
                "🤖 Gemini is analyzing your document..."
            ):

                result = summarize_text(
                    text,
                    summary_type,
                )

            if isinstance(result, str):

                result = result.strip()

                # Remove accidental markdown JSON fences
                if result.startswith("```json"):

                    result = result[7:]

                elif result.startswith("```"):

                    result = result[3:]

                if result.endswith("```"):

                    result = result[:-3]

                result = result.strip()

                result = json.loads(result)

            if not isinstance(result, dict):

                raise ValueError(
                    "Gemini returned an unexpected response format."
                )

            st.session_state["result"] = result

            st.session_state["analyzed_text"] = text

            st.session_state["summary_type"] = summary_type

            st.success(
                "✅ Analysis completed successfully!"
            )

        except json.JSONDecodeError:

            st.error(
                "❌ Gemini returned invalid JSON."
            )

            st.info(
                "Please try analyzing the document again."
            )

        except Exception as e:

            st.error(
                "❌ Analysis failed."
            )

            st.info(
                "Please check your Gemini API configuration, "
                "internet connection, and API quota."
            )

            with st.expander(
                "Technical details"
            ):

                st.code(str(e))

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.header("📊 Analysis Results")

    download_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )

    st.download_button(
        label="⬇️ Download Analysis as JSON",
        data=download_json,
        file_name="ai_text_analysis.json",
        mime="application/json",
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="card-title">📝 Summary</div>',
        unsafe_allow_html=True,
    )

    summary = result.get(
        "summary",
        "No summary available.",
    )

    st.write(summary)

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="card-title">🔑 Key Points</div>',
            unsafe_allow_html=True,
        )

        key_points = result.get(
            "key_points",
            [],
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

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="card-title">😊 Sentiment</div>',
            unsafe_allow_html=True,
        )

        sentiment = str(
            result.get(
                "sentiment",
                "Unknown",
            )
        ).strip()

        sentiment_lower = sentiment.lower()


        if sentiment_lower == "positive":

            st.success(
                "😊 Positive"
            )

            st.markdown(
                '<div class="sentiment-positive">'
                "Positive Sentiment"
                "</div>",
                unsafe_allow_html=True,
            )


        elif sentiment_lower == "negative":

            st.error(
                "😞 Negative"
            )

            st.markdown(
                '<div class="sentiment-negative">'
                "Negative Sentiment"
                "</div>",
                unsafe_allow_html=True,
            )


        else:

            st.info(
                "😐 Neutral"
            )

            st.markdown(
                '<div class="sentiment-neutral">'
                "Neutral Sentiment"
                "</div>",
                unsafe_allow_html=True,
            )


        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="card-title">🏷️ Keywords</div>',
        unsafe_allow_html=True,
    )

    keywords = result.get(
        "keywords",
        [],
    )


    if keywords:

        keyword_html = (
            '<div class="keyword-container">'
        )

        for keyword in keywords:

            keyword_html += (
                '<span class="keyword-chip">'
                f"{keyword}"
                "</span>"
            )

        keyword_html += "</div>"

        st.markdown(
            keyword_html,
            unsafe_allow_html=True,
        )

    else:

        st.write(
            "No keywords found."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="card-title">🏢 Named Entities</div>',
        unsafe_allow_html=True,
    )

    entities = result.get(
        "entities",
        [],
    )


    if entities:

        entity_html = (
            '<div class="entity-container">'
        )

        for entity in entities:

            entity_html += (
                '<span class="entity-chip">'
                f"{entity}"
                "</span>"
            )

        entity_html += "</div>"

        st.markdown(
            entity_html,
            unsafe_allow_html=True,
        )

    else:

        st.write(
            "No named entities found."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="card-title">✅ Action Items</div>',
        unsafe_allow_html=True,
    )

    action_items = result.get(
        "action_items",
        [],
    )


    if action_items:

        for index, action in enumerate(
            action_items
        ):

            st.checkbox(
                action,
                key=f"action_item_{index}",
            )

    else:

        st.write(
            "No action items found."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    with st.expander(
        "🔧 View Raw JSON"
    ):

        st.json(result)

st.markdown(
    """
    <div class="footer">
        🤖 AI Text Analyzer &nbsp;•&nbsp;
        Powered by Google Gemini &nbsp;•&nbsp;
        Built with Python and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)