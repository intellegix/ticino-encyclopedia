# Ticinese Language Database Schema Design

## Overview
Comprehensive database structure for Ticinese (Western Lombard) dialect spoken 1850-1915 in Ticino canton and northern Lombardy.

**Language Classification:**
- Family: Indo-European → Romance → Gallo-Italic → Lombard → Western Lombard → Alpine Lombard → Ticinese
- ISO Code: lmo (Lombard)
- Period: Mid-1800s to early 1900s
- Region: Swiss Canton Ticino, Northern Lombardy (Varese, Lecco, Como)

---

## Database Tables Structure

### 1. VOCABULARY (`vocabulary.json`)
Main lexicon with all Ticinese words

**Fields:**
- `word_id` (string): Unique identifier (e.g., "TICIN_0001")
- `ticinese` (string): Word in Ticinese spelling
- `english` (string): English translation
- `italian_standard` (string): Standard Italian equivalent
- `part_of_speech` (string): noun, verb, adjective, adverb, pronoun, article, preposition, conjunction, interjection
- `gender` (string): masculine, feminine, neuter, n/a
- `number` (string): singular, plural, invariable, n/a
- `pronunciation_simple` (string): Simple phonetic (e.g., "mahn-yah")
- `pronunciation_ipa` (string): IPA transcription
- `category` (string): family, body, animals, food, nature, actions, descriptions, time, numbers, function_words
- `subcategory` (string): More specific grouping
- `usage_notes` (string): Context and usage information
- `example_sentence` (string): Example in Ticinese
- `example_translation` (string): Example in English
- `etymology_latin` (string): Latin root if applicable
- `etymology_notes` (string): Historical development notes
- `regional_variants` (array): Alternative forms in different valleys
- `frequency` (string): common, uncommon, rare, archaic
- `time_period` (string): Dating of usage (e.g., "1850-1915")
- `source` (string): Attestation source

**Example Entry:**
```json
{
  "word_id": "TICIN_0001",
  "ticinese": "magna",
  "english": "eat",
  "italian_standard": "mangiare",
  "part_of_speech": "verb",
  "gender": "n/a",
  "number": "n/a",
  "pronunciation_simple": "mahn-yah",
  "pronunciation_ipa": "ˈmaɲa",
  "category": "actions",
  "subcategory": "eating_drinking",
  "usage_notes": "Common verb for eating, used in all contexts",
  "example_sentence": "La nonna la magna pan e formai",
  "example_translation": "The grandmother eats bread and cheese",
  "etymology_latin": "manducare",
  "etymology_notes": "From Latin manducare → Lombard magna, lost -ducare ending",
  "regional_variants": ["magnà", "magnare"],
  "frequency": "common",
  "time_period": "1200-present",
  "source": "Oral tradition, rural Ticino valleys 1850-1910"
}
```

---

### 2. VERB_CONJUGATIONS (`verb_conjugations.json`)
Complete conjugation tables for all verbs

**Fields:**
- `verb_id` (string): References vocabulary word_id
- `infinitive` (string): Base form
- `verb_type` (string): regular, irregular, auxiliary
- `conjugation_class` (string): -à, -i, -e classes
- `present_tense` (object):
  - `first_singular` (string): mi magni
  - `second_singular` (string): ti magni
  - `third_singular` (string): el/la magna
  - `first_plural` (string): nun magnòm
  - `second_plural` (string): vun magnè
  - `third_plural` (string): lor magnen
- `past_tense` (object): Same structure
- `future_tense` (object): Same structure
- `imperative` (object): Command forms
- `participle_past` (string): Past participle
- `participle_present` (string): Present participle
- `gerund` (string): Gerund form
- `subject_pronoun_required` (boolean): true/false
- `auxiliary_verb` (string): avé or éss
- `notes` (string): Irregularities and usage notes

---

### 3. GRAMMAR_RULES (`grammar_rules.json`)
Linguistic rules and patterns

**Fields:**
- `rule_id` (string): Unique identifier (e.g., "GRAM_001")
- `category` (string): phonology, morphology, syntax, orthography
- `subcategory` (string): More specific (e.g., articles, word_order, negation)
- `rule_name` (string): Short descriptive name
- `description` (string): Full explanation
- `examples_ticinese` (array): Example sentences in Ticinese
- `examples_english` (array): Corresponding English translations
- `exceptions` (string): When rule doesn't apply
- `comparison_italian` (string): How it differs from Standard Italian
- `time_period` (string): When this rule was active
- `source` (string): Linguistic attestation

