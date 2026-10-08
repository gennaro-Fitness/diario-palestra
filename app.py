import streamlit as st
import pandas as pd
import os
import time
from datetime import date

FILE_DATI = "storico_allenamenti.csv"

# Database completo degli esercizi con parametri target previsti dalla scheda
esercizi_db = {
    # SEDUTA 1: PETTO E BICIPITI
    "Distensioni Manubri P. 30": {"seduta": "Seduta 1: Petto e Bicipiti", "serie": 4, "reps": "8", "recupero": 90},
    "Chest Press": {"seduta": "Seduta 1: Petto e Bicipiti", "serie": 4, "reps": "10", "recupero": 60},
    "Pec Fly": {"seduta": "Seduta 1: Petto e Bicipiti", "serie": 4, "reps": "10", "recupero": 60},
    "Croci Man. P. 30": {"seduta": "Seduta 1: Petto e Bicipiti", "serie": 3, "reps": "12", "recupero": 60},
    "Bicipiti Manubri Alt. P. 70": {"seduta": "Seduta 1: Petto e Bicipiti", "serie": 4, "reps": "10", "recupero": 60},
    "Bicipiti Cavo Basso Asta D.": {"seduta": "Seduta 1: Petto e Bicipiti", "serie": 4, "reps": "12", "recupero": 60},
    "Plank": {"seduta": "Seduta 1: Petto e Bicipiti", "serie": 4, "reps": "Max", "recupero": 60},
    "Crunch su Panca": {"seduta": "Seduta 1: Petto e Bicipiti", "serie": 3, "reps": "Max", "recupero": 60},

    # SEDUTA 2: GAMBE E TRICIPITI
    "Leg Press 45": {"seduta": "Seduta 2: Gambe e Tricipiti", "serie": 4, "reps": "10", "recupero": 90},
    "Leg Extension": {"seduta": "Seduta 2: Gambe e Tricipiti", "serie": 4, "reps": "10", "recupero": 60},
    "Leg Curl": {"seduta": "Seduta 2: Gambe e Tricipiti", "serie": 4, "reps": "12", "recupero": 60},
    "Calf Press": {"seduta": "Seduta 2: Gambe e Tricipiti", "serie": 3, "reps": "15", "recupero": 60},
    "Triceps Press": {"seduta": "Seduta 2: Gambe e Tricipiti", "serie": 4, "reps": "12", "recupero": 60},
    "Push Down Asta": {"seduta": "Seduta 2: Gambe e Tricipiti", "serie": 4, "reps": "12", "recupero": 60},
    "Crunch Obliqui Panca": {"seduta": "Seduta 2: Gambe e Tricipiti", "serie": 3, "reps": "Max", "recupero": 60},

    # SEDUTA 3: DORSO E SPALLE
    "Lat Machine Avanti": {"seduta": "Seduta 3: Dorso e Spalle", "serie": 4, "reps": "8", "recupero": 90},
    "Seated Row": {"seduta": "Seduta 3: Dorso e Spalle", "serie": 4, "reps": "10", "recupero": 60},
    "Pulley Stretto": {"seduta": "Seduta 3: Dorso e Spalle", "serie": 3, "reps": "10", "recupero": 60},
    "Shoulder Press": {"seduta": "Seduta 3: Dorso e Spalle", "serie": 4, "reps": "8", "recupero": 90},
    "Rear Delt": {"seduta": "Seduta 3: Dorso e Spalle", "serie": 4, "reps": "10", "recupero": 60},
    "Alzate Laterali P. 90": {"seduta": "Seduta 3: Dorso e Spalle", "serie": 3, "reps": "12", "recupero": 60},
    "Reverse Crunch Panca": {"seduta": "Seduta 3: Dorso e Spalle", "serie": 3, "reps": "Max", "recupero": 60}
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
    
    # Selezione della seduta e dell'esercizio
    elenco_sedute = sorted(list(set(d["seduta"] for d in esercizi_db.values())))
    seduta_selezionata = st.selectbox("Seleziona la Seduta", elenco_sedute)
    
    esercizi_disponibili = [nome for nome, info in esercizi_db.items() if info["seduta"] == seduta_selezionata]
    esercizio_selezionato = st.selectbox("Seleziona Esercizio", esercizi_disponibili)
    
    # Dati target dell'esercizio prescelto
    target = esercizi_db[esercizio_selezionato]
    
    # Scheda parametri consigliati
    st.info(f"📋 **Target Scheda per {esercizio_selezionato}:** {target['serie']} Serie | {target['reps']} Ripetizioni | Recupero: {target['recupero']} sec")

    # Timer di Recupero Integrato
    with st.expander("⏱️ Timer di Recupero Serie", expanded=True):
        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            # Preseleziona il recupero suggerito dalla scheda
            secondi_recupero = st.number_input("Recupero (secondi)", min_value=10, max_value=300, value=target["recupero"], step=10)
            avvia_timer = st.button("▶️ Avvia Timer", use_container_width=True)
        with col_t2:
            placeholder_timer = st.empty()
            if avvia_timer:
                for secondi in range(secondi_recupero, -1, -1):
                    mins, secs = divmod(secondi, 60)
                    placeholder_timer.metric("Tempo Rimanente", f"{mins:02d}:{secs:02d}")
                    time.sleep(1)
                placeholder_timer.success("🔔 Tempo di recupero terminato! Pronto per la prossima serie.")

    st.markdown("---")
    st.header("📝 Registra Allenamento")
    
    c1, c2 = st.columns(2)
    with c1:
        data_allenamento = st.date_input("Data", date.today())
        serie_eseguite = st.number_input("Serie completate", min_value=1, max_value=10, value=target["serie"])
    with c2:
        ripetizioni_eseguite = st.text_input("Ripetizioni eseguite (es. 10-10-8-8)", value=str(target["reps"]))
        carico = st.number_input("Carico Utilizzato (kg)", min_value=0.0, step=1.0)
        
    note = st.text_area("Note e sensazioni post-workout")
        
    if st.button("💾 Salva Allenamento", use_container_width=True):
        df = carica_dati()
        nuovo_dato = pd.DataFrame([{
            "Data": data_allenamento,
            "Seduta": seduta_selezionata,
            "Esercizio": esercizio_selezionato,
            "Serie": serie_eseguite,
            "Ripetizioni": ripetizioni_eseguite,
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
