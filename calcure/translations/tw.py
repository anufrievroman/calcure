"""Chinese Traditional translations of the program interface"""

MSG_WELCOME_1 = "歡迎使用 Calcure"
MSG_WELCOME_2 = "您的終端日曆與任務管理器！"
MSG_WELCOME_3 = "配置檔案和資料檔案已創建於："
MSG_WELCOME_4 = "如需支援、貢獻或更多資訊，請造訪："
MSG_WELCOME_5 = "按 ? 查看所有快捷鍵，或按任意鍵繼續。"

TITLE_KEYS_GENERAL = "一般快捷鍵"
TITLE_KEYS_CALENDAR = "日曆快捷鍵"
TITLE_KEYS_JOURNAL  = "日誌快捷鍵"

KEYS_GENERAL = {
        " Space ": "切換日曆和日誌",
        "   /   ": "切換螢幕分割顯示",
        "   *   ": "切換全域隱私模式",
        "   ?   ": "顯示此說明",
        "   Q   ": "重新載入",
        "   q   ": "退出",
        }

KEYS_CALENDAR = {
        "  a(A) ": "新增（重複）行程",
        "   n   ": "下個月（天）",
        "   p   ": "上個月（天）",
        "   x   ": "刪除行程",
        "   r   ": "重新命名行程",
        "  m(M) ": "移動行程（當月）",
        "  g(G) ": "跳至指定日期（當月）",
        "   v   ": "切換每日/每月顯示",
        "   h   ": "標記行程為高優先級",
        "   l   ": "標記行程為低優先級",
        "   d   ": "標記行程為已完成",
        "   .   ": "切換行程隱私設定",
        "   C   ": "從 Calcurse 匯入行程",
        "   R   ": "回到目前月份（天）",
        }

KEYS_TODO = {
        "  a(A) ": "新增新的（子）任務",
        "  h(H) ": "將單個（所有）任務設為高優先級",
        "  l(L) ": "將單個（所有）任務設為低優先級",
        "  d(D) ": "將單個（所有）任務標記為已完成",
        "  u(U) ": "取消標記單個（所有）任務",
        "  x(X) ": "刪除單個（所有）任務（含所有子任務）",
        "  t(T) ": "為任務開始/暫停（移除）計時器",
        "   r   ": "重新命名任務",
        "   s   ": "切換主任務與子任務",
        "   .   ": "切換任務隱私設定",
        "  f(F) ": "修改（移除）任務期限",
        "   m   ": "移動任務",
        "  C(W) ": "從 Calcurse (Taskwarrior) 匯入任務",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "方向鍵和 Vim 快捷鍵（j、k、ZZ、ZQ）也可以使用！"
MSG_INFO          = "更多資訊，請造訪："
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "確定退出？(y/n)"

MSG_EVENT_HIGH    = "標記為高優先級行程編號："
MSG_EVENT_LOW     = "標記為低優先級行程編號："
MSG_EVENT_DONE    = "標記為已完成行程編號："
MSG_EVENT_RESET   = "重設行程狀態、編號："
MSG_EVENT_DEL     = "刪除行程編號："
MSG_EVENT_REN     = "重新命名行程編號："
MSG_NEW_TITLE     = "輸入新標題："
MSG_EVENT_MV      = "移動行程編號："
MSG_EVENT_MV_TO   = "移動行程至(YYYY/MM/DD)："
MSG_EVENT_MV_TO_D = "移動行程至："
MSG_EVENT_DATE    = "輸入日期："
MSG_EVENT_TITLE   = "輸入標題："
MSG_EVENT_REP     = "行程重複次數："
MSG_EVENT_FR      = "行程重複頻率：日(d)、週(w)、月(m)或年(y)？"
MSG_EVENT_IMP     = "從 Calcurse 匯入行程？(y/n)"
MSG_EVENT_PRIVACY = "切換行程編號隱私設定："
MSG_TM_ADD        = "為任務編號新增/暫停計時器："
MSG_TM_RESET      = "移除任務編號的計時器："
MSG_TS_HIGH       = "將任務編號標記為高優先級："
MSG_TS_LOW        = "將任務編號標記為低優先級："
MSG_TS_RES        = "重設任務編號狀態："
MSG_TS_DONE       = "將任務編號標記為已完成："
MSG_TS_DEL        = "刪除任務編號："
MSG_TS_DEL_ALL    = "確定刪除所有任務？(y/n)"
MSG_TS_EDT_ALL    = "確定執行此動作？(y/n)"
MSG_TS_MOVE       = "將任務從編號移動："
MSG_TS_MOVE_TO    = "移動任務至編號："
MSG_TS_EDIT       = "編輯任務編號："
MSG_TS_TOG        = "切換子任務編號："
MSG_TS_SUB        = "為任務編號新增子任務："
MSG_TS_TITLE      = "輸入子任務："
MSG_TS_IM         = "從 Calcurse 匯入任務？(y/n)"
MSG_TS_TW         = "從 Taskwarrior 匯入任務？(y/n)"
MSG_TS_NOTHING    = "沒有計劃..."
MSG_TS_PRIVACY    = "切換任務編號隱私設定："
MSG_TS_DEAD_ADD   = "為任務編號新增截止日期："
MSG_TS_DEAD_DEL   = "移除任務編號的截止日期："
MSG_TS_DEAD_DATE  = "設定截止日期(YYYY/MM/DD)："
MSG_WEATHER       = "正在載入天氣..."
MSG_ERRORS        = "發生錯誤，詳情請查看配置資料夾中的 info.log。"
MSG_INPUT         = "輸入錯誤。"
MSG_GOTO          = "前往日期(YYYY/MM/DD)："
MSG_GOTO_D        = "前往日期："

CALENDAR_HINT     = "Space · 切換至日誌   a · 新增行程   n/p · 切換月份   ? · 所有快捷鍵"
CALENDAR_HINT_D   = "Space · 切換至日誌   a · 新增行程   n/p · 切換天數   ? · 所有快捷鍵"
JOURNAL_HINT      = "Space · 切換至日曆   a · 新增任務   d · 完成   i · 重要   ? · 所有快捷鍵"

DAYS = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]