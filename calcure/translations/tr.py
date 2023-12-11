"""Turkish translations of the program interface"""

MSG_WELCOME_1 = "Calcure'a hoş geldiniz"
MSG_WELCOME_2 = "Terminal takviminiz ve görev yöneticiniz!"
MSG_WELCOME_3 = "Yapılandırma ve veri dosyaları şu adreste oluşturuldu:"
MSG_WELCOME_4 = "Destek, katkı ve ek bilgi için şu adresi ziyaret edin:"
MSG_WELCOME_5 = "Tüm tuş atamalarını görmek için ? tuşuna veya devam etmek için başka bir tuşa basın."

TITLE_KEYS_GENERAL  = "GENEL TUŞ ATAMALARI"
TITLE_KEYS_CALENDAR = "TAKVIM TUŞ ATAMALARI"
TITLE_KEYS_JOURNAL  = "GÜNLÜK TUŞ ATAMALARI"

KEYS_GENERAL = {
        " Space ": "Takvim ve günlük arasında geçiş yapma",
        "   /   ": "Bölünmüş ekranı aç / kapat",
        "   *   ": "Genel gizliliği aç / kapat",
        "   ?   ": "Bu yardımı aç / kapat",
        "   Q   ": "Reload",
        "   q   ": "Çıkış",
        }

KEYS_CALENDAR = {
        "  a(A) ": "Etkinlik (yinelenen) ekleme",
        "   n   ": "Gelecek ay (gün)",
        "   p   ": "Önceki ay (gün)",
        "   x   ": "Etkinlik silme",
        "  e,r  ": "Etkinlik düzenleme",
        "  m(M) ": "Etkinlik taşıma",
        "  g(G) ": "Belirli bir güne git",
        "   v   ": "Günlük/aylık görünümü değiştir",
        "   h   ": "Etkinliği yüksek öncelikli olarak değiştir",
        "   l   ": "Etkinliği düşük öncelikli olarak değiştir",
        "   d   ": "Toggle event as done",
        "   .   ": "Etkinlik gizliliğini aç / kapat",
        "   C   ": "Calcurse'den etkinlikleri içe aktarma",
        "   R   ": "Geçerli aya (güne) dön",
        }

KEYS_TODO = {
        "  a(A) ": "Yeni (alt) görev ekle",
        "  h(H) ": "Görevlerden birini (tümünü) yüksek öncelikli olarak değiştirin",
        "  l(L) ": "Görevlerden birini (tümünü) düşük öncelikli olarak değiştirin",
        "  d(D) ": "Görevlerden birini (tümünü) yapıldı olarak değiştirin",
        "  u(U) ": "Görevlerden birinin (tümünün) işaretini kaldırın",
        "  x(X) ": "Görevlerden birini (tümünü) silme (tüm alt görevlerle birlikte)",
        "  t(T) ": "Bir görev için zamanlayıcıyı başlatma/duraklatma (kaldırma)",
        "  e,c  ": "Görev düzenleme",
        "   s   ": "Görev ve alt görev arasında geçiş yapma",
        "   .   ": "Görev gizliliğini aç / kapat",
        "  f(F) ": "Görev son tarihini değiştir (kaldır)",
        "   m   ": "Görev taşıma",
        "  C(W) ": "Calcurse'den görevleri içe aktarma (taskwarrior)",
        }

MSG_NAME          = "CALCURE"
MSG_VIM           = "Vim tuşları (j, k, ZZ, ZQ) da çalışıyor!"
MSG_INFO          = "Daha fazla bilgi için ziyaret edin:"
MSG_SITE          = "https://anufrievroman.gitbook.io/calcure"
MSG_EXIT          = "Gerçekten çıkıyorsun musun? (y/n) "

