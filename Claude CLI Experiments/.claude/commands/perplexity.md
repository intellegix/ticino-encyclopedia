# Perplexity Research Command

Run a deep research query using Perplexity Pro with Research mode.

## Usage
```
/perplexity [your research question]
```

## What This Does
1. Authenticates with Perplexity using saved cookies
2. Activates Pro Research mode for comprehensive results
3. Waits for deep research generation (2-3 minutes)
4. Extracts and presents:
   - Comprehensive answer
   - Source citations
   - Related follow-up questions
5. Saves results to `.claude/sessions/screenshots/research_result.txt`

## Instructions for Claude

When the user runs `/perplexity [question]`:

1. Extract the research question from the command arguments
2. Run the research script:
   ```bash
   .venv/Scripts/python.exe .claude/simple_research.py "[question]" 150
   ```
3. Wait for completion (approximately 2.5 minutes)
4. Read the results from `.claude/sessions/screenshots/research_result.txt`
5. Present a well-formatted summary to the user including:
   - Main findings
   - Key sources (with citations)
   - Related questions for follow-up
6. Ask if the user wants to explore any related questions or topics

## Example

User: `/perplexity What are the best practices for implementing microservices architecture in 2024?`

Claude should:
- Run: `.venv/Scripts/python.exe .claude/simple_research.py "What are the best practices for implementing microservices architecture in 2024?" 150`
- Wait for completion
- Read and summarize the research results
- Present findings with sources
- Offer to explore related topics

## Notes
- Research mode provides more comprehensive results with sources
- Typical wait time: 2-3 minutes for quality research
- Results are cached in session files
- Screenshots are saved for visual reference
