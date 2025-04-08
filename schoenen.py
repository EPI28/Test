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
    
    # Controleer of nodige kolommen bestaan
    required_cols = {'verkoopdatum', 'prijs', 'aantal'}
    if required_cols.issubset(df.columns):
        st.subheader("📈 Omzet per maand")

        # Zorg dat verkoopdatum als datetime wordt herkend
        df['verkoopdatum'] = pd.to_datetime(df['verkoopdatum'], errors='coerce')

        # Bereken omzet
        df['omzet'] = df['prijs'] * df['aantal']

        # Groepeer per maand
        df['maand'] = df['verkoopdatum'].dt.to_period('M').astype(str)
        omzet_per_maand = df.groupby('maand')['omzet'].sum().reset_index()

        # Plotten
        st.line_chart(data=omzet_per_maand, x='maand', y='omzet')
    else:
        st.warning(f"De volgende kolommen ontbreken voor omzetberekening: {required_cols - set(df.columns)}")

except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat als dit script.")
except Exception as e:
    st.error(f"Er is een fout opgetreden bij het laden of verwerken van het bestand: {e}")
