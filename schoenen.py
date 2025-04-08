import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Schoenen Verkoop Analyse", layout="wide")
st.title("👟 Exclusieve Schoenen Verkoop met Locatie, Omzetanalyse en Targets")

# CSV inlezen
try:
    df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')
    st.success("CSV-bestand succesvol geladen.")
    
    # Toon de ruwe data
    st.subheader("🔍 Dataset")
    st.dataframe(df, use_container_width=True)

    # Vereiste kolommen checken
    required_cols = {'aankoopdatum', 'prijs', 'aantal'}
    if required_cols.issubset(df.columns):
        st.subheader("📈 Totale Omzet per maand")

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

        # Totale omzet per maand berekenen
        omzet_per_maand = (
            gefilterde_df
            .groupby(['maand'])['omzet']
            .sum()
            .reset_index()
        )

        # Target voor de totale omzet
        target = st.number_input("Doel (target) voor totale omzet per maand", min_value=0.0, value=0.0, step=100.0)

        # Grafiek opbouwen met Altair (staafdiagram)
        st.subheader("📊 Totale omzet per maand met target (Staafdiagram)")

        base = alt.Chart(omzet_per_maand).mark_bar().encode(
            x='maand:T',
            y='omzet:Q',
            color=alt.value('blue'),
            tooltip=['maand', 'omzet']
        )

        # Voeg de target lijn toe
        target_line = alt.Chart(omzet_per_maand).mark_rule(color='red', strokeDash=[4, 4]).encode(
            y=alt.datum(target),
            tooltip=alt.value(f"Target: {target}")
        )

        # Combineer de staafgrafiek met de targetlijn
        full_chart = base + target_line

        # Toon de grafiek
        st.altair_chart(full_chart.interactive(), use_container_width=True)

    else:
        st.warning(f"De volgende kolommen ontbreken voor omzetberekening: {required_cols - set(df.columns)}")

except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat als dit script.")
except Exception as e:
    st.error(f"Er is een fout opgetreden bij het laden of verwerken van het bestand: {e}")
