"""O‘quv reja, namunaviy ma’lumotlar va ularning rus/ingliz tilidagi tarjimalari."""
import re

LANG_INDEX = {"ru": 0, "en": 1}

# (kurs, semestr, fan nomi, turi, modul)
COURSES = [
    (1, 1, "Asosiy chet tili 1", "Majburiy", ""),
    (1, 1, "O‘zbek / Rus tili 1", "Majburiy", ""),
    (1, 1, "Iqtisodiyot nazariyasi", "Majburiy", ""),
    (1, 1, "Falsafa", "Majburiy", ""),
    (1, 1, "Hisoblash 1", "Majburiy", ""),
    (1, 1, "Iqtisodiyotda axborot texnologiyalari", "Majburiy", ""),
    (1, 1, "Jismoniy madaniyat va sport", "Majburiy", ""),
    (1, 2, "Asosiy chet tili 2", "Majburiy", ""),
    (1, 2, "O‘zbek / Rus tili 2", "Majburiy", ""),
    (1, 2, "Hisoblash 2", "Majburiy", ""),
    (1, 2, "Jamiyat va din", "Majburiy", ""),
    (1, 2, "Diplomatiya asoslari", "Majburiy", ""),
    (1, 2, "Akademik yozuv", "Majburiy", ""),
    (1, 2, "Davlat va huquq nazariyasi", "Majburiy", ""),
    (2, 3, "Asosiy chet tili 3 / Ingliz tili", "Majburiy", ""),
    (2, 3, "Ikkinchi chet tili 1", "Majburiy", ""),
    (2, 3, "Menejment", "Majburiy", ""),
    (2, 3, "Mikroiqtisodiyot", "Majburiy", ""),
    (2, 3, "Iqtisodiyotda miqdoriy usullar", "Majburiy", ""),
    (2, 3, "Arab tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Fors tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Fransuz tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Hind tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Ispan tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Italyan tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Koreys tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Nemis tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Turk tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Urdu tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Xitoy tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Yapon tili", "Tanlov", "Ikkinchi til 1"),
    (2, 3, "Biznes asoslari", "Tanlov", "Umumiy tanlov"),
    (2, 3, "Mediya asoslari", "Tanlov", "Umumiy tanlov"),
    (2, 3, "Pythonda dasturlash asoslari", "Tanlov", "Umumiy tanlov"),
    (2, 3, "Boshqaruv hisobi", "Tanlov", "Umumiy tanlov"),
    (2, 3, "Xalqaro turizm", "Tanlov", "Umumiy tanlov"),
    (2, 3, "Atrof-muhit siyosati", "Tanlov", "Umumiy tanlov"),
    (2, 3, "Barqarorlik fanlari", "Tanlov", "Umumiy tanlov"),
    (2, 4, "Asosiy chet tili 4", "Majburiy", ""),
    (2, 4, "Ikkinchi chet tili 2", "Majburiy", ""),
    (2, 4, "Makroiqtisodiyot", "Majburiy", ""),
    (2, 4, "Marketing", "Majburiy", ""),
    (2, 4, "Ehtimollik va statistika", "Majburiy", ""),
    (2, 4, "Moliyaviy hisob", "Tanlov", ""),
    (2, 4, "Moliyaviy matematika va modellashtirish", "Tanlov", ""),
    (2, 4, "Ma’lumotlar vizualizatsiyasi va biznes tahlil", "Tanlov", ""),
    (2, 4, "Boshqaruv qarorlarini qabul qilish usullari", "Tanlov", ""),
    (2, 4, "Yashil iqtisodiyot", "Tanlov", ""),
    (2, 4, "Mutaxassisning nutq madaniyati va notiqlik san’ati", "Tanlov", ""),
    (3, 5, "Ikkinchi chet tili 3", "Majburiy", ""),
    (3, 5, "Jahon iqtisodiyoti", "Majburiy", ""),
    (3, 5, "Ekonometrika", "Majburiy", ""),
    (3, 5, "Xalqaro marketing", "Majburiy", ""),
    (3, 5, "Rivojlanish iqtisodiyoti", "Majburiy", ""),
    (3, 5, "Soliq va soliqqa tortish", "Tanlov", ""),
    (3, 5, "Iqtisodchilar uchun o‘yinlar nazariyasi", "Tanlov", ""),
    (3, 5, "Rivojlanishni moliyalashtirish", "Tanlov", ""),
    (3, 5, "Loyihalarni boshqarish", "Tanlov", ""),
    (3, 5, "Bank ishi", "Tanlov", ""),
    (3, 5, "Zamonaviy xalqaro munosabatlar, jahon iqtisodiyoti va O‘zbekiston manfaatlari", "Tanlov", ""),
    (3, 5, "Energetika iqtisodiyoti", "Tanlov", ""),
    (3, 6, "Energetika iqtisodiyoti", "Majburiy", ""),
    (3, 6, "Ikkinchi chet tili 4", "Majburiy", ""),
    (3, 6, "Xalqaro mikroiqtisodiyot", "Majburiy", ""),
    (3, 6, "Xalqaro moliya", "Majburiy", ""),
    (3, 6, "Xalqaro menejment", "Majburiy", ""),
    (3, 6, "Buxgalteriya hisobi", "Tanlov", ""),
    (3, 6, "Vaqt qatorlari tahlili va prognozlash", "Tanlov", ""),
    (3, 6, "Migratsiya iqtisodiyoti", "Tanlov", ""),
    (3, 6, "Xalqaro investitsion faoliyat", "Tanlov", ""),
    (3, 6, "O‘zbekiston Respublikasi Milliy iqtisodiyoti", "Tanlov", ""),
    (3, 6, "Davlat-xususiy sherikchilik", "Tanlov", ""),
    (3, 6, "Moliyaviy menejment", "Tanlov", ""),
    (3, 6, "Zamonaviy xalqaro munosabatlar, jahon iqtisodiyoti va O‘zbekiston manfaatlari", "Tanlov", ""),
    (3, 6, "Rivojlanishni moliyalashtirish institutlari", "Tanlov", ""),
    (3, 6, "Xizmat yozishmalari", "Tanlov", ""),
    (4, 7, "Bitiruv loyiha", "Majburiy", ""),
    (4, 7, "Xalqaro iqtisodiyot 2", "Majburiy", ""),
    (4, 7, "Xalqaro audit", "Tanlov", "1-modul"),
    (4, 7, "Siyosiy iqtisodiyot", "Tanlov", "1-modul"),
    (4, 7, "Xalqaro logistika", "Tanlov", "1-modul"),
    (4, 7, "Iqtisodiyotda katta ma’lumotlarni tahlil qilish", "Tanlov", "1-modul"),
    (4, 7, "Iqtisodiyotda mashinaviy o‘qitish asoslari", "Tanlov", "2-modul"),
    (4, 7, "Xalqaro moliya", "Tanlov", "2-modul"),
    (4, 7, "Madaniyatlararo muloqot va Ispan tili amaliyoti", "Tanlov", "2-modul"),
    (4, 7, "Moliyaviy risklarni boshqarish", "Tanlov", "2-modul"),
    (4, 7, "Innovatsion menejment", "Tanlov", "3-modul"),
    (4, 7, "Xalqaro biznes", "Tanlov", "3-modul"),
    (4, 7, "Makrotahlil", "Tanlov", "3-modul"),
    (4, 7, "Sug‘urta", "Tanlov", "3-modul"),
    (4, 7, "Strategik moliyaviy hisob va moliyaviy hisobotlarni tahlil qilish", "Tanlov", "4-modul"),
    (4, 7, "Strategik menejment", "Tanlov", "4-modul"),
    (4, 7, "Xalqaro moliyaviy texnologiyalar", "Tanlov", "4-modul"),
    (4, 7, "Iqtisodiy diplomatiya", "Tanlov", "5-modul"),
    (4, 7, "Jahon savdo tashkiloti huquqi", "Tanlov", "5-modul"),
    (4, 7, "Xalqaro investitsiya huquqi", "Tanlov", "5-modul"),
    (4, 7, "Xalqaro iqtisodiy huquq", "Tanlov", "5-modul"),
    (4, 7, "Ilmiy tadqiqot asoslari", "Tanlov", "6-modul"),
    (4, 7, "Amaliy keys tadqiqoti", "Tanlov", "6-modul"),
    (4, 7, "Tadbirkorlik asoslari", "Tanlov", "6-modul"),
    (4, 8, "Bitiruv loyiha", "Majburiy", ""),
    (4, 8, "Amaliyot", "Majburiy", ""),
]

