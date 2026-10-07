import streamlit as st
import pandas as pd
import os
import urllib.request
from datetime import date

FILE_DATI = "storico_allenamenti.csv"
CARTELLA_IMMAGINI = "img_esercizi"

# Database con collegamenti diretti alle immagini di ogni esercizio
esercizi_db = {
    "Distensioni Manubri P. 30": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Incline_Dumbbell_Bench_Press/0.jpg"
    },
    "Chest Press": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Lever_Seated_Chest_Press/0.jpg"
    },
    "Pec Fly": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Lever_Pec_Deck_Fly/0.jpg"
    },
    "Croci Man. P. 30": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Incline_Dumbbell_Fly/0.jpg"
    },
    "Bicipiti Manubri Alt. P. 70": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Incline_Dumbbell_Curl/0.jpg"
    },
    "Bicipiti Cavo Basso Asta D.": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Cable_Curl/0.jpg"
    },
    "Plank": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Plank/0.jpg"
    },
    "Crunch su Panca": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Crunch/0.jpg"
    },
    "Leg Press 45": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Sled_45_Degree_Leg_Press/0.jpg"
    },
    "Leg Extension": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Lever_Leg_Extension/0.jpg"
    },
    "Leg Curl": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Lever_Lying_Leg_Curl/0.jpg"
    },
    "Calf Press": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Calf_Raise_on_Leg_Press/0.jpg"
    },
    "Triceps Press": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Lever_Overhead_Triceps_Extension/0.jpg"
    },
    "Push Down Asta": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Cable_Pushdown/0.jpg"
    },
    "Crunch Obliqui Panca": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Cross_Body_Crunch/0.jpg"
    },
    "Lat Machine Avanti": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Cable_Lat_Pulldown/0.jpg"
    },
    "Seated Row": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Cable_Seated_Row/0.jpg"
    },
    "Shoulder Press": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Dumbbell_Shoulder_Press/0.jpg"
    },
    "Rear Delt": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Lever_Seated_Rear_Lateral_Raise/0.jpg"
    },
    "Alzate Laterali P. 90": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Dumbbell_Lateral_Raise/0.jpg"
    },
    "Reverse Crunch Panca": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Reverse_Crunch/0.jpg"
    }
}

# Funzione per caricare lo storico CSV
def carica_dati():
    if os.path.exists(FILE_DATI):
        return pd.read_csv(FILE_DATI)
    else:
        return pd.DataFrame(columns=["Data", "Seduta", "Esercizio", "Serie", "Ripetizioni", "Carico (kg)", "Note"])

# Configurazione pagina Streamlit
st.set_page_config(page_title="Diario Allenamento Ipertrofia", layout="wide")
st.title("💪 Diario Allenamento - Massa Muscolare")

# Sidebar per il download offline opzionale
with st.sidebar:
    st.header("Opzioni")
    if st.button("📥 Scarica immagini per uso Offline"):
        if not os.path.exists(CARTELLA_IMMAGINI):
            os.makedirs(CARTELLA_IMMAGINI)
        progress_bar = st.progress(0)
        totale = len(esercizi_db)
        for idx, (nome_ex, info) in enumerate(esercizi_db.items()):
            nome_file = nome_ex.replace(" ", "_") + ".jpg"
            percorso_file = os.path.join(CARTELLA_IMMAGINI, nome_file)
            if not os.path.exists(percorso_file):
                try:
                    urllib.request.urlretrieve(info["url"], percorso_file)
                except Exception:
                    pass
            progress_bar.progress((idx + 1) / totale)
        st.success("Tutte le immagini sono state salvate in locale!")

# Selezione della seduta
elenco_sedute = sorted(list(set(info["seduta"] for info in esercizi_db.values())))
seduta_selezionata = st.selectbox("Seleziona la Seduta", elenco_sedute)

# Filtraggio esercizi per la seduta scelta
esercizi_disponibili = [nome for nome, info in esercizi_db.items() if info["seduta"] == seduta_selezionata]

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Registra Esercizio")
    data_allenamento = st.date_input("Data", date.today())
    esercizio_selezionato = st.selectbox("Esercizio", esercizi_disponibili)
    
    serie = st.number_input("Serie completate", min_value=1, max_value=10, value=4)
    ripetizioni = st.text_input("Ripetizioni eseguite (es. 10-10-8-8)", "10")
    carico = st.number_input("Carico Utilizzato (kg)", min_value=0.0, step=1.0)
    note = st.text_area("Note (es. 'Ottima esecuzione, aumentare peso proxima volta')")
    
    if st.button("Salva Allenamento"):
        df = carica_dati()
        nuovo_dato = pd.DataFrame([{
            "Data": data_allenamento,
            "Seduta": seduta_selezionata,
            "Esercizio": esercizio_selezionato,
            "Serie": serie,
            "Ripetizioni": ripetizioni,
            "Carico (kg)": carico,
            "Note": note
        }])
        df = pd.concat([df, nuovo_dato], ignore_index=True)
        df.to_csv(FILE_DATI, index=False)
        st.success(f"Dati salvati per: {esercizio_selezionato}")

with col2:
    st.header("Esecuzione Esercizio")
    nome_immagine_locale = esercizio_selezionato.replace(" ", "_") + ".jpg"
    percorso_locale = os.path.join(CARTELLA_IMMAGINI, nome_immagine_locale)
    
    # Priorità all'immagine locale se presente, altrimenti carica dall'URL online
    if os.path.exists(percorso_locale):
        st.image(percorso_locale, caption=f"{esercizio_selezionato} (Locale)", use_column_width=True)
    elif esercizio_selezionato in esercizi_db:
        url_immagine = esercizi_db[esercizio_selezionato]["url"]
        st.image(url_immagine, caption=f"{esercizio_selezionato} (Online)", use_column_width=True)

st.markdown("---")
st.header("📊 Storico Progressioni")
df_storico = carica_dati()
if not df_storico.empty:
    st.dataframe(df_storico.sort_values(by="Data", ascending=False), use_container_width=True)
else:
    st.info("Nessun dato registrato. Inizia a tracciare i tuoi carichi!")