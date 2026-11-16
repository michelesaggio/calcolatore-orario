import streamlit as st

st.title("🕒 Calcolatore Orario di Lavoro - Versione Avanzata")
st.write("Personalizza le ore, gestisci le pause e tieni traccia della cronologia della giornata.")

if 'cronologia' not in st.session_state:
    st.session_state.cronologia = []

col1, col2 = st.columns(2)
with col1:
    arrivo = st.text_input("A che ora sei arrivato? (es. 08:00 o 8.00)", "08:00")
with col2:
    ore_lavoro_scelte = st.number_input("Ore di lavoro previste oggi", min_value=1.0, max_value=14.0, value=8.0, step=0.5)

minuti_lavoro_base = int(ore_lavoro_scelte * 60)

extra_minuti = st.number_input("Minuti extra o da recuperare (+ o -)", value=0, step=5, help="Usa un numero positivo per straordinari/recupero in più, negativo se devi fare meno ore.")

st.subheader("Gestione Pausa")
inizio_pausa = st.text_input("A che ora hai iniziato pausa? (es. 13:00)", "13:00")
fine_pausa = st.text_input("A che ora hai finito pausa? (es. 13:45)", "13:45")

if st.button("Calcola orario di uscita"):
    try:
        def parse_orario(testo):
            testo = testo.strip().replace(".", ":").replace(",", ":")
            if ":" not in testo:
                testo += ":00"
            parti = testo.split(":")
            if len(parti) != 2 or not parti[0].isdigit() or not parti[1].isdigit():
                return None
            ore, minuti = int(parti[0]), int(parti[1])
            if not (0 <= ore < 24 and 0 <= minuti < 60):
                return None
            return (ore * 60) + minuti

        m_arrivo = parse_orario(arrivo)
        m_iniz_p = parse_orario(inizio_pausa)
        m_fine_p = parse_orario(fine_pausa)

        if m_arrivo is None or m_iniz_p is None or m_fine_p is None:
            st.error("Errore: Formato orario non valido o inesistente (usa es. 08:00 o 8.30).")
        else:
            durata_pausa = m_fine_p - m_iniz_p
            
            if durata_pausa < 0:
                st.warning("⚠️ Attenzione: l'orario di fine pausa precede quello di inizio! La pausa è stata considerata di 0 minuti.")
                durata_pausa = 0

            minuti_uscita = m_arrivo + minuti_lavoro_base + durata_pausa + extra_minuti
            ora_u = minuti_uscita // 60
            minuto_u = minuti_uscita % 60

            arrivo_str = f"{m_arrivo // 60:02d}:{m_arrivo % 60:02d}"
            pausa_ore = durata_pausa // 60
            pausa_min = durata_pausa % 60
            uscita_str = f"{ora_u:02d}:{minuto_u:02d}"

            st.success(f"### 🥳 Puoi andare via alle: {uscita_str}")
            
            st.info(f"**Riepilogo:** Arrivo: {arrivo_str} | Pausa: {pausa_ore}h {pausa_min}m | Previste: {ore_lavoro_scelte}h")

            dettaglio_cronologia = f"Arrivo: {arrivo_str} | Lavoro: {ore_lavoro_scelte}h | Pausa: {pausa_ore}h{pausa_min}m | Uscita: {uscita_str}"
            st.session_state.cronologia.append(dettaglio_cronologia)

    except Exception as e:
        st.error(f"Si è verificato un errore: {e}")

if st.session_state.cronologia:
    st.divider()
    st.subheader("🗓️ Cronologia dei calcoli effettuati")
    for i, item in enumerate(reversed(st.session_state.cronologia), 1):
        st.text(f"{i}. {item}")
    
    if st.button("Pulisci cronologia"):
        st.session_state.cronologia = []
        st.rerun()