# Fan nomlari tarjimasi: o‘zbekcha -> (ruscha, inglizcha)
COURSE_TR = {
    "O‘zbek / Rus tili 1": ("Узбекский / Русский язык 1", "Uzbek / Russian Language 1"),
    "O‘zbek / Rus tili 2": ("Узбекский / Русский язык 2", "Uzbek / Russian Language 2"),
    "Iqtisodiyot nazariyasi": ("Экономическая теория", "Economic Theory"),
    "Falsafa": ("Философия", "Philosophy"),
    "Hisoblash 1": ("Математический анализ 1", "Calculus 1"),
    "Hisoblash 2": ("Математический анализ 2", "Calculus 2"),
    "Iqtisodiyotda axborot texnologiyalari": ("Информационные технологии в экономике", "Information Technology in Economics"),
    "Jismoniy madaniyat va sport": ("Физическая культура и спорт", "Physical Education and Sports"),
    "Jamiyat va din": ("Общество и религия", "Society and Religion"),
    "Diplomatiya asoslari": ("Основы дипломатии", "Fundamentals of Diplomacy"),
    "Akademik yozuv": ("Академическое письмо", "Academic Writing"),
    "Davlat va huquq nazariyasi": ("Теория государства и права", "Theory of State and Law"),
    "Asosiy chet tili 3 / Ingliz tili": ("Основной иностранный язык 3 / Английский язык", "Primary Foreign Language 3 / English"),
    "Menejment": ("Менеджмент", "Management"),
    "Mikroiqtisodiyot": ("Микроэкономика", "Microeconomics"),
    "Iqtisodiyotda miqdoriy usullar": ("Количественные методы в экономике", "Quantitative Methods in Economics"),
    "Arab tili": ("Арабский язык", "Arabic"),
    "Fors tili": ("Персидский язык", "Persian"),
    "Fransuz tili": ("Французский язык", "French"),
    "Hind tili": ("Хинди", "Hindi"),
    "Ispan tili": ("Испанский язык", "Spanish"),
    "Italyan tili": ("Итальянский язык", "Italian"),
    "Koreys tili": ("Корейский язык", "Korean"),
    "Nemis tili": ("Немецкий язык", "German"),
    "Turk tili": ("Турецкий язык", "Turkish"),
    "Urdu tili": ("Урду", "Urdu"),
    "Xitoy tili": ("Китайский язык", "Chinese"),
    "Yapon tili": ("Японский язык", "Japanese"),
    "Biznes asoslari": ("Основы бизнеса", "Business Fundamentals"),
    "Mediya asoslari": ("Основы медиа", "Media Fundamentals"),
    "Pythonda dasturlash asoslari": ("Основы программирования на Python", "Programming Fundamentals in Python"),
    "Boshqaruv hisobi": ("Управленческий учёт", "Management Accounting"),
    "Xalqaro turizm": ("Международный туризм", "International Tourism"),
    "Atrof-muhit siyosati": ("Экологическая политика", "Environmental Policy"),
    "Barqarorlik fanlari": ("Науки об устойчивом развитии", "Sustainability Studies"),
    "Makroiqtisodiyot": ("Макроэкономика", "Macroeconomics"),
    "Marketing": ("Маркетинг", "Marketing"),
    "Ehtimollik va statistika": ("Теория вероятностей и статистика", "Probability and Statistics"),
    "Moliyaviy hisob": ("Финансовый учёт", "Financial Accounting"),
    "Moliyaviy matematika va modellashtirish": ("Финансовая математика и моделирование", "Financial Mathematics and Modelling"),
    "Ma’lumotlar vizualizatsiyasi va biznes tahlil": ("Визуализация данных и бизнес-аналитика", "Data Visualization and Business Analytics"),
    "Boshqaruv qarorlarini qabul qilish usullari": ("Методы принятия управленческих решений", "Managerial Decision-Making Methods"),
    "Yashil iqtisodiyot": ("Зелёная экономика", "Green Economy"),
    "Mutaxassisning nutq madaniyati va notiqlik san’ati": ("Культура речи и ораторское искусство специалиста", "Professional Speech Culture and Public Speaking"),
    "Jahon iqtisodiyoti": ("Мировая экономика", "World Economy"),
    "Ekonometrika": ("Эконометрика", "Econometrics"),
    "Xalqaro marketing": ("Международный маркетинг", "International Marketing"),
    "Rivojlanish iqtisodiyoti": ("Экономика развития", "Development Economics"),
    "Soliq va soliqqa tortish": ("Налоги и налогообложение", "Taxes and Taxation"),
    "Iqtisodchilar uchun o‘yinlar nazariyasi": ("Теория игр для экономистов", "Game Theory for Economists"),
    "Rivojlanishni moliyalashtirish": ("Финансирование развития", "Development Finance"),
    "Loyihalarni boshqarish": ("Управление проектами", "Project Management"),
    "Bank ishi": ("Банковское дело", "Banking"),
    "Zamonaviy xalqaro munosabatlar, jahon iqtisodiyoti va O‘zbekiston manfaatlari": (
        "Современные международные отношения, мировая экономика и интересы Узбекистана",
        "Contemporary International Relations, the World Economy and Uzbekistan’s Interests",
    ),
    "Energetika iqtisodiyoti": ("Экономика энергетики", "Energy Economics"),
    "Xalqaro mikroiqtisodiyot": ("Международная микроэкономика", "International Microeconomics"),
    "Xalqaro moliya": ("Международные финансы", "International Finance"),
    "Xalqaro menejment": ("Международный менеджмент", "International Management"),
    "Buxgalteriya hisobi": ("Бухгалтерский учёт", "Accounting"),
    "Vaqt qatorlari tahlili va prognozlash": ("Анализ временных рядов и прогнозирование", "Time Series Analysis and Forecasting"),
    "Migratsiya iqtisodiyoti": ("Экономика миграции", "Migration Economics"),
    "Xalqaro investitsion faoliyat": ("Международная инвестиционная деятельность", "International Investment Activity"),
    "O‘zbekiston Respublikasi Milliy iqtisodiyoti": ("Национальная экономика Республики Узбекистан", "National Economy of the Republic of Uzbekistan"),
    "Davlat-xususiy sherikchilik": ("Государственно-частное партнёрство", "Public-Private Partnership"),
    "Moliyaviy menejment": ("Финансовый менеджмент", "Financial Management"),
    "Rivojlanishni moliyalashtirish institutlari": ("Институты финансирования развития", "Development Finance Institutions"),
    "Xizmat yozishmalari": ("Деловая переписка", "Business Correspondence"),
    "Bitiruv loyiha": ("Выпускной проект", "Graduation Project"),
    "Xalqaro iqtisodiyot 2": ("Международная экономика 2", "International Economics 2"),
    "Xalqaro audit": ("Международный аудит", "International Audit"),
    "Siyosiy iqtisodiyot": ("Политическая экономия", "Political Economy"),
    "Xalqaro logistika": ("Международная логистика", "International Logistics"),
    "Iqtisodiyotda katta ma’lumotlarni tahlil qilish": ("Анализ больших данных в экономике", "Big Data Analytics in Economics"),
    "Iqtisodiyotda mashinaviy o‘qitish asoslari": ("Основы машинного обучения в экономике", "Fundamentals of Machine Learning in Economics"),
    "Madaniyatlararo muloqot va Ispan tili amaliyoti": ("Межкультурная коммуникация и практика испанского языка", "Intercultural Communication and Spanish Language Practice"),
    "Moliyaviy risklarni boshqarish": ("Управление финансовыми рисками", "Financial Risk Management"),
    "Innovatsion menejment": ("Инновационный менеджмент", "Innovation Management"),
    "Xalqaro biznes": ("Международный бизнес", "International Business"),
    "Makrotahlil": ("Макроэкономический анализ", "Macroeconomic Analysis"),
    "Sug‘urta": ("Страхование", "Insurance"),
    "Strategik moliyaviy hisob va moliyaviy hisobotlarni tahlil qilish": (
        "Стратегический финансовый учёт и анализ финансовой отчётности",
        "Strategic Financial Accounting and Financial Statement Analysis",
    ),
    "Strategik menejment": ("Стратегический менеджмент", "Strategic Management"),
    "Xalqaro moliyaviy texnologiyalar": ("Международные финансовые технологии", "International Financial Technologies"),
    "Iqtisodiy diplomatiya": ("Экономическая дипломатия", "Economic Diplomacy"),
    "Jahon savdo tashkiloti huquqi": ("Право Всемирной торговой организации", "World Trade Organization Law"),
    "Xalqaro investitsiya huquqi": ("Международное инвестиционное право", "International Investment Law"),
    "Xalqaro iqtisodiy huquq": ("Международное экономическое право", "International Economic Law"),
    "Ilmiy tadqiqot asoslari": ("Основы научных исследований", "Research Fundamentals"),
    "Amaliy keys tadqiqoti": ("Прикладное кейс-исследование", "Applied Case Study"),
    "Tadbirkorlik asoslari": ("Основы предпринимательства", "Fundamentals of Entrepreneurship"),
    "Amaliyot": ("Практика", "Internship"),
}
for _n in range(1, 5):
    COURSE_TR[f"Asosiy chet tili {_n}"] = (f"Основной иностранный язык {_n}", f"Primary Foreign Language {_n}")
    COURSE_TR[f"Ikkinchi chet tili {_n}"] = (f"Второй иностранный язык {_n}", f"Second Foreign Language {_n}")

