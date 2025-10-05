"""Spanish translations of the program interface"""

MSG_WELCOME_1 = "Bienvenido a Calcure"
MSG_WELCOME_2 = "¡Tu calendario y administrador de tareas en la terminal!"
MSG_WELCOME_3 = "Se han creados archivos de configuración en:"
MSG_WELCOME_4 = "Para soporte, contribución e información adicional, visite:"
MSG_WELCOME_5 = "Presione ? para ver los atajos u otra tecla para continuar"

TITLE_KEYS_GENERAL = "ATAJOS GENERALES"
TITLE_KEYS_CALENDAR = "ATAJOS DEL CALENDARIO"
TITLE_KEYS_JOURNAL  = "ATAJOS DEL DIARIO"

KEYS_GENERAL = {
        " Espacio ": "Cambiar entre el calendario y el diario",
        "   /   ": "Alternar pantalla dividida",
        "   *   ": "Alternar privacidad global",
        "   ?   ": "Alternar para ayuda",
        "   Q   ": "Recargar",
        "   q   ": "Salir",
        }

KEYS_CALENDAR = {
        "  a(A) ": "Agregar un evento (recurrente)",
        "   n   ": "Próximo mes (día)",
        "   p   ": "Mes anterior (día)",
        "   x   ": "Elimine un evento",
        "   r   ": "Renombrar un evento",
        "  m(M) ": "Mover evento (en este mes)",
        "  g(G) ": "Ir a un día específico (en este mes)",
        "   v   ": "Alternar vista diaria/mensual",
        "   h   ": "Alternar evento como alta prioridad",
        "   l   ": "Alternar evento como baja prioridad",
        "   d   ": "Alternar evento como terminado",
        "   .   ": "Alternar la privacidad del evento",
        "   C   ": "Importar eventos desde calcurse",
        "   R   ": "Regresar al mes actual",
        }

KEYS_TODO = {
        "  a(A) ": "Agregar nueva (sub)tarea",
        "  h(H) ": "Alternar una (todas) de las tareas como alta prioridad",
        "  l(L) ": "Alternar una (todas) de las tareas como baja prioridad",
        "  d(D) ": "Alternar una (todas) de las tareas como terminadas",
        "  u(U) ": "Desmarcar una (todas) de las tareas",
        "  x(X) ": "Eliminar una (todas) de las tareas (con todas las subtareas)",
        "  t(T) ": "Iniciar/pausar (remover) el temporizador de una tarea",
        "   r   ": "Renombra una tarea",
        "   s   ": "Alternar entre tarea y subtarea",
        "   .   ": "Alternar la privacidad de la tarea",
        "  f(F) ": "Cambiar (remover) el límite de la tarea",
        "   m   ": "Mover una tarea",
        "   C   ": "Importar tareas desde calcurse",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "¡Flechas y atajos de Vim (j, k, ZZ, ZQ) también funcionan!"
MSG_INFO          = "Para más información, visite:"
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "¿Realmente quire salir? (y/n) "

MSG_EVENT_HIGH    = "Marcar como alta prioridad el evento número: ";
MSG_EVENT_LOW     = "Marcar como baja prioridad el evento número: "
MSG_EVENT_DONE    = "Marcar como terminado el evento número: "
MSG_EVENT_RESET   = "Resetear el estatus para el evento número: "
MSG_EVENT_DEL     = "Eliminar el evento número: "
MSG_EVENT_REN     = "Renombrar el evento número: "
MSG_NEW_TITLE     = "Ingrese un nuevo título: "
MSG_EVENT_MV      = "Move event number: "
MSG_EVENT_MV      = "Mover evento número: "
MSG_EVENT_MV_TO   = "Mover evento a (YYYY/MM/DD): "
MSG_EVENT_MV_TO_D = "Mover evento a: "
MSG_EVENT_DATE    = "Ingrese la fecha: "
MSG_EVENT_TITLE   = "Ingrese un titulo: "
MSG_EVENT_REP     = "Cuantas veces quiere repetir el evento: "
MSG_EVENT_FR      = "¿Repetir el evento cada (d)ía, (w)semana, (m)mes o (y)año? "
MSG_EVENT_IMP     = "¿Importar eventos desde Calcurse? (y/n)"
MSG_EVENT_PRIVACY = "Alternar privacidad del evento número: "
MSG_TM_ADD        = "Agregar/pausar temporizador por número de tarea: "
MSG_TM_RESET      = "Remover temporizador para la tarea número: "
MSG_TS_HIGH       = "Mark as high priority the task number: "
MSG_TS_HIGH       = "Marcar como alta prioridad el número de la tarea: "
MSG_TS_LOW        = "Mark as low priority the task number: "
MSG_TS_RES        = "Reset status for the task number: "
MSG_TS_DONE       = "Mark as done the task number: "
MSG_TS_DEL        = "Delete task number: "
MSG_TS_DEL_ALL    = "Really delete all tasks? (y/n)"
MSG_TS_EDT_ALL    = "Do you confirm this action? (y/n)"
MSG_TS_MOVE       = "Move task from number: "
MSG_TS_MOVE_TO    = "Move task to number: "
MSG_TS_EDIT       = "Edit task number: "
MSG_TS_TOG        = "Toggle subtask number: "
MSG_TS_SUB        = "Add subtask for task number: "
MSG_TS_TITLE      = "Enter subtask: "
MSG_TS_IM         = "Import tasks from Calcurse? (y/n)"
MSG_TS_TW         = "Import tasks from Taskwarrior? (y/n)"
MSG_TS_NOTHING    = "Nothing planned..."
MSG_TS_PRIVACY    = "Toggle privacy of task number: "
MSG_TS_DEAD_ADD   = "Add deadline for task number: "
MSG_TS_DEAD_DEL   = "Remove deadline of the task number: "
MSG_TS_DEAD_DATE  = "Add deadline on (YYYY/MM/DD): "
MSG_WEATHER       = "Weather is loading..."
MSG_ERRORS        = "Errors have occurred. See info.log in your config folder."
MSG_INPUT         = "Incorrect input."
MSG_GOTO          = "Go to date (YYYY/MM/DD): "
MSG_GOTO_D        = "Go to date: "

CALENDAR_HINT     = "Space · Switch to journal   a · Add event  n/p · Change month   ? · All keybindings"
CALENDAR_HINT_D   = "Space · Switch to journal   a · Add event  n/p · Change day   ? · All keybindings"
JOURNAL_HINT      = "Space · Switch to calendar   a · Add task   d · Done   i · Important   ? · All keybindings"

DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]
