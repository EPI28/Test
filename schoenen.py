import streamlit as st
import pandas as pd

# Lees het CSV-bestand in
df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')

st.set_page_config(page_title="Schoenen Verkoop", layout="wide")

st.title("📊 Exclusieve Schoenen Verkoop met Locatie")


# Toon de eerste rijen van de dataset
print(df.head())