ROOMS = [
    ("A-204", "A bino", "Dars xonasi", 30),
    ("B-301", "B bino", "Seminar xonasi", 24),
    ("C-105", "C bino", "Auditoriya", 40),
    ("L-02", "Asosiy bino", "Leksiya zali", 180),
    ("S-01", "Asosiy bino", "Seminar xonasi", 20),
    ("A-101", "A bino", "Dars xonasi", 35),
    ("K-110", "Asosiy bino", "Kompyuter xonasi", 28),
]

FACULTIES = {
    "Xalqaro munosabatlar fakulteti": ("Факультет международных отношений", "Faculty of International Relations"),
    "Xalqaro huquq fakulteti": ("Факультет международного права", "Faculty of International Law"),
    "Xalqaro iqtisodiyot va menejment fakulteti": ("Факультет международной экономики и менеджмента", "Faculty of International Economics and Management"),
}

PROGRAMS = {
    "Jahon iqtisodiyoti": ("Мировая экономика", "World Economy"),
    "Xalqaro munosabatlar": ("Международные отношения", "International Relations"),
    "Xalqaro huquq": ("Международное право", "International Law"),
    "Siyosatshunoslik": ("Политология", "Political Science"),
    "Menejment": ("Менеджмент", "Management"),
}

DAYS = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"]
_DAY_TR = {
    "Dushanba": ("Понедельник", "Monday"),
    "Seshanba": ("Вторник", "Tuesday"),
    "Chorshanba": ("Среда", "Wednesday"),
    "Payshanba": ("Четверг", "Thursday"),
    "Juma": ("Пятница", "Friday"),
    "Shanba": ("Суббота", "Saturday"),
}

