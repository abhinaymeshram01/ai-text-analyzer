from app.analyzer import summarize_text


with open("data/long_text.txt", "r", encoding="utf-8") as file:
    text = file.read()


print("Text length:", len(text))

result = summarize_text(
    text,
    "medium"
)

print("\n========== FINAL RESULT ==========\n")
print(result)