def build_summary_prompt(text, summary_type):
    if summary_type == 'short':
        summary_instruction = """
        create a short summary in 2-3 sentences.
        focus only on the most important information.
        """
    elif summary_type == 'medium':
        summary_instruction = """
        create a medium-length summary in one consice paragraph.
        include main ideas and important details.
        """
    elif summary_type == 'detailed':
        summary_instruction = """
        create a detailed summary.
        inlcude important ideas, facts and relevent details.
        but make the summary substantially shorter thean originally text.
        """
    else:
        raise ValueError("Invalid Summary type choose: short, medium, detailed.")
    prompt = f"""
    You are an expert document summarizer.
    summarize the following text.
    summary_type: {summary_type}

    Reequirements:
    - keep the summary factual.
    - Do not add information that is not present.
    - Focus on the most important information.
    - use only information present in the provided text.
    - do no return markdown
    - do not use a '''json code block.
    return valid json only

    The json must contain exactly these fields:
    {{
        'summary':'A summary based on requested summary type',
        'key_points': [
            "Important point 1",
            "Important point 2"
        ],
        'keywords': [
            "keyword 1",
            "keyword 2"
        ],
        'sentiment': 'Positive',
        'entities':[
            "entity 1",
            "entity 2"
        ],
        'action_items': [
            "action_item 1",
            "action_item 2"
        ]
    }}

    Rules:
    - 'summary' must be a string.
    - 'key_points' must be a JSON array of strings.
    - 'keyword' must be a JSON array of strings.
    - 'sentiment' must be exactly 'positive', 'Negative', or 'Neutral'.
    - 'entities' must be a JSON array of strings.
    - 'action_items' must be a JSON array of strings.
    - if there are no action items, return an empty array.
    - if thee is no entities, return an empty array.
    - Do not add information that is not present in text 

    {summary_instruction}
    TEXT:
    {text}
    """
    return prompt