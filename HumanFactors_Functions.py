# visualization.py
import os
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sqlite3
import panel as pn
from io import BytesIO
import base64

# Function to create a word cloud


def generate_wordcloud():
    conn = sqlite3.connect(f'{os.getcwd()}/data/crash_data.db')
    query = """
    SELECT t1.Factor, t2.Description
    FROM ksp_factors t1
    JOIN unit_factor_code_lut t2
        ON t1.Factor = t2.Factor_Code
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    text = " ".join(df['Description'].tolist())
    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return pn.pane.Markdown(f"![wordcloud](data:image/png;base64,{image_base64})")

# Function to create a bar chart for top factors


def generate_top_factors_bar_chart():
    conn = sqlite3.connect(f'{os.getcwd()}/data/crash_data.db')
    query = """
    SELECT t1.Factor, t2.Description
    FROM ksp_factors t1
    JOIN unit_factor_code_lut t2
        ON t1.Factor = t2.Factor_Code
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    factor_counts = df['Description'].value_counts()
    top_10_factors = factor_counts.head(10)
    top_10_factors_df = pd.DataFrame({
        'Factor': top_10_factors.index,
        'Count': top_10_factors.values,
    })

    plt.figure(figsize=(9, 6))
    plt.bar(top_10_factors_df['Factor'],
            top_10_factors_df['Count'], color='skyblue')
    plt.xlabel('Human Factors')
    plt.ylabel('Count')
    plt.title('Top Human Factors')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return pn.pane.Markdown(f"![bar_chart](data:image/png;base64,{image_base64})")

# Function to create a pie chart for top factors


def generate_top_factors_pie_chart():
    conn = sqlite3.connect(f'{os.getcwd()}/data/crash_data.db')
    query = """
    SELECT t1.Factor, t2.Description
    FROM ksp_factors t1
    JOIN unit_factor_code_lut t2
        ON t1.Factor = t2.Factor_Code
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    factor_counts = df['Description'].value_counts()
    top_10_factors = factor_counts.head(10)
    top_10_factors_df = pd.DataFrame({
        'Factor': top_10_factors.index,
        'Count': top_10_factors.values,
    })

    def autopct_format(pct):
        return f'{pct:.2f}%'

    plt.figure(figsize=(9, 6))
    wedges, texts, autotexts = plt.pie(
        top_10_factors_df['Count'], labels=top_10_factors_df['Factor'], autopct=autopct_format, colors=plt.cm.Paired.colors)

    for autotext in autotexts:
        autotext.set_fontsize(8)

    plt.title('Top 10 Human Factors')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return pn.pane.Markdown(f"![pie_chart](data:image/png;base64,{image_base64})")
