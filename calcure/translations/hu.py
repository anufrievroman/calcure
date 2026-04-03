"""Hungarian translations of the program interface"""

MSG_WELCOME_1 = "Üdvözöl a Calcure"
MSG_WELCOME_2 = "Terminálos naptár- és feladatkezelőd!"
MSG_WELCOME_3 = "A konfigurációs és adatfájlok létrejöttek itt:"
MSG_WELCOME_4 = "Támogatásért, hozzájárulásért és további információért látogasd meg:"
MSG_WELCOME_5 = "Nyomj ?-t a gyorsbillentyűk listájához, vagy bármely más gombot a folytatáshoz."

TITLE_KEYS_GENERAL = "ÁLTALÁNOS BILLENTYŰK"
TITLE_KEYS_CALENDAR = "NAPTÁR BILLENTYŰK"
TITLE_KEYS_JOURNAL  = "NAPLÓ BILLENTYŰK"

KEYS_GENERAL = {
        " Space ": "Váltás a naptár és napló között",
        "   /   ": "Képernyő felosztás be-/kikapcsolása",
        "   *   ": "Adatvédelmi mód be-/kikapcsolása",
        "   ?   ": "Súgó megjelenítése",
        "   Q   ": "Újratöltés",
        "   q   ": "Kilépés",
        }

KEYS_CALENDAR = {
        "  a(A) ": "Új (ismétlődő) esemény hozzáadása",
        "   n   ": "Következő hónap (nap)",
        "   p   ": "Előző hónap (nap)",
        "   x   ": "Esemény törlése",
        "   r   ": "Esemény átnevezése",
        "  m(M) ": "Esemény áthelyezése (ebben a hónapban)",
        "  g(G) ": "Ugrás egy napra (ebben a hónapban)",
        "   v   ": "Napi/havi nézet váltása",
        "   w   ": "Hét számok megjelenítése",
        "   h   ": "Esemény magas prioritásúvá tétele",
        "   l   ": "Esemény alacsony prioritásúvá tétele",
        "   d   ": "Esemény késznek jelölése",
        "   .   ": "Esemény privátként jelölése",
        "   C   ": "Események importálása Calcurse-ból",
        "   R   ": "Vissza az aktuális hónaphoz (naphoz)",
        }

