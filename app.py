from flask import Flask, request
import subprocess
import os
import re
import pandas as pd
from collections import Counter

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Text Insights Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #232526, #414345);
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 40px;
        }
        h1 { font-size: 2.2rem; margin-bottom: 10px; }
        p { opacity: 0.9; margin-bottom: 30px; }
        .upload-box {
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 30px;
            width: 420px;
            text-align: center;
            box-shadow: 0 4px 25px rgba(0,0,0,0.3);
        }
        input[type="file"] {
            display: block;
            margin: 20px auto;
            color: #fff;
        }
        button {
            background-color: #06b6d4;
            border: none;
            border-radius: 6px;
            color: white;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover { background-color: #0891b2; }
        #result {
            margin-top: 40px;
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 10px;
            width: 600px;
            max-width: 95%;
            color: #fff;
            font-family: 'Segoe UI', sans-serif;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 15px;
        }
        th, td {
            border-bottom: 1px solid rgba(255,255,255,0.2);
            padding: 8px;
            text-align: left;
        }
        th { background: rgba(255,255,255,0.1); }
        .loader {
            display: none;
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid #fff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            margin: 20px auto;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% {transform: rotate(0deg);} 100% {transform: rotate(360deg);} }
    </style>
</head>
<body>
    <h1>Text Insights Dashboard</h1>
    <p>Upload a text file to get word frequency and key insights</p>
    <div class="upload-box">
        <input type="file" id="fileInput" accept=".txt">
        <button onclick="uploadFile()">Analyze</button>
        <div class="loader" id="loader"></div>
    </div>
    <div id="result"></div>

    <script>
        async function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const loader = document.getElementById('loader');
            const result = document.getElementById('result');
            result.textContent = '';
            if (!fileInput.files.length) {
                alert('Please select a text file!');
                return;
            }
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('file', file);
            loader.style.display = 'block';
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const html = await res.text();
            loader.style.display = 'none';
            result.innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = 'uploaded.txt'
    file.save(filename)

    # Run MRJob to get word counts
    output = subprocess.getoutput(f'python wordcount.py {filename}')

    # Parse the MRJob output into a dictionary
    counts = {}
    for line in output.strip().splitlines():
        parts = re.findall(r'"(.*?)"|(\S+)', line)
        if not parts:
            continue
        word = parts[0][0] or parts[0][1]
        num = int(re.findall(r'\d+', line)[-1]) if re.findall(r'\d+', line) else 0
        counts[word] = num

    if not counts:
        return "<p>No valid words found in file.</p>"

    # Calculate additional insights
    total_words = sum(counts.values())
    unique_words = len(counts)
    most_common_word, max_count = max(counts.items(), key=lambda x: x[1])
    avg_word_length = sum(len(w) * c for w, c in counts.items()) / total_words

    # Re-read the file to analyze text structure
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    sentence_count = len(re.findall(r'[.!?]', text))
    reading_time = round(total_words / 200, 2)  # ~200 words/minute

    # Top 10 words table
    df = pd.DataFrame(list(counts.items()), columns=["Word", "Count"]).sort_values("Count", ascending=False).head(10)
    table_html = df.to_html(index=False, border=0, classes="word-table")

    # Build result HTML
    insights_html = f"""
    <h2>📊 Insights</h2>
    <ul>
        <li><b>Total Words:</b> {total_words}</li>
        <li><b>Unique Words:</b> {unique_words}</li>
        <li><b>Most Frequent Word:</b> '{most_common_word}' ({max_count} times)</li>
        <li><b>Average Word Length:</b> {avg_word_length:.2f} letters</li>
        <li><b>Sentence Count:</b> {sentence_count}</li>
        <li><b>Estimated Reading Time:</b> {reading_time} minute(s)</li>
    </ul>
    <h3>🔠 Top 10 Words</h3>
    {table_html}
    """

    return insights_html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
