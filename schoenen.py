import streamlit as st
import pandas as pd

st.set_page_config(page_title="Schoenen Verkoop Analyse", layout="wide")
st.title("👟 Exclusieve Schoenen Verkoop met Locatie en Omzetanalyse")

# CSV inlezen
try:
    df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')
    st.success("CSV-bestand succesvol geladen.")
    
    # Toon de ruwe data
    st.subheader("🔍 Dataset")
    st.dataframe(df, use_container_width=True)

    # Kaartweergave als latitude/longitude aanwezig zijn
    if {'latitude', 'longitude'}.issubset(df.columns):
        st.subheader("🗺️ Verkooplocaties")
        st.map(df[['latitude', 'longitude']])

    # Vereiste kolommen checken
    required_cols = {'aankoopdatum', 'prijs', 'aantal'}
    if required_cols.issubset(df.columns):
        st.subheader("📈 Omzet per maand")

        # Datum verwerken
        df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'], errors='coerce')
        df = df.dropna(subset=['aankoopdatum
