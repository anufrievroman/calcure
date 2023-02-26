"""French translations of the program interface"""

MSG_WELCOME_1 = "Bienvenue à Calcure"
MSG_WELCOME_2 = "Le calendrier et le gestionnaire de tâches pour votre terminal!"
MSG_WELCOME_3 = "Les fichiers de configuration et de données ont été créés à:"
MSG_WELCOME_4 = "Pour obtenir de l'aide, des contributions et des informations supplémentaires, visitez:"
MSG_WELCOME_5 = "Presse ? pour voir les combinaisons de touches ou toute autre touche pour continuer."

TITLE_KEYS_GENERAL = "GÉNÉRALE"
TITLE_KEYS_CALENDAR = "CALENDRIER"
TITLE_KEYS_JOURNAL = "JOURNAL"

KEYS_GENERAL = {
        " Space ": "Basculer entre calendrier et journal",
        "   /   ": "Basculer l'écran partagé",
        "   *   ": "Basculer la confidentialité globale",
        "   ?   ": "Basculer cette aide",
        "   q   ": "Quitter",
        }

KEYS_CALENDAR = {
        "  a(A) ": "Ajouter un événement (récurrent)",
        "  n,🠒  ": "Le mois (jour) prochain",
        "  p,🠐  ": "mois (jour) précédent",
        "  d,x  ": "Supprimer un événement",
        "  e,c  ": "Modifier un événement",
        "   m   ": "Déplacer l'événement",
        "   v   ": "Basculer la vue quotidienne/mensuelle",
        "   g   ": "Aller à un certain jour",
        "   h   ": "Désactiver l'événement en haute priorité",
        "   l   ": "Basculer l'événement en priorité basse",
        "   .   ": "Activer la confidentialité des événements",
        "   C   ": "Importer des événements depuis calcurse",
        "   G   ": "Revenir au mois (jour) en cours",
        }

KEYS_TODO = {
        "  a(A) ": "Ajouter une nouvelle (sous-)tâche",
        "  h(H) ": "Bascule une (toutes) des tâches en haute priorité",
        "  l(L) ": "Désactiver une (toutes) les tâches en priorité basse",
        "  v(V) ": "Bascule une (toutes) les tâches comme terminée",
        "  u(U) ": "Démarquer une (toutes) les tâches",
        "  d(D) ": "Supprimer une (toutes) les tâches (avec toutes les sous-tâches)",
        "  t(T) ": "Démarrer/mettre en pause (supprimer) le minuteur pour une tâche",
        "  e,c  ": "Modifier une tâche",
        "   s   ": "Basculer entre tâche et sous-tâche",
        "   .   ": "Basculer la confidentialité des tâches",
        "  f(F) ": "Modifier (supprimer) l'échéance de la tâche",
        "   m   ": "Déplacer une tâche",
        "  C(W) ": "Importer des tâches de calcurse (taskwarrior)",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "Les touches de Vim (j, k, ZZ, ZQ) fonctionnent également!"
MSG_INFO          = "Pour plus d'informations, visitez:"
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "Vraiment quitter ? (y/n) "

MSG_EVENT_HIGH    = "Marquer comme numéro d'événement hautement prioritaire: "
MSG_EVENT_LOW     = "Marquer comme numéro d'événement basse priorité: "
MSG_EVENT_RESET   = "Réinitialiser le statut pour l'événement numéro : "
MSG_EVENT_DEL     = "Supprimer le numéro d'événement: "
MSG_EVENT_REN     = "Renommer le numéro d'événement: "
MSG_NEW_TITLE     = "Entrez un nouveau titre: "
MSG_EVENT_MOVE    = "Déplacer le numéro d'événement: "
MSG_EVENT_MOVE_TO = "Déplacer l'événement vers: "
MSG_EVENT_DATE    = "Entrez la date: "
MSG_EVENT_TITLE   = "Entrez le titre: "
MSG_EVENT_REP     = "Combien de répétitions de l'événement: "
MSG_EVENT_FR      = "Répéter l'événement tous les jours (d), semaines (w), mois (m) ou années (y) ?"
MSG_EVENT_IMP     = "Importer des événements depuis Calcurse ? (y/n)"
MSG_EVENT_PRIVACY = "Basculer la confidentialité du numéro d'événement: "
MSG_TM_ADD        = "Ajouter/mettre en pause le temporisateur pour la tâche numéro: "
MSG_TM_RESET      = "Supprimer le temporisateur pour la tâche numéro: "
MSG_TS_HIGH       = "Marquer comme haute priorité le numéro de tâche: "
MSG_TS_LOW        = "Marquer comme basse priorité le numéro de tâche: "
MSG_TS_RES        = "Réinitialiser l'état de la tâche numéro: "
MSG_TS_DONE       = "Marquer comme terminé le numéro de tâche: "
MSG_TS_DEL        = "Supprimer le numéro de tâche: "
MSG_TS_DEL_ALL    = "Vraiment supprimer toutes les tâches ? (y/n)"
MSG_TS_MOVE       = "Déplacer la tâche du numéro: "
MSG_TS_MOVE_TO    = "Déplacer la tâche vers le numéro: "
MSG_TS_EDIT       = "Modifier le numéro de tâche: "
MSG_TS_TOG        = "Basculer le numéro de sous-tâche: "
MSG_TS_SUB        = "Ajouter une sous-tâche pour la tâche numéro: "
MSG_TS_TITLE      = "Entrez la sous-tâche: "
MSG_TS_IM         = "Importer des tâches depuis Calcurse ? (y/n)"
MSG_TS_TW         = "Importer des tâches depuis Taskwarrior ? (y/n)"
MSG_TS_NOTHING    = "Rien de prévu..."
MSG_TS_PRIVACY    = "Basculer la confidentialité du numéro de tâche: "
MSG_TS_DEAD_ADD   = "Ajouter un délai pour la tâche numéro: "
MSG_TS_DEAD_DEL   = "Supprimer l'échéance de la tâche numéro: "
MSG_TS_DEAD_DATE  = "Ajouter une date limite le (AAAA/MM/JJ): "
MSG_WEATHER       = "La météo se charge..."

CALENDAR_HINT     = "Espace · Passer au journal  a · Ajouter un événement  n/p · Changer de mois  ? · Aider"
CALENDAR_HINT_D   = "Espace · Passer au journal  a · Ajouter un événement  n/p · Changer de jour  ? · All keybindings"
JOURNAL_HINT      = "Espace · Passer au calendrier  a · Ajouter une tâche  v · Terminé  i · Important  ? · All keybindings"

DAYS = ["LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI", "SAMEDI", "DIMANCHE"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]
