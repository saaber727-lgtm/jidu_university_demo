# JIDU University Management System — Demo

Jahon Iqtisodiyoti va Diplomatiya Universiteti uchun demo Student Portal va Admin Dashboard.

## Ishga tushirish (Windows / VS Code)

1. ZIP faylni oching va papkani VS Code orqali oching.
2. Terminalda virtual muhit yarating:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Kutubxonalarni o‘rnating:

```bash
pip install -r requirements.txt
```

4. Saytni ishga tushiring:

```bash
streamlit run app.py
```

Brauzerda odatda `http://localhost:8501` ochiladi.

## Demo loginlar

- Talaba: `student` / `student123`
- Administrator: `admin` / `admin123`

## Nimalar mavjud?

- JIDU uchun demo bosh sahifa
- Talaba login/parol orqali shaxsiy kabinet
- 1–8-semestr o‘quv rejasi
- Majburiy va tanlov fanlari
- 3-kurs namunaviy talaba va jadval
- Fanlar bo‘yicha baholar
- Admin: talabalar, fanlar, xonalar, dars jadvali va baholarni boshqarish
- SQLite ma’lumotlar bazasi

## Muhim eslatma

Talabalar soni, loginlar, guruhlar, xonalar, dars jadvali va baholar demo ma’lumotlaridir. Ular JIDUning tasdiqlangan rasmiy statistikasi yoki haqiqiy talabalar yozuvlari emas.

Bu prototip internetga joylashtirishga tayyor dastlabki versiya. Barcha talabalar bir xil umumiy link orqali kirishi uchun Streamlit Community Cloud yoki boshqa hostingga deploy qilish kerak. Ommaviy ishga tushirishdan oldin parol saqlashini, sessiyalarni, rol tekshiruvlarini, maxfiylikni va admin xavfsizligini kuchaytirish zarur. Demo parollarini ommaviy serverda ishlatmang.
