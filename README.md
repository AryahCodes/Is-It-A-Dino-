# 🦖 Is-It-A-Dino?

**Is-It-A-Dino?** is a fun AI web app that classifies whether an uploaded image looks like a *dinosaur* or *not*.  
Built using **TensorFlow**, **Keras**, and **Streamlit**, it combines a custom-trained deep-learning CNN with an interactive, responsive UI.

---

## 🚀 Live Demo
👉 [Try It Here](https://ckbwkowcenzhard6kesdlx.streamlit.app)

---

## 🧠 How It Works
1. You upload an image (face, body, or object).  
2. The app preprocesses it to **224×224 RGB** format and normalizes pixel values.  
3. A **custom CNN model** predicts whether it’s a “🦕 Dinosaur” or “👤 Not a Dinosaur.”  
4. Confidence scores, interpretability messages, and fun feedback appear in real-time.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit 1.38.0 |
| **Model Framework** | TensorFlow 2.20.0 + Keras 3.10.0 |
| **Data Processing** | NumPy 1.26.4, Pillow 10.4.0 |
| **Visualization** | Matplotlib 3.9.2 |
| **Deployment** | Streamlit Cloud |
| **Python Runtime** | 3.11 |

---

## 📂 Dataset

A proprietary dataset of **1,900+ curated images**, collected and labeled manually:
- Dinosaurs 🦕 (T-Rex, Velociraptor, Stegosaurus, etc.)
- Humans / Non-Dinosaurs 👤 (people, everyday objects, animals)

All images were cleaned, resized to `224×224`, normalized, and augmented (flips, rotations, zoom)  
to enhance model generalization.

📁 Dataset: [processed_data_complete.zip (Google Drive)](https://drive.google.com/drive/folders/YOUR-LINK-HERE)

---

## 🧰 Model Training

The CNN was trained using TensorFlow 2.20 + Keras 3.10 with:
- Data augmentation layers (RandomFlip, RandomRotation, RandomZoom)
- Dropout regularization to prevent overfitting
- Adam optimizer with binary crossentropy loss  
- Early stopping and model checkpointing

Final model: `models/dinosaur_classifier.keras`

Achieved **~95% validation accuracy** after 30 epochs.

---

## 🖥️ Run Locally

### 1️⃣ Clone the repository
```bash
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
