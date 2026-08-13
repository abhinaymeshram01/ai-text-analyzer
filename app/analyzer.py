from app.gemini_api import generate_response
from app.prompts import build_summary_prompt


MAX_TEXT_LENGTH = 12000
CHUNK_SIZE = 8000


def split_text(text, chunk_size=CHUNK_SIZE):
    """Split text while trying to preserve paragraph boundaries."""

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # If adding this paragraph stays within the limit
        if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:
            # Save the current chunk
            if current_chunk:
                chunks.append(current_chunk)

            # If one paragraph itself is too large,
            # split it into smaller pieces
            if len(paragraph) > chunk_size:
                for i in range(0, len(paragraph), chunk_size):
                    chunks.append(
                        paragraph[i:i + chunk_size]
                    )

                current_chunk = ""

            else:
                current_chunk = paragraph

    # Add remaining text
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def analyze_chunk(text, summary_type):
    """Analyze a single text chunk."""

    prompt = build_summary_prompt(
        text,
        summary_type
    )

    response = generate_response(prompt)

    return response


def summarize_text(text, summary_type):
    """Analyze short or long text."""

    # Remove unnecessary whitespace
    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    # -------------------------------------------------
    # SHORT TEXT
    # -------------------------------------------------

    if len(text) <= MAX_TEXT_LENGTH:

        return analyze_chunk(
            text,
            summary_type
        )

    # -------------------------------------------------
    # LONG TEXT
    # -------------------------------------------------

    chunks = split_text(text)

    chunk_results = []

    for i, chunk in enumerate(chunks, start=1):

        print(f"Analyzing chunk {i}/{len(chunks)}...")

        result = analyze_chunk(
            chunk,
            summary_type
        )

        chunk_results.append(result)

    # -------------------------------------------------
    # COMBINE CHUNK RESULTS
    # -------------------------------------------------

    combined_results = "\n\n".join(
        chunk_results
    )

    final_prompt = f"""
    You are an expert document analyzer.

    The following are analysis results generated from
    different sections of the same document.

    Combine them into ONE final analysis.

    Return:

    SUMMARY
    KEY POINTS
    KEYWORDS
    SENTIMENT
    ENTITIES
    ACTION ITEMS

    Requirements:

    - Keep the information factual.
    - Do not invent information.
    - Remove duplicate information.
    - Combine related key points.
    - Keep the final summary substantially shorter
    than the original document.
    - Preserve important dates, names, organizations,
    locations and action items.

    DOCUMENT ANALYSIS RESULTS:

    {combined_results}
    """

    final_response = generate_response(
        final_prompt
    )

    return final_response