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

    # Kaartweergave als latitude/longitude aanwezig zijn
    if {'latitude', 'longitude'}.issubset(df.columns):
        st.subheader("🗺️ Verkooplocaties")
        st.map(df[['latitude', 'longitude']])

    # Vereiste kolommen checken
    required_cols = {'aankoopdatum', 'prijs', 'aantal', 'land'}
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

        landen = sorted(gefilterde_df['land'].unique())

        st.subheader("🎯 Targets per land")
        targets = {}
        for land in landen:
            targets[land] = st.number_input(f"Target omzet per maand voor {land}", min_value=0.0, value=0.0, step=100.0)

        # Omzet per maand per land berekenen
        omzet_per_maand = (
            gefilterde_df
            .groupby(['maand', 'land'])['omzet']
            .sum()
            .reset_index()
        )

        # Voeg de target kolom toe aan de dataset
        omzet_per_maand['target'] = omzet_per_maand['land'].map(targets)

        # Grafiek opbouwen met Altair
        st.subheader("📊 Maandelijkse omzet per land met targets")

        base = alt.Chart(omzet_per_maand).mark_line(point=True).encode(
            x='maand:T',
            y='omzet:Q',
            color=alt.condition(
                alt.datum.omzet > alt.datum.target,
                alt.value('green'),
                alt.value('red')
            ),
            tooltip=['maand', 'land', 'omzet', 'target']
        )

        # Voeg de target lijn toe per land
        target_lines = []
        for land, target in targets.items():
            if target > 0:
                line = alt.Chart(omzet_per_maand[omzet_per_maand['land'] == land]).mark_rule(color='red', strokeDash=[4, 4]).encode(
                    y=alt.datum(target),
                    tooltip=alt.value(f"Target: {target}")
                ).properties(title=f"Targetlijn voor {land}")
                target_lines.append(line)

        full_chart = base
        for tline in target_lines:
            full_chart += tline

        st.altair_chart(full_chart.interactive(), use_container_width=True)

    else:
        st.warning(f"De volgende kolommen ontbreken voor omzetberekening: {required_cols - set(df.columns)}")

except FileNotFoundError:
    st.error("CSV-bestand niet gevonden. Zorg dat het bestand 'exclusieve_schoenen_verkoop_met_locatie.csv' in dezelfde map staat als dit script.")
except Exception as e:
    st.error(f"Er is een fout opgetreden bij het laden of verwerken van het bestand: {e}")