KINDS = ["Majburiy", "Tanlov"]
_KIND_TR = {"Majburiy": ("Обязательная", "Core"), "Tanlov": ("По выбору", "Elective")}

ROOM_KINDS = ["Dars xonasi", "Seminar xonasi", "Auditoriya", "Leksiya zali", "Kompyuter xonasi"]
_ROOM_KIND_TR = {
    "Dars xonasi": ("Учебная аудитория", "Classroom"),
    "Seminar xonasi": ("Семинарская аудитория", "Seminar room"),
    "Auditoriya": ("Аудитория", "Auditorium"),
    "Leksiya zali": ("Лекционный зал", "Lecture hall"),
    "Kompyuter xonasi": ("Компьютерный класс", "Computer lab"),
}

_MODULE_TR = {
    "Ikkinchi til 1": ("Второй язык 1", "Second language 1"),
    "Umumiy tanlov": ("Общий выбор", "General elective"),
}


def _lookup(value, table, lang):
    if lang == "uz" or not value:
        return value
    return table.get(value, (value, value))[LANG_INDEX[lang]]


def tr_kind(v, lang):
    return _lookup(v, _KIND_TR, lang)


def tr_day(v, lang):
    return _lookup(v, _DAY_TR, lang)


def tr_room_kind(v, lang):
    return _lookup(v, _ROOM_KIND_TR, lang)


def tr_faculty(v, lang):
    return _lookup(v, FACULTIES, lang)


def tr_program(v, lang):
    return _lookup(v, PROGRAMS, lang)


def tr_module(v, lang):
    if lang == "uz" or not v:
        return v
    m = re.fullmatch(r"(\d+)-modul", v)
    if m:
        return ("Модуль {}" if lang == "ru" else "Module {}").format(m.group(1))
    return _lookup(v, _MODULE_TR, lang)


def tr_building(v, lang):
    if lang == "uz" or not v:
        return v
    if v == "Asosiy bino":
        return "Главный корпус" if lang == "ru" else "Main building"
    m = re.fullmatch(r"(\S+) bino", v)
    if m:
        return ("Корпус {}" if lang == "ru" else "Building {}").format(m.group(1))
    return v
