1. **Choose a provider:**
   - **OpenRouter:** Visit [openrouter.ai/keys](https://openrouter.ai/keys) to get a free API key
   - **Groq:** Visit [console.groq.com/keys](https://console.groq.com/keys) for a free API key

2. **Copy your API key.** You will need to paste it when prompted.

### ⚙️ Installation

We provide simple installation methods for your convenience.

#### **Quick Install (Recommended)**

**Linux / macOS / Termux:**

```bash
bash <(curl -s https://raw.githubusercontent.com/BlackTechX011/Hacx-GPT/main/scripts/install.sh)
```

**Windows:**

1. Download `install.bat` from this repository
2. Double-click to run

#### **Manual Installation**

```bash
# 1. Clone the repository
git clone https://github.com/roop37/unrestricted_ai_chatbot.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install package (optional, for command shortcuts)
pip install -e .
```

---

## 👀 Usage

### 🖥️ Terminal Interface (Original)

Run the classic command-line interface:

```bash
hacxgpt
# OR
python -m hacxgpt.main
```

python hacxgpt_web.py

# OR (after pip install)

hacxgpt-web

Then open your browser to: **http://127.0.0.1:7860**

# Custom port

python hacxgpt_web.py --port 8080

# Allow network access (access from other devices)

python hacxgpt_web.py --host 0.0.0.0

# Create public share link

python hacxgpt_web.py --share

# Combined options

python hacxgpt_web.py --host 0.0.0.0 --port 8080 --share

### Configuration File

Settings are stored in `.hacx` file in your home directory or current directory.

## 🎯 Quick Start Summary

```bash
# 1. Install
git clone https://github.com/BlackTechX011/Hacx-GPT.git
cd Hacx-GPT
pip install -r requirements.txt

# 2. Get API Key
# Visit openrouter.ai/keys or console.groq.com/keys

# 3. Launch (choose one)
# Terminal:
hacxgpt

# Web:
python hacxgpt_web.py
# Then open: http://127.0.0.1:7860

# 4. Configure and chat!
```
