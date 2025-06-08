
import streamlit as st
import pandas as pd
import os
from utils.matcher import oversæt_fuzzy
from utils.image_utils import load_image, detect_hand_and_food_area
from PIL import Image

st.title("Kalorie Estimator fra Billede")

kaloriedata = pd.read_csv("kaloriedata.csv")
food_list = kaloriedata["fødevare"].tolist()

uploaded_file = st.file_uploader("Upload billede", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = load_image(uploaded_file)
    st.image(img, caption="Dit billede", use_container_width=True)

    st.markdown("### Billedeanalyse")
    detekterede = [
        {"label": "kartoffel", "areal_cm2": 60},
        {"label": "broccoli", "areal_cm2": 20},
        {"label": "æg", "areal_cm2": 30},
        {"label": "smør", "areal_cm2": 10}
    ]

    results = []
    for d in detekterede:
        label = d["label"]
        fallback = st.selectbox(f"Er det korrekt for: {label}?", food_list, index=food_list.index(label) if label in food_list else 0)
        valgt_label = oversæt_fuzzy(fallback, food_list)
        d["label"] = valgt_label
        results.append(d)

    st.markdown("### Resultat")
    def estimer_vægt_cm2(areal, madtype):
        vægtfaktor = {
            "kartoffel": 2.5,
            "broccoli": 1.2,
            "æg": 3.0,
            "smør": 1.0
        }
        return areal * vægtfaktor.get(madtype, 2.0)

    total_txt = []
    for item in results:
        label = item["label"]
        vægt = estimer_vægt_cm2(item["areal_cm2"], label)
        rad = kaloriedata[kaloriedata["fødevare"] == label]
        if not rad.empty:
            kcal_pr_100g = rad.iloc[0]["kcal_pr_100g"]
            kcal = vægt * kcal_pr_100g / 100
            total_txt.append(f"{round(vægt)} g {label} ({round(kcal)} kcal)")
    st.success(", ".join(total_txt))
