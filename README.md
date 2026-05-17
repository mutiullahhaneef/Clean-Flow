<div align="center">

<!-- BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00dc99,50:0066ff,100:03050f&height=200&section=header&text=CleanFlow%20AI&fontSize=72&fontColor=ffffff&fontAlignY=38&desc=Raw%20CSV%20→%20Production-Ready%20Data%20·%20Powered%20by%20Google%20Gemini%20Pro&descAlignY=60&descColor=aaaaaa&animation=fadeIn" width="100%"/>

<!-- BADGES -->
<p>
  <img src="https://img.shields.io/badge/Python-3.9+-00dc99?style=for-the-badge&logo=python&logoColor=white&labelColor=03050f"/>
  <img src="https://img.shields.io/badge/Streamlit-1.x-0066ff?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=03050f"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-Pro-aa44ff?style=for-the-badge&logo=google&logoColor=white&labelColor=03050f"/>
  <img src="https://img.shields.io/badge/License-MIT-ffaa33?style=for-the-badge&labelColor=03050f"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Pandas-✓-00dc99?style=flat-square&labelColor=1a1a2e"/>
  <img src="https://img.shields.io/badge/NumPy-✓-0066ff?style=flat-square&labelColor=1a1a2e"/>
  <img src="https://img.shields.io/badge/Plotly-✓-aa44ff?style=flat-square&labelColor=1a1a2e"/>
  <img src="https://img.shields.io/badge/PyArrow-✓-ffaa33?style=flat-square&labelColor=1a1a2e"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-00dc99?style=flat-square&labelColor=1a1a2e"/>
</p>

<br/>

> **CleanFlow AI** is a SaaS-ready data preparation platform that fuses heuristic cleaning algorithms  
> with **Google Gemini Pro** to transform raw, broken datasets into production-ready data —  
> fully explainable, inside one unified dark-first workspace.



</div>

## ⚡ What It Does

<div align="center">

| Problem | CleanFlow AI Solution |
|---|---|
| 🕰️ Manual null-hunting across 50 columns | **5-dimension Health Score** flags everything instantly |
| 🤷 "Why is this column broken?" | **Gemini Pro explains** in plain English |
| 😰 Irreversible cleaning mistakes | **Full Undo/Redo pipeline** — experiment safely |
| 📋 No record of what changed | **Audit Log** — every transformation logged |
| 🔄 Cleaning the same issues repeatedly | **AI suggestions** — fixes applied in one click |
| 📦 "They need it in Excel, not CSV" | **4 export formats** — CSV, Excel, JSON, Parquet |

</div>

---

## ✨ Features

### 🧠 Gemini-Powered AI Engine
- **Conversational Analysis** — ask *"Why are there so many nulls in zip_code?"* and get real, context-aware answers
- **Semantic Type Inference** — goes beyond `dtypes` to detect Category, DateTime, Numeric intent
- **Intelligent Suggestions** — AI recommends the right cleaning strategy per column, not just flags the problem
- **Heuristic Fallback** — works even when your API quota is exhausted

### 📊 Deep Data Profiling
- **Composite Health Score** — a 0–100 score across 5 dimensions: Completeness, Consistency, Uniqueness, Validity, Shape
- **Radar Health Maps** — visualize all 5 dimensions at once with interactive Plotly radar charts
- **Correlation Heatmaps** — instantly spot relationships between numeric features
- **Distribution Plots** — before/after overlays to quantify noise removed

### 🔧 Professional Cleaning Studio
- **Granular Column Controls** — IQR Capping, Mode Filling, Mean/Median imputation, title-case standardization
- **Duplicate Detection** — row-level and semantic deduplication
- **Outlier Management** — Z-score and IQR-based capping with visual confirmation
- **Undo / Redo System** — full state-management pipeline for safe experimentation
- **Audit Logging** — timestamped record of every transformation for full reproducibility

### 📦 Enterprise Export
- **4 Formats** — CSV, Excel (`.xlsx`), JSON, Parquet
- **Before vs. After Charts** — prove exactly how much quality improved
- **Export-Ready Metadata** — schema and type information bundled with output

### 🎨 Premium UI/UX
- **Dark-First Glassmorphism** — sleek aesthetic with vibrant gradients and micro-animations
- **Distraction-Free Layout** — optimized Streamlit configuration for a true app-like experience
- **Responsive Design** — adapts cleanly across screen sizes

---

