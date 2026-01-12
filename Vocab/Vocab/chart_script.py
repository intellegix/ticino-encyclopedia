import plotly.graph_objects as go
import pandas as pd

# Data from the provided JSON
categories = ["Actions/Verbs", "Household & Buildings", "Food & Eating", "Adjectives", "Animals", "Tools & Objects", "Clothing & Textiles", "Landscape & Geography", "Body Parts", "Plants & Flowers", "Time & Seasons", "Numbers", "Weather & Nature", "Additional Words", "Pronouns & Basic", "Demonstratives", "Question Words"]
word_counts = [150, 107, 93, 100, 66, 82, 62, 32, 54, 40, 24, 29, 13, 50, 11, 9, 5]

# Create DataFrame and sort by word count (descending)
df = pd.DataFrame({'category': categories, 'count': word_counts})
df = df.sort_values('count', ascending=False)

# Abbreviate category names to fit 15-character limit
category_abbrev = {
    'Actions/Verbs': 'Actions/Verbs',
    'Household & Buildings': 'Household/Build',
    'Food & Eating': 'Food/Eating', 
    'Adjectives': 'Adjectives',
    'Animals': 'Animals',
    'Tools & Objects': 'Tools/Objects',
    'Clothing & Textiles': 'Clothing/Text',
    'Landscape & Geography': 'Landscape/Geo',
    'Body Parts': 'Body Parts',
    'Plants & Flowers': 'Plants/Flowers',
    'Time & Seasons': 'Time/Seasons',
    'Numbers': 'Numbers',
    'Weather & Nature': 'Weather/Nature',
    'Additional Words': 'Additional',
    'Pronouns & Basic': 'Pronouns/Basic',
    'Demonstratives': 'Demonstratives',
    'Question Words': 'Question Words'
}

df['category_short'] = df['category'].map(category_abbrev)

# Create bar chart
fig = go.Figure(data=go.Bar(
    x=df['category_short'],
    y=df['count'],
    marker_color='#1FB8CD'
))

# Update layout
fig.update_layout(
    title='Ticinese Vocabulary by Category',
    xaxis_title='Category',
    yaxis_title='Word Count'
)

# Apply cliponaxis=False for bar charts as per instructions
fig.update_traces(cliponaxis=False)

# Rotate x-axis labels for better readability
fig.update_xaxes(tickangle=45)

# Save as both PNG and SVG
fig.write_image("ticinese_vocab_chart.png")
fig.write_image("ticinese_vocab_chart.svg", format="svg")

fig.show()