import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Dashboard Étudiants Marocains en France", layout="wide")

# Titre principal
st.title("📊 Analyse des Étudiants Marocains en France (2022-2025)")
st.markdown("""
Cette plateforme présente les statistiques et les tendances d'évolution des étudiants marocains, 
basées sur les données extraites du rapport de Campus France.
""")

# Chargement et nettoyage des données
@st.cache_data
def load_data():
    df_raw = pd.read_csv('statistique Etudiant marocaine en France.csv', sep=';', header=None)
    
    # 1. Extraction Tendances Annuelles (Lignes 0 à 10)
    df_trends = df_raw.iloc[0:10, 0:4].copy()
    df_trends.columns = df_trends.iloc[0]
    df_trends = df_trends.drop(df_trends.index[0]).reset_index(drop=True)
    
    # Nettoyage des nombres (enlever espaces et conversion)
    def clean_num(x):
        if isinstance(x, str):
            return float(x.replace(' ', '').replace(',', '.').replace('%', ''))
        return x

    # 2. Extraction Répartition par établissement (Lignes 11 à 15)
    df_repart = df_raw.iloc[11:15, 0:4].copy()
    df_repart.columns = ["Type", "Part", "Master", "Licence"]
    df_repart = df_repart.drop(df_repart.index[0])

    # 3. Extraction Filières (Lignes 17+)
    df_filieres = df_raw.iloc[17:, 0:3].copy()
    df_filieres.columns = ["Filière", "Part", "Évolution"]
    df_filieres = df_filieres.dropna(subset=["Filière"]).drop(df_filieres.index[0])
    
    return df_trends, df_repart, df_filieres

try:
    df_trends, df_repart, df_filieres = load_data()

    # --- SIDEBAR / FILTRES ---
    st.sidebar.header("Paramètres")
    annee_sel = st.sidebar.selectbox("Choisir l'année de focus", ["2022-2023", "2023-2024", "2024-2025"])

    # --- KPI SECTION ---
    st.subheader(f"Chiffres clés pour {annee_sel}")
    col1, col2, col3, col4 = st.columns(4)
    
    # Récupération des valeurs pour les KPI
    val_total = df_trends.loc[df_trends['Années'] == 'Nombre etudiant Marocains', annee_sel].values[0]
    val_uni = df_trends.loc[df_trends['Années'] == 'Universités', annee_sel].values[0]
    val_rentre = df_trends.loc[df_trends['Années'] == ' Des étudiants marocains rentrent au Maroc', annee_sel].values[0]
    val_etrangers = df_trends.loc[df_trends['Années'] == 'Nombre étudiant étrangers', annee_sel].values[0]

    col1.metric("Total Étudiants Marocains", val_total)
    col2.metric("En Universités", val_uni)
    col3.metric("Retour au Maroc", val_rentre)
    col4.metric("Total Étudiants Étrangers (FR)", val_etrangers)

    st.divider()

    # --- VISUALISATIONS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Évolution du nombre d'étudiants")
        # Transformation pour le graphique
        plot_data = df_trends[df_trends['Années'] == 'Nombre etudiant Marocains'].melt(id_vars=['Années'], var_name='Année', value_name='Nombre')
        plot_data['Nombre'] = plot_data['Nombre'].str.replace(' ', '').astype(int)
        fig_evol = px.line(plot_data, x='Année', y='Nombre', markers=True, title="Tendance 2022-2025")
        st.plotly_chart(fig_evol, use_container_width=True)

    with c2:
        st.subheader("Répartition par établissement")
        # Nettoyage des parts pour le camembert
        df_repart['Part_Num'] = df_repart['Part'].str.replace('%', '').astype(float)
        fig_pie = px.pie(df_repart, values='Part_Num', names='Type', hole=0.4,
                         title="Distribution des inscriptions")
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- FILIÈRES ET DÉTAILS ---
    st.subheader("Domaines d'études et Perspectives")
    st.table(df_filieres)

except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
    st.info("Assurez-vous que le fichier 'statistique Etudiant marocaine en France.csv' est dans le même dossier.")

# Footer
st.markdown("---")
st.caption("Plateforme générée pour l'analyse des mobilités étudiantes.")