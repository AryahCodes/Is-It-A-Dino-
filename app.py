

import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import keras

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="Are You a Dinosaur?",
    page_icon="🦖",
    layout="centered"
)

st.write("TensorFlow version:", tf.__version__)
st.write("Keras version:", keras.__version__)

# -------------------------------------------------------------
# Custom CSS Styling
# -------------------------------------------------------------
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
        text-align: center;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .dinosaur {
        background-color: #90EE90;
        border: 3px solid #228B22;
    }
    .not-dinosaur {
        background-color: #87CEEB;
        border: 3px solid #4682B4;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Model Loader
# -------------------------------------------------------------
@st.cache_resource
def load_model():
    """Load the trained Keras 3 model (.keras format)."""
    model_path = 'models/dinosaur_classifier.keras'

    if not os.path.exists(model_path):
        st.error(f"❌ Model not found at {model_path}")
        st.info("Please ensure 'dinosaur_classifier.keras' is in the 'models/' folder.")
        st.stop()

    try:
        # 🧠 Keras 3 fix → disable safety checks for custom / legacy layers
        model = tf.keras.models.load_model(model_path, compile=False, safe_mode=False)
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------
def preprocess_image(image):
    """Prepare image for prediction."""
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array.astype(np.float32)

def get_dinosaur_message(confidence):
    if confidence > 90:
        return "🦕 EXTREMELY DINOSAUR! You're practically a T-Rex!"
    elif confidence > 75:
        return "🦖 Very dinosaur-like! Strong prehistoric vibes detected!"
    elif confidence > 60:
        return "🦕 Moderately dinosaur! You've got that reptilian charm!"
    else:
        return "🦖 Slightly dinosaur! Maybe a distant ancestor?"

def get_not_dinosaur_message(confidence):
    if confidence > 90:
        return "👤 Definitely human! Not a scale in sight!"
    elif confidence > 75:
        return "🧑 Very human! Sorry, no prehistoric DNA detected."
    elif confidence > 60:
        return "👨 Probably human. But there might be a little dino in you!"
    else:
        return "🤔 Hmm, this is close! Are you sure you're not hiding scales?"

# -------------------------------------------------------------
# Streamlit UI
# -------------------------------------------------------------
def main():
    st.markdown('<p class="big-font">🦖 Are You a Dinosaur? 🦕</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the Dinosaur Detector!
    Upload a photo and discover if you're secretly a prehistoric creature.
    
    📸 **Best results with:**
    - Clear photos of faces or full bodies  
    - Good lighting  
    - Front-facing angles  
    
    *Disclaimer: This is a fun AI project for entertainment purposes!*
    """)

    # Load the model once
    with st.spinner("🔄 Loading AI model..."):
        model = load_model()
    st.success("✅ Model loaded successfully!")

    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a photo to analyze"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption='Your uploaded image', use_column_width=True)

        with st.spinner("🔍 Analyzing with AI..."):
            img_array = preprocess_image(image)
            prediction = float(model.predict(img_array, verbose=0).flatten()[0])

        st.markdown("---")

        if prediction > 0.5:
            confidence = prediction * 100
            message = get_dinosaur_message(confidence)
            st.markdown(f"""
            <div class="result-box dinosaur">
                <h2 style="text-align: center;">🦕 DINOSAUR DETECTED! 🦕</h2>
                <h3 style="text-align: center;">{confidence:.1f}% Dinosaur</h3>
                <p style="text-align: center; font-size: 18px;">{message}</p>
            </div>
            """, unsafe_allow_html=True)
            st.progress(float(prediction))

            with st.expander("🦖 Dinosaur Traits Detected"):
                traits = []
                if confidence > 80:
                    traits.extend(["Scales detected", "Prehistoric energy", "Sharp teeth potential"])
                if confidence > 60:
                    traits.extend(["Reptilian features", "Ancient wisdom", "Tail-like appendages (maybe)"])
                if confidence > 40:
                    traits.extend(["Roaring capability", "Love of Jurassic period", "Tiny arms energy"])
                for trait in traits:
                    st.write(f"✅ {trait}")
        else:
            confidence = (1 - prediction) * 100
            message = get_not_dinosaur_message(confidence)
            st.markdown(f"""
            <div class="result-box not-dinosaur">
                <h2 style="text-align: center;">👤 NOT A DINOSAUR</h2>
                <h3 style="text-align: center;">{confidence:.1f}% Not a Dinosaur</h3>
                <p style="text-align: center; font-size: 18px;">{message}</p>
                </div>
                """, unsafe_allow_html=True)
            st.progress(float(1 - prediction))

            with st.expander("🧩 Traits Detected"):
                st.write("✅ No dino-like scales detected")
                st.write("✅ Possibly human or object")
                st.write("✅ Definitely from the modern era (not Jurassic!)")

    st.markdown("<hr><center>Made with ❤️ by Aryahvishwa Babu </center>", unsafe_allow_html=True)

# -------------------------------------------------------------
# Run App
# -------------------------------------------------------------
if __name__ == "__main__":
    main()