import streamlit as st
from utils.image_utils import load_image
from utils.matcher import oversæt_fuzzy
import pandas as pd

st.title("Kalorieestimering fra billede")
uploaded_file = st.file_uploader("Upload billede med hånd og mad", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = load_image(uploaded_file)
    st.image(img, caption="Dit billede", use_container_width=True)

    st.markdown("### Analyse")
    # Dummy analyse
    detected_food = ["æg", "kartofler", "smør", "broccoli"]
    weights = [100, 200, 50, 25]  # gram

    df = pd.read_csv("kaloriedata.csv")
    food_names = df["navn"].tolist()

    result = []
    for food, gram in zip(detected_food, weights):
        matched = oversæt_fuzzy(food, food_names)
        kcal_pr_100 = df[df["navn"] == matched]["kcal_pr_100g"].values[0] if matched else 0
        kcal = gram * kcal_pr_100 / 100
        result.append((food, matched, gram, round(kcal)))

    for original, match, g, kcal in result:
        st.write(f"🔍 {original} → **{match}**: {g} g → **{kcal} kcal**")

    total_kcal = sum([r[3] for r in result])
    st.markdown(f"### Totalt: **{total_kcal} kcal**")