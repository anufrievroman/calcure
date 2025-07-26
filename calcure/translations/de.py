"""German translations of the program interface"""

MSG_WELCOME_1 = "Willkommen bei Calcure"
MSG_WELCOME_2 = "Ihr Terminal-Kalender und Aufgabenmanager!"
MSG_WELCOME_3 = "Konfigurations- und Datendateien wurden erstellt unter:"
MSG_WELCOME_4 = "Für Unterstützung, Beiträge und weitere Informationen besuchen Sie:"
MSG_WELCOME_5 = "Drücken Sie ? für alle Tastenkombinationen oder eine andere Taste zum Fortfahren."

TITLE_KEYS_GENERAL = "ALLGEMEINE TASTENKOMBINATIONEN"
TITLE_KEYS_CALENDAR = "KALENDER-TASTENKOMBINATIONEN"
TITLE_KEYS_JOURNAL  = "JOURNAL-TASTENKOMBINATIONEN"

KEYS_GENERAL = {
        " Space ": "Zwischen Kalender und Journal wechseln",
        "   /   ": "Geteilte Ansicht umschalten",
        "   *   ": "Globale Privatsphäre umschalten",
        "   ?   ": "Diese Hilfe ein-/ausblenden",
        "   Q   ": "Neu laden",
        "   q   ": "Beenden",
        }

KEYS_CALENDAR = {
        "  a(A) ": "Ereignis (wiederkehrend) hinzufügen",
        "   n   ": "Nächster Monat (Tag)",
        "   p   ": "Vorheriger Monat (Tag)",
        "   x   ": "Ereignis löschen",
        "   r   ": "Ereignis umbenennen",
        "  m(M) ": "Ereignis verschieben (in diesem Monat)",
        "  g(G) ": "Zu bestimmtem Tag gehen (in diesem Monat)",
        "   v   ": "Tages-/Monatsübersicht umschalten",
        "   h   ": "Ereignis als hohe Priorität markieren",
        "   l   ": "Ereignis als niedrige Priorität markieren",
        "   d   ": "Ereignis als erledigt markieren",
        "   .   ": "Privatsphäre des Ereignisses umschalten",
        "   C   ": "Ereignisse aus calcurse importieren",
        "   R   ": "Zum aktuellen Monat (Tag) zurückkehren",
        }

