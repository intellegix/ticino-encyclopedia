# 🇨🇭 Ticinese Language Encyclopedia 🇮🇹

An interactive web-based encyclopedia for the Ticinese dialect (Western Lombard) as spoken by Swiss-Italian emigrants from Canton Ticino and Northern Lombardy during 1890-1915.

---

## 🚀 How to Use

### Quick Start

1. **Open the Encyclopedia:**
   - Double-click `index.html` to open in your web browser
   - Or right-click → "Open with" → Choose your preferred browser

2. **Navigate:**
   - Use the top navigation buttons to switch between sections
   - Click on **Vocabulary**, **Pronouns**, **Grammar Rules**, or **Sample Story**

3. **Search:**
   - Type in the search bar to find words, meanings, or grammar rules
   - Search works across all sections simultaneously

4. **Filter:**
   - Use filter buttons in Vocabulary and Pronouns sections
   - Filter by category (Family, Animals, Food, etc.) or pronoun type

---

## 📚 Features

### 🔍 Interactive Search
- **Real-time search** across all database entries
- Search by Ticinese word, English meaning, or Italian equivalent
- Filters applied instantly as you type

### 🎯 Smart Filtering
- **Vocabulary filters:** All Words, Family, Animals, Actions, Food
- **Pronoun filters:** All, Personal, Possessive, Demonstrative, Interrogative
- Click to activate, search updates automatically

### 📖 Sections

#### 1. Overview
- Introduction to Ticinese dialect
- Language classification and history
- Key linguistic features
- Research methodology

#### 2. Vocabulary (19 words)
Each entry includes:
- ✅ Ticinese spelling
- ✅ English translation
- ✅ Simple pronunciation + IPA transcription
- ✅ Part of speech and gender
- ✅ Example sentences (Ticinese + English)
- ✅ Latin etymology and development
- ✅ Regional variants
- ✅ Italian Standard equivalent

#### 3. Pronouns (28 entries)
Complete pronoun system:
- ✅ Personal pronouns (strong & weak forms)
- ✅ Direct and indirect object pronouns
- ✅ Possessive pronouns
- ✅ Demonstrative pronouns
- ✅ Interrogative pronouns
- ✅ Impersonal pronouns
- ✅ Usage rules and examples

#### 4. Grammar Rules (18 rules)
Comprehensive grammar documentation:
- ✅ Subject-verb agreement
- ✅ Four-conjugation verb system
- ✅ Article system
- ✅ Negation patterns
- ✅ Interrogative forms
- ✅ Pronominal particle ordering
- ✅ Examples in Ticinese + English
- ✅ Comparison with Standard Italian

#### 5. Sample Story
**"La Nona e l'Órca"** (The Grandmother and the Orka)
- Complete A1-level beginner story
- Line-by-line translation
- Demonstrates grammar rules in context

---

## 💾 Database Structure

```
Ticino/
├── index.html                      ← OPEN THIS FILE
├── README.md                       ← This file
├── database/
│   ├── vocabulary.json             ← 19 words
│   ├── pronouns.json               ← 28 pronouns
│   ├── grammar_rules.json          ← 18 grammar rules
│   └── SCHEMA_DESIGN.md            ← Database documentation
├── DATABASE_PROJECT_SUMMARY.md     ← Project overview
└── Ticinese Language Info.txt      ← Original story
```

---

## 🎨 Visual Design

### Color Scheme
- **Primary Green:** Swiss/Italian heritage colors
- **Accent Red:** Secondary Swiss color
- **Gold Highlights:** Important information
- **Clean Cards:** Encyclopedia-style layout

### Typography
- **Serif fonts** for classical encyclopedia feel
- **Large, readable** Ticinese words
- **Italicized** English translations
- **Monospace** for IPA transcriptions

### Responsive Design
- Works on **desktop, tablet, and mobile**
- Grid layout adapts to screen size
- Touch-friendly buttons

---

## 📊 Statistics

**Current Database Content:**
- **19 Vocabulary Words**
- **28 Pronouns**
- **18 Grammar Rules**
- **65+ Total Entries**
- **1 Complete Sample Story**

---

## 🔬 Research Method

This database was created using:
- **Multi-Agent Orchestration:** Claude Code CLI
- **Research Engine:** Perplexity Pro (6-7 parallel queries)
- **Data Gathered:** ~50,000 characters of linguistic information
- **Academic Sources:** Wikibooks, Wikipedia, Verbix, University archives
- **Time Period Focus:** 1850-1915 (emigration era)

---

## 🌍 Language Information

### Classification
**Full Taxonomy:**
Indo-European → Romance → Gallo-Italic → Lombard → Western Lombard → Alpine Lombard → Ticinese

**ISO 639-3 Code:** lmo (Lombard)

### Geographic Region
- **Primary:** Canton Ticino, Switzerland
- **Secondary:** Northern Lombardy, Italy (Varese, Lecco, Como)

### Historical Context
- **Origins:** 1200-1400 CE (stabilization of Western Lombard)
- **Target Period:** 1850-1915 (as spoken by emigrants)
- **Emigration:** 1890-1915 (peak Swiss-Italian migration to USA)

### Key Linguistic Features
✅ Four-conjugation verb system (preserved from Latin)
✅ Mandatory subject clitics for 2nd/3rd person
✅ Characteristic ö vowel (söna, nöff)
✅ Dual pronoun system (strong + weak)
✅ Regional negation particles (minga, miga)
✅ Past participle gender agreement (historical)

---

## 🔧 Technical Details

### Requirements
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **No installation needed** - runs entirely in browser
- **No internet required** - all data is local