MSG_EVENT_HIGH    = "Yüksek öncelikli olay numarası olarak işaretle: "
MSG_EVENT_LOW     = "Düşük öncelikli olay numarası olarak işaretle: "
MSG_EVENT_DONE    = "Mark as done event number: "
MSG_EVENT_RESET   = "Etkinlik numarası için durumu sıfırla: "
MSG_EVENT_DEL     = "Etkinlik numarasını sil: "
MSG_EVENT_REN     = "Etkinlik numarasını yeniden adlandır: "
MSG_NEW_TITLE     = "Yeni başlık girin: "
MSG_EVENT_MV      = "Etkinlik numarasını taşı: "
MSG_EVENT_MV_TO   = "Etkinliği şuraya taşı (YYYY/MM/DD): "
MSG_EVENT_MV_TO_D = "Etkinliği şuraya taşı: "
MSG_EVENT_DATE    = "Tarih girin: "
MSG_EVENT_TITLE   = "Başlığı girin: "
MSG_EVENT_REP     = "Etkinliğin kaç kez tekrarlanacağı: "
MSG_EVENT_FR      = "Etkinliği her gün(d), hafta(w), ay(m) veya yıl(y) tekrarlayın? "
MSG_EVENT_IMP     = "Calcurse'den etkinlikleri içe aktarma? (y/n)"
MSG_EVENT_PRIVACY = "Etkinlik numarasının gizliliğini aç / kapat: "
MSG_TM_ADD        = "Görev numarası için zamanlayıcı ekle/duraklat: "
MSG_TM_RESET      = "Görev numarası için zamanlayıcıyı kaldır: "
MSG_TS_HIGH       = "Görev numarasını yüksek öncelikli olarak işaretleyin: "
MSG_TS_LOW        = "Görev numarasını düşük öncelikli olarak işaretleyin: "
MSG_TS_RES        = "Görev numarasının durumunu sıfırla: "
MSG_TS_DONE       = "Görev numarasını tamamlandı olarak işaretle: "
MSG_TS_DEL        = "Görev numarasını sil: "
MSG_TS_DEL_ALL    = "Gerçekten tüm görevleri silecek misiniz? (y/n)"
MSG_TS_EDT_ALL    = "Do you confirm this action? (y/n)"
MSG_TS_MOVE       = "Numaradan görevi taşı: "
MSG_TS_MOVE_TO    = "Görevi numaraya taşı: "
MSG_TS_EDIT       = "Görev numarasını düzenle: "
MSG_TS_TOG        = "Alt görev numarasını değiştir: "
MSG_TS_SUB        = "Görev numarası için alt görev ekleyin: "
MSG_TS_TITLE      = "Alt görev girin: "
MSG_TS_IM         = "Calcurse'den görevleri içe aktarma? (y/n)"
MSG_TS_TW         = "Taskwarrior'dan görevleri içe aktarma? (y/n)"
MSG_TS_NOTHING    = "Planlanmış bir şey yok..."
MSG_TS_PRIVACY    = "Görev numarasının gizliliğini aç / kapat: "
MSG_TS_DEAD_ADD   = "Görev numarası için son tarih ekle: "
MSG_TS_DEAD_DEL   = "Görev numarasının son tarihini kaldırın: "
MSG_TS_DEAD_DATE  = "Son tarih ekleyin (YYYY/MM/DD): "
MSG_WEATHER       = "Hava durumu yükleniyor..."
MSG_ERRORS        = "Errors have occurred. See info.log in your config folder."
MSG_GOTO          = "Go to date (YYYY/MM/DD): "
MSG_GOTO_G        = "Go to date: "
MSG_INPUT         = "Incorrect input."

CALENDAR_HINT     = "Space · Günlüğe geç   a · Etkinlik ekle  n/p · Ayı değiştir   ? · Tüm tuş atamaları"
CALENDAR_HINT_D   = "Space · Günlüğe geç   a · Etkinlik ekle  n/p · Günü değiştir   ? · Tüm tuş atamaları"
JOURNAL_HINT      = "Space · Takvime geç   a · Görev ekle   d · Tamamlandı   i · Önemli   ? · Tüm tuş atamaları"

DAYS = ["PAZARTESİ", "SALI", "ÇARŞAMBA", "PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR"]
DAYS_PERSIAN = ["SHANBEH", "YEKSHANBEH", "DOSHANBEH", "SESHANBEH", "CHAHARSHANBEH", "PANJSHANBEH", "JOMEH"]

MONTHS = ["OCAK", "ŞUBAT", "MART", "NİSAN", "MAYIS", "HAZİRAN", "TEMMUZ", "AĞUSTOS", "EYLÜL", "EKİM", "KASIM", "ARALIK"]
MONTHS_PERSIAN = ["FARVARDIN", "ORDIBEHESHT", "KHORDAD", "TIR", "MORDAD", "SHAHRIVAR", "MEHR", "ABAN", "AZAR", "DEY", "BAHMAN", "ESFAND"]
