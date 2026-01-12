#!/usr/bin/env python3
"""
Merge original vocabulary.json (19 words) with vocabulary_expanded.json (1,269 words)
Ensure all original detailed entries are preserved
"""

import json

# Read original vocabulary with full etymological detail
with open('database/vocabulary.json', 'r', encoding='utf-8') as f:
    original = json.load(f)

# Read expanded vocabulary
with open('database/vocabulary_expanded.json', 'r', encoding='utf-8') as f:
    expanded = json.load(f)

print(f"Original vocabulary: {len(original['vocabulary'])} words")
print(f"Expanded vocabulary: {len(expanded['vocabulary'])} words")

# Create a set of Ticinese words from original for lookup
original_words = {entry['ticinese']: entry for entry in original['vocabulary']}
expanded_words_set = {entry['ticinese'] for entry in expanded['vocabulary']}

# Check which original words are missing from expanded
missing_from_expanded = set(original_words.keys()) - expanded_words_set

if missing_from_expanded:
    print(f"\n[WARNING] {len(missing_from_expanded)} original words missing from expanded:")
    for word in missing_from_expanded:
        print(f"  - {word}")

    # Add missing original words to expanded
    for word in missing_from_expanded:
        expanded['vocabulary'].append(original_words[word])

    print(f"\n[FIXED] Added {len(missing_from_expanded)} missing words to expanded vocabulary")

# Now replace basic entries in expanded with detailed original entries
print("\n[PROCESSING] Enhancing expanded entries with original detailed data...")

enhanced_count = 0
for i, entry in enumerate(expanded['vocabulary']):
    ticinese_word = entry['ticinese']

    # If this word exists in original with full detail, replace it
    if ticinese_word in original_words:
        original_entry = original_words[ticinese_word]

        # Check if original has more detail (etymology, IPA, examples)
        if original_entry.get('etymology_notes') and not entry.get('etymology_notes'):
            # Replace with original detailed entry, keeping expanded ID
            original_entry_copy = original_entry.copy()
            original_entry_copy['word_id'] = entry['word_id']  # Keep sequential ID
            expanded['vocabulary'][i] = original_entry_copy
            enhanced_count += 1

print(f"[ENHANCED] {enhanced_count} entries replaced with detailed original data")

# Update metadata
expanded['database_info']['total_entries'] = len(expanded['vocabulary'])
expanded['database_info']['notes'] = "Merged vocabulary database: 1,269 words from CSV + 19 detailed original entries. Full etymologies and IPA included where available."

# Save merged vocabulary
with open('database/vocabulary_expanded.json', 'w', encoding='utf-8') as f:
    json.dump(expanded, f, ensure_ascii=False, indent=2)

print(f"\n[SUCCESS] Merged vocabulary saved!")
print(f"Final count: {len(expanded['vocabulary'])} total words")
print(f"  - {enhanced_count} with full etymological detail from original")
print(f"  - {len(expanded['vocabulary']) - enhanced_count} with basic detail from CSV")
