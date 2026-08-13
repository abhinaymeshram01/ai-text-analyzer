import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.analyzer import summarize_text


# ==================================================
# LOAD EVALUATION DATASET
# ==================================================

with open(
    "data/evaluation_samples.json",
    "r",
    encoding="utf-8"
) as file:

    samples = json.load(file)


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def normalize_text(text):
    """Normalize text for comparison."""

    return (
        str(text)
        .strip()
        .lower()
        .replace("-", " ")
    )


def keyword_match(expected, predicted):
    """
    Calculate keyword coverage.

    A keyword is considered matched when:
    1. The complete phrase appears in a prediction, OR
    2. All words from the expected phrase are found
       across the predicted keywords.
    """

    if not expected:
        return 100.0

    expected = [
        normalize_text(item)
        for item in expected
    ]

    predicted = [
        normalize_text(item)
        for item in predicted
    ]

    matched = 0

    for keyword in expected:

        # Exact phrase match
        if any(
            keyword in prediction
            for prediction in predicted
        ):
            matched += 1
            continue

        # Word-level match
        words = keyword.split()

        found_words = set()

        for word in words:

            for prediction in predicted:

                if word in prediction:

                    found_words.add(word)

                    break

        if len(found_words) == len(words):

            matched += 1

    return (
        matched / len(expected)
    ) * 100


def entity_match(expected, predicted):
    """
    Calculate entity coverage.
    """

    if not expected:
        return 100.0

    expected = [
        normalize_text(item)
        for item in expected
    ]

    predicted = [
        normalize_text(item)
        for item in predicted
    ]

    matched = 0

    for entity in expected:

        if any(
            entity in prediction
            or prediction in entity
            for prediction in predicted
        ):

            matched += 1

    return (
        matched / len(expected)
    ) * 100


def action_item_match(expected, predicted):
    """
    Calculate action-item coverage using
    important-word overlap.
    """

    if not expected:
        return 100.0

    predicted_text = " ".join(
        normalize_text(item)
        for item in predicted
    )

    matched = 0

    stop_words = {
        "the",
        "a",
        "an",
        "to",
        "by",
        "and",
        "of",
        "is",
        "are",
        "was",
        "were",
        "be",
        "this",
        "that"
    }

    for action in expected:

        words = normalize_text(
            action
        ).split()

        important_words = [
            word
            for word in words
            if word not in stop_words
        ]

        if not important_words:
            continue

        found = sum(
            1
            for word in important_words
            if word in predicted_text
        )

        coverage = (
            found / len(important_words)
        )

        if coverage >= 0.5:

            matched += 1

    return (
        matched / len(expected)
    ) * 100


def summary_similarity(
    expected_summary,
    predicted_summary
):
    """
    Calculate TF-IDF cosine similarity
    between expected and predicted summaries.

    Returns a percentage from 0 to 100.
    """

    if not expected_summary:
        return 100.0

    if not predicted_summary:
        return 0.0

    expected_summary = normalize_text(
        expected_summary
    )

    predicted_summary = normalize_text(
        predicted_summary
    )

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [
            expected_summary,
            predicted_summary
        ]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return similarity * 100


# ==================================================
# INITIALIZE METRICS
# ==================================================

sentiment_correct = 0

keyword_scores = []

entity_scores = []

action_scores = []

summary_scores = []

total = len(samples)


# ==================================================
# START EVALUATION
# ==================================================

print("=" * 60)

print(
    "                 LLM EVALUATION"
)

print("=" * 60)


# ==================================================
# PROCESS EACH SAMPLE
# ==================================================

