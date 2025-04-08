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
        st.subheader("📈 Omzet per maand per land")

        # Datum verwerken
        df['aankoopdatum'] = pd.to_datetime(df['aankoopdatum'], errors='coerce')
        df = df.dropna(subset=['aankoopdatum'])

        # Extra kolommen
        df['jaar'] = df['aankoopdatum'].dt.year
        df['maand'] = df['aankoopdatum'].dt.to_period('M').astype(str)
        df['omzet'] = df['prijs'] * df['aantal']

        # Filters: jaar en merk
        jaren = sorted(df['jaar'].unique())
        jaren_keuze = ['Alle jaren'] + list(map(str, jaren))
        geselecteerd_jaar = st.selectbox("Filter op jaar", jaren_keuze)

        merken = sorted(df['merk'].dropna().unique()) if 'merk' in df.columns else []
        merken_keuze = ['Alle merken'] + merken
        geselecteerd_merk = st.selectbox("Filter op merk", merken_keuze)

        # Filtering toepassen
        gefilterde_df = df.copy()
        if geselecteerd_jaar != 'Alle jaren':
            gefilterde_df = gefilterde_df[gefilterde_df['jaar'] == int(geselecteerd_jaar)]
        if geselecteerd_merk != 'Alle merken':
            gefilterde_df = gefilterde_df[gefilterde_df['merk'] == geselecteerd_merk]

        # Controleer of kolom 'land' bestaat
        if 'land' not in gefilterde_df.columns:
            st.warning("Kolom 'land' ontbreekt in de dataset. Kan geen lijnen per land tekenen.")
        else:
            # Groepeer per maand en land
            omzet_per_maand_land = (
                gefilterde_df
                .groupby(['maand', 'land'])['omzet']
                .sum()
                .reset_index()
                .pivot(index='maand', columns='land', values='omzet')
                .fillna(0)
            )

            # Lijndiagram tonen
            st.line_chart(omzet_per_maand_land)
    else:
        st.warning(f"De volgende kolommen ontbreken voor omzetberekening: {required_cols - set(df.columns)}")

except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat als dit script.")
except Exception as e:
    st.error(f"Er is een fout opgetreden bij het laden of verwerken van het bestand: {e}")
