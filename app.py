"""JIDU — Jahon iqtisodiyoti va diplomatiya universiteti: raqamli portal (demo)."""
import base64
import hashlib
import hmac
import html
import os
import sqlite3
from contextlib import closing
from datetime import datetime, time
from pathlib import Path

import streamlit as st

from data import (
    COURSE_TR, COURSES, DAYS, FACULTIES, KINDS, PROGRAMS, ROOM_KINDS, ROOMS,
    tr_building, tr_day, tr_faculty, tr_kind, tr_module, tr_program, tr_room_kind,
)
from i18n import LANGS, tr

DB_PATH = Path(__file__).with_name("jidu_demo.db")
PHOTO_PATH = Path(__file__).with_name("assets") / "jidu_hall.jpg"

st.set_page_config(page_title="JIDU | UWED Portal", page_icon="🎓", layout="wide")

# ---------------------------------------------------------------- Til (language)
if "lang" not in st.session_state:
    _qp = st.query_params.get("lang")
    st.session_state.lang = _qp if _qp in LANGS else "uz"


def lang():
    return st.session_state.lang


def t(key, **kw):
    return tr(key, lang(), **kw)


# ---------------------------------------------------------------- Ma’lumotlar bazasi
def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def q(sql, params=()):
    """SELECT natijasini oddiy dict ro‘yxati sifatida qaytaradi (Streamlit vidjetlari uchun xavfsiz)."""
    with closing(connect()) as c:
        return [dict(r) for r in c.execute(sql, params).fetchall()]


def q1(sql, params=()):
    rows = q(sql, params)
    return rows[0] if rows else None


def run(sql, params=()):
    with closing(connect()) as c:
        with c:
            c.execute(sql, params)


# ---------------------------------------------------------------- Parollar
def pw_hash(password, salt=None):
    salt = salt or os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return f"pbkdf2${salt.hex()}${dk.hex()}"


def pw_verify(password, stored):
    if stored and stored.startswith("pbkdf2$"):
        _, salt_hex, _ = stored.split("$")
        return hmac.compare_digest(pw_hash(password, bytes.fromhex(salt_hex)), stored)
    # Eski versiyadagi tuzsiz SHA-256 xeshlar bilan moslik
    legacy = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return bool(stored) and hmac.compare_digest(legacy, stored)


SCHEMA = """
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT,
    full_name TEXT, student_id TEXT, faculty TEXT, program TEXT, year INTEGER, group_name TEXT);
CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER, semester INTEGER, name TEXT,
    kind TEXT, module TEXT DEFAULT '', name_ru TEXT DEFAULT '', name_en TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS enrollments(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, course_id INTEGER,
    UNIQUE(user_id, course_id));
CREATE TABLE IF NOT EXISTS grades(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, course_id INTEGER, score REAL,
    letter TEXT, updated TEXT, UNIQUE(user_id, course_id));
CREATE TABLE IF NOT EXISTS rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, building TEXT, kind TEXT,
    capacity INTEGER);
CREATE TABLE IF NOT EXISTS schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER, semester INTEGER,
    group_name TEXT, day TEXT, start_time TEXT, end_time TEXT, course_id INTEGER, room_id INTEGER, teacher TEXT);
"""


def letter_grade(score):
    return "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"


def national_grade(score):
    """O‘zbekistondagi 5 ballik baholash tizimi."""
    return 5 if score >= 86 else 4 if score >= 71 else 3 if score >= 55 else 2


