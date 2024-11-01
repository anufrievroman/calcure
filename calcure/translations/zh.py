"""Chinese Simplified translations of the program interface"""

MSG_WELCOME_1 = "欢迎使用 Calcure"
MSG_WELCOME_2 = "您的终端日历和任务管理工具！"
MSG_WELCOME_3 = "配置文件和数据文件已创建于："
MSG_WELCOME_4 = "如需支持、贡献或了解更多信息，请访问："
MSG_WELCOME_5 = "按 ? 查看所有键位绑定，或按任意键继续。"

TITLE_KEYS_GENERAL  = "通用键位绑定"
TITLE_KEYS_CALENDAR = "日历键位绑定"
TITLE_KEYS_JOURNAL  = "任务键位绑定"

KEYS_GENERAL = {
        " Space ": "切换日历和任务视图",
        "   /   ": "切换分屏模式",
        "   *   ": "切换全局隐私模式",
        "   ?   ": "显示此帮助",
        "   Q   ": "重新加载",
        "   q   ": "退出程序",
        }

KEYS_CALENDAR = {
        "  a(A) ": "添加一个（重复）事件",
        "   n   ": "下一个月（天）",
        "   p   ": "上一个月（天）",
        "   x   ": "删除事件",
        "   r   ": "重命名事件",
        "  m(M) ": "移动事件（在本月内）",
        "  g(G) ": "跳转到指定日期（本月内）",
        "   v   ": "切换日视图/月视图",
        "   h   ": "标记事件为高优先级",
        "   l   ": "标记事件为低优先级",
        "   d   ": "标记事件为已完成",
        "   .   ": "切换事件隐私模式",
        "   C   ": "从 Calcurse 导入事件",
        "   R   ": "回到当前月（天）",
        }

KEYS_TODO = {
        "  a(A) ": "新增任务（子任务）",
        "  h(H) ": "标记任务（全部）为高优先级",
        "  l(L) ": "标记任务（全部）为低优先级",
        "  d(D) ": "标记任务（全部）为已完成",
        "  u(U) ": "取消标记任务（全部）",
        "  x(X) ": "删除任务（全部任务及其子任务）",
        "  t(T) ": "为任务开始/暂停计时（删除计时）",
        "   r   ": "重命名任务",
        "   s   ": "切换任务和子任务",
        "   .   ": "切换任务隐私模式",
        "  f(F) ": "更改（删除）任务截止日期",
        "   m   ": "移动任务",
        "  C(W) ": "从 Calcurse (Taskwarrior) 导入任务",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "方向键和 Vim 键 (j, k, ZZ, ZQ) 也可使用！"
MSG_INFO          = "如需更多信息，请访问："
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "确认退出？(y/n) "

MSG_EVENT_HIGH    = "标记事件为高优先级，事件编号："
MSG_EVENT_LOW     = "标记事件为低优先级，事件编号："
MSG_EVENT_DONE    = "标记事件为已完成，事件编号："
MSG_EVENT_RESET   = "重置事件状态，事件编号："
MSG_EVENT_DEL     = "删除事件编号："
MSG_EVENT_REN     = "重命名事件编号："
MSG_NEW_TITLE     = "输入新的标题："
MSG_EVENT_MV      = "移动事件编号："
MSG_EVENT_MV_TO   = "移动事件到 (YYYY/MM/DD)："
MSG_EVENT_MV_TO_D = "移动事件到："
MSG_EVENT_DATE    = "输入日期："
MSG_EVENT_TITLE   = "输入标题："
MSG_EVENT_REP     = "设置事件重复次数："
MSG_EVENT_FR      = "事件重复周期 (d)天, (w)周, (m)月 或 (y)年？"
MSG_EVENT_IMP     = "从 Calcurse 导入事件？(y/n)"
MSG_EVENT_PRIVACY = "切换事件隐私模式，事件编号："
MSG_TM_ADD        = "为任务编号添加/暂停计时："
MSG_TM_RESET      = "移除任务编号的计时器："
MSG_TS_HIGH       = "标记任务为高优先级，任务编号："
MSG_TS_LOW        = "标记任务为低优先级，任务编号："
MSG_TS_RES        = "重置任务状态，任务编号："
MSG_TS_DONE       = "标记任务为已完成，任务编号："
MSG_TS_DEL        = "删除任务编号："
MSG_TS_DEL_ALL    = "确认删除所有任务？(y/n)"
MSG_TS_EDT_ALL    = "确认执行此操作？(y/n)"
MSG_TS_MOVE       = "移动任务编号："
MSG_TS_MOVE_TO    = "移动任务到编号："
MSG_TS_EDIT       = "编辑任务编号："
MSG_TS_TOG        = "切换子任务编号："
MSG_TS_SUB        = "为任务编号添加子任务："
MSG_TS_TITLE      = "输入子任务："
MSG_TS_IM         = "从 Calcurse 导入任务？(y/n)"
MSG_TS_TW         = "从 Taskwarrior 导入任务？(y/n)"
MSG_TS_NOTHING    = "暂无计划任务..."
MSG_TS_PRIVACY    = "切换任务隐私模式，任务编号："
MSG_TS_DEAD_ADD   = "为任务编号添加截止日期："
MSG_TS_DEAD_DEL   = "移除任务编号的截止日期："
MSG_TS_DEAD_DATE  = "设置截止日期 (YYYY/MM/DD)："
MSG_WEATHER       = "正在加载天气信息..."
MSG_ERRORS        = "发生错误。查看配置文件夹中的 info.log。"
MSG_INPUT         = "输入有误。"
MSG_GOTO          = "跳转至日期 (YYYY/MM/DD)："
MSG_GOTO_D        = "跳转至日期："

CALENDAR_HINT     = "Space · 切换到任务栏   a · 新增事件   n/p · 切换月份   ? · 所有键位绑定"
CALENDAR_HINT_D   = "Space · 切换到任务栏   a · 新增事件   n/p · 切换日期   ? · 所有键位绑定"
JOURNAL_HINT      = "Space · 切换到日历栏   a · 新增任务   d · 完成   i · 重要   ? · 所有键位绑定"

DAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]