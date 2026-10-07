import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO
from datetime import date

FILE_DATI = "storico_allenamenti.csv"
CARTELLA_IMMAGINI = "img_esercizi"

esercizi_db = {
    "Distensioni Manubri P. 30": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600"
    },
    "Chest Press": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600"
    },
    "Pec Fly": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600"
    },
    "Croci Man. P. 30": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600"
    },
    "Bicipiti Manubri Alt. P. 70": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600"
    },
    "Bicipiti Cavo Basso Asta D.": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600"
    },
    "Plank": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=600"
    },
    "Crunch su Panca": {
        "seduta": "Seduta 1: Petto e Bicipiti",
        "url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600"
    },
    "Leg Press 45": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600"
    },
    "Leg Extension": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600"
    },
    "Leg Curl": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600"
    },
    "Calf Press": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600"
    },
    "Triceps Press": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600"
    },
    "Push Down Asta": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600"
    },
    "Crunch Obliqui Panca": {
        "seduta": "Seduta 2: Gambe e Tricipiti",
        "url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600"
    },
    "Lat Machine Avanti": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600"
    },
    "Seated Row": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600"
    },
    "Shoulder Press": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600"
    },
    "Rear Delt": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600"
    },
    "Alzate Laterali P. 90": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600"
    },
    "Reverse Crunch Panca": {
        "seduta": "Seduta 3: Dorso e Spalle",
        "url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600"
    }
}

def carica_dati():
    if os.path.exists(FILE_DATI):
        return pd.read_csv(FILE_DATI)
    else:
        return pd.DataFrame(columns=["Data", "Seduta", "Esercizio", "Serie", "Ripetizioni", "Carico (kg)", "Note"])

def mostra_immagine(url_o_percorso, didascalia):
    try:
        if os.path.exists(url_o_percorso):
            st.image(url_o_percorso, caption=didascalia, use_container_width=True)
        else:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url_o_percorso, headers=headers, timeout=5)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=didascalia, use_container_width=True)
    except Exception:
        st.info("Immagine non disponibile al momento.")

st.set_page_config(page_title="Diario Allenamento Ipertrofia", layout="wide")
st.title("💪 Diario Allenamento - Massa Muscolare")

elenco_sedute = sorted(list(set(info["seduta"] for info in esercizi_db.values())))
seduta_selezionata = st.selectbox("Seleziona la Seduta", elenco_sedute)

esercizi_disponibili = [nome for nome, info in esercizi_db.items() if info["seduta"] == seduta_selezionata]

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Registra Esercizio")
    data_allenamento = st.date_input("Data", date.today())
    esercizio_selezionato = st.selectbox("Esercizio", esercizi_disponibili)
    
    serie = st.number_input("Serie completate", min_value=1, max_value=10, value=4)
    ripetizioni = st.text_input("Ripetizioni eseguite (es. 10-10-8-8)", "10")
    carico = st.number_input("Carico Utilizzato (kg)", min_value=0.0, step=1.0)
    note = st.text_area("Note (es. 'Buon pump, nessuna vertigine')")
    
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
    
    if os.path.exists(percorso_locale):
        mostra_immagine(percorso_locale, f"{esercizio_selezionato} (Locale)")
    elif esercizio_selezionato in esercizi_db:
        url_immagine = esercizi_db[esercizio_selezionato]["url"]
        mostra_immagine(url_immagine, f"{esercizio_selezionato}")

st.markdown("---")
st.header("📊 Storico Progressioni")
df_storico = carica_dati()
if not df_storico.empty:
    st.dataframe(df_storico.sort_values(by="Data", ascending=False), use_container_width=True)
else:
    st.info("Nessun dato registrato.")
