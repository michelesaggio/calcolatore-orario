import streamlit as st

st.title("🕒 Calcolatore Orario di Lavoro")
st.write("Inserisci i dati della tua giornata per scoprire a che ora puoi andare via.")

arrivo = st.text_input("A che ora sei arrivato? (es. 08:00 o 8.00)", "08:00")
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
                st.warning("⚠️ L'orario di fine pausa precede quello di inizio! La pausa è stata considerata di 0 minuti.")
                durata_pausa = 0

            minuti_uscita = m_arrivo + 480 + durata_pausa
            ora_u = minuti_uscita // 60
            minuto_u = minuti_uscita % 60

            st.success(f"### 👉 Puoi andare via alle: {ora_u:02d}:{minuto_u:02d}")
            
            pausa_ore = durata_pausa // 60
            pausa_min = durata_pausa % 60
            st.info(f"**Riepilogo:** Pausa effettuata: {pausa_ore}h {pausa_min}m")

    except Exception as e:
        st.error(f"Si è verificato un errore: {e}")