@st.cache_resource
def init_db():
    with closing(connect()) as c:
        c.executescript(SCHEMA)
        # Eski bazalar uchun migratsiya: tarjima ustunlari
        cols = {r["name"] for r in c.execute("PRAGMA table_info(courses)")}
        for col in ("name_ru", "name_en"):
            if col not in cols:
                c.execute(f"ALTER TABLE courses ADD COLUMN {col} TEXT DEFAULT ''")

        if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            c.execute("INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",
                      ("admin", pw_hash("admin123"), "admin", "JIDU Administrator"))
            c.execute("""INSERT INTO users(username,password,role,full_name,student_id,faculty,program,year,group_name)
                         VALUES(?,?,?,?,?,?,?,?,?)""",
                      ("student", pw_hash("student123"), "student", "Aliyev Azizbek", "JIDU-2025-001",
                       "Xalqaro iqtisodiyot va menejment fakulteti", "Jahon iqtisodiyoti", 2, "XIM-21"))
            c.executemany("INSERT INTO courses(year,semester,name,kind,module) VALUES(?,?,?,?,?)", COURSES)
            c.executemany("INSERT INTO rooms(code,building,kind,capacity) VALUES(?,?,?,?)", ROOMS)

            uid = c.execute("SELECT id FROM users WHERE username='student'").fetchone()[0]
            sample_scores = [91, 84, 77, 88, 69, 95, 73, 86]
            core = c.execute("SELECT id, semester FROM courses WHERE semester<=3 AND kind='Majburiy' ORDER BY id").fetchall()
            for i, cr in enumerate(core):
                c.execute("INSERT OR IGNORE INTO enrollments(user_id,course_id) VALUES(?,?)", (uid, cr["id"]))
                if cr["semester"] < 3 or i % 2 == 0:  # joriy semestrda baholarning bir qismi kiritilgan
                    s = sample_scores[i % len(sample_scores)]
                    c.execute("INSERT OR IGNORE INTO grades(user_id,course_id,score,letter,updated) VALUES(?,?,?,?,?)",
                              (uid, cr["id"], s, letter_grade(s), "2026-11-10" if cr["semester"] == 3 else "2026-06-20"))

            ids = {r["name"]: r["id"] for r in c.execute("SELECT id,name FROM courses WHERE semester=3")}
            room = {r["code"]: r["id"] for r in c.execute("SELECT id,code FROM rooms")}
            rows = [
                ("Dushanba", "09:00", "10:20", "Menejment", "A-204", "PhD. Karimova M."),
                ("Dushanba", "10:30", "11:50", "Mikroiqtisodiyot", "L-02", "PhD. Rahimov A."),
                ("Seshanba", "09:00", "10:20", "Asosiy chet tili 3 / Ingliz tili", "C-105", "J. Smith"),
                ("Seshanba", "12:00", "13:20", "Mikroiqtisodiyot", "B-301", "PhD. Rahimov A."),
                ("Chorshanba", "13:30", "14:50", "Iqtisodiyotda miqdoriy usullar", "K-110", "DSc. Tursunov B."),
                ("Payshanba", "11:00", "12:20", "Ikkinchi chet tili 1", "S-01", "L. Chen"),
                ("Juma", "09:00", "10:20", "Menejment", "A-101", "PhD. Karimova M."),
            ]
            c.executemany(
                "INSERT INTO schedule(year,semester,group_name,day,start_time,end_time,course_id,room_id,teacher) "
                "VALUES(2,3,'XIM-21',?,?,?,?,?,?)",
                [(d, s, e, ids[n], room[r], tch) for d, s, e, n, r, tch in rows],
            )

        # Fan nomlari tarjimalarini to‘ldirish (yangi va eski bazalar uchun)
        for uz, (ru, en) in COURSE_TR.items():
            c.execute("UPDATE courses SET name_ru=? WHERE name=? AND COALESCE(name_ru,'')=''", (ru, uz))
            c.execute("UPDATE courses SET name_en=? WHERE name=? AND COALESCE(name_en,'')=''", (en, uz))
        c.commit()
    return True


init_db()


# ---------------------------------------------------------------- Yordamchi funksiyalar
def cname(row):
    """Fan nomini joriy tilda qaytaradi."""
    if lang() != "uz":
        return row.get(f"name_{lang()}") or row["name"]
    return row["name"]


def course_label(row):
    mod = tr_module(row.get("module") or "", lang())
    return cname(row) + (f" ({mod})" if mod else "")


def esc(v):
    return html.escape(str(v if v is not None else "—"))


def semester_label(s):
    return t("semester_n", n=s)


def year_label(y):
    return t("year_n", n=y)


def day_index(d):
    return DAYS.index(d) if d in DAYS else len(DAYS)


def stat_cards(items):
    cards = "".join(
        f"<div class='jd-stat'><div class='jd-stat-ico'>{ico}</div>"
        f"<div><div class='jd-stat-val'>{esc(val)}</div><div class='jd-stat-lbl'>{esc(lbl)}</div></div></div>"
        for ico, val, lbl in items
    )
    st.markdown(f"<div class='jd-stats'>{cards}</div>", unsafe_allow_html=True)


@st.cache_data
def campus_photo_b64():
    return base64.b64encode(PHOTO_PATH.read_bytes()).decode()


