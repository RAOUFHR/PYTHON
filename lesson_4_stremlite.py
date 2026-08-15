
import streamlit as st
import pandas as pd
from pathlib import Path
# from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------------------------
# CONFIGURATION DE LA PAGE
# ---------------------------------------------------------------------
st.set_page_config(page_title="Mini SCADA", page_icon="factory", layout="wide")
st.title("Mini SCADA - Supervision atelier")

# ---------------------------------------------------------------------
# AUTO-REFRESH : relance le script toutes les 5 secondes (5000 ms)
# ---------------------------------------------------------------------
# st_autorefresh(interval=5000, key="refresh")

# ---------------------------------------------------------------------
# CHOIX DE LA MACHINE A SUPERVISER
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "automatisme_donnees.csv"

df = pd.read_csv(CSV_FILE, parse_dates=["timestamp"])
machines_disponibles = df["machine_id"].unique()
machine_choisie = st.selectbox("Choisir une machine", machines_disponibles)

sub = df[df["machine_id"] == machine_choisie]
derniere = sub.iloc[-1]   # derniere mesure connue pour cette machine

temperature = derniere["temperature_C"]
pression = derniere["pression_bar"]
vitesse = derniere["vitesse_rpm"]
statut = derniere["statut"]
horodatage = derniere["timestamp"]

st.caption(f"Derniere mesure : {horodatage}")

# ---------------------------------------------------------------------
# AFFICHAGE EN COLONNES
# ---------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{temperature:.1f} degres C")
col2.metric("Pression", f"{pression:.2f} bar")
col3.metric("Vitesse", f"{vitesse:.0f} rpm")

# ---------------------------------------------------------------------
# STATUT AVEC COULEUR DYNAMIQUE (selon la temperature)
# ---------------------------------------------------------------------
if pd.isna(temperature):
    st.warning("Donnee temperature manquante pour cette mesure")
elif temperature > 65:
    st.error(f"ALARME : temperature trop elevee ({temperature:.1f} degres C)")
elif temperature > 58:
    st.warning(f"Attention : temperature elevee ({temperature:.1f} degres C)")
else:
    st.success(f"Temperature normale ({temperature:.1f} degres C)")

# ---------------------------------------------------------------------
# STATUT MACHINE (issu directement de la colonne "statut" du CSV)
# ---------------------------------------------------------------------
if statut == "ALARME":
    st.error(f"Statut machine : {statut}")
elif statut == "MAINTENANCE":
    st.warning(f"Statut machine : {statut}")
elif statut == "ARRET":
    st.info(f"Statut machine : {statut}")
else:
    st.success(f"Statut machine : {statut}")

# ---------------------------------------------------------------------
# HISTORIQUE - petit graphique de la temperature de cette machine
# ---------------------------------------------------------------------
st.subheader("Historique temperature")
st.line_chart(sub.set_index("timestamp")["temperature_C"])
