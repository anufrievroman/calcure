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
        "   x   ": "Eliminar un evento",
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
        "  f(F) ": "Cambiar (remover) la fecha límite de la tarea",
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
MSG_NEW_TITLE     = "Ingresar un nuevo título: "
MSG_EVENT_MV      = "Mover evento número: "
MSG_EVENT_MV_TO   = "Mover evento a (YYYY/MM/DD): "
MSG_EVENT_MV_TO_D = "Mover evento a: "
MSG_EVENT_DATE    = "Ingresar la fecha: "
MSG_EVENT_TITLE   = "Ingresar un titulo: "
MSG_EVENT_REP     = "Cuantas veces quiere repetir el evento: "
MSG_EVENT_FR      = "¿Repetir el evento cada (d)ía, (w)semana, (m)mes o (y)año? "
MSG_EVENT_IMP     = "¿Importar eventos desde Calcurse? (y/n)"
MSG_EVENT_PRIVACY = "Alternar privacidad del evento número: "
MSG_TM_ADD        = "Agregar/pausar temporizador por número de tarea: "
MSG_TM_RESET      = "Remover temporizador para la tarea número: "
MSG_TS_HIGH       = "Marcar como alta prioridad la tarea número: "
MSG_TS_LOW        = "Marcar como baja prioridad la tarea número: "
MSG_TS_RES        = "Resetear el estatus para la tarea número: "
MSG_TS_DONE       = "Marcar como terminada la tarea número: "
MSG_TS_DEL        = "Eliminar la tarea número: "
MSG_TS_DEL_ALL    = "¿Realmente quiere eliminar todas las tareas? (y/n)"
MSG_TS_EDT_ALL    = "¿Confirmas esta acción? (y/n)"
MSG_TS_MOVE       = "Mover tarea desde el número: "
MSG_TS_MOVE_TO    = "Mover tarea al número: "
MSG_TS_EDIT       = "Editar tarea número: "
MSG_TS_TOG        = "Alternar subtarea número: "
MSG_TS_SUB        = "Agregar subtarea para la tarea número: "
MSG_TS_TITLE      = "Ingresar subtarea: "
MSG_TS_IM         = "¿Importar tareas desde Calcurse? (y/n)"
MSG_TS_TW         = "¿Importar tareas desde Taskwarrior? (y/n)"
MSG_TS_NOTHING    = "Nada planificado..."
MSG_TS_PRIVACY    = "Alternar privacidad de la tarea número: "
MSG_TS_DEAD_ADD   = "Agregar fecha límite para la tarea número: "
MSG_TS_DEAD_DEL   = "Remover fecha límite para la tarea número: "
MSG_TS_DEAD_DATE  = "Agregar fecha límite en (YYY/MM/DD): "
MSG_WEATHER       = "Cargando el clima..."
MSG_ERRORS        = "Han ocurrido errores. Vea info.log en su carpeta config."
MSG_INPUT         = "Entrada incorrecta."
MSG_GOTO          = "Ir a la fecha (YYYY/MM/DD): "
MSG_GOTO_D        = "Ir a la fecha: "

CALENDAR_HINT     = "Espacio · Ir al diario   a · Agregar evento  n/p · Cambiar mes   ? · Mostrar atajos"
CALENDAR_HINT_D   = "Espacio · Ir al diario   a · Agregar evento  n/p · Cambiar día   ? · Mostrar atajos"
JOURNAL_HINT      = "Espacio · Ir al calendario   a · Agregar tarea   d · Hecho   i · Importante   ? · Mostrar atajos"

DAYS = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]
