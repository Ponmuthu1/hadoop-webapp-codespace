Text Insights Dashboard – Hadoop + Flask

Project Link: https://mysterious-spooky-tomb-jx9qxwqwqxjfpp5-5000.app.github.dev/

---

Project Overview

This project is a Text Insights Dashboard that performs word frequency analysis and other key textual insights on uploaded .txt files using Python MapReduce (MRJob) and a Flask web interface.  

The dashboard shows:  
- Total words and unique words  
- Most frequent words  
- Average word length  
- Sentence count and estimated reading time  
- Top 10 words table  

It demonstrates integration of Python, MRJob (MapReduce), Pandas, and Flask with cloud-friendly deployment using GitHub Codespaces.

---

Technologies Used

- Flask – Web framework for frontend and API handling  
- MRJob – MapReduce-style word count backend  
- Pandas – Data analysis and table generation  
- GitHub Codespaces / Azure App Service – Cloud-based hosting environment  
- Optional Hadoop – For distributed MapReduce execution  

---

Setup Instructions

1. Clone the repository  
   git clone <your-repo-url>  
   cd <repo-folder>

2. Install dependencies  
   pip install -r requirements.txt

3. Run the Flask app  
   python app.py

4. Open Codespaces port 5000  
   Go to Live Demo: https://mysterious-spooky-tomb-jx9qxwqwqxjfpp5-5000.app.github.dev/

5. Upload a .txt file to see insights.

---

Project Objective

To demonstrate how MapReduce concepts can be integrated with Python web applications to process and analyze text efficiently, with a modern web interface and optional cloud deployment.