KEYS_TODO = {
        "  a(A) ": "Új (al)feladat hozzáadása",
        "  h(H) ": "Egy (vagy minden) feladat magas prioritásúvá tétele",
        "  l(L) ": "Egy (vagy minden) feladat alacsony prioritásúvá tétele",
        "  d(D) ": "Egy (vagy minden) feladat késznek jelölése",
        "  u(U) ": "Egy (vagy minden) feladat kész jelölésének törlése",
        "  x(X) ": "Egy (vagy minden) feladat törlése (az összes alfeladattal együtt)",
        "  t(T) ": "Időzítő indítása/szüneteltetése (vagy törlése) feladathoz",
        "   r   ": "Feladat átnevezése",
        "   s   ": "Váltás feladat/alfeladat között",
        "   .   ": "Feladat privátként jelölése",
        "  f(F) ": "Határidő módosítása (hozzáadása/törlése)",
        "   m   ": "Feladat áthelyezése",
        "   C   ": "Feladatok importálása Calcurse-ból",
        "  f(F) ": "Feladatok importálása Taskwarriorból",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "A nyilak és Vim gombok (j, k, ZZ, ZQ) is működnek!"
MSG_INFO          = "További információért látogasd meg:"
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "Valóban kilépsz? (y/n) "

MSG_EVENT_HIGH    = "Esemény magas prioritásúvá tétele (sorszám): "
MSG_EVENT_LOW     = "Esemény alacsony prioritásúvá tétele (sorszám): "
MSG_EVENT_DONE    = "Esemény késznek jelölése (sorszám): "
MSG_EVENT_RESET   = "Esemény státuszának visszaállítása (sorszám): "
MSG_EVENT_DEL     = "Esemény törlése (sorszám): "
MSG_EVENT_REN     = "Esemény átnevezése (sorszám): "
MSG_NEW_TITLE     = "Új cím megadása: "
MSG_EVENT_MV      = "Esemény áthelyezése (sorszám): "
MSG_EVENT_MV_TO   = "Áthelyezés ide (ÉÉÉÉ/HH/NN): "
MSG_EVENT_MV_TO_D = "Áthelyezés ide: "
MSG_EVENT_DATE    = "Dátum megadása: "
MSG_EVENT_TITLE   = "Cím megadása: "
MSG_EVENT_REP     = "Hányszor ismétlődjön az esemény: "
MSG_EVENT_FR      = "Ismétlődjön az esemény minden (d)nap, (w)hét, (b)kéthetente, (m)hónap vagy (y)év? "
MSG_EVENT_IMP     = "Események importálása Calcurse-ból? (y/n)"
MSG_EVENT_PRIVACY = "Esemény privátként jelölése (sorszám): "
MSG_TM_ADD        = "Időzítő hozzáadása/szüneteltetése feladathoz (sorszám): "
MSG_TM_RESET      = "Időzítő eltávolítása feladathoz (sorszám): "
MSG_TS_HIGH       = "Feladat magas prioritásúvá tétele (sorszám): "
MSG_TS_LOW        = "Feladat alacsony prioritásúvá tétele (sorszám): "
MSG_TS_RES        = "Feladat státuszának visszaállítása (sorszám): "
MSG_TS_DONE       = "Feladat késznek jelölése (sorszám): "
MSG_TS_DEL        = "Feladat törlése (sorszám): "
MSG_TS_DEL_ALL    = "Valóban minden feladatot törölni? (y/n)"
MSG_TS_EDT_ALL    = "Megerősíted a műveletet? (y/n)"
MSG_TS_MOVE       = "Feladat áthelyezése (sorszám): "
MSG_TS_MOVE_TO    = "Feladat áthelyezése ide (sorszám): "
MSG_TS_EDIT       = "Feladat szerkesztése (sorszám): "
MSG_TS_TOG        = "Alfeladat váltása (sorszám): "
MSG_TS_SUB        = "Alfeladat hozzáadása (sorszám): "
MSG_TS_TITLE      = "Alfeladat megadása: "
MSG_TS_IM         = "Feladatok importálása Calcurse-ból? (y/n)"
MSG_TS_TW         = "Feladatok importálása Taskwarriorból? (y/n)"
MSG_TS_NOTHING    = "Semmi sem szerepel..."
MSG_TS_PRIVACY    = "Feladat privátként jelölése (sorszám): "
MSG_TS_DEAD_ADD   = "Határidő hozzáadása feladathoz (sorszám): "
MSG_TS_DEAD_DEL   = "Határidő eltávolítása feladathoz (sorszám): "
MSG_TS_DEAD_DATE  = "Határidő hozzáadása (ÉÉÉÉ/HH/NN): "
MSG_WEATHER       = "Időjárás betöltése..."
MSG_ERRORS        = "Hiba történt. Lásd info.log a konfigurációs mappában."
MSG_INPUT         = "Hibás bemenet."
MSG_GOTO          = "Ugrás dátumra (ÉÉÉÉ/HH/NN): "
MSG_GOTO_D        = "Ugrás dátumra: "

CALENDAR_HINT     = "Space · Váltás naplóhoz   a · Esemény hozzáadása  n/p · Hónap váltása   ? · Súgó"
CALENDAR_HINT_D   = "Space · Váltás naplóhoz   a · Esemény hozzáadása  n/p · Nap váltása   ? · Súgó"
JOURNAL_HINT      = "Space · Váltás naptárhoz   a · Feladat hozzáadása   d · Kész   i · Fontos   ? · Súgó"

DAYS = ["HÉTFŐ", "KEDD", "SZERDA", "CSÜTÖRTÖK", "PÉNTEK", "SZOMBAT", "VASÁRNAP"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["JANUÁR", "FEBRUÁR", "MÁRCIUS", "ÁPRILIS", "MÁJUS", "JÚNIUS", "JÚLIUS", "AUGUSZTUS", "SZEPTEMBER", "OKTÓBER", "NOVEMBER", "DECEMBER"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]
