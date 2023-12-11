"""Portuguese translations of the program interface"""

MSG_WELCOME_1 = "Bem vindo ao Calcure"
MSG_WELCOME_2 = "Seu calendário e gerenciador de tarefas do terminal!"
MSG_WELCOME_3 = "Configuração e arquivos de dados criados em:"
MSG_WELCOME_4 = "Para apoio, contribuição, e informações adicionais, visitar:"
MSG_WELCOME_5 = "Aperte ? para ver todas as combinações de teclas ou qualquer outra tecla para continuar."

TITLE_KEYS_GENERAL = "COMBINAÇÃO DE TECLAS GERAIS"
TITLE_KEYS_CALENDAR = "COMBINAÇÃO DE TECLAS DO CALENDÁRIO"
TITLE_KEYS_JOURNAL  = "COMBINAÇÃO DE TECLAS DO DIÁRIO"

KEYS_GENERAL = {
        " Espaço ": "Muda entre calendário e diário",
        "   /   ": "Alternar tela dividida",
        "   *   ": "Alternar privacidade global",
        "   ?   ": "Alternar essa ajuda",
        "   Q   ": "Reload",
        "   q   ": "Sair",
        }

KEYS_CALENDAR = {
        "  a(A) ": "Adiciona um evento (recorrente)",
        "   n   ": "Próximo mês (dia)",
        "   p   ": "Mês (dia) anterior",
        "   x   ": "Deletar um evento",
        "   r   ": "Editar um evento",
        "  m(M) ": "Mover evento",
        "   v   ": "Alternar visualização diária/mensal",
        "  g(G) ": "Ir para dia específico",
        "   h   ": "Alternar evento como alta prioridade",
        "   l   ": "Alternar evento como baixa prioridade",
        "   d   ": "Toggle event as done",
        "   .   ": "Alternar privacidade do evento",
        "   C   ": "Importar eventos do calcurse",
        "   G   ": "Retornar para o mês (dia) recorrente",
        }

KEYS_TODO = {
        "  a(A) ": "Adicionar uma nova (sub)tarefa",
        "  h(H) ": "Alternar uma (todas) as tarefas como alta prioridade",
        "  l(L) ": "Alternar uma (todas) as tarefas como baixa prioridade",
        "  d(D) ": "Alternar uma (todas) as tarefas como feitas",
        "  u(U) ": "Desmarcar uma (todas) as tarefas",
        "  x(X) ": "Deletar uma (todas) as tarefas (com todas as subtarefas)",
        "  t(T) ": "Começar/pausar temporizador para a tarefa",
        "   r   ": "Editar uma tarefa",
        "   s   ": "Alternar entre tarefa e subtarefa",
        "   .   ": "Alternar privacidade da tarefa",
        "  f(F) ": "Mudar (remover) data limite da tarefa",
        "   m   ": "Mover tarefa",
        "  C(W) ": "Importar tarefas do calcurse (taskwarrior)",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "Teclas Vim (j, k, ZZ, ZQ) também funcionam!"
MSG_INFO          = "Para mais informações, visite:"
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "Realmente sair? (y/n) "

MSG_EVENT_HIGH    = "Marca como alta prioridade evento número: "
MSG_EVENT_LOW     = "Marca como baixa prioridade evento número: "
MSG_EVENT_DONE    = "Mark as done event number: "
MSG_EVENT_RESET   = "Reseta status para evento número:"
MSG_EVENT_DEL     = "Deleta evento número: "
MSG_EVENT_REN     = "Renomeia evento número: "
MSG_NEW_TITLE     = "Digitar novo título: "
MSG_EVENT_MV      = "Move evento número: "
MSG_EVENT_MV_TO   = "Mover evento para (YYYY/MM/DD): "
MSG_EVENT_MV_TO_D = "Mover evento para: "
MSG_EVENT_DATE    = "Digitar data: "
MSG_EVENT_TITLE   = "Digitar título: "
MSG_EVENT_REP     = "Repetir evento quantas vezes: "
MSG_EVENT_FR      = "Repetir evento cada (d)ia, (w)semana, (m)ês ou (y)ano? "
MSG_EVENT_IMP     = "Importar eventos do Calcurse? (y/n)"
MSG_EVENT_PRIVACY = "Alternar privacidade do evento número: "
MSG_TM_ADD        = "Adicionar/pausar temporizador para tarefa número: "
MSG_TM_RESET      = "Remover temporizador para tarefa número: "
MSG_TS_HIGH       = "Marcar como alta prioridade tarefa número: "
MSG_TS_LOW        = "Marcar como baixa prioridade tarefa número: "
MSG_TS_RES        = "Resetar status para tarefa número: "
MSG_TS_DONE       = "Marcar como feita tarefa número: "
MSG_TS_DEL        = "Deletar tarefa número: "
MSG_TS_DEL_ALL    = "Quer mesmo deletar todas as tarefas? (y/n)"
MSG_TS_EDT_ALL    = "Do you confirm this action? (y/n)"
MSG_TS_MOVE       = "Mover tarefa de número: "
MSG_TS_MOVE_TO    = "Mover tarefa para número: "
MSG_TS_EDIT       = "Editar tarefa número: "
MSG_TS_TOG        = "Alternar subtarefa número: "
MSG_TS_SUB        = "Adicionar subtarefa para tarefa número: "
MSG_TS_TITLE      = "Digitar subtarefa: "
MSG_TS_IM         = "Importar tarefas do Calcurse? (y/n)"
MSG_TS_TW         = "Importar tarefas do Taskwarrior? (y/n)"
MSG_TS_NOTHING    = "Nada planejado..."
MSG_TS_PRIVACY    = "Alternar privacidade de tarefa número: "
MSG_TS_DEAD_ADD   = "Adicionar data limite da tarefa número: "
MSG_TS_DEAD_DEL   = "Remover data limite da tarefa número: "
MSG_TS_DEAD_DATE  = "Adicionar data limite em (AAAA/MM/DD): "
MSG_WEATHER       = "Clima está carregando..."
MSG_ERRORS        = "Errors have occurred. See info.log file in your config folder."
MSG_GOTO          = "Go to date (YYYY/MM/DD): "
MSG_GOTO_D        = "Go to date: "
MSG_INPUT         = "Incorrect input."

CALENDAR_HINT     = "Espaço · Mudar para diário   a · Adicionar evento  n/p · Mudar mês   ? · Todas as combinações de teclas"
CALENDAR_HINT_D   = "Espaço · Mudar para diário   a · Adicionar evento  n/p · Mudar dia   ? · Todas as combinações de teclas"
JOURNAL_HINT      = "Espaço · Mudar para calendar   a · Adicionar tarefa   d · Feito   i · Importante   ? · Todas as combinações de teclas"

DAYS = ["SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO", "DOMINGO"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]
