
from app.services.nlp_processor import (
    clean_text,
    split_into_chunks,
    extract_keywords,
)

sample_text = """
Annual leave: Employees receive 18 days of annual leave.
Sick leave: Employees receive 8 days of paid sick leave.
"""

cleaned = clean_text(sample_text)
chunks = split_into_chunks(cleaned, chunk_size=10, overlap=2)
keywords = extract_keywords(cleaned)

print("CLEANED TEXT:")
print(cleaned)

print("\nCHUNKS:")
for index, chunk in enumerate(chunks, start=1):
    print(f"{index}: {chunk}")

print("\nKEYWORDS:")
print(keywords)
