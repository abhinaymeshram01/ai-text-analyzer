from app.analyzer import summarize_text


text = """
Our company will launch a new product in September.
The marketing team will prepare the campaign by August 20.
The sales team will begin customer outreach after the campaign is completed.
"""

result = summarize_text(text, "short")

print("========== RESULT ==========")
print(result)
