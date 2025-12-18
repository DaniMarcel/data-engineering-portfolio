"""Basic NLP Text Analysis"""
import pandas as pd
from collections import Counter
import re

# Sample product descriptions
products = [
    "High quality laptop with latest processor and graphics card",
    "Ergonomic office chair with lumbar support",
    "Professional camera for photography enthusiasts",
    "Wireless headphones with noise cancellation",
    "Gaming mouse with RGB lighting and precision sensor"
]

print("📝 NLP TEXT ANALYSIS\n")

# 1. Tokenization
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

all_tokens = []
for product in products:
    tokens = tokenize(product)
    all_tokens.extend(tokens)
    print(f"Product: {product[:50]}...")
    print(f"Tokens: {tokens}\n")

# 2. Word frequency
word_freq = Counter(all_tokens)
print(f"Most common words:")
for word, count in word_freq.most_common(10):
    print(f"  {word}: {count}")

# 3. Basic statistics
print(f"\nText Statistics:")
print(f"  Total products: {len(products)}")
print(f"  Total words: {len(all_tokens)}")
print(f"  Unique words: {len(word_freq)}")
print(f"  Avg words per product: {len(all_tokens)/len(products):.1f}")

# 4. Stop words removal (simple)
stop_words = {'with', 'and', 'the', 'for', 'a'}
filtered_tokens = [w for w in all_tokens if w not in stop_words]
print(f"  Words after stop word removal: {len(filtered_tokens)}")

print("\n✅ NLP analysis completed!")