### Browser Compatibility
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Internet Explorer NOT supported

### File Access
- Database loads JSON files via `fetch()` API
- Must be opened from a local file path
- Some browsers may require a local web server for JSON loading

**If JSON files don't load:**
1. Try a different browser (Chrome works best)
2. Or run a simple local server:
   ```bash
   # Python 3
   python -m http.server 8000
   # Then open: http://localhost:8000
   ```

---

## 📖 How to Read Entries

### Vocabulary Card Example

```
magna
eat

Pronunciation: mahn-yah
IPA: /ˈmaɲa/

Italian: mangiare
Part of Speech: verb

Example:
  La nonna la magna pan e formai
  The grandmother eats bread and cheese

Etymology: From Latin manducare → Lombard magna

Variants: magnà, magnare
```

### Pronoun Card Example

```
lù
he

IPA: /ly/

Type: personal | subject_strong | third person | singular

Usage: Strong form. MUST be accompanied by weak clitic 'el'

Examples:
  Lù el magna (He eats)
  Lù el canta (He sings)

Weak Clitic: el/l' (required)
```

---

## 🎯 Use Cases

### Family Heritage
- Understand your ancestors' dialect
- Read historical family letters
- Preserve cultural linguistic heritage

### Academic Research
- Historical linguistics study
- Romance language evolution
- Dialectology and migration patterns

### Language Learning
- Learn Ticinese from structured database
- Practice with example sentences
- Understand grammar systematically

### Cultural Preservation
- Document endangered heritage language
- Share with family members
- Educational resource for descendants

---

## 🚀 Future Expansions

The database is designed for growth:

**Planned Additions:**
- ⏳ Articles database (el, la, i, on, ona)
- ⏳ Prepositions database
- ⏳ Numbers & time expressions (1-100, days, months)
- ⏳ Phonetics/IPA system database
- ⏳ Verb conjugation tables (complete)
- ⏳ Expanded vocabulary (100+ → 500+ → 3,000+ words)
- ⏳ More sample texts
- ⏳ Audio pronunciations (future)

**Research Data Available:**
- 6 completed Perplexity Pro queries (~50K characters)
- Ready to integrate into database tables

---

## 📝 Credits

**Created:** November 4, 2025
**Version:** 1.0
**Method:** Multi-Agent Claude + Perplexity Pro Research

**Research Sources:**
- Wikibooks (Lombard language documentation)
- Wikipedia (Ticinese dialect articles)
- Verbix (verb conjugation databases)
- Alpilink (Alpine linguistic resources)
- University of Milan linguistic archives

**Original Story:** "La Nona e l'Órca" (A1 beginner text)

---

## 🤝 Sharing & Usage

### Personal Use
- ✅ Use freely for family heritage research
- ✅ Share with family members
- ✅ Print or save pages

### Educational Use
- ✅ Use for language learning
- ✅ Reference in research papers
- ✅ Teaching material (with attribution)

### Attribution
When sharing or citing:
> "Ticinese Language Encyclopedia - Western Lombard Dialect Database (1850-1915)
> Created via Multi-Agent Claude + Perplexity Pro Research, November 2025"

---

## 📞 Support

### Troubleshooting

**Problem:** JSON files won't load
**Solution:** Try Chrome browser or run a local web server

**Problem:** Search not working
**Solution:** Ensure JavaScript is enabled in browser

**Problem:** Cards not displaying
**Solution:** Check browser console for errors (F12 → Console)

### File Structure Check
Ensure these files exist:
- ✅ `index.html` (main page)
- ✅ `database/vocabulary.json`
- ✅ `database/pronouns.json`
- ✅ `database/grammar_rules.json`

---

## 🎓 Learning Path

**Recommended Order:**
1. **Overview** - Understand the language and history
2. **Sample Story** - See Ticinese in context
3. **Vocabulary** - Learn basic words from the story
4. **Grammar Rules** - Understand how the language works
5. **Pronouns** - Master the pronoun system

**Study Tips:**
- 📌 Use search to find related words
- 📌 Compare Ticinese → Italian → English
- 📌 Pay attention to pronunciation (IPA)
- 📌 Study example sentences in context
- 📌 Note regional variants and historical features

---

## 📚 Additional Resources

**In This Directory:**
- `DATABASE_PROJECT_SUMMARY.md` - Complete project documentation
- `database/SCHEMA_DESIGN.md` - Database structure details
- `Ticinese Language Info.txt` - Original story and context

**Related Topics:**
- Lombard language (ISO 639-3: lmo)
- Gallo-Italic languages
- Swiss-Italian emigration (1890-1915)
- Romance language evolution
- Historical dialectology

---

## 🌟 Highlights

### What Makes This Special

✨ **Historically Accurate** - Focuses on 1850-1915 emigration period
✨ **Academically Sourced** - Perplexity Pro research with citations
✨ **Comprehensive** - Etymology, IPA, examples, regional variants
✨ **Interactive** - Search, filter, navigate easily
✨ **Beautiful Design** - Clean encyclopedia-style interface
✨ **Family Heritage** - Preserves ancestors' actual dialect

### Database Quality

✅ **20 fields per vocabulary entry**
✅ **IPA transcriptions for all words**
✅ **Latin etymology traced**
✅ **Example sentences in context**
✅ **Regional variants documented**
✅ **Historical period dating**
✅ **Comparison with Standard Italian**

---

**Enjoy exploring your linguistic heritage!** 🇨🇭🇮🇹

---

*Last Updated: November 4, 2025*
*Database Version: 1.0*
*Created with Claude Code + Perplexity Pro*