for sample in samples:

    sample_id = sample["id"]

    text = sample["text"]

    expected_sentiment = sample[
        "expected_sentiment"
    ]

    expected_keywords = sample.get(
        "expected_keywords",
        []
    )

    expected_entities = sample.get(
        "expected_entities",
        []
    )

    expected_actions = sample.get(
        "expected_action_items",
        []
    )

    expected_summary = sample.get(
        "expected_summary",
        ""
    )


    print("\n" + "-" * 60)

    print(
        f"Sample {sample_id}"
    )


    # ==================================================
    # CALL GEMINI
    # ==================================================

    try:

        result = summarize_text(
            text,
            "medium"
        )


        # ==================================================
        # PARSE JSON
        # ==================================================

        if isinstance(result, str):

            result = json.loads(result)


        # ==================================================
        # SUMMARY
        # ==================================================

        predicted_summary = result.get(
            "summary",
            ""
        )

        summary_score = summary_similarity(
            expected_summary,
            predicted_summary
        )

        summary_scores.append(
            summary_score
        )


        print("\nSummary")

        print(
            f"Expected : {expected_summary}"
        )

        print(
            f"Predicted: {predicted_summary}"
        )

        print(
            f"Similarity: {summary_score:.2f}%"
        )


        # ==================================================
        # SENTIMENT
        # ==================================================

        predicted_sentiment = result.get(
            "sentiment",
            "Unknown"
        )


        sentiment_match = (
            normalize_text(
                predicted_sentiment
            )
            ==
            normalize_text(
                expected_sentiment
            )
        )


        if sentiment_match:

            sentiment_correct += 1

            sentiment_result = "PASS"

        else:

            sentiment_result = "FAIL"


        print("\nSentiment")

        print(
            f"Expected : {expected_sentiment}"
        )

        print(
            f"Predicted: {predicted_sentiment}"
        )

        print(
            f"Result   : {sentiment_result}"
        )


        # ==================================================
        # KEYWORDS
        # ==================================================

        predicted_keywords = result.get(
            "keywords",
            []
        )


        keyword_score = keyword_match(
            expected_keywords,
            predicted_keywords
        )


        keyword_scores.append(
            keyword_score
        )


        print("\nKeywords")

        print(
            f"Expected : {expected_keywords}"
        )

        print(
            f"Predicted: {predicted_keywords}"
        )

        print(
            f"Match    : {keyword_score:.2f}%"
        )


        # ==================================================
        # ENTITIES
        # ==================================================

        predicted_entities = result.get(
            "entities",
            []
        )


        entity_score = entity_match(
            expected_entities,
            predicted_entities
        )


        entity_scores.append(
            entity_score
        )


        print("\nEntities")

        print(
            f"Expected : {expected_entities}"
        )

        print(
            f"Predicted: {predicted_entities}"
        )

        print(
            f"Match    : {entity_score:.2f}%"
        )


        # ==================================================
        # ACTION ITEMS
        # ==================================================

        predicted_actions = result.get(
            "action_items",
            []
        )


        action_score = action_item_match(
            expected_actions,
            predicted_actions
        )


        action_scores.append(
            action_score
        )


        print("\nAction Items")

        print(
            f"Expected : {expected_actions}"
        )

        print(
            f"Predicted: {predicted_actions}"
        )

        print(
            f"Match    : {action_score:.2f}%"
        )


    # ==================================================
    # ERROR HANDLING
    # ==================================================

    except json.JSONDecodeError:

        print(
            "\n❌ Invalid JSON returned by Gemini."
        )


    except Exception as e:

        print(
            "\n❌ Analysis failed:"
        )

        print(
            f"Error: {e}"
        )


# ==================================================
# FINAL METRICS
# ==================================================

sentiment_accuracy = (
    sentiment_correct / total * 100
    if total > 0
    else 0
)


average_keyword_score = (
    sum(keyword_scores)
    / len(keyword_scores)
    if keyword_scores
    else 0
)


average_entity_score = (
    sum(entity_scores)
    / len(entity_scores)
    if entity_scores
    else 0
)


average_action_score = (
    sum(action_scores)
    / len(action_scores)
    if action_scores
    else 0
)


average_summary_score = (
    sum(summary_scores)
    / len(summary_scores)
    if summary_scores
    else 0
)


# ==================================================
# FINAL REPORT
# ==================================================

print("\n")

print("=" * 60)

print(
    "                 FINAL REPORT"
)

print("=" * 60)

print(
    f"Sentiment Accuracy : "
    f"{sentiment_accuracy:.2f}%"
)

print(
    f"Keyword Match      : "
    f"{average_keyword_score:.2f}%"
)

print(
    f"Entity Match       : "
    f"{average_entity_score:.2f}%"
)

print(
    f"Action Item Match  : "
    f"{average_action_score:.2f}%"
)

print(
    f"Summary Similarity : "
    f"{average_summary_score:.2f}%"
)

print("=" * 60)