# ⏳ KaalVerse

### Step into the world of the past.

**KaalVerse** is an AI-powered historical experience simulator that lets users travel across different regions and time periods of India and experience everyday life through the perspective of a chosen character.

Instead of simply reading historical facts, users can **step into a historical world** and experience a day as a merchant, teacher, farmer, artisan, politician, or other role.

---

## ✨ Features

* 🗺️ Explore different regions of India
* ⏳ Travel through different historical periods
* 👤 Choose your historical role
* ⚧️ Choose your character's gender
* 🎂 Choose your character's age
* 📜 Generate an immersive one-day historical experience
* 🖼️ Generate AI-powered historical scene images
* 🔊 Generate narration audio
* 💾 Save and revisit previous journeys
* 🗑️ Delete individual journeys or clear all saved journeys
* 🍛 Explore historical food, clothing, occupations, homes, crafts and daily life
* 🎭 Experience culture, traditions, festivals, games and architecture

---

## 🧠 How It Works

```text
Choose Region
      ↓
Choose Historical Era
      ↓
Choose Role, Gender & Age
      ↓
AI Generates Historical Experience
      ↓
Generate Scene Images & Narration
      ↓
Save Journey
      ↓
Revisit Your Historical Journey
```

---

## 🛠️ Technologies Used

* **Python** — Core application development
* **Streamlit** — Interactive web interface
* **Ollama Cloud** — AI-powered historical experience generation
* **Hugging Face** — AI image generation
* **FLUX.1-schnell** — Historical scene generation
* **gTTS** — Text-to-speech narration
* **JSON** — Historical data storage
* **Git & GitHub** — Version control

---

## 📁 Project Structure

```text
KaalVerse/
│
├── app.py
├── ai_engine.py
├── image_generator.py
├── audio_generator.py
├── historical_data.json
├── .gitignore
└── README.md
```

### Main Files

| File                   | Purpose                                                  |
| ---------------------- | -------------------------------------------------------- |
| `app.py`               | Streamlit user interface and application flow            |
| `ai_engine.py`         | Generates historical experiences using AI                |
| `image_generator.py`   | Generates historical scene images                        |
| `audio_generator.py`   | Creates narration audio                                  |
| `historical_data.json` | Stores historical information                            |
| `.gitignore`           | Prevents sensitive/unnecessary files from being uploaded |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/velpulaindhuvarsha/KaalVerse.git
cd KaalVerse
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install required packages

```bash
pip install streamlit huggingface_hub python-dotenv gTTS
```

Install any additional packages required by the AI engine.

---

## 🔐 API Configuration

Create a `.env` file in the project folder.

```env
OLLAMA_API_KEY=your_ollama_api_key
HF_API_KEY=your_huggingface_api_key
```

### ⚠️ Important

Never upload your actual API keys to GitHub.

The `.env` file is excluded using `.gitignore`.

---

## ▶️ Run the Project

After activating the virtual environment, run:

```bash
streamlit run app.py
```

The KaalVerse application will open in your browser.

---

## 🎯 Project Goal

KaalVerse aims to make history more **interactive, immersive and relatable**.

Rather than only learning *what happened in the past*, users can explore:

> **What would my life have been like if I had lived there?**

---

## 🚀 Future Scope

* 🌏 Support for more regions and historical periods
* 🗣️ Multiple Indian language support
* 🎙️ Voice-based interaction
* 🗺️ Interactive historical maps
* 👥 More historical characters and occupations
* 🎓 Educational mode for students
* 🏛️ Interactive historical environments
* 🤖 AI historical characters for conversations
* 📚 Verified historical knowledge sources

---

## 👩‍💻 Project

**KaalVerse — AI-Powered Historical Experience Simulator**

**Tagline:**

### *Step into the world of the past.*
