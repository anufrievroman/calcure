"""Chinese translations of the program interface"""

MSG_WELCOME_1 = "欢迎来到 Calcure"
MSG_WELCOME_2 = "你的终端日历和任务管理器!"
MSG_WELCOME_3 = "配置文件和数据文件被创建在:"
MSG_WELCOME_4 = "用于支持、贡献和其他信息，请参看:"
MSG_WELCOME_5 = "按 ? 查看所有的键位绑定或者任何其它的键位以继续。"

TITLE_KEYS_GENERAL  = "通用的键位绑定"
TITLE_KEYS_CALENDAR = "日历栏的键位绑定"
TITLE_KEYS_JOURNAL  = "通知栏的键位绑定"

KEYS_GENERAL = {
        " Space ": "切换日历和通知栏目",
        "   /   ": "切换屏幕分割模式",
        "   *   ": "切换全局隐私模式",
        "   ?   ": "显示此帮助文档",
        "   q   ": "退出",
        }

KEYS_CALENDAR = {
        "  a(A) ": "增加一个（再次发生）事件",
        "  n,🠒  ": "下个月 (日)",
        "  p,🠐  ": "上个月 (日)",
        "  d,x  ": "删除事件",
        "  e,c  ": "编辑事件",
        "   m   ": "移动事件",
        "   g   ": "跳转到指定的一天",
        "   v   ": "切换每天/每月视图模式",
        "   h   ": "切换事件为更高的优先级",
        "   l   ": "切换事件为更低的优先级",
        "   .   ": "切换事件为隐私模式",
        "   C   ": "从calcurse中导入事件",
        "   G   ": "返回当前的月 (日)",
        }

KEYS_TODO = {
        "  a(A) ": "新增一个 (子) 任务",
        "  h(H) ": "切换一个 (所有) 任务为更高优先级",
        "  l(L) ": "切换一个 (所有) 任务为更低优先级",
        "  v(V) ": "切换一个 (所有) 任务为已完成",
        "  u(U) ": "不标记一个 (所有) 任务",
        "  d(D) ": "删除一个 (所有) 任务 (和其子任务)",
        "  t(T) ": "开始/暂停 (移除) 时刻为一个任务",
        "  e,c  ": "编辑一个任务",
        "   s   ": "切换任务和子任务",
        "   .   ": "切换任务为隐私模式",
        "  f(F) ": "修改 (移除) 任务的截止日期",
        "   m   ": "移动一个任务",
        "  C(W) ": "导入任务从calcurse (taskwarrior)",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "Vim 键位 (j, k, ZZ, ZQ) 也可以工作!"
MSG_INFO          = "对于更多信息, 参看:"
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "是否真的要退出? (y/n) "

MSG_EVENT_HIGH    = "标记为更高优先级的事件号码: "
MSG_EVENT_LOW     = "标记为更低优先级的事件号码: "
MSG_EVENT_RESET   = "重设状态的事件号码: "
MSG_EVENT_DEL     = "删除事件的号码: "
MSG_EVENT_REN     = "重命名事件的号码: "
MSG_NEW_TITLE     = "输入新的标题: "
MSG_EVENT_MOVE    = "移动事件的号码: "
MSG_EVENT_MOVE_TO = "移动事件到: "
MSG_EVENT_DATE    = "输入日期: "
MSG_EVENT_TITLE   = "输入标题: "
MSG_EVENT_REP     = "事件重复多少次: "
MSG_EVENT_FR      = "重复事件 (d)天, (w)周, (m)月 或者 (y)年? "
MSG_EVENT_IMP     = "是否从Calcurse中导入事件? (y/n)"
MSG_EVENT_PRIVACY = "切换为隐私模式的事件号码: "
MSG_TM_ADD        = "增加/暂停计时器的任务号码: "
MSG_TM_RESET      = "移除计时器的任务号码: "
MSG_TS_HIGH       = "标记为更高优先级的任务号码: "
MSG_TS_LOW        = "标记为更低优先级的任务号码: "
MSG_TS_RES        = "重设状态的任务号码: "
MSG_TS_DONE       = "标记为已完成的任务号码: "
MSG_TS_DEL        = "删除的任务号码: "
MSG_TS_DEL_ALL    = "是否真的删除所有任务? (y/n)"
MSG_TS_MOVE       = "移动任务的号码: "
MSG_TS_MOVE_TO    = "移动任务到新的号码: "
MSG_TS_EDIT       = "编辑任务的号码: "
MSG_TS_TOG        = "切换子任务的号码: "
MSG_TS_SUB        = "添加子任务的任务号码: "
MSG_TS_TITLE      = "输入子任务: "
MSG_TS_IM         = "是否从Calcurse导入任务? (y/n)"
MSG_TS_TW         = "是否从Taskwarrior导入任务? (y/n)"
MSG_TS_NOTHING    = "没有事情被计划..."
MSG_TS_PRIVACY    = "切换为隐私模式的事件号码: "
MSG_TS_DEAD_ADD   = "增加截至日期为事件号码: "
MSG_TS_DEAD_DEL   = "移除截止日期为事件号码: "
MSG_TS_DEAD_DATE  = "增加截至日期在(YYYY/MM/DD): "
MSG_WEATHER       = "天气插件正在加载..."

CALENDAR_HINT     = "Space · 转换到通知栏   a · 增加事件  n/p · 改变月   ? · 所有键位绑定"
CALENDAR_HINT_D   = "Space · 转换到通知栏   a · 增加事件  n/p · 改变日   ? · 所有键位绑定"
JOURNAL_HINT      = "Space · 转换到日历栏   a · 增加任务   v · 已完成   i · 重要的   ? · 所有键位绑定"

DAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]