KEYS_TODO = {
        "  a(A) ": "Neue (Unter-)Aufgabe hinzufügen",
        "  h(H) ": "Eine (alle) Aufgaben als hohe Priorität markieren",
        "  l(L) ": "Eine (alle) Aufgaben als niedrige Priorität markieren",
        "  d(D) ": "Eine (alle) Aufgaben als erledigt markieren",
        "  u(U) ": "Markierung einer (aller) Aufgaben zurücksetzen",
        "  x(X) ": "Eine (alle) Aufgaben (inkl. Unteraufgaben) löschen",
        "  t(T) ": "Timer für Aufgabe starten/pausieren (entfernen)",
        "   r   ": "Aufgabe umbenennen",
        "   s   ": "Zwischen Aufgabe und Unteraufgabe wechseln",
        "   .   ": "Aufgaben-Privatsphäre umschalten",
        "  f(F) ": "Aufgaben-Deadline ändern (entfernen)",
        "   m   ": "Aufgabe verschieben",
        "   C   ": "Aufgaben aus calcurse importieren",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "Pfeil- und Vim-Tasten (j, k, ZZ, ZQ) funktionieren ebenso!"
MSG_INFO          = "Für weitere Informationen besuchen Sie:"
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "Wirklich beenden? (j/n)"

MSG_EVENT_HIGH    = "Als hohe Priorität markieren, Ereignisnummer: "
MSG_EVENT_LOW     = "Als niedrige Priorität markieren, Ereignisnummer: "
MSG_EVENT_DONE    = "Als erledigt markieren, Ereignisnummer: "
MSG_EVENT_RESET   = "Status zurücksetzen für Ereignisnummer: "
MSG_EVENT_DEL     = "Ereignis löschen, Nummer: "
MSG_EVENT_REN     = "Ereignis umbenennen, Nummer: "
MSG_NEW_TITLE     = "Neuen Titel eingeben: "
MSG_EVENT_MV      = "Ereignis verschieben, Nummer: "
MSG_EVENT_MV_TO   = "Ereignis verschieben zu (JJJJ/MM/TT): "
MSG_EVENT_MV_TO_D = "Ereignis verschieben zu: "
MSG_EVENT_DATE    = "Datum eingeben: "
MSG_EVENT_TITLE   = "Titel eingeben: "
MSG_EVENT_REP     = "Wie oft soll das Ereignis wiederholt werden: "
MSG_EVENT_FR      = "Ereignis wiederholen jeden (T)ag, (W)oche, (M)onat oder (J)ahr? "
MSG_EVENT_IMP     = "Ereignisse aus Calcurse importieren? (j/n)"
MSG_EVENT_PRIVACY = "Privatsphäre für Ereignisnummer umschalten: "
MSG_TM_ADD        = "Timer hinzufügen/pausieren für Aufgabennummer: "
MSG_TM_RESET      = "Timer für Aufgabennummer entfernen: "
MSG_TS_HIGH       = "Aufgabe als hohe Priorität markieren, Nummer: "
MSG_TS_LOW        = "Aufgabe als niedrige Priorität markieren, Nummer: "
MSG_TS_RES        = "Status für Aufgabennummer zurücksetzen: "
MSG_TS_DONE       = "Aufgabe als erledigt markieren, Nummer: "
MSG_TS_DEL        = "Aufgabe löschen, Nummer: "
MSG_TS_DEL_ALL    = "Wirklich alle Aufgaben löschen? (j/n)"
MSG_TS_EDT_ALL    = "Möchten Sie diese Aktion bestätigen? (j/n)"
MSG_TS_MOVE       = "Aufgabe verschieben von Nummer: "
MSG_TS_MOVE_TO    = "Aufgabe verschieben zu Nummer: "
MSG_TS_EDIT       = "Aufgabe bearbeiten, Nummer: "
MSG_TS_TOG        = "Unteraufgabe umschalten, Nummer: "
MSG_TS_SUB        = "Unteraufgabe für Aufgabennummer hinzufügen: "
MSG_TS_TITLE      = "Unteraufgabe eingeben: "
MSG_TS_IM         = "Aufgaben aus Calcurse importieren? (j/n)"
MSG_TS_TW         = "Aufgaben aus Taskwarrior importieren? (j/n)"
MSG_TS_NOTHING    = "Nichts geplant..."
MSG_TS_PRIVACY    = "Privatsphäre für Aufgabennummer umschalten: "
MSG_TS_DEAD_ADD   = "Deadline für Aufgabennummer hinzufügen: "
MSG_TS_DEAD_DEL   = "Deadline für Aufgabennummer entfernen: "
MSG_TS_DEAD_DATE  = "Deadline hinzufügen am (JJJJ/MM/TT): "
MSG_WEATHER       = "Wetter wird geladen..."
MSG_ERRORS        = "Es sind Fehler aufgetreten. Siehe info.log im Konfigurationsordner."
MSG_INPUT         = "Ungültige Eingabe."
MSG_GOTO          = "Zum Datum gehen (JJJJ/MM/TT): "
MSG_GOTO_D        = "Zum Datum gehen: "

CALENDAR_HINT     = "Space · Zum Journal wechseln   a · Ereignis hinzufügen  n/p · Monat wechseln   ? · Alle Tastenkombinationen"
CALENDAR_HINT_D   = "Space · Zum Journal wechseln   a · Ereignis hinzufügen  n/p · Tag wechseln   ? · Alle Tastenkombinationen"
JOURNAL_HINT      = "Space · Zum Kalender wechseln   a · Aufgabe hinzufügen   d · Erledigt   i · Wichtig   ? · Alle Tastenkombinationen"

DAYS = ["MONTAG", "DIENSTAG", "MITTWOCH", "DONNERSTAG", "FREITAG", "SAMSTAG", "SONNTAG"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["JANUAR", "FEBRUAR", "MÄRZ", "APRIL", "MAI", "JUNI", "JULI", "AUGUST", "SEPTEMBER", "OKTOBER", "NOVEMBER", "DEZEMBER"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]