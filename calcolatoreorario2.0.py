def leggi_orario(messaggio):
    while True:
        try:
            testo = input(messaggio).strip()
            if not testo:
                print("Inserisci un orario valido!")
                continue

            testo = testo.replace(".", ":").replace(",", ":")

            if ":" not in testo:
                testo += ":00"

            parti = testo.split(":")
            
            if len(parti) != 2:
                print("Formato non valido! Usa il formato con un punto o due punti.")
                continue

            if not parti[0].isdigit() or not parti[1].isdigit():
                print("Errore: inserisci solo numeri interi!")
                continue

            ore = int(parti[0])
            minuti = int(parti[1])

            if not (0 <= ore < 24 and 0 <= minuti < 60):
                print("Errore: orario inesistente! Le ore vanno da 0 a 23 e i minuti da 0 a 59.")
                continue

            return (ore * 60) + minuti

        except ValueError:
            print("Formato non valido! Usa il formato con un punto o due punti.")


minuti_arrivo_totali = leggi_orario("A che ora sei arrivato?: ")

minuti_lavoro_totali = 480

while True:
    minuti_inizio_pausa_totali = leggi_orario("A che ora hai iniziato pausa?: ")
    minuti_fine_pausa_totali = leggi_orario("A che ora hai finito pausa?: ")

    durata_pausa = minuti_fine_pausa_totali - minuti_inizio_pausa_totali

    if durata_pausa < 0:
        print("\nAttenzione: l'orario di fine pausa precede quello di inizio!")
        scelta = input("Vuoi reinserire gli orari della pausa? (si/no): ").strip().lower()

        if scelta in ('s', 'si', 'sì'):
            print("\nPerfetto, inseriscili di nuovo:\n")
            continue
        else:
            print("Ok, considero la pausa pari a 0 minuti.")
            durata_pausa = 0
            break
    else:
        break


minuti_uscita_totali = minuti_arrivo_totali + minuti_lavoro_totali + durata_pausa

ora_uscita = minuti_uscita_totali // 60
minuto_uscita = minuti_uscita_totali % 60


arrivo_str = f"{minuti_arrivo_totali // 60:02d}:{minuti_arrivo_totali % 60:02d}"
pausa_ore = durata_pausa // 60
pausa_min = durata_pausa % 60

print("\n")
print("Riepilogo giornata:")
print(f"- Arrivo: {arrivo_str}")
print(f"- Pausa effettuata: {pausa_ore}h {pausa_min}m")
print(f"- Puoi uscire alle: {ora_uscita:02d}:{minuto_uscita:02d}")
print("\n")