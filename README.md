# 🐝 Spelling Bee Trainer

A desktop application built with **Python + PySide6** to help students practice spelling bee words using **active recall**, **typing practice**, and **multiple-choice reinforcement**.

Designed with a clean, distraction-free interface inspired by **Monkeytype**.

---

## ✨ Features

- 📖 Word introduction (word + definition)
- ⌨️ Sentence typing practice (strict mode)
- 🟩 Monkeytype-style visual feedback
- 🔤 Multiple-choice spelling reinforcement
- 🧠 Session-based word tracking with tiers
- 🧪 Quiz mode after practice set
- 🌙 Dark mode UI
- 🪟 Cross-platform (Windows & Linux)

---

## 🖥️ Application Flow

```
Start Screen
   ↓
Word Intro Screen
   ↓
Typing Screen
   ↓
Multiple Choice Screen
   ↓
(next word...)
   ↓
Quiz Screen
```

---

## 📂 Project Structure

```
spelling_bee/
│
├── core/
│   ├── session_manager.py
│   ├── data_loader.py
│   ├── distractors.py
│   └── models.py
│
├── ui/
│   ├── main_window.py
│   ├── config.py
│   └── screens/
│       ├── start_screen.py
│       ├── word_screen.py
│       ├── typing_screen.py
│       ├── multi_choice_screen.py
│       └── quiz_screen.py
│
├── assets/
│   └── audio/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Running the App (Development)

### 1️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app

```bash
python main.py
```

---

## 📦 Building an Executable

This project supports **PyInstaller**.

```bash
pyinstaller --onefile --windowed main.py
```

⚠️ You must build on each target OS:

- Windows → `.exe`
- Linux → Linux binary

---

## 📄 CSV Word List Format

CSV files should include headers like:

```csv
word,definition,sentence,origin
```

Additional optional fields:

- `phonetic`
- `distractors` (semicolon-separated)

Users can import CSV files directly from the UI.

---

## 🎯 Educational Goals

- Reinforce correct spelling through repetition
- Encourage accuracy with strict typing mode
- Combine recall + recognition learning
- Track mastery and areas needing review

---

## 🛠️ Planned Enhancements

- Text-to-speech pronunciation
- Persistent user profiles
- Difficulty-weighted word selection
- Official spelling bee list imports
- Progress visualization

---

## 📜 License

MIT License (or your preferred license)

---

Built with ❤️ to make spelling practice effective and fun.
