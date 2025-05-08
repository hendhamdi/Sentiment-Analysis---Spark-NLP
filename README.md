# 🧠 Analyse de Sentiments Étudiants - Spark NLP

Ce projet réalise une **analyse de sentiments** sur des avis d'étudiants du Master MP2L, à l'aide d'un pipeline de traitement de texte basé sur **Apache Spark (PySpark)** et un modèle de **régression logistique**.

---

## 🚀 Objectifs

- Automatiser la **classification des avis étudiants** (positif, neutre, négatif)
- Visualiser la répartition des sentiments de manière globale et par année
- Offrir une **interface web interactive** pour explorer les résultats dynamiquement


## 🔧 Technologies utilisées

- **Python 3**:  Langage principal du projet.
- **Apache Spark (PySpark)**: Framework de calcul distribué pour le traitement des données massives.
- **Flask** - Interface web
- **Spark MLlib** : Librairie de machine learning incluse dans Spark pour la régression logistique.
- **Hadoop** (configuration de `winutils.exe` nécessaire sous Windows)
- **Bibliothèques Python** :
  - `pyspark`
  - `pandas`
  - `matplotlib`
  - `PrettyTable`|


## 📂 Structure du Projet

```plaintext
sentiment-analysis-spark/
├── data/
│ └── avis_etudiants_dataset.csv # Dataset des avis
├── src/
│ ├── main.py # Script principal d'analyse
│ └── webapp/ # Interface Flask
│ ├── app.py
│ ├── static/
│ │ └── style.css
│ ├── templates/
│ │ └── index.html
│ └── images/
│ ├── uvt_logo.png
│ └── isi_logo.png
├── output/ # Résultats
│ ├── results.txt # Prédictions détaillées
│ ├── results.png # Graphique des sentiments
│ └── sentiments_par_annee.json # Données par année (pour l'interface)
└── README.md
 ``` 

## 🚀 Comment lancer le projet

1. **Analyse des données**:

```bash
python src/main.py
```
2. **Interface web**:

```bash
python src/webapp/app.py
```

## 📊 Résultats

- Précision du modèle : ~99%
- Prédictions (extrait) sauvegardées dans output/results.txt.
- Graphique global des sentiments généré automatiquement :

![Répartition des sentiments](https://github.com/hendhamdi/Sentiment-Analysis---Spark-NLP/blob/main/output/results.png)

- Répartition des sentiments par année : affichée sous forme de graphiques interactifs dans l'interface Flask.

## 📈 Fonctionnalités de l'interface web

- Visualisation globale de la répartition des sentiments
- Graphiques interactifs par année
- Affichage dynamique avec Chart.js
- Navigation fluide et design épuré


## 🚀 Améliorations futures

- Génération automatique de recommandations pédagogiques
- Authentification pour permettre la personnalisation des résultats

