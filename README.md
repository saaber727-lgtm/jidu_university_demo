# JIDU Raqamli universitet portali — Demo

Jahon iqtisodiyoti va diplomatiya universiteti (JIDU / УМЭД / UWED) uchun demo talaba kabineti va administrator paneli.
Interfeys 3 tilda: **o‘zbek**, **rus** va **ingliz** (sahifaning yuqori o‘ng burchagidagi tugmalar orqali almashtiriladi).

## Ishga tushirish (Windows / VS Code)

1. Loyiha papkasini VS Code’da oching va terminalni oching (`Ctrl + ~`).
2. Virtual muhit yarating va faollashtiring:

```powershell
python -m venv venv
venv\Scripts\activate
```

> PowerShell “running scripts is disabled” xatosini bersa, avval bir marta:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

3. Kutubxonalarni o‘rnating:

```powershell
pip install -r requirements.txt
```

4. Saytni ishga tushiring:

```powershell
streamlit run app.py
```

Brauzer avtomatik ochiladi: <http://localhost:8501>. Til URL orqali ham tanlanadi:
`http://localhost:8501/?lang=ru` yoki `?lang=en`.

To‘xtatish uchun terminalda `Ctrl + C` bosing.

## Demo loginlar

| Kirish turi   | Login     | Parol        |
|---------------|-----------|--------------|
| Talaba        | `student` | `student123` |
| Administrator | `admin`   | `admin123`   |

Kirish sahifasida avval **Kirish turi**ni tanlang (Talaba yoki Administrator), so‘ng login va parolni kiriting.

## Imkoniyatlar

- JIDU uslubidagi bosh sahifa (universitet haqida, fakultetlar, aloqa)
- Talaba kabineti: bosh sahifa, bugungi darslar, fanlar, tanlov fanlarini tanlash, haftalik jadval, baholar (100 ballik, harfli va 5 ballik), 1–8-semestr o‘quv reja
- Administrator: talabalar, fanlar (3 tilda nom), xonalar, dars jadvali (vaqt to‘qnashuvini tekshirish, o‘chirish), baholar
- SQLite ma’lumotlar bazasi (`jidu_demo.db` birinchi ishga tushirishda avtomatik yaratiladi)

## Fayllar

- `app.py` — asosiy ilova
- `i18n.py` — interfeys matnlarining o‘zbek/rus/ingliz tarjimalari
- `data.py` — o‘quv reja, xonalar, fakultetlar va ularning tarjimalari

Bazani boshlang‘ich holatga qaytarish uchun ilovani to‘xtating va `jidu_demo.db` faylini o‘chiring.

## Muhim eslatma

Talabalar, guruhlar, xonalar, dars jadvali va baholar demo ma’lumotlaridir — ular JIDUning rasmiy ma’lumotlari emas.
Ommaviy serverga joylashdan oldin demo parollarni almashtiring va xavfsizlikni kuchaytiring.
