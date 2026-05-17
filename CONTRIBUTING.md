# Contributing to CleanFlow AI

Thank you for investing your time in contributing! Any contribution makes CleanFlow AI better for the entire data science community. ✨

---

## 🚀 Quick Start for Contributors

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/cleanflow-ai.git
cd cleanflow-ai
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure your `.env`

```bash
cp .env.example .env
# Add your GOOGLE_API_KEY
```

### 4. Create a branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

---

## 📐 Code Standards

- Follow **PEP 8** for Python style
- All functions must have **docstrings**
- New features must include **unit tests** where applicable
- Keep the `core/` layer free of Streamlit imports — it must stay framework-agnostic

---

## 🐛 Reporting Bugs

Open an issue using the **Bug Report** template. Include:
- Your Python version
- OS
- Steps to reproduce
- Expected vs. actual behavior
- Any error tracebacks

---

## ✨ Suggesting Features

Open an issue using the **Feature Request** template. Describe:
- The problem your feature solves
- Your proposed solution
- Alternatives you considered

---

## 📬 Pull Request Process

1. Update `README.md` if your change affects usage or setup
2. Add/update tests for your changes
3. Make sure `streamlit run app.py` runs without errors
4. Reference the related issue in your PR description: `Closes #123`
5. Wait for review — we aim to respond within 48 hours

---

## 💬 Code of Conduct

Be kind, be constructive, be collaborative. We're all here because we love data.
