# Traccia: trasforma la pagina in un vero chatbot. Deve mostrare tutta la conversazione, 
# inviare a Gemini l'intera cronologia a ogni messaggio (così ricorda cosa si è detto) e 
# avere un pulsante per ricominciare da capo. Prova a scrivere "Mi chiamo Luca" e 
# poi "Come mi chiamo?"

# streamlit run chatbot_conversation_history_streamlit.py

import streamlit as st

from gemini_utils import chiedi

ISTRUZIONE = (
    "Sei l'assistente virtuale di una libreria."
    "Rispondi in italiano in massimo tre frasi, con tono cordiale"
)

st.title("Benvenuto nel mondo dei Chatbot virtuali")

if "cronologia" not in st.session_state:
    st.session_state.cronologia = []

if st.sidebar.button("Nuova conversazione"):
    st.session_state.cronologia = []
    st.rerun()

for messaggio in st.session_state.cronologia:
    with st.chat_message(messaggio["role"]):
        st.write(messaggio["content"])

domanda = st.chat_input("Scrivi un messaggio")

if domanda:
    st.session_state.cronologia.append({"role": "user", "content": domanda})
    with st.chat_message("user"):
        st.write(domanda)

    risposta = chiedi(st.session_state.cronologia, ISTRUZIONE)

    if risposta is None:
        risposta = "Al momento non riesco a rispondere. Riprova tra qualche minuto."

    st.session_state.cronologia.append({"role": "assistant", "content": risposta})
    with st.chat_message("assistant"):
        st.write(risposta)