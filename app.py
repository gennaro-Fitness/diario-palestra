import streamlit as st
import pandas as pd
import os
import time
from datetime import date

FILE_DATI = "storico_allenamenti.csv"

# Database essenziale degli esercizi suddivisi per seduta
esercizi_db = {
    # SEDUTA 1: PETTO E BICIPITI
    "Distensioni Manubri P. 30": "Seduta 1: Petto e Bicipiti",
    "Chest Press": "Seduta 1: Petto e Bicipiti",
    "Pec Fly": "Seduta 1: Petto e Bicipiti",
    "Croci Man. P. 30": "Seduta 1: Petto e Bicipiti",
    "Bicipiti Manubri Alt. P. 70": "Seduta 1: Petto e Bicipiti",
    "Bicipiti Cavo Basso Asta D.": "Seduta 1: Petto e Bicipiti",
    "Plank": "Seduta 1: Petto e Bicipiti",
    "Crunch su Panca": "Seduta 1: Petto e Bicipiti",

    # SEDUTA 2: GAMBE E TRICIPITI
    "Leg Press 45": "Seduta 2: Gambe e Tricipiti",
    "Leg Extension": "Seduta 2: Gambe e Tricipiti",
    "Leg Curl": "Seduta 2: Gambe e Tricipiti",
    "Calf Press": "Seduta 2: Gambe e Tricipiti",
    "Triceps Press": "Seduta 2: Gambe e Tricipiti",
    "Push Down Asta": "Seduta 2: Gambe e Tricipiti",
    "Crunch Obliqui Panca": "Seduta 2: Gambe e Tricipiti",

    # SEDUTA 3: DORSO E SPALLE
    "Lat Machine Avanti": "Seduta 3: Dorso e Spalle",
    "Seated Row": "Seduta 3: Dorso e Spalle",
    "Shoulder Press": "Seduta 3: Dorso e Spalle",
    "Rear Delt": "Seduta 3: Dorso e Spalle",
    "Alzate Laterali P. 90": "Seduta 3: Dorso e Spalle",
    "Reverse Crunch Panca": "Seduta 3: Dorso e Spalle"
}

def carica_dati():
    if os.path.exists(FILE_DATI):
        return pd.read_csv(FILE_DATI)
    else:
        return pd.DataFrame(columns=["Data", "Seduta", "Esercizio", "Serie", "Ripetizioni", "Carico (kg)", "Note"])

st.set_page_config(page_title="Diario Allenamento Ipertrofia", layout="wide")

tab1, tab2 = st.tabs(["🏋️ Registra & Timer", "📊 Dashboard Statistiche"])

with tab1:
    st.title("💪 Diario Allenamento & Recupero")
    
    # Timer di Recupero Integrato
    with st.expander("⏱️ Timer di Recupero Serie", expanded=True):
        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            secondi_recupero = st.selectbox("Seleziona Recupero (secondi)", [60, 90, 120, 150, 180], index=2)
            avvia_timer = st.button("▶️ Avvia Timer")
        with col_t2:
            placeholder_timer = st.empty()
            if avvia_timer:
                for secondi in range(secondi_recupero, -1, -1):
                    mins, secs = divmod(secondi, 60)
                    placeholder_timer.metric("Tempo Rimanente", f"{mins:02d}:{secs:02d}")
                    time.sleep(1)
                placeholder_timer.success("🔔 Tempo di recupero terminato! Pronto per la prossima serie.")

    st.markdown("---")
    
    elenco_sedute = sorted(list(set(esercizi_db.values())))
    seduta_selezionata = st.selectbox("Seleziona la Seduta", elenco_sedute)
    esercizi_disponibili = [nome for nome, seduta in esercizi_db.items() if seduta == seduta_selezionata]

    st.header("Registra Esercizio")
    c1, c2 = st.columns(2)
    with c1:
        data_allenamento = st.date_input("Data", date.today())
        esercizio_selezionato = st.selectbox("Esercizio", esercizi_disponibili)
        serie = st.number_input("Serie completate", min_value=1, max_value=10, value=4)
    with c2:
        ripetizioni = st.text_input("Ripetizioni eseguite (es. 10-10-8-8)", "10")
        carico = st.number_input("Carico Utilizzato (kg)", min_value=0.0, step=1.0)
        note = st.text_area("Note e sensazioni post-workout")
        
    if st.button("Salva Allenamento", use_container_width=True):
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

    st.markdown("---")
    st.header("📜 Registro Ultimi Allenamenti")
    df_storico = carica_dati()
    if not df_storico.empty:
        st.dataframe(df_storico.sort_values(by="Data", ascending=False), use_container_width=True)
    else:
        st.info("Nessun dato registrato. Inizia l'allenamento!")

with tab2:
    st.title("📈 Dashboard Analitica e Progressioni")
    df_storico = carica_dati()
    
    if not df_storico.empty:
        totale_sessioni = df_storico["Data"].nunique()
        totale_esercizi = len(df_storico)
        carico_max_assoluto = df_storico["Carico (kg)"].max()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Sessioni Totali", totale_sessioni)
        m2.metric("Esercizi Registrati", totale_esercizi)
        m3.metric("Record Carico Assoluto", f"{carico_max_assoluto} kg")
        
        st.markdown("---")
        st.subheader("📊 Progressione del Carico (kg) nel Tempo")
        
        tutti_esercizi = sorted(df_storico["Esercizio"].unique())
        ex_scelto = st.selectbox("Seleziona l'Esercizio da Analizzare", tutti_esercizi)
        
        df_ex = df_storico[df_storico["Esercizio"] == ex_scelto].copy()
        df_ex["Data"] = pd.to_datetime(df_ex["Data"])
        df_ex = df_ex.sort_values("Data")
        
        if not df_ex.empty:
            st.line_chart(data=df_ex, x="Data", y="Carico (kg)", use_container_width=True)
            
            st.subheader("🏆 Record Personale (PR)")
            pr_row = df_ex.loc[df_ex["Carico (kg)"].idxmax()]
            st.write(f"**Massimo Carico Sollevato:** {pr_row['Carico (kg)']} kg il {pr_row['Data'].strftime('%d/%m/%Y')} ({pr_row['Serie']} serie x {pr_row['Ripetizioni']} rep)")
        else:
            st.info("Nessun dato disponibile per questo esercizio.")
            
    else:
        st.info("Registra almeno un allenamento nella prima scheda per sbloccare la dashboard e i grafici!")
