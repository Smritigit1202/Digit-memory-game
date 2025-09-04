
# 🧠 Enhanced Digit Span Test (Memory Evaluation Game)

A cognitive memory training and evaluation game built with Python and Tkinter, designed to test and enhance short-term memory, focus, and attention span using dynamically generated digit or alphabet sequences. Inspired by psychological memory span assessments.

## 🎯 Features

* 🔢 **Number Mode** and 🔤 **Alphabet Mode**
* 🔁 **Reverse Recall** after Level 3 to boost working memory
* ⬆️ **Adaptive Difficulty** – levels up after 2 consecutive correct answers
* 🎤 **Speech Input** using Google Speech Recognition
* 🔂 **Repeat Sequence** option with score penalty
* ⏸️ **Pause/Resume** function for user control
* 🧠 **Attention Evaluation** at the end
* 💬 **Motivational Feedback** after each answer

---

## 🖥️ How It Works

1. Choose between **Numbers** or **Alphabets** mode.
2. A sequence of 3+ characters is shown one-by-one.
3. Depending on your level, you're asked to:

   * Repeat the sequence normally (Level 1–3)
   * Repeat the **reversed** sequence (Level 4+)
4. Type your answer or use voice input.
5. Correct answers earn points and build level progression.
6. Make 3 mistakes, and the test ends with a performance report.

---

## 📊 Game Logic & Progression

| Parameter               | Details                              |
| ----------------------- | ------------------------------------ |
| Starting Digits         | 3                                    |
| Max Sequence Characters | Up to 10 digits or 26 alphabets      |
| Level Up Condition      | 2 consecutive correct answers        |
| Reverse Mode Trigger    | From Level 4 (i.e., when DIGITS ≥ 6) |
| Repeat Penalty          | -2 points & reset streak             |
| Fail Attempts           | Allowed up to 3 before test ends     |

---

## 🧪 Performance Evaluation

At the end of the game, you'll see:

* ✅ Total Score
* 🔢 Highest Level Reached
* 🧾 Number of Entries
* ⌛ Total Time Taken
* 📈 **Attention Level**:

  * Level 5+ → **Excellent**
  * Level 4 → **High**
  * Level 3 → **Good**
  * Level 2 → **Moderate**
  * Below 2 → **Needs Improvement**

---

## 🎥 Demo Videos



https://github.com/user-attachments/assets/ed118ad7-abc2-4a45-92fe-fce019a39d96




https://github.com/user-attachments/assets/aff4dfc3-7c36-4fe9-b8b5-7221b46549a4


---

## 🛠️ Tech Stack

* **Python 3.x**
* **Tkinter** for GUI
* **SpeechRecognition** (Google API)
* **Pillow (PIL)** for image handling (optional)
* **Random, String, Time, OS** (standard libraries)

---



### Requirements

```text
speechrecognition
pyaudio
pillow
```

> ⚠️ Note: If you're having issues installing `pyaudio` on Windows, use:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## 💡 Use Cases

This test is ideal for:

* 🧠 **Neurocognitive Training**
* 🧒 **Children with attention challenges (e.g., ADHD)**
* 👵 **Cognitive decline monitoring in elders**
* 🎓 **Student brain training tools**
* 🧘 **Focus improvement and memory games**

---