**Example Entry:**
```json
{
  "rule_id": "GRAM_001",
  "category": "syntax",
  "subcategory": "articles",
  "rule_name": "Subject pronoun + definite article before verb",
  "description": "Ticinese uses doubled subject marking: subject pronoun + matching article + verb. Pattern: [SUBJECT] + [la/el/i] + [VERB]",
  "examples_ticinese": [
    "La nonna la magna",
    "El can el baila",
    "I gat i dormen"
  ],
  "examples_english": [
    "The grandmother eats",
    "The dog dances",
    "The cats sleep"
  ],
  "exceptions": "First and second person pronouns don't take article: 'Mi magni' not *'Mi el magni'",
  "comparison_italian": "Standard Italian omits the article: 'La nonna mangia' not *'La nonna la mangia'",
  "time_period": "1200-present",
  "source": "Core feature of Western Lombard, attested in all periods"
}
```

---

### 4. PHONETICS (`phonetics.json`)
Sound system and pronunciation rules

**Fields:**
- `sound_id` (string): Unique identifier
- `category` (string): vowel, consonant, diphthong, cluster
- `grapheme` (string): Written form (e.g., "ö")
- `ipa` (string): IPA symbol
- `description` (string): How to produce the sound
- `simple_pronunciation` (string): English approximation
- `position_rules` (string): Where this sound appears
- `examples_words` (array): Words containing this sound
- `examples_ipa` (array): IPA transcriptions of examples
- `comparison_italian` (string): How it differs from Italian
- `regional_variation` (string): Differences between valleys
- `frequency` (string): common, uncommon, rare

**Example Entry:**
```json
{
  "sound_id": "PHON_V_001",
  "category": "vowel",
  "grapheme": "ö",
  "ipa": "ø",
  "description": "Close-mid front rounded vowel, like German 'ö' or French 'eu'",
  "simple_pronunciation": "like 'uh' with rounded lips",
  "position_rules": "Can appear in any syllable position; often from Latin ō or ŏ before nasals",
  "examples_words": ["söna", "böc", "föra"],
  "examples_ipa": ["ˈsøna", "bøk", "ˈføra"],
  "comparison_italian": "Italian doesn't have this sound; closest is 'o'",
  "regional_variation": "More common in Locarno and Varese areas, less in southern valleys",
  "frequency": "common"
}
```

---

### 5. PRONOUNS (`pronouns.json`)
Complete pronoun system

**Fields:**
- `pronoun_id` (string): Unique identifier
- `type` (string): personal, possessive, demonstrative, relative, interrogative, indefinite
- `form` (string): The pronoun itself
- `person` (string): first, second, third, n/a
- `number` (string): singular, plural, n/a
- `gender` (string): masculine, feminine, neuter, n/a
- `case` (string): subject, object, indirect, n/a
- `english_equivalent` (string): English translation
- `usage_notes` (string): When and how to use
- `examples` (array): Example sentences
- `pronunciation_ipa` (string): IPA transcription

---

### 6. ARTICLES (`articles.json`)
Definite and indefinite articles

**Fields:**
- `article_id` (string): Unique identifier
- `type` (string): definite, indefinite
- `form` (string): The article
- `gender` (string): masculine, feminine
- `number` (string): singular, plural
- `usage_context` (string): before_consonant, before_vowel, general
- `english_equivalent` (string): the, a, an, etc.
- `examples` (array): Example phrases
- `pronunciation_ipa` (string): IPA transcription

---

### 7. PREPOSITIONS (`prepositions.json`)
All prepositions and their usage

**Fields:**
- `preposition_id` (string): Unique identifier
- `form` (string): The preposition
- `english_equivalent` (string): English meaning
- `usage_type` (string): location, time, manner, possession, etc.
- `examples_ticinese` (array): Example phrases
- `examples_english` (array): English translations
- `contracts_with_articles` (boolean): Does it combine with articles?
- `contracted_forms` (array): Combined forms (e.g., "a + el = al")
- `pronunciation_ipa` (string): IPA transcription

---

### 8. NUMBERS (`numbers.json`)
Counting system

**Fields:**
- `number_id` (string): Unique identifier
- `numeric_value` (integer): The number (1, 2, 3, etc.)
- `ticinese_form` (string): Ticinese word
- `type` (string): cardinal, ordinal
- `gender_forms` (object): masculine/feminine variants if applicable
- `english` (string): English translation
- `pronunciation_simple` (string): Simple pronunciation
- `pronunciation_ipa` (string): IPA transcription
- `usage_notes` (string): Special rules
- `etymology` (string): Latin origin

---

### 9. TIME_EXPRESSIONS (`time_expressions.json`)
Days, months, seasons, time words

**Fields:**
- `expression_id` (string): Unique identifier
- `category` (string): day, month, season, time_of_day, temporal_adverb
- `ticinese` (string): Ticinese form
- `english` (string): English translation
- `italian_standard` (string): Standard Italian
- `pronunciation_simple` (string): Simple pronunciation
- `pronunciation_ipa` (string): IPA transcription
- `order_number` (integer): Position in sequence (1st day, 2nd month, etc.)
- `usage_examples` (array): Example sentences

---

### 10. ETYMOLOGY (`etymology.json`)
Historical development of words