## 🏗️ Architecture

```
cleanflow-ai/
│
├── app.py                    # Thin entry point & orchestration layer
│
├── config/
│   ├── settings.py           # Constants, palettes, dataset definitions
│   └── themes.py             # Premium CSS templates & glassmorphism rules
│
├── core/
│   ├── ai_engine.py          # Google GenAI SDK integration (Gemini Pro)
│   ├── cleaner.py            # Transformation logic & audit pipeline
│   └── profiler.py           # Health scoring & profiling algorithms
│
├── ui/
│   ├── charts.py             # Plotly visualization library (Radar, Heatmap, Dist)
│   ├── components.py         # Reusable UI fragments (cards, badges, metrics)
│   └── pages.py              # Tab rendering & UI state management
│
├── docs/
│   └── screenshots/          # UI previews for README
│
├── .env.example              # API key template
├── requirements.txt
└── README.md
```

**Design principle:** Fully decoupled — each layer is independently replaceable. The `core/` layer has zero Streamlit dependencies, making migration to FastAPI or Django a drop-in operation.

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- A [Google AI Studio](https://aistudio.google.com/) API key (free tier works)

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/cleanflow-ai.git
cd cleanflow-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

```bash
cp .env.example .env
```

Open `.env` and add your key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Launch

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🎮 Quick Start

```python
# You can also use the core engine programmatically
from core.profiler import DataProfiler
from core.cleaner import DataCleaner
import pandas as pd

df = pd.read_csv("your_data.csv")

# Profile your dataset
profiler = DataProfiler(df)
health = profiler.compute_health_score()
print(f"Health Score: {health['overall']}/100")

# Clean it
cleaner = DataCleaner(df)
cleaner.fill_missing(strategy="mode", columns=["zip_code", "city"])
cleaner.remove_duplicates()
cleaned_df = cleaner.get_result()
```

---

## 📊 Health Score Breakdown

| Dimension | What It Measures | Weight |
|---|---|---|
| **Completeness** | % of non-null values across all columns | 25% |
| **Consistency** | Uniformity of formats, types, and ranges | 25% |
| **Uniqueness** | Absence of duplicate rows and values | 20% |
| **Validity** | Values conforming to expected domain rules | 20% |
| **Shape** | Structural integrity (columns, schema) | 10% |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|---|---|---|
| Frontend / Orchestration | `Streamlit` | App UI, session state, routing |
| Artificial Intelligence | `Google Gemini Pro` | LLM reasoning, suggestions, Q&A |
| Data Engineering | `Pandas` + `NumPy` | Transformations, profiling |
| Serialization | `PyArrow` | Parquet export, type-safe I/O |
| Visualizations | `Plotly` | Radar, Heatmap, Distribution charts |
| Styling | Vanilla CSS (Glassmorphism) | Dark-first UI, micro-animations |
| Config | `python-dotenv` | API key management |

</div>

---

## 🗺️ Roadmap

- [x] Core 5-dimension health scoring
- [x] Gemini Pro AI integration
- [x] Conversational data Q&A
- [x] Full Undo/Redo + Audit Log
- [x] 4-format export pipeline
- [ ] 🔄 FastAPI migration (REST API layer)
- [ ] 🔗 SQL query interface (natural language → SQL)
- [ ] 🤝 Real-time collaboration mode
- [ ] ☁️ Cloud storage integration (GCS / S3)
- [ ] 📋 Auto schema detection & enforcement
- [ ] 🐳 Docker containerization

---

## 🤝 Contributing

Contributions are what make the open-source community extraordinary. Any contribution you make is **greatly appreciated**.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our code of conduct and pull request process.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## 👤 Author

**Your Name**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0066ff?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=03050f)](https://www.linkedin.com/in/mutiullahhaneef/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-00dc99?style=for-the-badge&logo=github&logoColor=white&labelColor=03050f)](https://github.com/mutiullahhaneef)
[![Email](https://img.shields.io/badge/Email-Contact-aa44ff?style=for-the-badge&logo=gmail&logoColor=white&labelColor=03050f)](mailto:haneefmutiullah@email.com)

---

## 🌟 Show Your Support

If CleanFlow AI saved you time or sparked an idea — a ⭐ on this repo means the world and helps others find it.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:03050f,50:0066ff,100:00dc99&height=120&section=footer" width="100%"/>

*Built with ❤️ for the Data Science Community*

</div>
