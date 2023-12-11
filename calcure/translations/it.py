"""Italian translations of the program interface"""

MSG_WELCOME_1 = "Benvenuto in Calcure"
MSG_WELCOME_2 = "Il tuo calendario da terminale e gestore di attività!"
MSG_WELCOME_3 = "File di dati e di configurazione creati al:"
MSG_WELCOME_4 = "Per ulteriore supporto, per contribuire e per avere informazioni aggiuntive, visitare:"
MSG_WELCOME_5 = "Premi ? per visualizzare tutte le scorciatoie da tastiera o qualunque altro tasto per continuare."

TITLE_KEYS_GENERAL = "SCORCIATOIE DA TASTIERA GENERALI"
TITLE_KEYS_CALENDAR = "SCORCIATOIE DA TASTIERA PER IL CALENDARIO"
TITLE_KEYS_JOURNAL  = "SCORCIATOIE DA TASTIERA PER IL DIARIO"

KEYS_GENERAL = {
        " Barra spaziatrice ": "Cambia fra calendario e diario",
        "   /   ": "Attiva la divisione dello schermo",
        "   *   ": "Attiva la privacy globale",
        "   ?   ": "Aiuto",
        "   Q   ": "Reload",
        "   q   ": "Esci",
        }

KEYS_CALENDAR = {
        "  a(A) ": "Aggiungi un evento (ricorrente)",
        "   n   ": "Mese successivo (giorno)",
        "   p   ": "Mese precedente (giorno)",
        "   x   ": "Cancella un evento",
        "   r   ": "Modifica un evento",
        "  m(M) ": "Sposta un evento",
        "   v   ": "Alterna la visualizzazione giornaliera/mensile",
        "  g(G) ": "Vai ad un determinato giorno",
        "   h   ": "Imposta un evento come ad alta priorità",
        "   l   ": "Imposta un evento come a bassa priorità",
        "   d   ": "Imposta un evento come fatto",
        "   .   ": "Imposta la privacy per un evento",
        "   C   ": "Importa eventi da calcurse",
        "   R   ": "Ritorna al mese corrente (giorno)",
        }

KEYS_TODO = {
        "  a(A) ": "Aggiungi una nuova (sotto)attività",
        "  h(H) ": "Imposta una fra (o tutte) le attività come ad alta priorità",
        "  l(L) ": "Imposta una fra (o tutte) le attività come a bassa priorità",
        "  d(D) ": "Imposta una fra (o tutte) le attività come completate",
        "  u(U) ": "Deseleziona una fra (o tutte) le attività",
        "  x(X) ": "Cancella una fra (o tutte) le attività (con tutte le sue sottoattività)",
        "  t(T) ": "Avvia/ferma (o cancella) il timer per una attività",
        "   r   ": "Modifica una attività",
        "   s   ": "Passa da attività a sottoattività (e viceversa)",
        "   .   ": "Imposta la privacy dell'attività",
        "  f(F) ": "Cambia (o rimuovi) la scadenza per una attività",
        "   m   ": "Sposta una attività",
        "  C(W) ": "Importa le attività da calcurse (taskwarrior)",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "È possibile usare i tasti di Vim (j, k, ZZ, ZQ)!"
MSG_INFO          = "Per maggiori informazioni, visitare:"
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "Vuoi davvero uscire? (y/n) "

MSG_EVENT_HIGH    = "Imposta ad alta priorità l'evento con numero: "
MSG_EVENT_LOW     = "Imposta come a bassa priorità l'evento con numero: "
MSG_EVENT_DONE    = "Mark as done event number: "
MSG_EVENT_RESET   = "Ripristina lo stato per l'evento con numero: "
MSG_EVENT_DEL     = "Cancella l'evento con numero: "
MSG_EVENT_REN     = "Rinomina l'evento con numero: "
MSG_NEW_TITLE     = "Inserisci il nuovo titolo: "
MSG_EVENT_MV      = "Sposta l'evento con numero: "
MSG_EVENT_MV_TO   = "Postponi l'evento a (YYYY/MM/DD): "
MSG_EVENT_MV_TO_D = "Postponi l'evento a: "
MSG_EVENT_DATE    = "Inserisci una data: "
MSG_EVENT_TITLE   = "Inserisci un titolo: "
MSG_EVENT_REP     = "Quante volte vuoi ripetere l'evento: "
MSG_EVENT_FR      = "Ripetere l'evento ogni giorno(d), settimana(w), mese(m) o anno(y)? "
MSG_EVENT_IMP     = "Vuoi importare un evento da Calcurse? (y/n)"
MSG_EVENT_PRIVACY = "Attiva la privacy dell'evento con numero: "
MSG_TM_ADD        = "Avvia/ferma il timer per l'attività con numero: "
MSG_TM_RESET      = "Rimuovi il timer per l'attività con numero: "
MSG_TS_HIGH       = "Imposta come ad alta priorità l'attività con numero: "
MSG_TS_LOW        = "Imposta come a bassa priorità l'attività con numero: "
MSG_TS_RES        = "Ripristina lo stato per l'attività con numero: "
MSG_TS_DONE       = "Segna come completata l'attività con numero: "
MSG_TS_DEL        = "Cancella l'attività con numero: "
MSG_TS_DEL_ALL    = "Vuoi davvero cancellare tutte le attività? (y/n)"
MSG_TS_EDT_ALL    = "Do you confirm this action? (y/n)"
MSG_TS_MOVE       = "Sposta il task dal numero: "
MSG_TS_MOVE_TO    = "Sposta il task al numero: "
MSG_TS_EDIT       = "Modifica il numero dell'attività: "
MSG_TS_TOG        = "Attiva la sottoattività con numero: "
MSG_TS_SUB        = "Aggiungi una sottoattività all'attività con numero: "
MSG_TS_TITLE      = "Inserisci la sottoattività: "
MSG_TS_IM         = "Vuoi importare le attività da Calcurse? (y/n)"
MSG_TS_TW         = "Vuoi importare le attività da Taskwarrior? (y/n)"
MSG_TS_NOTHING    = "Nulla di pianificato..."
MSG_TS_PRIVACY    = "Attiva la privacy dell'attività con numero: "
MSG_TS_DEAD_ADD   = "Aggiungi una scadenza per l'attività con numero: "
MSG_TS_DEAD_DEL   = "Rimuovi la scadenza per l'attività con numero: "
MSG_TS_DEAD_DATE  = "Aggiungi una scandeza per il (AAAA/MM/GG): "
MSG_WEATHER       = "Caricamento del meteo..."
MSG_ERRORS        = "Errors have occurred. See info.log file in your config folder."
MSG_GOTO          = "Vai alla data (YYYY/MM/DD): "
MSG_GOTO_D        = "Vai alla data: "
MSG_INPUT         = "Inserimento errato."

CALENDAR_HINT     = "Barra spaziatrice · Passa al diario   a · Aggiungi un evento  n/p · Cambia mese   ? · Mostra tutte le scorciatoie"
CALENDAR_HINT_D   = "Barra spaziatrice · Passa al diario   a · Aggiungi un evento  n/p · Cambia giorno  ? · Mostra tutte le scorciatoie"
JOURNAL_HINT      = "Barra spaziatrice · Passa al calendario   a · Add task   d · Finito   i · Importante   ? · Mostra tutte le scorciatoie"

DAYS = ["LUNEDÌ", "MARTEDÌ", "MERCOLEDÌ", "GIOVEDÌ", "VENERDì", "SABATO", "DOMENICA"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO", "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]