def section(title, subtitle=None):
    sub = f"<div class='jd-section-sub'>{esc(subtitle)}</div>" if subtitle else ""
    st.markdown(f"<div class='jd-section'><h2>{esc(title)}</h2>{sub}</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------- Dizayn
st.markdown("""
<style>
:root{--jd-navy:#0B2B5C;--jd-navy-2:#164A8A;--jd-gold:#C9A54B;--jd-gold-soft:#F4ECD6;
      --jd-ink:#14233A;--jd-muted:#5B6B82;--jd-line:#E3E8F0;--jd-card:#FFFFFF;}
.block-container{padding-top:3.2rem;max-width:1240px}
h1,h2,h3{color:var(--jd-navy)}
.jd-hero{position:relative;overflow:hidden;border-radius:18px;padding:26px 30px;color:#fff;
  background:radial-gradient(1200px 400px at 85% -20%,rgba(201,165,75,.28),transparent 60%),
             linear-gradient(115deg,#071F45 0%,#0B2B5C 45%,#164A8A 100%);
  box-shadow:0 10px 30px rgba(11,43,92,.18);display:flex;gap:22px;align-items:center}
.jd-hero:after{content:"";position:absolute;left:0;right:0;bottom:0;height:5px;
  background:linear-gradient(90deg,var(--jd-gold),#E9D18F,var(--jd-gold))}
.jd-emblem{flex:0 0 auto;width:78px;height:78px;border-radius:50%;border:3px solid var(--jd-gold);
  display:flex;align-items:center;justify-content:center;flex-direction:column;
  background:rgba(255,255,255,.06);font-family:Georgia,'Times New Roman',serif}
.jd-emblem b{font-size:17px;letter-spacing:.5px;color:#fff;line-height:1}
.jd-emblem small{font-size:9px;letter-spacing:2px;color:var(--jd-gold);margin-top:3px}
.jd-kicker{font-size:12px;letter-spacing:2.5px;text-transform:uppercase;color:#E9D18F;opacity:.95}
.jd-title{font-family:Georgia,'Times New Roman',serif;font-size:30px;font-weight:700;line-height:1.2;margin:4px 0}
.jd-sub{opacity:.85;font-size:15px}
@media (max-width:700px){.jd-hero{flex-direction:column;align-items:flex-start;padding:22px}
  .jd-title{font-size:23px}}
.jd-section{margin:22px 0 10px}
.jd-section h2{font-family:Georgia,'Times New Roman',serif;font-size:26px;margin:0;padding:0;
  border-left:5px solid var(--jd-gold);padding-left:12px}
.jd-section-sub{color:var(--jd-muted);margin:4px 0 0 17px}
.jd-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:12px 0 18px}
.jd-stat{background:var(--jd-card);border:1px solid var(--jd-line);border-radius:14px;padding:16px 18px;
  display:flex;gap:14px;align-items:center;box-shadow:0 2px 8px rgba(11,43,92,.05)}
.jd-stat-ico{width:44px;height:44px;border-radius:12px;background:var(--jd-gold-soft);display:flex;
  align-items:center;justify-content:center;font-size:22px;flex:0 0 auto}
.jd-stat-val{font-size:22px;font-weight:700;color:var(--jd-navy);line-height:1.1}
.jd-stat-lbl{font-size:13px;color:var(--jd-muted)}
.jd-card{background:var(--jd-card);border:1px solid var(--jd-line);border-radius:16px;padding:20px 22px;
  box-shadow:0 2px 10px rgba(11,43,92,.05);margin-bottom:14px}
.jd-card h4{margin:0 0 10px;color:var(--jd-navy);font-size:17px}
.jd-list{margin:0;padding-left:0;list-style:none}
.jd-list li{padding:7px 0;border-bottom:1px dashed var(--jd-line)}
.jd-list li:last-child{border-bottom:none}
.jd-profile{display:flex;gap:18px;align-items:center}
.jd-avatar{width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,var(--jd-navy),var(--jd-navy-2));
  color:#fff;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;
  border:3px solid var(--jd-gold);flex:0 0 auto}
.jd-kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px 24px;margin-top:14px}
.jd-kv div span{display:block;font-size:12px;color:var(--jd-muted);text-transform:uppercase;letter-spacing:.6px}
.jd-kv div b{color:var(--jd-ink);font-weight:600}
.jd-day{background:var(--jd-card);border:1px solid var(--jd-line);border-radius:14px;margin-bottom:12px;overflow:hidden}
.jd-day-h{background:#F1F4F9;padding:9px 16px;font-weight:700;color:var(--jd-navy);display:flex;justify-content:space-between}
.jd-day.today{border-color:var(--jd-gold);box-shadow:0 0 0 2px var(--jd-gold-soft)}
.jd-day.today .jd-day-h{background:var(--jd-gold-soft)}
.jd-lesson{display:flex;gap:16px;padding:12px 16px;border-top:1px solid var(--jd-line)}
.jd-time{flex:0 0 auto;min-width:96px;font-weight:700;color:var(--jd-navy-2);font-variant-numeric:tabular-nums}
.jd-lesson-meta{color:var(--jd-muted);font-size:13px;margin-top:2px}
.jd-badge{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:20px;margin-left:6px;
  vertical-align:middle}
.jd-core{background:#E3ECF8;color:var(--jd-navy)}
.jd-elec{background:var(--jd-gold-soft);color:#7A5A12}
.jd-course{padding:9px 0;border-bottom:1px solid var(--jd-line)}
.jd-course:last-child{border-bottom:none}
.jd-footer{margin-top:34px;padding:18px 4px 6px;border-top:3px solid var(--jd-gold);color:var(--jd-muted);
  font-size:13px;display:flex;flex-wrap:wrap;gap:6px 24px;justify-content:space-between}
.jd-footer b{color:var(--jd-navy)}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0B2B5C 0%,#0E3770 100%)}
section[data-testid="stSidebar"] *{color:#EEF2F8}
section[data-testid="stSidebar"] .stButton button{background:transparent;border:1px solid var(--jd-gold);color:#fff}
section[data-testid="stSidebar"] .stButton button:hover{background:var(--jd-gold);color:#0B2B5C}
section[data-testid="stSidebar"] [role="radiogroup"] label{padding:6px 10px;border-radius:9px;margin-bottom:2px;width:100%}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.07)}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:rgba(201,165,75,.22);
  box-shadow:inset 3px 0 0 var(--jd-gold)}
.jd-side-brand{font-family:Georgia,serif;font-size:20px;font-weight:700;color:#fff}
.jd-side-brand small{display:block;font-family:inherit;font-size:11px;letter-spacing:1.5px;color:var(--jd-gold)!important;
  font-weight:400;text-transform:uppercase}
.jd-side-user{margin-top:14px;padding:12px;border-radius:12px;background:rgba(255,255,255,.08)}
.jd-side-user small{opacity:.75}
</style>
""", unsafe_allow_html=True)


def lang_switcher():
    codes = list(LANGS)

    def _changed():
        st.session_state.lang = st.session_state._lang_widget
        st.query_params["lang"] = st.session_state.lang

    _, right = st.columns([3, 2])
    with right:
        st.radio("Til / Язык / Language", codes, index=codes.index(lang()), format_func=LANGS.get,
                 key="_lang_widget", horizontal=True, on_change=_changed, label_visibility="collapsed")


def header():
    st.markdown(f"""
    <div class="jd-hero">
      <div class="jd-emblem"><b>{esc(t('uni_short'))}</b><small>1992</small></div>
      <div>
        <div class="jd-kicker">{esc(t('country_line'))}</div>
        <div class="jd-title">{esc(t('uni_name'))}</div>
        <div class="jd-sub">{esc(t('portal_name'))} · {esc(t('portal_tag'))}</div>
      </div>
    </div>""", unsafe_allow_html=True)


def footer():
    st.markdown(f"""
    <div class="jd-footer">
      <div><b>{esc(t('uni_name'))}</b><br>📍 {esc(t('address'))} · 🌐 uwed.uz</div>
      <div style="text-align:right">{esc(t('footer_demo'))}<br>© {datetime.now().year} JIDU Digital University</div>
    </div>""", unsafe_allow_html=True)


lang_switcher()
header()

# ================================================================ KIRISH SAHIFASI
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    # ZUST uslubidagi kirish sahifasi: butun fon — universitet surati
    st.markdown(f"""<style>
    @media (max-width:640px){{[data-testid="stHorizontalBlock"]:has(.st-key-jd_login_card){{flex-direction:column-reverse}}}}
    .stApp{{background:linear-gradient(180deg,rgba(6,22,50,.82) 0%,rgba(11,43,92,.60) 40%,rgba(6,22,50,.90) 100%),
            url(data:image/jpeg;base64,{campus_photo_b64()}) center/cover no-repeat fixed}}
    header[data-testid="stHeader"]{{background:transparent}}
    .st-key-_lang_widget p{{color:#fff!important}}
    .jd-hero{{background:rgba(7,31,69,.50);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.14)}}
    .st-key-jd_login_left .jd-section h2{{color:#fff}}
    .jd-about{{color:#E8EEF7;font-size:16px;line-height:1.65;margin-bottom:6px}}
    .st-key-jd_login_card{{background:#fff;border-radius:18px;padding:26px 24px 18px;
            box-shadow:0 24px 60px rgba(0,0,0,.35);border-top:5px solid var(--jd-gold)}}
    .jd-footer,.jd-footer b{{color:#DCE4F0}}
    .jd-credit{{color:#AFC0D8;font-size:11px;margin-top:8px}}
    .jd-credit a{{color:#AFC0D8}}
    </style>""", unsafe_allow_html=True)

    left, right = st.columns([1.35, 1], gap="large")
    with left, st.container(key="jd_login_left"):
        section(t("about_title"))
        st.markdown(f"<div class='jd-about'>{esc(t('about_text'))}</div>", unsafe_allow_html=True)
        stat_cards([
            ("🏛️", "1992", t("fact_founded")),
            ("🎓", len(FACULTIES), t("fact_faculties")),
            ("📚", "1–8", t("fact_semesters")),
            ("🌍", "12+", t("fact_languages")),
        ])
        fac_items = "".join(f"<li>🏛️ {esc(tr_faculty(f, lang()))}</li>" for f in FACULTIES)
        st.markdown(f"<div class='jd-card'><h4>{esc(t('faculties_title'))}</h4><ul class='jd-list'>{fac_items}</ul></div>",
                    unsafe_allow_html=True)
    with right, st.container(key="jd_login_card"):
        section(t("login_title"), t("login_sub"))
        role_hint = st.selectbox(t("login_role"), ["student", "admin"], format_func=lambda r: t(f"role_{r}"))
        with st.form("login", border=False):
            username = st.text_input(t("username"))
            password = st.text_input(t("password"), type="password")
            submit = st.form_submit_button(t("login_btn"), type="primary", width="stretch")
        if submit:
            username = username.strip()
            if not username or not password:
                st.warning(t("login_empty"))
            else:
                user = q1("SELECT * FROM users WHERE username=?", (username,))
                if user and pw_verify(password, user["password"]) and user["role"] == role_hint:
                    if not user["password"].startswith("pbkdf2$"):  # eski xeshni yangilash
                        run("UPDATE users SET password=? WHERE id=?", (pw_hash(password), user["id"]))
                    user.pop("password", None)
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(t("login_error"))
        with st.expander(t("demo_creds")):
            st.markdown(f"{t('role_student')}: `student` / `student123`  \n{t('role_admin')}: `admin` / `admin123`")
        st.markdown(f"<ul class='jd-list' style='font-size:14px;color:var(--jd-muted)'>"
                    f"<li>📍 {esc(t('address'))}</li><li>🌐 <a href='https://uwed.uz' target='_blank'>uwed.uz</a></li>"
                    f"</ul>", unsafe_allow_html=True)
        st.caption("ℹ️ " + t("demo_notice"))
    footer()
    st.markdown(f"<div class='jd-credit'>📷 {esc(t('photo_credit'))} · <a href='https://commons.wikimedia.org/wiki/"
                f"File:Ambassador_Spratlen_Visits_UWED_(40056516660).jpg' target='_blank'>Wikimedia Commons</a>"
                f" (Public domain)</div>", unsafe_allow_html=True)
    st.stop()

# ================================================================ SIDEBAR
u = st.session_state.user
is_admin = u["role"] == "admin"
PAGES = (["overview", "students", "courses", "rooms", "schedule", "grades_admin"] if is_admin
         else ["dashboard", "my_courses", "schedule", "grades", "curriculum"])
PAGE_ICONS = {"overview": "📊", "students": "👥", "courses": "📚", "rooms": "🏫", "schedule": "📅",
              "grades_admin": "📝", "dashboard": "🏠", "my_courses": "📘", "grades": "📝", "curriculum": "🗂️"}
if st.session_state.get("page") not in PAGES:
    st.session_state.page = PAGES[0]

with st.sidebar:
    who = t("role_admin") if is_admin else f"{t('role_student')} · {u['student_id']}"
    st.markdown(f"<div class='jd-side-brand'>🎓 {esc(t('uni_short'))} Portal<small>{esc(t('portal_name'))}</small></div>"
                f"<div class='jd-side-user'><b>{esc(u['full_name'])}</b><br><small>{esc(who)}</small></div>",
                unsafe_allow_html=True)
    st.write("")
    st.radio(t("nav_admin") if is_admin else t("nav_student"), PAGES, key="page",
             format_func=lambda p: f"{PAGE_ICONS[p]}  {t('p_' + p)}")
    st.divider()
    if st.button(t("logout"), width="stretch"):
        st.session_state.user = None
        st.session_state.pop("page", None)
        st.rerun()

page = st.session_state.page

# ================================================================ TALABA
if not is_admin:
    uid = u["id"]

    if page == "dashboard":
        section(t("p_dashboard"), t("welcome", name=u["full_name"]))
        initials = "".join(p[0] for p in u["full_name"].split()[:2]).upper()
        st.markdown(f"""
        <div class="jd-card"><div class="jd-profile"><div class="jd-avatar">{esc(initials)}</div>
          <div><div style="font-size:21px;font-weight:700;color:var(--jd-navy)">{esc(u['full_name'])}</div>
          <div style="color:var(--jd-muted)">{esc(t('role_student'))} · {esc(u['student_id'])}</div></div></div>
          <div class="jd-kv">
            <div><span>{esc(t('faculty'))}</span><b>{esc(tr_faculty(u['faculty'], lang()))}</b></div>
            <div><span>{esc(t('program'))}</span><b>{esc(tr_program(u['program'], lang()))}</b></div>
            <div><span>{esc(t('year'))}</span><b>{esc(year_label(u['year']))}</b></div>
            <div><span>{esc(t('group'))}</span><b>{esc(u['group_name'])}</b></div>
          </div></div>""", unsafe_allow_html=True)

        enrolled = q1("SELECT COUNT(*) n FROM enrollments WHERE user_id=?", (uid,))["n"]
        avg = q1("SELECT AVG(score) a FROM grades WHERE user_id=?", (uid,))["a"]
        lessons = q1("SELECT COUNT(*) n FROM schedule WHERE group_name=?", (u["group_name"],))["n"]
        stat_cards([
            ("📘", enrolled, t("enrolled_courses")),
            ("📊", f"{avg:.1f}" if avg else "—", t("avg_score")),
            ("⭐", national_grade(avg) if avg else "—", t("avg_national")),
            ("📅", lessons, t("weekly_lessons")),
        ])

        today = DAYS[datetime.now().weekday()] if datetime.now().weekday() < len(DAYS) else None
        todays = q("""SELECT s.start_time,s.end_time,c.name,c.name_ru,c.name_en,r.code FROM schedule s
                      JOIN courses c ON c.id=s.course_id JOIN rooms r ON r.id=s.room_id
                      WHERE s.group_name=? AND s.day=? ORDER BY s.start_time""", (u["group_name"], today))
        items = "".join(f"<li><b>{esc(r['start_time'])}–{esc(r['end_time'])}</b> · {esc(cname(r))} · 📍 {esc(r['code'])}</li>"
                        for r in todays) or f"<li>{esc(t('no_lessons_today'))}</li>"
        st.markdown(f"<div class='jd-card'><h4>📅 {esc(t('today_lessons'))}</h4><ul class='jd-list'>{items}</ul></div>",
                    unsafe_allow_html=True)
        st.info(t("student_demo_info"))

    elif page == "my_courses":
        section(t("p_my_courses"))
        sem = st.selectbox(t("semester"), list(range(1, 9)), index=2, format_func=semester_label)
        rows = q("""SELECT c.id,c.name,c.name_ru,c.name_en,c.kind,c.module FROM enrollments e
                    JOIN courses c ON c.id=e.course_id WHERE e.user_id=? AND c.semester=? ORDER BY c.kind,c.name""",
                 (uid, sem))
        if rows:
            html_rows = "".join(
                f"<div class='jd-course'><b>{esc(cname(r))}</b>"
                f"<span class='jd-badge {'jd-core' if r['kind'] == 'Majburiy' else 'jd-elec'}'>{esc(tr_kind(r['kind'], lang()))}</span>"
                + (f"<span class='jd-badge jd-elec'>{esc(tr_module(r['module'], lang()))}</span>" if r["module"] else "")
                + "</div>" for r in rows)
            st.markdown(f"<div class='jd-card'>{html_rows}</div>", unsafe_allow_html=True)
        else:
            st.info(t("no_courses_sem"))

        section(t("choose_elective"))
        taken = {r["id"] for r in rows}
        opts = [r for r in q("""SELECT id,name,name_ru,name_en,module FROM courses
                                WHERE semester=? AND kind='Tanlov' ORDER BY module,name""", (sem,))
                if r["id"] not in taken]
        if opts:
            choice = st.selectbox(t("elective"), opts, format_func=course_label)
            if st.button(t("add_to_plan"), type="primary"):
                run("INSERT OR IGNORE INTO enrollments(user_id,course_id) VALUES(?,?)", (uid, choice["id"]))
                st.toast(t("course_added"), icon="✅")
                st.rerun()
        else:
            st.caption(t("no_electives"))

    elif page == "schedule":
        section(t("p_schedule"), t("group_label", group=u["group_name"]))
        rows = q("""SELECT s.day,s.start_time,s.end_time,c.name,c.name_ru,c.name_en,r.code,r.kind,r.building,s.teacher
                    FROM schedule s JOIN courses c ON c.id=s.course_id JOIN rooms r ON r.id=s.room_id
                    WHERE s.group_name=?""", (u["group_name"],))
        if rows:
            rows.sort(key=lambda r: (day_index(r["day"]), r["start_time"]))
            today = DAYS[datetime.now().weekday()] if datetime.now().weekday() < len(DAYS) else None
            for d in DAYS:
                lessons = [r for r in rows if r["day"] == d]
                if not lessons:
                    continue
                body = "".join(
                    f"<div class='jd-lesson'><div class='jd-time'>{esc(r['start_time'])}–{esc(r['end_time'])}</div>"
                    f"<div><b>{esc(cname(r))}</b><div class='jd-lesson-meta'>📍 {esc(r['code'])} · "
                    f"{esc(tr_room_kind(r['kind'], lang()))} · {esc(tr_building(r['building'], lang()))}"
                    f" &nbsp;|&nbsp; 👨‍🏫 {esc(r['teacher'])}</div></div></div>" for r in lessons)
                badge = f"<span>{esc(t('today'))}</span>" if d == today else ""
                st.markdown(f"<div class='jd-day {'today' if d == today else ''}'>"
                            f"<div class='jd-day-h'><span>{esc(tr_day(d, lang()))}</span>{badge}</div>{body}</div>",
                            unsafe_allow_html=True)
        else:
            st.info(t("no_schedule"))

    elif page == "grades":
        section(t("p_grades"))
        rows = q("""SELECT c.name,c.name_ru,c.name_en,c.semester,g.score,g.letter,g.updated FROM grades g
                    JOIN courses c ON c.id=g.course_id WHERE g.user_id=? ORDER BY c.semester,c.name""", (uid,))
        if rows:
            avg = sum(r["score"] for r in rows) / len(rows)
            stat_cards([("📊", f"{avg:.1f}", t("avg_score")), ("⭐", national_grade(avg), t("avg_national")),
                        ("📝", len(rows), t("graded_courses"))])
            st.dataframe([{t("semester"): r["semester"], t("course"): cname(r), t("score"): r["score"],
                           t("letter"): r["letter"], t("grade5"): national_grade(r["score"]),
                           t("updated"): r["updated"]} for r in rows],
                         width="stretch", hide_index=True)
            st.caption(t("grade_scale_note"))
        else:
            st.info(t("no_grades"))

    elif page == "curriculum":
        section(t("p_curriculum"), t("curriculum_sub"))
        all_courses = q("SELECT semester,name,name_ru,name_en,kind,module FROM courses ORDER BY semester,kind,module,name")
        for sem in range(1, 9):
            rows = [r for r in all_courses if r["semester"] == sem]
            with st.expander(f"{semester_label(sem)} · {year_label((sem + 1) // 2)} · {t('n_courses', n=len(rows))}",
                             expanded=(sem == 3)):
                for r in rows:
                    icon = "🔹" if r["kind"] == "Majburiy" else "▫️"
                    mod = f" · {tr_module(r['module'], lang())}" if r["module"] else ""
                    st.markdown(f"{icon} **{cname(r)}** — {tr_kind(r['kind'], lang())}{mod}")

# ================================================================ ADMINISTRATOR
else:
    if page == "overview":
        section(t("admin_panel"))
        n = lambda sql: q1(sql)["n"]
        stat_cards([
            ("👥", n("SELECT COUNT(*) n FROM users WHERE role='student'"), t("stat_students")),
            ("📚", n("SELECT COUNT(*) n FROM courses"), t("stat_courses")),
            ("🏫", n("SELECT COUNT(*) n FROM rooms"), t("stat_rooms")),
            ("📅", n("SELECT COUNT(*) n FROM schedule"), t("stat_schedule")),
            ("📝", n("SELECT COUNT(*) n FROM grades"), t("stat_grades")),
        ])
        section(t("curriculum_by_sem"))
        rows = q("""SELECT semester, SUM(kind='Majburiy') core, SUM(kind='Tanlov') elec, COUNT(*) total
                    FROM courses GROUP BY semester ORDER BY semester""")
        st.dataframe([{t("semester"): semester_label(r["semester"]), t("core"): r["core"],
                       t("elective"): r["elec"], t("total"): r["total"]} for r in rows],
                     width="stretch", hide_index=True)
        st.warning(t("admin_warning"))

    elif page == "students":
        section(t("p_students"))
        with st.form("new_student", clear_on_submit=True):
            st.subheader(t("add_student"))
            c1, c2 = st.columns(2)
            name = c1.text_input(t("full_name"))
            sid = c2.text_input(t("student_id"))
            username = c1.text_input(t("username"))
            password = c2.text_input(t("temp_password"), type="password", help=t("password_rule"))
            faculty = st.selectbox(t("faculty"), list(FACULTIES), index=2, format_func=lambda f: tr_faculty(f, lang()))
            program = st.selectbox(t("program"), list(PROGRAMS), format_func=lambda p: tr_program(p, lang()))
            c3, c4 = st.columns(2)
            year = c3.selectbox(t("year"), [1, 2, 3, 4], format_func=year_label)
            group = c4.text_input(t("group"), value="XIM-21")
            if st.form_submit_button(t("create_student"), type="primary"):
                name, sid, username, group = name.strip(), sid.strip(), username.strip(), group.strip()
                if not all([name, sid, username, group]):
                    st.error(t("fill_all"))
                elif len(password) < 6:
                    st.error(t("password_rule"))
                elif q1("SELECT 1 FROM users WHERE username=? OR (student_id=? AND role='student')", (username, sid)):
                    st.error(t("student_exists"))
                else:
                    run("""INSERT INTO users(username,password,role,full_name,student_id,faculty,program,year,group_name)
                           VALUES(?,?,?,?,?,?,?,?,?)""",
                        (username, pw_hash(password), "student", name, sid, faculty, program, year, group))
                    st.success(t("student_created"))
        rows = q("SELECT full_name,student_id,username,faculty,program,year,group_name FROM users WHERE role='student' ORDER BY id")
        st.dataframe([{t("full_name"): r["full_name"], t("student_id"): r["student_id"], t("username"): r["username"],
                       t("faculty"): tr_faculty(r["faculty"], lang()), t("program"): tr_program(r["program"], lang()),
                       t("year"): r["year"], t("group"): r["group_name"]} for r in rows],
                     width="stretch", hide_index=True)

    elif page == "courses":
        section(t("p_courses"))
        sem = st.selectbox(t("semester"), list(range(1, 9)), format_func=semester_label)
        rows = q("SELECT name,name_ru,name_en,kind,module FROM courses WHERE semester=? ORDER BY kind,module,name", (sem,))
        st.dataframe([{t("course"): cname(r), t("kind"): tr_kind(r["kind"], lang()),
                       t("module"): tr_module(r["module"], lang())} for r in rows],
                     width="stretch", hide_index=True)
        with st.form("add_course", clear_on_submit=True):
            st.subheader(t("add_course"))
            name_uz = st.text_input(t("course_name_uz"))
            c1, c2 = st.columns(2)
            name_ru = c1.text_input(t("course_name_ru"))
            name_en = c2.text_input(t("course_name_en"))
            c3, c4, c5 = st.columns(3)
            semester = c3.selectbox(t("semester"), list(range(1, 9)), index=sem - 1, format_func=semester_label)
            kind = c4.selectbox(t("kind"), KINDS, format_func=lambda k: tr_kind(k, lang()))
            module = c5.text_input(t("module_optional"))
            if st.form_submit_button(t("add_course_btn"), type="primary"):
                if name_uz.strip():
                    run("INSERT INTO courses(year,semester,name,kind,module,name_ru,name_en) VALUES(?,?,?,?,?,?,?)",
                        ((semester + 1) // 2, semester, name_uz.strip(), kind, module.strip(),
                         name_ru.strip(), name_en.strip()))
                    st.success(t("course_created"))
                else:
                    st.error(t("course_name_required"))

    elif page == "rooms":
        section(t("p_rooms"))
        rows = q("SELECT code,building,kind,capacity FROM rooms ORDER BY building,code")
        st.dataframe([{t("room_code"): r["code"], t("building"): tr_building(r["building"], lang()),
                       t("room_type"): tr_room_kind(r["kind"], lang()), t("capacity"): r["capacity"]} for r in rows],
                     width="stretch", hide_index=True)
        with st.form("add_room", clear_on_submit=True):
            st.subheader(t("add_room"))
            c1, c2 = st.columns(2)
            code = c1.text_input(t("room_code"))
            building = c2.text_input(t("building"), placeholder="A bino")
            c3, c4 = st.columns(2)
            kind = c3.selectbox(t("room_type"), ROOM_KINDS, format_func=lambda k: tr_room_kind(k, lang()))
            capacity = c4.number_input(t("capacity"), min_value=1, max_value=1000, value=30)
            if st.form_submit_button(t("add_room_btn"), type="primary"):
                code, building = code.strip().upper(), building.strip()
                if not code or not building:
                    st.error(t("fill_all"))
                elif q1("SELECT 1 FROM rooms WHERE code=?", (code,)):
                    st.error(t("room_exists"))
                else:
                    run("INSERT INTO rooms(code,building,kind,capacity) VALUES(?,?,?,?)", (code, building, kind, int(capacity)))
                    st.success(t("room_created"))
                    st.rerun()

    elif page == "schedule":
        section(t("schedule_manage"))
        # Semestr forma tashqarisida — fanlar ro‘yxati darhol yangilanadi
        sem = st.selectbox(t("semester"), list(range(1, 9)), index=2, format_func=semester_label)
        courses = q("SELECT id,name,name_ru,name_en,module FROM courses WHERE semester=? ORDER BY kind,name", (sem,))
        rooms = q("SELECT id,code,kind,capacity FROM rooms ORDER BY code")
        with st.form("add_schedule"):
            c1, c2 = st.columns(2)
            group = c1.text_input(t("group"), value="XIM-21")
            teacher = c2.text_input(t("teacher"))
            course = c1.selectbox(t("course"), courses, format_func=course_label) if courses else None
            room = c2.selectbox(t("room"), rooms, format_func=lambda r: f"{r['code']} · {tr_room_kind(r['kind'], lang())} · {r['capacity']}") if rooms else None
            c3, c4, c5 = st.columns(3)
            day = c3.selectbox(t("day"), DAYS, format_func=lambda d: tr_day(d, lang()))
            start = c4.time_input(t("start"), value=time(9, 0), step=600)
            end = c5.time_input(t("end"), value=time(10, 20), step=600)
            if st.form_submit_button(t("add_to_schedule"), type="primary"):
                s, e, group = start.strftime("%H:%M"), end.strftime("%H:%M"), group.strip()
                if not (course and room):
                    st.error(t("need_course_room"))
                elif not group or not teacher.strip():
                    st.error(t("fill_all"))
                elif e <= s:
                    st.error(t("time_order"))
                else:
                    clash = q1("""SELECT s.group_name, r.code FROM schedule s JOIN rooms r ON r.id=s.room_id
                                  WHERE s.semester=? AND s.day=? AND s.start_time<? AND ?<s.end_time
                                  AND (s.room_id=? OR s.group_name=?)""", (sem, day, e, s, room["id"], group))
                    if clash:
                        st.error(t("clash", group=clash["group_name"], room=clash["code"]))
                    else:
                        run("""INSERT INTO schedule(year,semester,group_name,day,start_time,end_time,course_id,room_id,teacher)
                               VALUES(?,?,?,?,?,?,?,?,?)""",
                            ((sem + 1) // 2, sem, group, day, s, e, course["id"], room["id"], teacher.strip()))
                        st.success(t("schedule_added"))
        rows = q("""SELECT s.id,s.semester,s.group_name,s.day,s.start_time,s.end_time,c.name,c.name_ru,c.name_en,
                           r.code,s.teacher FROM schedule s JOIN courses c ON c.id=s.course_id
                           JOIN rooms r ON r.id=s.room_id""")
        rows.sort(key=lambda r: (r["group_name"], day_index(r["day"]), r["start_time"]))
        st.dataframe([{t("semester"): r["semester"], t("group"): r["group_name"], t("day"): tr_day(r["day"], lang()),
                       t("time"): f"{r['start_time']}–{r['end_time']}", t("course"): cname(r),
                       t("room"): r["code"], t("teacher"): r["teacher"]} for r in rows],
                     width="stretch", hide_index=True)
        if rows:
            with st.expander(t("delete_entry")):
                victim = st.selectbox(t("entry"), rows, format_func=lambda r: f"{r['group_name']} · {tr_day(r['day'], lang())} "
                                      f"{r['start_time']} · {cname(r)} · {r['code']}")
                if st.button(t("delete"), type="secondary"):
                    run("DELETE FROM schedule WHERE id=?", (victim["id"],))
                    st.rerun()

    elif page == "grades_admin":
        section(t("grades_manage"))
        students = q("SELECT id,full_name,student_id FROM users WHERE role='student' ORDER BY full_name")
        if not students:
            st.info(t("no_students"))
        else:
            c1, c2 = st.columns(2)
            student = c1.selectbox(t("role_student"), students, format_func=lambda x: f"{x['full_name']} · {x['student_id']}")
            sem = c2.selectbox(t("semester"), list(range(1, 9)), index=2, format_func=semester_label)
            courses = q("SELECT id,name,name_ru,name_en,module FROM courses WHERE semester=? ORDER BY kind,name", (sem,))
            if courses:
                c3, c4 = st.columns([3, 1])
                course = c3.selectbox(t("course"), courses, format_func=course_label)
                score = c4.number_input(t("score_range"), min_value=0.0, max_value=100.0, value=85.0, step=1.0)
                st.caption(f"{t('letter')}: **{letter_grade(score)}** · {t('grade5')}: **{national_grade(score)}**")
                if st.button(t("save_grade"), type="primary"):
                    run("INSERT OR IGNORE INTO enrollments(user_id,course_id) VALUES(?,?)", (student["id"], course["id"]))
                    run("""INSERT INTO grades(user_id,course_id,score,letter,updated) VALUES(?,?,?,?,?)
                           ON CONFLICT(user_id,course_id) DO UPDATE SET score=excluded.score,letter=excluded.letter,
                           updated=excluded.updated""",
                        (student["id"], course["id"], score, letter_grade(score), datetime.now().strftime("%Y-%m-%d")))
                    st.success(t("grade_saved"))
            rows = q("""SELECT c.name,c.name_ru,c.name_en,c.semester,g.score,g.letter,g.updated FROM grades g
                        JOIN courses c ON c.id=g.course_id WHERE g.user_id=? ORDER BY c.semester,c.name""", (student["id"],))
            st.dataframe([{t("semester"): r["semester"], t("course"): cname(r), t("score"): r["score"],
                           t("letter"): r["letter"], t("grade5"): national_grade(r["score"]), t("updated"): r["updated"]}
                          for r in rows], width="stretch", hide_index=True)

footer()
