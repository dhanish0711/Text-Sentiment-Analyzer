# 🌟 AI Text Sentiment Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![GitHub Ready](https://img.shields.io/badge/GitHub-Ready-181717?style=for-the-badge&logo=github&logoColor=white)

</div>

A modern, interactive, and visually stunning web-based dashboard application built using **Python (Flask)** on the backend and **Vanilla HTML5, CSS3, and JavaScript** on the frontend. It performs **real-time sentiment analysis** on user input and visualizes results dynamically.

---

## 📐 Architecture Diagram

Below is the flowchart representing the Flask client-server architecture:

```mermaid
flowchart TD
    A[User Keyboard Input] -->|1. Debounced JS Listener| B[POST /api/analyze]
    B -->|2. Receive Payload| C[Flask app.py Backend]
    
    subgraph Analysis Engine
        C --> D[Tokenization & Punctuation Clean]
        D --> E{Lexicon Matcher}
        F[(lexicon.json Database)] <-->|Load / Save custom words| E
        E -->|Counts matches| G[Score & Ratio Aggregations]
    end
    
    G -->|3. JSON Response| H[JavaScript app.js Client]
    
    subgraph UI Render
        H --> I[Update Dashboard Glow Theme]
        H --> J[Animate SVG Progress Gauge]
        H --> K[Render Interactive Word Pills]
        H --> L[Bounce Emoji Mood Badge]
    end
    
    style A fill:#0f172a,stroke:#334155,stroke-width:1px,color:#f8fafc
    style B fill:#0f172a,stroke:#38bdf8,stroke-width:1px,color:#f8fafc
    style C fill:#0f172a,stroke:#818cf8,stroke-width:1px,color:#f8fafc
    style D fill:#0f172a,stroke:#475569,stroke-width:1px,color:#f8fafc
    style E fill:#0f172a,stroke:#e2e8f0,stroke-width:1px,color:#f8fafc
    style F fill:#0f172a,stroke:#f59e0b,stroke-width:1px,color:#f8fafc
    style G fill:#0f172a,stroke:#ec4899,stroke-width:1px,color:#f8fafc
    style H fill:#0f172a,stroke:#10b981,stroke-width:1px,color:#f8fafc
    style I fill:#0f172a,stroke:#00F5D4,stroke-width:1px,color:#f8fafc
    style J fill:#0f172a,stroke:#FF007F,stroke-width:1px,color:#f8fafc
    style K fill:#0f172a,stroke:#64748B,stroke-width:1px,color:#f8fafc
    style L fill:#0f172a,stroke:#F8FAFC,stroke-width:1px,color:#f8fafc
```

---

## ✨ Features

- **⚡ Real-Time Web Analysis**: Keystroke binding with a 250ms debouncer. The JavaScript client continuously communicates with the Flask server API without reloading the page.
- **🎨 Premium Glassmorphic Web UI**: A dark-mode dashboard styled with dynamic neon drop-shadows and subtle glass borders that dynamically change colors (Teal for positive, Pink for negative, Slate for neutral).
- **📊 SVG Circular Gauge**: An animated SVG-drawn ring visualizing the exact balance of positive-to-negative words.
- **🎭 Dynamic Animated Mood Indicator**: High-fidelity emojis that perform scale-up/bounce animations whenever the sentiment classification shifts.
- **🎛️ Live Lexicon Manager**: Add or remove custom words directly from the browser listboxes. The additions are instantly saved to the server and written to `lexicon.json`, surviving server restarts.
- **🚀 Examples Deck**: Quick buttons to instantly load positive, negative, and mixed sentences for testing.

---

## 🛠️ How it Works

1. **Clean & Tokenize**: The Flask backend strips all punctuation, converts text to lowercase, and splits it into list tokens.
2. **Lexicon Matching**: Tokens are compared against the positive and negative lists loaded from `lexicon.json`.
3. **Scoring**:
   - If $\text{Positive} > \text{Negative} \rightarrow$ **POSITIVE** (🌟 Emoji)
   - If $\text{Negative} > \text{Positive} \rightarrow$ **NEGATIVE** (😢 Emoji)
   - If $\text{Positive} == \text{Negative} \rightarrow$ **NEUTRAL** (😐 Emoji)
4. **Data Sync**: Lexicon updates (add/remove) are written back to `lexicon.json` on the server immediately, and the client automatically triggers a re-analysis.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.x** installed.
- **Flask** framework installed.

### Setup and Running

1. Clone or download the repository:
   ```bash
   git clone https://github.com/dhanish0711/text-sentiment-analyzer.git
   cd text-sentiment-analyzer
   ```
2. Install Flask dependency:
   ```bash
   pip install Flask
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to:
   ```url
   http://127.0.0.1:5000/
   ```

---

## 📂 Project Structure

```
text-sentiment-analyzer/
├── static/
│   ├── css/
│   │   └── styles.css      # Premium dark-mode dashboard styling
│   └── js/
│       └── app.js          # Asynchronous UI controller & event binder
├── templates/
│   └── index.html          # Semantic HTML dashboard template
├── .gitignore              # Standard Python gitignore rules
├── app.py                  # Main Python/Flask backend and API server
├── lexicon.json            # Persistent JSON word bank
└── README.md               # Beautiful project documentation
```

---

<div align="center">

Made with ❤️ by [Dhanish Ladwani](https://github.com/dhanish0711/)

</div>