**Fields:**
- `etymology_id` (string): Unique identifier
- `word_id` (string): References vocabulary word_id
- `latin_root` (string): Classical Latin form
- `vulgar_latin` (string): Late Latin/Proto-Romance form
- `proto_lombard` (string): Early Medieval Lombard form (1000-1200 CE)
- `old_ticinese` (string): Medieval form (1200-1400 CE)
- `early_modern` (string): 1400-1800 CE form
- `modern_ticinese` (string): 1850-1915 form (our focus period)
- `sound_changes` (array): Phonological evolution steps
- `semantic_changes` (string): Meaning shifts over time
- `cognates` (object): Related words in other Romance languages
  - `italian` (string)
  - `french` (string)
  - `spanish` (string)
  - `romanian` (string)
- `loanwords_from` (string): If borrowed from German, Celtic, etc.
- `scholarly_sources` (array): Academic references

---

### 11. PHRASES (`phrases.json`)
Common expressions and idioms

**Fields:**
- `phrase_id` (string): Unique identifier
- `ticinese_phrase` (string): The complete phrase
- `literal_translation` (string): Word-for-word English
- `meaning` (string): Actual meaning/usage
- `category` (string): greeting, farewell, courtesy, idiom, proverb, exclamation
- `context` (string): When to use this phrase
- `pronunciation_simple` (string): Simple pronunciation
- `examples_in_context` (array): Example dialogues
- `cultural_notes` (string): Background information
- `equivalent_italian` (string): Standard Italian equivalent
- `time_period` (string): When this phrase was common

---

### 12. HISTORICAL_CONTEXT (`historical_context.json`)
Background information about language and culture

**Fields:**
- `context_id` (string): Unique identifier
- `category` (string): migration, geography, culture, language_contact, social_history
- `title` (string): Short descriptive title
- `time_period` (string): Date range
- `description` (string): Full explanation
- `linguistic_impact` (string): How this affected the language
- `relevant_words` (array): Word IDs affected by this context
- `sources` (array): Historical references

---

### 13. SAMPLE_TEXTS (`sample_texts.json`)
Complete stories and texts in Ticinese

**Fields:**
- `text_id` (string): Unique identifier
- `title` (string): Story title
- `level` (string): A1, A2, B1, B2, C1, C2 (CEFR)
- `full_text_ticinese` (string): Complete text
- `full_text_english` (string): Complete translation
- `line_by_line` (array): Each sentence separately
  - `line_number` (integer)
  - `ticinese` (string)
  - `english` (string)
  - `pronunciation` (string)
  - `word_ids` (array): References to vocabulary
- `vocabulary_used` (array): All word_ids in the text
- `grammar_features` (array): Grammar rule_ids demonstrated
- `cultural_notes` (string): Background information
- `source` (string): Origin of the text
- `time_period` (string): When it was written/spoken

---

## Data Format Standards

### File Formats
- **JSON**: Primary format for structured data
- **CSV**: Alternative for simple tables
- **Markdown**: Documentation and explanatory text

### Encoding
- UTF-8 throughout
- Preserve all diacritical marks (à, è, ì, ò, ù, ö, ü, ä, ñ)

### Naming Conventions
- Files: lowercase_with_underscores.json
- IDs: UPPERCASE_PREFIX_#### (e.g., TICIN_0001)
- Fields: lowercase_with_underscores

### ID Prefixes
- TICIN_ : Vocabulary entries
- VERB_ : Verb conjugations
- GRAM_ : Grammar rules
- PHON_ : Phonetic entries
- PRON_ : Pronouns
- ART_ : Articles
- PREP_ : Prepositions
- NUM_ : Numbers
- TIME_ : Time expressions
- ETYM_ : Etymology entries
- PHRA_ : Phrases
- HIST_ : Historical context entries
- TEXT_ : Sample texts

---

## Data Collection Sources

All data being gathered via Perplexity Pro Research from:
1. **Linguistic databases**: Academic sources on Lombard dialects
2. **Historical texts**: 1850-1915 attestations
3. **Oral tradition**: Recorded from emigrant communities
4. **Comparative Romance**: Etymology from Latin and cognates
5. **Regional variations**: Ticino, Varese, Lecco, Como valley forms

---

## Implementation Phases

### Phase 1: Core Vocabulary (In Progress)
- Extract from provided story
- Perplexity research for semantic categories
- 500-1000 most common words

### Phase 2: Grammar System
- Complete verb conjugations
- Pronoun and article systems
- Sentence structure rules

### Phase 3: Phonetics
- Complete sound inventory
- Pronunciation rules
- IPA transcription system

### Phase 4: Extended Vocabulary
- Expand to 2000-3000 words
- Specialized domains
- Regional variants

### Phase 5: Cultural Context
- Historical development
- Etymology and language evolution
- Sample texts and phrases

---

**Schema Version:** 1.0
**Last Updated:** 2025-11-04
**Research Method:** Multi-agent Perplexity + Claude collaboration
**Target Completion:** Complete database for 1850-1915 Ticinese dialect
