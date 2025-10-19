# 🦖 Is-It-A-Dino?

**Is-It-A-Dino?** is a fun AI app that classifies whether an uploaded image looks like a *dinosaur* or a *human*.  
Built with **TensorFlow**, **Streamlit**, and **Python**, it combines computer-vision models with a playful UI.

---

## 🚀 Live Demo
👉 [Run on Streamlit Cloud](https://share.streamlit.io/) *(link once deployed)*

---

## 🧠 How It Works
1. You upload an image (face or full-body photo).  
2. The app preprocesses it (224×224 RGB scaling).  
3. A trained **CNN** model predicts “Dinosaur 🦕” or “Human 👤”.  
4. Confidence scores and fun feedback messages are displayed.

---

## 🧩 Tech Stack
| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Model | TensorFlow / Keras |
| Data | Custom human vs. dinosaur dataset |
| Deployment | Streamlit Cloud |

---

## 🖥️ Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/AryahCodes/Is-It-A-Dino-.git
cd Is-It-A-Dino-
