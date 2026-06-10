# dashboard_reunion.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Économique La Réunion - Analyse en Temps Réel",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #0055A4, #EF4135, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .live-badge {
        background: linear-gradient(45deg, #0055A4, #EF4135);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0055A4;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #0055A4;
        border-bottom: 2px solid #EF4135;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .sector-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #0055A4;
        background-color: #f8f9fa;
    }
    .growth-indicator {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .positive { background-color: #d4edda; border-left: 4px solid #28a745; color: #155724; }
    .negative { background-color: #f8d7da; border-left: 4px solid #dc3545; color: #721c24; }
    .neutral { background-color: #e2e3e5; border-left: 4px solid #6c757d; color: #383d41; }
    .sector-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .reunion-flag {
        background: linear-gradient(90deg, #0055A4 33%, #EF4135 33%, #EF4135 66%, #FFFFFF 66%);
        height: 4px;
        margin: 0.5rem 0;
        border-radius: 2px;
    }
    .micro-region {
        background-color: #e8f4fd;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        border-left: 3px solid #0055A4;
    }
</style>
""", unsafe_allow_html=True)

class ReunionDashboard:
    def __init__(self):
        self.secteurs = self.define_secteurs()
        self.economic_data = self.initialize_economic_data()
        self.tourism_data = self.initialize_tourism_data()
        self.agriculture_data = self.initialize_agriculture_data()
        self.energy_data = self.initialize_energy_data()
        self.demographic_data = self.initialize_demographic_data()
        
    def define_secteurs(self):
        """Définit les secteurs économiques de La Réunion"""
        return {
            'Tourisme': {
                'nom_complet': 'Tourisme et Hôtellerie',
                'poids_pib': 18.7,
                'croissance': 6.2,
                'emplois': 35000,
                'couleur': '#EF4135',
                'description': 'Premier secteur économique de l\'île',
                'entreprises_cles': ['Accor', 'Club Med', 'Palm Hotel', 'LUX*'],
                'perspectives': 'Très positives avec reprise post-COVID'
            },
            'Agriculture': {
                'nom_complet': 'Agriculture et Agroalimentaire',
                'poids_pib': 12.3,
                'croissance': 2.1,
                'emplois': 28000,
                'couleur': '#28a745',
                'description': 'Canne à sucre, fruits tropicaux, élevage',
                'entreprises_cles': ['Tereos', 'Sucrerie de Bois Rouge', 'Chambre d\'Agriculture'],
                'perspectives': 'Stable avec diversification'
            },
            'BTP': {
                'nom_complet': 'Bâtiment et Travaux Publics',
                'poids_pib': 15.4,
                'croissance': 8.9,
                'emplois': 42000,
                'couleur': '#FF6B00',
                'description': 'Construction, infrastructures, grands chantiers',
                'entreprises_cles': ['Vinci', 'Eiffage', 'Bouygues', 'Sogea'],
                'perspectives': 'Très positives avec NEO'
            },
            'Commerce': {
                'nom_complet': 'Commerce et Distribution',
                'poids_pib': 14.2,
                'croissance': 3.8,
                'emplois': 52000,
                'couleur': '#6f42c1',
                'description': 'Grande distribution, commerce de détail',
                'entreprises_cles': ['Carrefour', 'Leader Price', 'Jumbo', 'Run Market'],
                'perspectives': 'Stable'
            },
            'Services Publics': {
                'nom_complet': 'Services Publics et Administration',
                'poids_pib': 22.1,
                'croissance': 1.2,
                'emplois': 68000,
                'couleur': '#0055A4',
                'description': 'Administration, éducation, santé publique',
                'entreprises_cles': ['ARS', 'Rectorat', 'Conseil Départemental', 'Conseil Régional'],
                'perspectives': 'Stable'
            },
            'Énergie': {
                'nom_complet': 'Énergie et Environnement',
                'poids_pib': 5.8,
                'croissance': 12.4,
                'emplois': 8500,
                'couleur': '#FFD100',
                'description': 'Énergies renouvelables, transition écologique',
                'entreprises_cles': ['EDF', 'Albioma', 'Akuo Energy', 'SIDELEC'],
                'perspectives': 'Très positives'
            },
            'Numérique': {
                'nom_complet': 'Numérique et Télécoms',
                'poids_pib': 4.2,
                'croissance': 9.7,
                'emplois': 6200,
                'couleur': '#00A3E0',
                'description': 'Télécommunications, services numériques',
                'entreprises_cles': ['Orange', 'SFR', 'Zeop', 'Runware'],
                'perspectives': 'Très positives'
            },
            'Industrie': {
                'nom_complet': 'Industrie et Transformation',
                'poids_pib': 7.3,
                'croissance': 4.5,
                'emplois': 12500,
                'couleur': '#8B4513',
                'description': 'Agroalimentaire, BTP, énergie',
                'entreprises_cles': ['Sofraca', 'Bourbon', 'Groupe Quartier Français'],
                'perspectives': 'Modérément positives'
            }
        }
    
    def initialize_economic_data(self):
        """Initialise les données économiques historiques"""
        # Correction: Utilisation de 'ME' au lieu de 'M'
        dates = pd.date_range('2014-01-01', datetime.now(), freq='ME')
        data = []
        
        for date in dates:
            # Données économiques de base avec tendances réalistes
            pib_base = 20.5  # Milliards EUR
            croissance_base = 2.8  # %
            
            # Impact COVID (2020-2021)
            if date.year == 2020:
                covid_impact = random.uniform(-0.08, -0.03)  # -3% à -8%
            elif date.year == 2021:
                covid_impact = random.uniform(-0.02, 0.02)   # -2% à +2%
            else:
                covid_impact = random.uniform(0.02, 0.06)    # +2% à +6%
            
            inflation = random.uniform(1.5, 4.0)
            chomage = random.uniform(18.0, 24.0)  # Taux de chômage structurellement élevé
            
            data.append({
                'date': date,
                'pib_mensuel': pib_base * (1 + croissance_base/100) ** ((date.year-2014)*12 + date.month-1),
                'croissance_pib': croissance_base + covid_impact * 100,
                'inflation': inflation,
                'taux_chomage': chomage,
                'revenu_median': random.uniform(1800, 2200),
                'exportations': random.uniform(0.3, 0.6),  # Milliards EUR
                'importations': random.uniform(4.5, 5.5),  # Milliards EUR
                'balance_commerciale': random.uniform(-4.8, -4.2)  # Déficit structurel
            })
        
        return pd.DataFrame(data)
    
    def initialize_tourism_data(self):
        """Initialise les données touristiques"""
        # Correction: Utilisation de 'ME' au lieu de 'M'
        dates = pd.date_range('2014-01-01', datetime.now(), freq='ME')
        data = []
        
        for date in dates:
            # Saisonnalité touristique très marquée
            if date.month in [7, 8, 12, 1]:  # Haute saison (été austral + Noël)
                base_touristes = 120000
            elif date.month in [2, 3, 9, 10]:   # Moyenne saison
                base_touristes = 80000
            else:                               # Basse saison
                base_touristes = 50000
            
            # Impact COVID très fort sur le tourisme
            if date.year == 2020 or (date.year == 2021 and date.month <= 6):
                covid_factor = random.uniform(0.02, 0.08)  # 2-8% de la normale
            elif date.year == 2021:
                covid_factor = random.uniform(0.2, 0.4)    # 20-40% de la normale
            elif date.year == 2022:
                covid_factor = random.uniform(0.6, 0.8)    # 60-80% de la normale
            else:
                covid_factor = random.uniform(0.9, 1.1)    # Retour à la normale
            
            touristes = base_touristes * covid_factor
            recettes = touristes * random.uniform(1500, 2200)  # Dépense moyenne par touriste
            
            data.append({
                'date': date,
                'arrivees_touristes': touristes,
                'recettes_tourisme': recettes,
                'duree_sejour_moyenne': random.uniform(10, 16),
                'taux_occupation_hotels': random.uniform(0.5, 0.85) * covid_factor,
                'principaux_marches': random.choice(['France Métropolitaine', 'Mayotte', 'Maurice', 'Afrique du Sud'])
            })
        
        return pd.DataFrame(data)
    
    def initialize_agriculture_data(self):
        """Initialise les données agricoles"""
        # Correction: Utilisation de 'ME' au lieu de 'M'
        dates = pd.date_range('2014-01-01', datetime.now(), freq='ME')
        produits = ['Canne à sucre', 'Fruits tropicaux', 'Viande bovine', 'Lait', 'Légumes', 'Fleurs']
        
        data = []
        for date in dates:
            # Production saisonnière
            if date.month in [7, 8, 9]:  # Saison sèche
                production_factor = 0.8
            elif date.month in [1, 2, 3]:  # Saison des pluies
                production_factor = 1.2
            else:
                production_factor = 1.0
            
            data.append({
                'date': date,
                'production_canne_tonnes': random.uniform(1500000, 1800000) * production_factor,
                'production_fruits_tonnes': random.uniform(50000, 80000) * production_factor,
                'production_viande_tonnes': random.uniform(4000, 6000),
                'prix_sucre_tonne': random.uniform(400, 600),
                'export_agricole': random.uniform(0.1, 0.3),  # Milliards EUR
                'produit_principal': random.choice(produits)
            })
        
        return pd.DataFrame(data)
    
    def initialize_energy_data(self):
        """Initialise les données énergétiques"""
        # Correction: Utilisation de 'ME' au lieu de 'M'
        dates = pd.date_range('2014-01-01', datetime.now(), freq='ME')
        data = []
        
        for date in dates:
            # Croissance des énergies renouvelables
            if date.year <= 2016:
                part_renouvelable = random.uniform(0.25, 0.35)
            elif date.year <= 2020:
                part_renouvelable = random.uniform(0.35, 0.45)
            else:
                part_renouvelable = random.uniform(0.45, 0.55)
            
            data.append({
                'date': date,
                'production_totale_mwh': random.uniform(250000, 350000),
                'part_renouvelable': part_renouvelable,
                'production_solaire': random.uniform(30000, 60000),
                'production_eolien': random.uniform(15000, 30000),
                'production_biomasse': random.uniform(40000, 80000),
                'production_hydraulique': random.uniform(20000, 40000),
                'importation_energie': random.uniform(0.05, 0.15)  # Milliards EUR
            })
        
        return pd.DataFrame(data)
    
    def initialize_demographic_data(self):
        """Initialise les données démographiques"""
        # Correction: Utilisation de 'YE' au lieu de 'Y' pour les données annuelles
        dates = pd.date_range('2014-01-01', datetime.now(), freq='YE')
        data = []
        
        population_base = 850000
        for date in dates:
            annee = date.year
            croissance_pop = random.uniform(0.8, 1.2)  # Croissance démographique forte
            
            data.append({
                'date': date,
                'population': population_base * (1 + croissance_pop/100) ** (annee - 2014),
                'taux_natalite': random.uniform(12.0, 15.0),
                'taux_mortalite': random.uniform(5.0, 6.5),
                'solde_migratoire': random.uniform(2000, 5000),
                'densite_population': random.uniform(330, 360),
                'population_jeune': random.uniform(32, 35),  # % < 25 ans
                'population_agee': random.uniform(12, 15)    # % > 65 ans
            })
        
        return pd.DataFrame(data)
    
    def update_live_data(self):
        """Met à jour les données en temps réel"""
        # Simulation de mises à jour économiques
        dernier_pib = self.economic_data.iloc[-1]['croissance_pib']
        nouvelle_croissance = dernier_pib + random.uniform(-0.1, 0.1)
        
        # Ajout de nouvelles données mensuelles si nécessaire
        derniere_date = self.economic_data['date'].max()
        if datetime.now() - derniere_date > timedelta(days=30):
            nouvelle_date = derniere_date + timedelta(days=30)
            
            nouvelle_ligne = {
                'date': nouvelle_date,
                'pib_mensuel': self.economic_data.iloc[-1]['pib_mensuel'] * (1 + nouvelle_croissance/100),
                'croissance_pib': nouvelle_croissance,
                'inflation': random.uniform(1.8, 3.5),
                'taux_chomage': random.uniform(19.0, 22.0),
                'revenu_median': random.uniform(1850, 2250),
                'exportations': random.uniform(0.35, 0.65),
                'importations': random.uniform(4.6, 5.4),
                'balance_commerciale': random.uniform(-4.7, -4.3)
            }
            
            self.economic_data = pd.concat([self.economic_data, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🌋 Dashboard Économique La Réunion</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="live-badge">🔴 DONNÉES ÉCONOMIQUES EN TEMPS RÉEL</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Surveillance et analyse des performances économiques de La Réunion**")
            st.markdown('<div class="reunion-flag"></div>', unsafe_allow_html=True)
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés économiques"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS ÉCONOMIQUES CLÉS</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques à partir des dernières données
        derniere_data = self.economic_data.iloc[-1]
        derniers_touristes = self.tourism_data.iloc[-1]
        derniere_demo = self.demographic_data.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Croissance du PIB",
                f"{derniere_data['croissance_pib']:.1f}%",
                f"{random.uniform(-0.3, 0.4):.1f}% vs trimestre précédent"
            )
        
        with col2:
            st.metric(
                "Taux de Chômage",
                f"{derniere_data['taux_chomage']:.1f}%",
                f"{random.uniform(-0.5, 0.3):.1f}% vs trimestre précédent",
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                "Arrivées Touristiques Mensuelles",
                f"{derniers_touristes['arrivees_touristes']:,.0f}",
                f"{random.randint(-3000, 8000):+,} vs mois précédent"
            )
        
        with col4:
            st.metric(
                "Population",
                f"{derniere_demo['population']:,.0f}",
                f"+{random.randint(4000, 8000):,} vs année précédente"
            )
    
    def create_economic_overview(self):
        """Crée la vue d'ensemble économique"""
        st.markdown('<h3 class="section-header">🏛️ VUE D\'ENSEMBLE ÉCONOMIQUE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Indicateurs Macro", "Secteurs Économiques", "Commerce Extérieur", "Démographie"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution du PIB
                fig = px.line(self.economic_data, 
                             x='date', 
                             y='croissance_pib',
                             title='Évolution de la Croissance du PIB (%)',
                             color_discrete_sequence=['#0055A4'])
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Inflation et chômage
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(
                    go.Scatter(x=self.economic_data['date'], y=self.economic_data['inflation'],
                              name="Inflation", line=dict(color='#EF4135')),
                    secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=self.economic_data['date'], y=self.economic_data['taux_chomage'],
                              name="Chômage", line=dict(color='#0055A4')),
                    secondary_y=True,
                )
                fig.update_layout(title_text="Inflation et Taux de Chômage")
                fig.update_yaxes(title_text="Inflation (%)", secondary_y=False)
                fig.update_yaxes(title_text="Chômage (%)", secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition du PIB par secteur
                secteur_data = []
                for secteur, info in self.secteurs.items():
                    secteur_data.append({
                        'secteur': secteur,
                        'poids_pib': info['poids_pib'],
                        'croissance': info['croissance'],
                        'emplois': info['emplois']
                    })
                
                df_secteurs = pd.DataFrame(secteur_data)
                fig = px.pie(df_secteurs, 
                            values='poids_pib', 
                            names='secteur',
                            title='Répartition du PIB par Secteur (%)',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Croissance par secteur
                fig = px.bar(df_secteurs, 
                            x='secteur', 
                            y='croissance',
                            title='Taux de Croissance par Secteur (%)',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution du commerce extérieur
                fig = px.line(self.economic_data, 
                             x='date', 
                             y=['exportations', 'importations'],
                             title='Évolution des Exportations et Importations (Milliards EUR)',
                             color_discrete_map={'exportations': '#28a745', 'importations': '#EF4135'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Balance commerciale structurellement déficitaire
                fig = px.area(self.economic_data, 
                             x='date', 
                             y='balance_commerciale',
                             title='Balance Commerciale (Milliards EUR)',
                             color_discrete_sequence=['#EF4135'])
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution démographique
                fig = px.line(self.demographic_data, 
                             x='date', 
                             y='population',
                             title='Évolution de la Population',
                             color_discrete_sequence=['#0055A4'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Structure par âge
                derniere_annee = self.demographic_data.iloc[-1]
                ages_data = {
                    'Tranche': ['0-25 ans', '25-65 ans', '65+ ans'],
                    'Pourcentage': [derniere_annee['population_jeune'], 
                                  100 - derniere_annee['population_jeune'] - derniere_annee['population_agee'],
                                  derniere_annee['population_agee']]
                }
                df_ages = pd.DataFrame(ages_data)
                fig = px.pie(df_ages, 
                            values='Pourcentage', 
                            names='Tranche',
                            title='Structure de la Population par Âge (%)',
                            color_discrete_sequence=['#0055A4', '#EF4135', '#FFD100'])
                st.plotly_chart(fig, use_container_width=True)
    
    def create_sectors_analysis(self):
        """Analyse détaillée par secteur"""
        st.markdown('<h3 class="section-header">🏢 ANALYSE PAR SECTEUR DÉTAILLÉE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Performance Secteurs", "Emploi par Secteur", "Entreprises Clés"])
        
        with tab1:
            # Sélection du secteur à analyser
            secteur_selectionne = st.selectbox("Sélectionnez un secteur:", 
                                             list(self.secteurs.keys()))
            
            if secteur_selectionne:
                info_secteur = self.secteurs[secteur_selectionne]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Poids dans le PIB",
                        f"{info_secteur['poids_pib']}%",
                        f"{random.uniform(-0.3, 0.4):.1f}% vs année précédente"
                    )
                
                with col2:
                    st.metric(
                        "Taux de Croissance",
                        f"{info_secteur['croissance']}%",
                        f"{random.uniform(-1, 1.5):.1f}% vs année précédente"
                    )
                
                with col3:
                    st.metric(
                        "Emplois Directs",
                        f"{info_secteur['emplois']:,}",
                        f"{random.randint(-500, 1500):+,} vs année précédente"
                    )
                
                st.markdown(f"**📋 Description:** {info_secteur['description']}")
                st.markdown(f"**🔮 Perspectives:** {info_secteur['perspectives']}")
                
                # Entreprises clés
                st.markdown("**🏢 Entreprises Clés:**")
                for entreprise in info_secteur['entreprises_cles']:
                    st.markdown(f"- {entreprise}")
        
        with tab2:
            # Emploi par secteur
            emploi_data = []
            for secteur, info in self.secteurs.items():
                emploi_data.append({
                    'secteur': secteur,
                    'emplois': info['emplois'],
                    'part_emploi_total': (info['emplois'] / sum([s['emplois'] for s in self.secteurs.values()])) * 100
                })
            
            df_emploi = pd.DataFrame(emploi_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(df_emploi, 
                            x='secteur', 
                            y='emplois',
                            title='Nombre d\'Emplois par Secteur',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.pie(df_emploi, 
                            values='part_emploi_total', 
                            names='secteur',
                            title='Répartition de l\'Emploi par Secteur (%)',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Carte des entreprises réunionnaises
            st.subheader("Carte des Principales Entreprises Réunionnaises")
            
            entreprises_data = []
            for secteur, info in self.secteurs.items():
                for entreprise in info['entreprises_cles']:
                    entreprises_data.append({
                        'entreprise': entreprise,
                        'secteur': secteur,
                        'chiffre_affaires_estime': random.uniform(5, 300),  # Millions EUR
                        'employes': random.randint(50, 3000),
                        'localisation': random.choice(['Saint-Denis', 'Saint-Pierre', 'Le Port', 'Saint-Paul', 'Saint-André'])
                    })
            
            df_entreprises = pd.DataFrame(entreprises_data)
            st.dataframe(df_entreprises, use_container_width=True)
    
    def create_tourism_analysis(self):
        """Analyse détaillée du tourisme"""
        st.markdown('<h3 class="section-header">🏖️ ANALYSE DU SECTEUR TOURISTIQUE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Performance Touristique", "Marchés Émetteurs", "Infrastructures"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Arrivées touristiques
                fig = px.line(self.tourism_data, 
                             x='date', 
                             y='arrivees_touristes',
                             title='Évolution des Arrivées Touristiques Mensuelles',
                             color_discrete_sequence=['#EF4135'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Recettes touristiques
                fig = px.line(self.tourism_data, 
                             x='date', 
                             y='recettes_tourisme',
                             title='Évolution des Recettes Touristiques (Millions EUR)',
                             color_discrete_sequence=['#0055A4'])
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Analyse des marchés émetteurs
            marches_data = {
                'Marché': ['France Métropolitaine', 'Mayotte', 'Maurice', 'Afrique du Sud', 'Europe', 'Autres'],
                'Part_Marché': [65, 12, 8, 5, 7, 3],
                'Croissance': [4.2, 8.7, 6.1, 12.3, 5.8, 9.4]
            }
            
            df_marches = pd.DataFrame(marches_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(df_marches, 
                            values='Part_Marché', 
                            names='Marché',
                            title='Répartition des Marchés Émetteurs (%)',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(df_marches, 
                            x='Marché', 
                            y='Croissance',
                            title='Croissance par Marché Émetteur (%)',
                            color='Croissance',
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Infrastructures Touristiques")
            
            infrastructures = [
                {'Type': 'Hôtels', 'Nombre': 125, 'Capacité': '15,000 chambres', 'Taux Occupation': '68%'},
                {'Type': 'Résidences de tourisme', 'Nombre': 85, 'Capacité': '3,200 appartements', 'Taux Occupation': '62%'},
                {'Type': 'Gîtes et meublés', 'Nombre': 1200, 'Capacité': '8,500 lits', 'Taux Occupation': '58%'},
                {'Type': 'Campings', 'Nombre': 25, 'Capacité': '1,200 emplacements', 'Taux Occupation': '72%'},
                {'Type': 'Restaurants', 'Nombre': 1800, 'Capacité': '85,000 couverts', 'Taux Occupation': '65%'},
            ]
            
            for infra in infrastructures:
                with st.expander(f"🏨 {infra['Type']} - {infra['Capacité']}"):
                    st.write(f"**Nombre:** {infra['Nombre']}")
                    st.write(f"**Taux d'occupation:** {infra['Taux Occupation']}")
                    st.write(f"**Tendance:** {random.choice(['En hausse', 'Stable', 'En baisse modérée'])}")
    
    def create_energy_analysis(self):
        """Analyse de la transition énergétique"""
        st.markdown('<h3 class="section-header">⚡ TRANSITION ÉNERGÉTIQUE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Mix Énergétique", "Énergies Renouvelables", "Projets"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution de la part renouvelable
                fig = px.line(self.energy_data, 
                             x='date', 
                             y='part_renouvelable',
                             title='Évolution de la Part des Énergies Renouvelables (%)',
                             color_discrete_sequence=['#28a745'])
                fig.update_layout(yaxis_tickformat='.0%')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Production par type d'énergie
                derniere_data = self.energy_data.iloc[-1]
                production_data = {
                    'Type': ['Solaire', 'Éolien', 'Biomasse', 'Hydraulique', 'Fossile'],
                    'Production': [
                        derniere_data['production_solaire'],
                        derniere_data['production_eolien'],
                        derniere_data['production_biomasse'],
                        derniere_data['production_hydraulique'],
                        derniere_data['production_totale_mwh'] - (derniere_data['production_solaire'] + 
                                                               derniere_data['production_eolien'] + 
                                                               derniere_data['production_biomasse'] + 
                                                               derniere_data['production_hydraulique'])
                    ]
                }
                
                df_production = pd.DataFrame(production_data)
                fig = px.pie(df_production, 
                            values='Production', 
                            names='Type',
                            title='Mix de Production Électrique',
                            color_discrete_sequence=['#FFD100', '#00A3E0', '#28a745', '#0055A4', '#6c757d'])
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Projets d'énergies renouvelables
            projets_energie = [
                {'Nom': 'Centrale photovoltaïque du Gol', 'Type': 'Solaire', 'Puissance': '10 MW', 'Avancement': '95%'},
                {'Nom': 'Parc éolien de Sainte-Rose', 'Type': 'Éolien', 'Puissance': '12 MW', 'Avancement': '75%'},
                {'Nom': 'Unité de méthanisation du Tampon', 'Type': 'Biomasse', 'Puissance': '5 MW', 'Avancement': '60%'},
                {'Nom': 'Centrale biomasse de Bois Rouge', 'Type': 'Biomasse', 'Puissance': '40 MW', 'Avancement': '85%'},
                {'Nom': 'Centrale hydroélectrique de Takamaka', 'Type': 'Hydraulique', 'Puissance': '7 MW', 'Avancement': '100%'},
            ]
            
            for projet in projets_energie:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{projet['Nom']}**")
                    st.write(f"Type: {projet['Type']} - {projet['Puissance']}")
                with col2:
                    st.write(f"Statut: {projet['Avancement']}")
                with col3:
                    progress = int(projet['Avancement'].replace('%', ''))
                    st.progress(progress/100)
        
        with tab3:
            st.subheader("Objectifs de Transition Énergétique")
            
            objectifs = {
                'Année': ['2020', '2023', '2025', '2030'],
                'Part_ENR': [35, 45, 60, 75],
                'Autonomie_energetique': [25, 35, 50, 65],
                'Reduction_GES': [15, 25, 40, 60]
            }
            
            df_objectifs = pd.DataFrame(objectifs)
            
            fig = px.line(df_objectifs, 
                         x='Année', 
                         y=['Part_ENR', 'Autonomie_energetique', 'Reduction_GES'],
                         title='Objectifs de Transition Énergétique (%)',
                         markers=True,
                         color_discrete_map={'Part_ENR': '#28a745', 'Autonomie_energetique': '#0055A4', 'Reduction_GES': '#EF4135'})
            st.plotly_chart(fig, use_container_width=True)
    
    def create_regional_analysis(self):
        """Analyse par micro-régions"""
        st.markdown('<h3 class="section-header">🗺️ ANALYSE PAR MICRO-RÉGIONS</h3>', 
                   unsafe_allow_html=True)
        
        # Données par micro-région
        micro_regions_data = {
            'Micro-région': ['Nord', 'Ouest', 'Sud', 'Est', 'Cirques'],
            'Population': [215000, 185000, 205000, 130000, 75000],
            'PIB_Regional': [6.2, 5.1, 4.8, 3.2, 1.2],
            'Taux_Chomage': [20.1, 22.5, 24.8, 26.2, 28.5],
            'Activite_Principale': ['Services/Admin', 'Tourisme/Commerce', 'Tourisme/Agriculture', 'Agriculture', 'Agriculture'],
            'Croissance': [3.2, 4.1, 3.8, 2.5, 1.8]
        }
        
        df_regions = pd.DataFrame(micro_regions_data)
        
        tab1, tab2, tab3 = st.tabs(["Carte Économique", "Spécialisations", "Développement Territorial"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # PIB par micro-région
                fig = px.bar(df_regions, 
                            x='Micro-région', 
                            y='PIB_Regional',
                            title='PIB par Micro-région (Milliards EUR)',
                            color='Micro-région',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Chômage par micro-région
                fig = px.bar(df_regions, 
                            x='Micro-région', 
                            y='Taux_Chomage',
                            title='Taux de Chômage par Micro-région (%)',
                            color='Taux_Chomage',
                            color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Spécialisations Régionales")
            
            specialisations = {
                'Nord': ['Administration', 'Services', 'Enseignement supérieur', 'Santé'],
                'Ouest': ['Tourisme balnéaire', 'Commerce', 'Immobilier', 'Services'],
                'Sud': ['Tourisme nature', 'Agriculture', 'Artisanat', 'Énergie renouvelable'],
                'Est': ['Agriculture', 'Pêche', 'Énergie', 'Industrie'],
                'Cirques': ['Agriculture de montagne', 'Tourisme rural', 'Artisanat', 'Produits locaux']
            }
            
            for region, specialites in specialisations.items():
                with st.expander(f"🏞️ {region}"):
                    for specialite in specialites:
                        st.markdown(f"- {specialite}")
        
        with tab3:
            st.subheader("Projets de Développement Territorial")
            
            projets_regionaux = [
                {'Nom': 'NEO Réunion', 'Région': 'Toute l\'île', 'Budget': '2.1 Md€', 'Échéance': '2030'},
                {'Nom': 'Tram-Train', 'Région': 'Nord-Ouest', 'Budget': '1.7 Md€', 'Échéance': '2028'},
                {'Nom': 'Pôle d\'excellence rural', 'Région': 'Cirques', 'Budget': '150 M€', 'Échéance': '2026'},
                {'Nom': 'Zone industrialo-portuaire', 'Région': 'Ouest', 'Budget': '300 M€', 'Échéance': '2027'},
                {'Nom': 'Pôle de compétitivité numérique', 'Région': 'Nord', 'Budget': '80 M€', 'Échéance': '2025'},
            ]
            
            for projet in projets_regionaux:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{projet['Nom']}**")
                    st.write(f"Région: {projet['Région']}")
                with col2:
                    st.write(f"Budget: {projet['Budget']}")
                with col3:
                    progress = random.randint(15, 65)
                    st.write(f"Progression: {progress}%")
                    st.progress(progress/100)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Filtres temporels
        st.sidebar.markdown("### 📅 Période d'analyse")
        date_debut = st.sidebar.date_input("Date de début", 
                                         value=datetime(2020, 1, 1))
        date_fin = st.sidebar.date_input("Date de fin", 
                                       value=datetime.now())
        
        # Filtres secteurs
        st.sidebar.markdown("### 🏢 Filtres sectoriels")
        secteurs_selectionnes = st.sidebar.multiselect(
            "Secteurs à afficher:",
            list(self.secteurs.keys()),
            default=list(self.secteurs.keys())[:4]
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=True)
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        
        # Bouton de rafraîchissement manuel
        if st.sidebar.button("🔄 Rafraîchir les données"):
            self.update_live_data()
            st.rerun()
        
        # Informations La Réunion
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🇫🇷 LA RÉUNION")
        st.sidebar.markdown("""
        **Informations Clés:**
        - Population: 865,000 habitants
        - Superficie: 2,512 km²
        - PIB: 20.5 milliards EUR
        - Croissance: 2.8%
        - Statut: Département et Région d'Outre-Mer
        """)
        
        # Comparaison avec autres DROM
        st.sidebar.markdown("### 🌴 COMPARAISON DROM")
        drom_comparison = {
            'Réunion': {'PIB/hab': 23700, 'Croissance': 2.8, 'Chômage': 21.5},
            'Martinique': {'PIB/hab': 24500, 'Croissance': 1.8, 'Chômage': 16.2},
            'Guadeloupe': {'PIB/hab': 22100, 'Croissance': 2.1, 'Chômage': 19.8},
            'Guyane': {'PIB/hab': 15300, 'Croissance': 3.5, 'Chômage': 23.1}
        }
        
        for territoire, data in drom_comparison.items():
            st.sidebar.metric(
                territoire,
                f"{data['PIB/hab']:,} EUR/hab",
                f"{data['Croissance']}% croissance"
            )
        
        return {
            'date_debut': date_debut,
            'date_fin': date_fin,
            'secteurs_selectionnes': secteurs_selectionnes,
            'auto_refresh': auto_refresh,
            'show_projections': show_projections
        }

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Mise à jour des données live
        self.update_live_data()
        
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📈 Économie", 
            "🏢 Secteurs", 
            "🏖️ Tourisme", 
            "⚡ Énergie", 
            "🗺️ Régions",
            "💡 Défis",
            "ℹ️ À Propos"
        ])
        
        with tab1:
            self.create_economic_overview()
        
        with tab2:
            self.create_sectors_analysis()
        
        with tab3:
            self.create_tourism_analysis()
        
        with tab4:
            self.create_energy_analysis()
        
        with tab5:
            self.create_regional_analysis()
        
        with tab6:
            st.markdown("## 💡 DÉFIS ET OPPORTUNITÉS")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎯 POINTS FORTS
                
                **💎 Atouts Naturels:**
                - Biodiversité exceptionnelle
                - Potentiel énergétique renouvelable important
                - Attractivité touristique forte
                
                **👨‍💼 Capital Humain:**
                - Population jeune et dynamique
                - Système éducatif développé
                - Couverture sociale complète
                
                **🏗️ Infrastructures:**
                - Équipements publics de qualité
                - Réseaux de communication modernes
                - Projets structurants (NEO, Tram-Train)
                """)
            
            with col2:
                st.markdown("""
                ### 🚨 DÉFIS STRUCTURELS
                
                **⚡ Économie:**
                - Taux de chômage structurellement élevé
                - Déficit commercial important
                - Dépendance aux transferts publics
                
                **🌍 Insularité:**
                - Éloignement et coûts de transport
                - Dépendance énergétique
                - Vulnérabilité aux aléas climatiques
                
                **🏞️ Environnement:**
                - Préservation de la biodiversité
                - Gestion des déchets et ressources
                - Adaptation au changement climatique
                """)
            
            st.markdown("""
            ### 📋 AXES STRATÉGIQUES
            
            1. **Transition Écologique:** Autonomie énergétique et économie verte
            2. **Innovation:** Développement du numérique et des filières d'excellence
            3. **Formation:** Adaptation des compétences aux besoins économiques
            4. **Connectivité:** Amélioration des liaisons régionales et internationales
            5. **Cohésion Sociale:** Réduction des inégalités territoriales
            """)
        
        with tab7:
            st.markdown("## 📋 À propos de ce dashboard")
            st.markdown("""
            Ce dashboard présente une analyse économique complète de La Réunion,
            département et région d'outre-mer français dans l'océan Indien.
            
            **Sources des données:**
            - INSEE Réunion
            - CEROM (Comptes Économiques Rapides de l'Outre-Mer)
            - IEDOM La Réunion
            - Observatoire du Tourisme de La Réunion
            - Région Réunion
            
            **Période couverte:**
            - Données historiques: 2014-2024
            - Analyses sectorielles détaillées
            - Projections et tendances
            
            **⚠️ Note:** 
            Les données présentées sont simulées pour la démonstration.
            Les données réelles sont disponibles sur les sites officiels des institutions.
            
            **🔒 Confidentialité:** 
            Toutes les données sensibles sont anonymisées.
            """)
            
            st.markdown("---")
            st.markdown("""
            **📞 Contact:**
            - INSEE Réunion: www.insee.fr
            - Région Réunion: www.regionreunion.com
            - Préfecture de La Réunion: www.reunion.gouv.fr
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(30)  # Rafraîchissement toutes les 30 secondes
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = ReunionDashboard()
    dashboard.run_dashboard()
