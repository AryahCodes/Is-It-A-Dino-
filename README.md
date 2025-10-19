# 🦖 Is-It-A-Dino?

**Is-It-A-Dino?** is a fun AI app that classifies whether an uploaded image looks like a *dinosaur* or a *human*.  
Built with **TensorFlow**, **Streamlit**, and **Python**, it combines a deep-learning CNN with a playful, interactive UI.

---

## 🚀 Live Demo
👉 [Run on Streamlit Cloud](https://share.streamlit.io/) *(link will be added after deployment)*

---

## 🧠 How It Works
1. Upload an image (face or full-body photo).  
2. The app preprocesses it to **224×224 RGB** format.  
3. A trained **Convolutional Neural Network (CNN)** predicts “🦕 Dinosaur” or “👤 Human.”  
4. The app displays the prediction with a confidence score and a fun verdict.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit 1.38.0 |
| **Model** | TensorFlow 2.19.0 + Keras 3.10.0 |
| **Data** | Custom human vs. dinosaur dataset |
| **Visualization** | Matplotlib 3.9.2 |
| **Deployment** | Streamlit Cloud |
| **Image Processing** | Pillow 10.4.0 |
| **Array Ops** | NumPy 2.1.3 |

---

## 🖥️ Run Locally (All Steps in One Go)

```bash
# 1. Clone the repository
git clone https://github.com/AryahCodes/Is-It-A-Dino-.git
cd Is-It-A-Dino-

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate     # macOS / Linux
# OR (Windows)
# .venv\Scripts\activate

# 3. Install dependencies (tested + stable versions)
pip install \
  "tensorflow==2.19.0" \
  "keras==3.10.0" \
  "streamlit==1.38.0" \
  "pillow==10.4.0" \
  "numpy==2.1.3" \
  "matplotlib==3.9.2"

# 4. Run the app
streamlit run app.py