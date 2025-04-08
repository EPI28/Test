import streamlit as st
import pandas as pd

# Lees het CSV-bestand in
df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')

st.set_page_config(page_title="Schoenen Verkoop", layout="wide")

st.title("📊 Exclusieve Schoenen Verkoop met Locatie")
# CSV inlezen
try:
    df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')
    st.success("CSV-bestand succesvol geladen.")
    
    # Toon de ruwe data
    st.subheader("🔍 Dataset")
    st.dataframe(df, use_container_width=True)

    # Optioneel: laat een kaart zien als er locatiegegevens zijn
    if {'latitude', 'longitude'}.issubset(df.columns):
        st.subheader("🗺️ Verkooplocaties")
        st.map(df[['latitude', 'longitude']])
    else:
        st.info("Geen locatiegegevens (latitude/longitude) gevonden voor kaartweergave.")

except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat als dit script.")
except Exception as e:
    st.error(f"Er is een fout opgetreden bij het laden van het bestand: {e
                                                                        
# Toon de eerste rijen van de dataset
print(df.head())



