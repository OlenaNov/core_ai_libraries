#Traccia: nella pagina del chatbot aggiungi una barra laterale con un menu a tendina per scegliere la personalità (libraio cordiale, maestro per bambini, esperto sintetico). 
# L'istruzione di sistema deve cambiare in base alla scelta. 
# Aggiungi anche il contatore dei messaggi e un pulsante per scaricare la conversazione come file di testo. 
# Prova a fare la stessa domanda con due personalità diverse.

import streamlit as st

from gemini_utils import chiedi

PERSONALITA = {
    "Libraio cordiale": (
        "Sei il libraio di una libreria. "
        "Rispondi in italiano in massimo tre frasi, con tono cordiale e professionale."
    ),
    "Maestro per bambini": (
        "Sei un maestro paziente. Rispondi in italiano con parole semplici, "
        "come a un bambino di dieci anni, in massimo tre frasi."
    ),
    "Esperto sintetico": (
        "Sei un esperto di libri e letteratura. "
        "Rispondi in italiano con una sola frase, precisa e senza giri di parole."
    ),
}


def costruisci_testo(cronologia):
    righe = []
    for messaggio in cronologia:
        if messaggio["role"] == "user":
            righe.append("Tu: " + messaggio["content"])
        else:
            righe.append("Bot: " + messaggio["content"])
    return "\n".join(righe)


st.title("Chatbot con personalità")

if "cronologia" not in st.session_state:
    st.session_state.cronologia = []

nome_personalita = st.sidebar.selectbox(
    "Scegli la personalità",
    list(PERSONALITA.keys())
)
istruzione = PERSONALITA[nome_personalita]

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

    risposta = chiedi(st.session_state.cronologia, istruzione)

    if risposta is None:
        risposta = "Al momento non riesco a rispondere. Riprova tra qualche minuto."

    st.session_state.cronologia.append({"role": "assistant", "content": risposta})
    with st.chat_message("assistant"):
        st.write(risposta)

st.sidebar.write("Messaggi nella conversazione:", len(st.session_state.cronologia))

if len(st.session_state.cronologia) > 0:
    st.sidebar.download_button(
        "Scarica la conversazione",
        data=costruisci_testo(st.session_state.cronologia),
        file_name="conversazione.pdf"
    )


