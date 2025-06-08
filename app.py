import streamlit as st
from PIL import Image
import pandas as pd
import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from utils.matcher import oversæt_fuzzy

@st.cache_resource
def load_model():
    extractor = AutoFeatureExtractor.from_pretrained("nateraw/food101")
    model = AutoModelForImageClassification.from_pretrained("nateraw/food101")
    return extractor, model

extractor, model = load_model()
df = pd.read_csv("kaloriedata.csv")
food_list = df["navn"].tolist()

st.title("🥗 Kalorieestimering via billede")

uploaded_file = st.file_uploader("Upload billede", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Dit billede", use_container_width=True)

    inputs = extractor(images=img, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.nn.functional.softmax(logits, dim=-1)
    confidence, pred_class = torch.max(probs, dim=1)
    label = model.config.id2label[pred_class.item()]
    conf_value = confidence.item()

    st.markdown(f"🔍 Modelgæt: `{label}` ({conf_value:.0%} sikkerhed)")
    if conf_value < 0.7:
        selected = st.selectbox("Modellen er usikker – vælg korrekt fødevare:", food_list)
    else:
        selected = oversæt_fuzzy(label.replace("_", " "), food_list)

    st.write(f"✅ Bruges som: **{selected}**")
    row = df[df["navn"] == selected]
    if not row.empty:
        kcal_100 = row["kcal_pr_100g"].values[0]
        vægt = 150  # dummy estimeret vægt
        kcal = vægt * kcal_100 / 100
        st.success(f"{vægt} g {selected} → {kcal:.0f} kcal")

        # Feedback
        user_feedback = st.text_input("Tilføj kommentar eller rettelse (valgfrit)")
        if st.button("Send feedback"):
            with open("feedback_log.csv", "a") as f:
                f.write(f"{label},{selected},{conf_value:.2f},{user_feedback}\n")
            st.info("✅ Feedback sendt. Tak!")
    else:
        st.warning("⚠️ Ukendt fødevare.")