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
food_list = df["food"].tolist()

st.title("🥗 WebKalorier – Billedbaseret Kalorieestimering")

file = st.file_uploader("Upload et billede af din mad", type=["jpg", "jpeg", "png"])
if file:
    img = Image.open(file).convert("RGB")
    st.image(img, caption="Dit billede", use_container_width=True)

    inputs = extractor(images=img, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.nn.functional.softmax(logits, dim=-1)
    confidence, pred_class = torch.max(probs, dim=1)
    label = model.config.id2label[pred_class.item()]
    conf_value = confidence.item()

    st.write(f"🤖 Modelgæt: **{label}** ({conf_value:.0%} sikkerhed)")

    if conf_value >= 0.7:
        food_raw = label.replace("_", " ")
    else:
        food_raw = st.selectbox("Modellen er usikker. Vælg fødevare:", sorted(food_list))

    food_label = oversæt_fuzzy(food_raw, food_list)
    st.write("🔍 Matcher som:", food_label)

    row = df[df["food"] == food_label]
    if not row.empty:
        kcal = float(row["kcal_per_gram"].values[0])
        density = float(row["g_per_cm2"].values[0])
        st.success(f"{food_label.title()}: {kcal} kcal/g, {density} g/cm²")
    else:
        st.warning("Ingen data fundet for denne fødevare.")
