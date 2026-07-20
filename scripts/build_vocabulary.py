import json
import os
import re
import random

# Set random seed for reproducible sampling of specific instructions
random.seed(42)

def normalize(text):
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.rstrip('.').strip()
    return text

input_file = "data/processed/json/gold_examples.jsonl"
vocab_file = "docs/vocabulary.json"
sample_file = "docs/specific_instructions_sample.json"

beats = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line_str = line.strip()
        if line_str:
            data = json.loads(line_str)
            beats.append({
                "beat_id": data.get("beat_id"),
                "visual": data.get("visual", "")
            })

total_beats_processed = len(beats)

# Group beats by normalized visual phrase (filtering out empty visuals)
norm_groups = {}
for b in beats:
    orig = b["visual"]
    if not orig or not orig.strip():
        continue
    norm = normalize(orig)
    if norm not in norm_groups:
        norm_groups[norm] = {
            "norm": norm,
            "orig_counts": {},
            "count": 0,
            "beats": [],
            "first_orig": orig
        }
    norm_groups[norm]["count"] += 1
    norm_groups[norm]["orig_counts"][orig] = norm_groups[norm]["orig_counts"].get(orig, 0) + 1
    norm_groups[norm]["beats"].append(b)

# Select the original phrase for each group (most frequent original phrase, breaking ties with first seen)
for norm, grp in norm_groups.items():
    sorted_origs = sorted(grp["orig_counts"].items(), key=lambda x: x[1], reverse=True)
    grp["selected_phrase"] = sorted_origs[0][0]

reusable_groups = [g for g in norm_groups.values() if g["count"] >= 2]
specific_groups = [g for g in norm_groups.values() if g["count"] == 1]

# Sort reusable groups by count descending
reusable_groups.sort(key=lambda x: x["count"], reverse=True)

# Build vocabulary list
vocabulary = []
for idx, grp in enumerate(reusable_groups, start=1):
    vocabulary.append({
        "id": f"VIS{idx:03d}",
        "phrase": grp["selected_phrase"],
        "count": grp["count"]
    })

# Build specific instructions sample (20 items from specific_groups)
sampled_specific = random.sample(specific_groups, 20) if len(specific_groups) >= 20 else specific_groups
specific_sample = []
for grp in sampled_specific:
    b = grp["beats"][0]
    specific_sample.append({
        "beat_id": b["beat_id"],
        "phrase": b["visual"]
    })

os.makedirs("docs", exist_ok=True)

with open(vocab_file, "w", encoding="utf-8") as f:
    json.dump(vocabulary, f, indent=2, ensure_ascii=False)
    f.write("\n")

with open(sample_file, "w", encoding="utf-8") as f:
    json.dump(specific_sample, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("================== STATISTICS ==================")
print(f"Total beats processed: {total_beats_processed}")
print(f"Unique visual phrases: {len(norm_groups)}")
print(f"Recurring vocabulary entries: {len(vocabulary)}")
print(f"Specific instructions: {len(specific_groups)}")
print("\nTop 20 most common phrases:")
for v in vocabulary[:20]:
    print(f"  {v['id']}: Count {v['count']:3d} | Phrase: {repr(v['phrase'])}")
