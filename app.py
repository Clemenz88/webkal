import streamlit as st
from utils.image_utils import load_image, detect_hand_and_food_area
from utils.matcher import oversæt_fuzzy
import pandas as pd

st.title("Kalorieestimering med håndreference")

uploaded_file = st.file_uploader("Upload et billede", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = load_image(uploaded_file)
    st.image(image, caption="Uploadet billede", use_container_width=True)

    hand_area, food_area = detect_hand_and_food_area(image)
    st.write(f"⚖️ Estimeret område: {food_area:.2f} cm² mad (vs. {hand_area:.2f} cm² hånd)")

    kaloriedata = pd.read_csv("kaloriedata.csv")
    food_list = kaloriedata["navn"].tolist()

    # Dummy-resultat (erstattes af modeloutput i rigtig version)
    detected_food = ["egg", "potato", "butter", "broccoli"]
    results = []
    for raw in detected_food:
        label = oversæt_fuzzy(raw, food_list)
        kalorie_pr_100g = kaloriedata[kaloriedata["navn"] == label]["kcal pr 100g"].values[0]
        mængde = 50  # dummy
        energi = mængde * kalorie_pr_100g / 100
        results.append((label, mængde, energi))

    st.subheader("🍽️ Madanalyse")
    for navn, g, kcal in results:
        st.write(f"- **{navn}**: {g} g → {kcal:.1f} kcal")

    st.selectbox("Hvis noget er forkert, vælg den rigtige madvare:", food_list)