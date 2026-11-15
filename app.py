
import streamlit as st
import sqlite3, hashlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).with_name("jidu_demo.db")
st.set_page_config(page_title="JIDU | University Portal", page_icon="🎓", layout="wide")

def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def pw_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

COURSES = [
(1,1,"Asosiy chet tili 1","Majburiy",""),
(1,1,"O‘zbek / Rus tili 1","Majburiy",""),
(1,1,"Iqtisodiyot nazariyasi","Majburiy",""),
(1,1,"Falsafa","Majburiy",""),
(1,1,"Hisoblash 1","Majburiy",""),
(1,1,"Iqtisodiyotda axborot texnologiyalari","Majburiy",""),
(1,1,"Jismoniy madaniyat va sport","Majburiy",""),
(1,2,"Asosiy chet tili 2","Majburiy",""),
(1,2,"O‘zbek / Rus tili 2","Majburiy",""),
(1,2,"Hisoblash 2","Majburiy",""),
(1,2,"Jamiyat va din","Majburiy",""),
(1,2,"Diplomatiya asoslari","Majburiy",""),
(1,2,"Akademik yozuv","Majburiy",""),
(1,2,"Davlat va huquq nazariyasi","Majburiy",""),
(2,3,"Asosiy chet tili 3 / Ingliz tili","Majburiy",""),
(2,3,"Ikkinchi chet tili 1","Majburiy",""),
(2,3,"Menejment","Majburiy",""),
(2,3,"Mikroiqtisodiyot","Majburiy",""),
(2,3,"Iqtisodiyotda miqdoriy usullar","Majburiy",""),
(2,3,"Arab tili","Tanlov","Ikkinchi til 1"),
(2,3,"Fors tili","Tanlov","Ikkinchi til 1"),
(2,3,"Fransuz tili","Tanlov","Ikkinchi til 1"),
(2,3,"Hind tili","Tanlov","Ikkinchi til 1"),
(2,3,"Ispan tili","Tanlov","Ikkinchi til 1"),
(2,3,"Italyan tili","Tanlov","Ikkinchi til 1"),
(2,3,"Koreys tili","Tanlov","Ikkinchi til 1"),
(2,3,"Nemis tili","Tanlov","Ikkinchi til 1"),
(2,3,"Turk tili","Tanlov","Ikkinchi til 1"),
(2,3,"Urdu tili","Tanlov","Ikkinchi til 1"),
(2,3,"Xitoy tili","Tanlov","Ikkinchi til 1"),
(2,3,"Yapon tili","Tanlov","Ikkinchi til 1"),
(2,3,"Biznes asoslari","Tanlov","Umumiy tanlov"),
(2,3,"Mediya asoslari","Tanlov","Umumiy tanlov"),
(2,3,"Pythonda dasturlash asoslari","Tanlov","Umumiy tanlov"),
(2,3,"Boshqaruv hisobi","Tanlov","Umumiy tanlov"),
(2,3,"Xalqaro turizm","Tanlov","Umumiy tanlov"),
(2,3,"Atrof-muhit siyosati","Tanlov","Umumiy tanlov"),
(2,3,"Barqarorlik fanlari","Tanlov","Umumiy tanlov"),
(2,4,"Asosiy chet tili 4","Majburiy",""),
(2,4,"Ikkinchi chet tili 2","Majburiy",""),
(2,4,"Makroiqtisodiyot","Majburiy",""),
(2,4,"Marketing","Majburiy",""),
(2,4,"Ehtimollik va statistika","Majburiy",""),
(2,4,"Moliyaviy hisob","Tanlov",""),
(2,4,"Moliyaviy matematika va modellashtirish","Tanlov",""),
(2,4,"Ma’lumotlar vizualizatsiyasi va biznes tahlil","Tanlov",""),
(2,4,"Boshqaruv qarorlarini qabul qilish usullari","Tanlov",""),
(2,4,"Yashil iqtisodiyot","Tanlov",""),
(2,4,"Mutaxassisning nutq madaniyati va notiqlik san’ati","Tanlov",""),
(3,5,"Ikkinchi chet tili 3","Majburiy",""),
(3,5,"Jahon iqtisodiyoti","Majburiy",""),
(3,5,"Ekonometrika","Majburiy",""),
(3,5,"Xalqaro marketing","Majburiy",""),
(3,5,"Rivojlanish iqtisodiyoti","Majburiy",""),
(3,5,"Soliq va soliqqa tortish","Tanlov",""),
(3,5,"Iqtisodchilar uchun o‘yinlar nazariyasi","Tanlov",""),
(3,5,"Rivojlanishni moliyalashtirish","Tanlov",""),
(3,5,"Loyihalarni boshqarish","Tanlov",""),
(3,5,"Bank ishi","Tanlov",""),
(3,5,"Zamonaviy xalqaro munosabatlar, jahon iqtisodiyoti va O‘zbekiston manfaatlari","Tanlov",""),
(3,5,"Energetika iqtisodiyoti","Tanlov",""),
(3,6,"Energetika iqtisodiyoti","Majburiy",""),
(3,6,"Ikkinchi chet tili 4","Majburiy",""),
(3,6,"Xalqaro mikroiqtisodiyot","Majburiy",""),
(3,6,"Xalqaro moliya","Majburiy",""),
(3,6,"Xalqaro menejment","Majburiy",""),
(3,6,"Buxgalteriya hisobi","Tanlov",""),
(3,6,"Vaqt qatorlari tahlili va prognozlash","Tanlov",""),
(3,6,"Migratsiya iqtisodiyoti","Tanlov",""),
(3,6,"Xalqaro investitsion faoliyat","Tanlov",""),
(3,6,"O‘zbekiston Respublikasi Milliy iqtisodiyoti","Tanlov",""),
(3,6,"Davlat-xususiy sherikchilik","Tanlov",""),
(3,6,"Moliyaviy menejment","Tanlov",""),
(3,6,"Zamonaviy xalqaro munosabatlar, jahon iqtisodiyoti va O‘zbekiston manfaatlari","Tanlov",""),
(3,6,"Rivojlanishni moliyalashtirish institutlari","Tanlov",""),
(3,6,"Xizmat yozishmalari","Tanlov",""),
(4,7,"Bitiruv loyiha","Majburiy",""),
(4,7,"Xalqaro iqtisodiyot 2","Majburiy",""),
(4,7,"Xalqaro audit","Tanlov","1-modul"),
(4,7,"Siyosiy iqtisodiyot","Tanlov","1-modul"),
(4,7,"Xalqaro logistika","Tanlov","1-modul"),
(4,7,"Iqtisodiyotda katta ma’lumotlarni tahlil qilish","Tanlov","1-modul"),
(4,7,"Iqtisodiyotda mashinaviy o‘qitish asoslari","Tanlov","2-modul"),
(4,7,"Xalqaro moliya","Tanlov","2-modul"),
(4,7,"Madaniyatlararo muloqot va Ispan tili amaliyoti","Tanlov","2-modul"),
(4,7,"Moliyaviy risklarni boshqarish","Tanlov","2-modul"),
(4,7,"Innovatsion menejment","Tanlov","3-modul"),
(4,7,"Xalqaro biznes","Tanlov","3-modul"),
(4,7,"Makrotahlil","Tanlov","3-modul"),
(4,7,"Sug‘urta","Tanlov","3-modul"),
(4,7,"Strategik moliyaviy hisob va moliyaviy hisobotlarni tahlil qilish","Tanlov","4-modul"),
(4,7,"Strategik menejment","Tanlov","4-modul"),
(4,7,"Xalqaro moliyaviy texnologiyalar","Tanlov","4-modul"),
(4,7,"Iqtisodiy diplomatiya","Tanlov","5-modul"),
(4,7,"Jahon savdo tashkiloti huquqi","Tanlov","5-modul"),
(4,7,"Xalqaro investitsiya huquqi","Tanlov","5-modul"),
(4,7,"Xalqaro iqtisodiy huquq","Tanlov","5-modul"),
(4,7,"Ilmiy tadqiqot asoslari","Tanlov","6-modul"),
(4,7,"Amaliy keys tadqiqoti","Tanlov","6-modul"),
(4,7,"Tadbirkorlik asoslari","Tanlov","6-modul"),
(4,8,"Bitiruv loyiha","Majburiy",""),
(4,8,"Amaliyot","Majburiy",""),
]

def init_db():
    c = db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, full_name TEXT, student_id TEXT, faculty TEXT, program TEXT, year INTEGER, group_name TEXT);
    CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER, semester INTEGER, name TEXT, kind TEXT, module TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS enrollments(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, course_id INTEGER, UNIQUE(user_id,course_id));
    CREATE TABLE IF NOT EXISTS grades(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, course_id INTEGER, score REAL, letter TEXT, updated TEXT, UNIQUE(user_id,course_id));
    CREATE TABLE IF NOT EXISTS rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, building TEXT, kind TEXT, capacity INTEGER);
    CREATE TABLE IF NOT EXISTS schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER, semester INTEGER, group_name TEXT, day TEXT, start_time TEXT, end_time TEXT, course_id INTEGER, room_id INTEGER, teacher TEXT);
    """)
    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        c.execute("INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",("admin",pw_hash("admin123"),"admin","JIDU Administrator"))
        c.execute("""INSERT INTO users(username,password,role,full_name,student_id,faculty,program,year,group_name)
        VALUES(?,?,?,?,?,?,?,?,?)""",("student",pw_hash("student123"),"student","Aliyev Azizbek","JIDU-2026-001","Xalqaro iqtisodiyot va menejment fakulteti","Jahon iqtisodiyoti",2,"IE-21"))
        c.executemany("INSERT INTO courses(year,semester,name,kind,module) VALUES(?,?,?,?,?)", COURSES)
        rooms = [("A-204","A bino","Dars xonasi",30),("B-301","B bino","Seminar xonasi",24),("C-105","C bino","Auditoriya",40),("L-02","Asosiy bino","Leksiya zali",180),("S-01","Asosiy bino","Seminar xonasi",20),("A-101","A bino","Dars xonasi",35)]
        c.executemany("INSERT INTO rooms(code,building,kind,capacity) VALUES(?,?,?,?)",rooms)
        uid = c.execute("SELECT id FROM users WHERE username='student'").fetchone()[0]
        for cr in c.execute("SELECT id FROM courses WHERE semester=3 AND kind='Majburiy'").fetchall():
            c.execute("INSERT OR IGNORE INTO enrollments(user_id,course_id) VALUES(?,?)",(uid,cr["id"]))
            c.execute("INSERT OR IGNORE INTO grades(user_id,course_id,score,letter,updated) VALUES(?,?,?,?,?)",(uid,cr["id"],82.0,"B","2026-11-10"))
        # Sample schedule for demo student
        ids = {r["name"]:r["id"] for r in c.execute("SELECT id,name FROM courses WHERE semester=3").fetchall()}
        room_ids = {r["code"]:r["id"] for r in c.execute("SELECT id,code FROM rooms").fetchall()}
        rows = [
        (2,3,"IE-21","Dushanba","09:00","10:30",ids.get("Menejment"),room_ids["A-204"],"PhD. Karimova M."),
        (2,3,"IE-21","Dushanba","10:40","12:10",ids.get("Mikroiqtisodiyot"),room_ids["B-301"],"PhD. Rahimov A."),
        (2,3,"IE-21","Seshanba","09:00","10:30",ids.get("Asosiy chet tili 3 / Ingliz tili"),room_ids["C-105"],"J. Smith"),
        (2,3,"IE-21","Chorshanba","13:30","15:00",ids.get("Iqtisodiyotda miqdoriy usullar"),room_ids["L-02"],"DSc. Tursunov B."),
        (2,3,"IE-21","Payshanba","11:00","12:30",ids.get("Ikkinchi chet tili 1"),room_ids["S-01"],"L. Chen"),
        ]
        c.executemany("INSERT INTO schedule(year,semester,group_name,day,start_time,end_time,course_id,room_id,teacher) VALUES(?,?,?,?,?,?,?,?,?)",rows)
    c.commit()
    c.close()

init_db()

def q(sql, params=(), one=False):
    c=db()
    cur=c.execute(sql,params)
    rows=cur.fetchall()
    c.close()
    return rows[0] if one and rows else (None if one else rows)

def run(sql, params=()):
    c=db(); c.execute(sql,params); c.commit(); c.close()

def header():
    st.markdown("<div style='background:linear-gradient(100deg,#082b55,#145b91);padding:24px 28px;border-radius:16px;color:white'><div style='font-size:13px;letter-spacing:2px;opacity:.85'>UNIVERSITY OF WORLD ECONOMY AND DIPLOMACY</div><div style='font-size:29px;font-weight:750;margin-top:5px'>JIDU | Raqamli universitet portali</div><div style='opacity:.85;margin-top:5px'>Demo platforma · Student Portal · Administration</div></div>", unsafe_allow_html=True)

if "user" not in st.session_state: st.session_state.user=None
if not st.session_state.user:
    header()
    st.write("")
    left, right = st.columns([1.2,1])
    with left:
        st.subheader("Universitet haqida")
        st.write("Jahon Iqtisodiyoti va Diplomatiya Universiteti uchun ishlab chiqilgan namoyish platformasi. Talabalar o‘z kabinetiga kirib, fanlari, dars jadvali va baholarini ko‘rishi mumkin.")
        a,b,c = st.columns(3)
        a.metric("Ta’lim bosqichi","1–4-kurs")
        b.metric("Semestrlar","1–8")
        c.metric("Portal","Demo")
        st.info("Bu prototipdagi talabalar soni, guruhlar, xonalar, jadval va baholar namuna ma’lumotlaridir. Rasmiy universitet statistikasi sifatida qabul qilinmasin.")
    with right:
        st.subheader("Tizimga kirish")
        role_hint=st.selectbox("Kirish turi",["Talaba","Administrator"])
        with st.form("login"):
            username=st.text_input("Login")
            password=st.text_input("Parol",type="password")
            submit=st.form_submit_button("Kirish",use_container_width=True)
        if submit:
            user=q("SELECT * FROM users WHERE username=? AND password=?",(username,pw_hash(password)),True)
            if user and ((role_hint=="Talaba" and user["role"]=="student") or (role_hint=="Administrator" and user["role"]=="admin")):
                st.session_state.user=dict(user); st.rerun()
            else: st.error("Login, parol yoki kirish turi noto‘g‘ri.")
        with st.expander("Demo kirish ma’lumotlari"):
            st.write("Talaba: `student` / `student123`")
            st.write("Admin: `admin` / `admin123`")
    st.stop()

u=st.session_state.user
with st.sidebar:
    st.markdown("### 🎓 JIDU Portal")
    st.write(u["full_name"])
    st.caption("Administrator" if u["role"]=="admin" else f"Talaba · {u['student_id']}")
    if st.button("Chiqish",use_container_width=True):
        st.session_state.user=None; st.rerun()
    st.divider()
    if u["role"]=="admin":
        page=st.radio("Boshqaruv",["Umumiy ko‘rinish","Talabalar","Fanlar va o‘quv reja","Xonalar","Dars jadvali","Baholar"])
    else:
        page=st.radio("Shaxsiy kabinet",["Dashboard","Mening fanlarim","Dars jadvali","Baholar","Semestrlar"])

header()
st.write("")

if u["role"]=="student":
    uid=u["id"]
    if page=="Dashboard":
        st.title("Talaba kabineti")
        x,y,z,w=st.columns(4)
        x.metric("Talaba ID",u["student_id"])
        y.metric("Kurs",f"{u['year']}-kurs")
        z.metric("Guruh",u["group_name"])
        w.metric("Fakultet",u["faculty"])
        st.subheader("Akademik ma’lumotlar")
        st.write(f"**Ta’lim yo‘nalishi:** {u['program']}")
        enroll=q("SELECT COUNT(*) n FROM enrollments WHERE user_id=?",(uid,),True)["n"]
        avg=q("SELECT AVG(score) a FROM grades WHERE user_id=?",(uid,),True)["a"]
        c1,c2=st.columns(2); c1.metric("Ro‘yxatdan o‘tgan fanlar",enroll); c2.metric("O‘rtacha ball",f"{avg:.1f}/100" if avg else "—")
        st.info("Baholar va jadval demo ma’lumotlari. Yakuniy ma’lumotlarni administrator kiritadi.")
    elif page=="Mening fanlarim":
        st.title("Mening fanlarim")
        sem=st.selectbox("Semestr",list(range(1,9)),index=2)
        rows=q("""SELECT c.name,c.kind,c.module,c.year FROM enrollments e JOIN courses c ON c.id=e.course_id WHERE e.user_id=? AND c.semester=? ORDER BY c.kind,c.name""",(uid,sem))
        if rows:
            for r in rows:
                st.write(("🟦 " if r["kind"]=="Majburiy" else "🟨 ")+f"**{r['name']}** — {r['kind']}"+(f" · {r['module']}" if r["module"] else ""))
        else: st.info("Bu semestr uchun tanlangan fanlar hali biriktirilmagan.")
        st.subheader("Tanlov fanlarini tanlash")
        opts=q("SELECT id,name,module FROM courses WHERE semester=? AND kind='Tanlov' ORDER BY module,name",(sem,))
        if opts:
            choice=st.selectbox("Tanlov fani",opts,format_func=lambda r: f"{r['name']}"+(f" ({r['module']})" if r['module'] else ""))
            if st.button("Fanni rejamga qo‘shish"):
                try: run("INSERT INTO enrollments(user_id,course_id) VALUES(?,?)",(uid,choice["id"])); st.success("Fan qo‘shildi.")
                except: st.warning("Bu fan avval qo‘shilgan.")
        else: st.caption("Ushbu semestrda tanlov fanlari kiritilmagan.")
    elif page=="Dars jadvali":
        st.title("Haftalik dars jadvali")
        rows=q("""SELECT s.day,s.start_time,s.end_time,c.name,r.code,r.kind,r.building,s.teacher FROM schedule s JOIN courses c ON c.id=s.course_id JOIN rooms r ON r.id=s.room_id WHERE s.group_name=? ORDER BY CASE s.day WHEN 'Dushanba' THEN 1 WHEN 'Seshanba' THEN 2 WHEN 'Chorshanba' THEN 3 WHEN 'Payshanba' THEN 4 ELSE 5 END,s.start_time""",(u["group_name"],))
        if rows:
            for r in rows:
                with st.container(border=True):
                    st.markdown(f"**{r['day']} · {r['start_time']}–{r['end_time']}**")
                    st.write(f"📘 {r['name']}")
                    st.caption(f"📍 {r['code']} · {r['kind']} · {r['building']}  |  👨‍🏫 {r['teacher']}")
        else: st.info("Guruhingiz uchun jadval hali tuzilmagan.")
    elif page=="Baholar":
        st.title("Fanlar bo‘yicha baholar")
        rows=q("""SELECT c.name,c.semester,g.score,g.letter,g.updated FROM grades g JOIN courses c ON c.id=g.course_id WHERE g.user_id=? ORDER BY c.semester,c.name""",(uid,))
        if rows:
            st.dataframe([{"Semestr":r["semester"],"Fan":r["name"],"Ball":r["score"],"Baho":r["letter"],"Yangilangan":r["updated"]} for r in rows],use_container_width=True,hide_index=True)
        else: st.info("Hozircha baholar kiritilmagan.")
    elif page=="Semestrlar":
        st.title("O‘quv reja · 1–8-semestr")
        for sem in range(1,9):
            rows=q("SELECT name,kind,module FROM courses WHERE semester=? ORDER BY kind,name",(sem,))
            with st.expander(f"{sem}-semestr · {len(rows)} ta fan"):
                for r in rows:
                    st.write(f"{'🔹' if r['kind']=='Majburiy' else '▫️'} **{r['name']}** — {r['kind']}"+(f" · {r['module']}" if r["module"] else ""))

else:
    if page=="Umumiy ko‘rinish":
        st.title("Administrator paneli")
        students=q("SELECT COUNT(*) n FROM users WHERE role='student'",one=True)["n"]
        courses=q("SELECT COUNT(*) n FROM courses",one=True)["n"]
        rooms=q("SELECT COUNT(*) n FROM rooms",one=True)["n"]
        schedules=q("SELECT COUNT(*) n FROM schedule",one=True)["n"]
        a,b,c,d=st.columns(4); a.metric("Demo talabalar",students); b.metric("O‘quv fanlari",courses); c.metric("Xonalar",rooms); d.metric("Jadval yozuvlari",schedules)
        st.subheader("Tizim modullari")
        st.write("Talabalar · Fakultetlar va yo‘nalishlar · 8 semestrli o‘quv reja · Majburiy va tanlov fanlari · Xonalar · Dars jadvali · Baholar")
        st.warning("Demo muhit: kiritilgan barcha ma’lumotlar sinov uchun. Haqiqiy talabalar ma’lumotlarini joylashdan oldin xavfsizlik va maxfiylik sozlamalarini kuchaytirish kerak.")
    elif page=="Talabalar":
        st.title("Talabalarni boshqarish")
        with st.form("new_student"):
            st.subheader("Yangi talaba qo‘shish")
            c1,c2=st.columns(2)
            name=c1.text_input("F.I.Sh.")
            sid=c2.text_input("Talaba ID")
            username=c1.text_input("Login")
            password=c2.text_input("Vaqtinchalik parol",type="password")
            faculty=st.text_input("Fakultet",value="Xalqaro iqtisodiyot va menejment fakulteti")
            program=st.text_input("Yo‘nalish",value="Jahon iqtisodiyoti")
            c3,c4=st.columns(2); year=c3.selectbox("Kurs",[1,2,3,4]); group=c4.text_input("Guruh",value="IE-21")
            if st.form_submit_button("Talabani yaratish"):
                try:
                    run("INSERT INTO users(username,password,role,full_name,student_id,faculty,program,year,group_name) VALUES(?,?,?,?,?,?,?,?,?)",(username,pw_hash(password),"student",name,sid,faculty,program,year,group))
                    st.success("Talaba yaratildi.")
                except Exception as e: st.error("Talaba yaratilmadi. Login yoki ID takrorlangan bo‘lishi mumkin.")
        rows=q("SELECT id,full_name,student_id,username,faculty,program,year,group_name FROM users WHERE role='student' ORDER BY id")
        st.dataframe([dict(r) for r in rows],use_container_width=True,hide_index=True)
    elif page=="Fanlar va o‘quv reja":
        st.title("Fanlar va o‘quv reja")
        sem=st.selectbox("Semestrni ko‘rish",list(range(1,9)))
        rows=q("SELECT id,year,semester,name,kind,module FROM courses WHERE semester=? ORDER BY kind,name",(sem,))
        st.dataframe([dict(r) for r in rows],use_container_width=True,hide_index=True)
        with st.form("add_course"):
            st.subheader("Yangi fan qo‘shish")
            name=st.text_input("Fan nomi")
            c1,c2=st.columns(2); year=c1.selectbox("Kurs",[1,2,3,4]); semester=c2.selectbox("Semestr",list(range(1,9)),index=sem-1)
            c3,c4=st.columns(2); kind=c3.selectbox("Fan turi",["Majburiy","Tanlov"]); module=c4.text_input("Modul (ixtiyoriy)")
            if st.form_submit_button("Fan qo‘shish"):
                if name.strip():
                    run("INSERT INTO courses(year,semester,name,kind,module) VALUES(?,?,?,?,?)",(year,semester,name,kind,module))
                    st.success("Fan qo‘shildi.")
    elif page=="Xonalar":
        st.title("Dars xonalari va auditoriyalar")
        rows=q("SELECT * FROM rooms ORDER BY building,code")
        st.dataframe([dict(r) for r in rows],use_container_width=True,hide_index=True)
        with st.form("add_room"):
            st.subheader("Yangi xona qo‘shish")
            c1,c2=st.columns(2); code=c1.text_input("Xona kodi"); building=c2.text_input("Bino")
            c3,c4=st.columns(2); kind=c3.selectbox("Xona turi",["Dars xonasi","Seminar xonasi","Auditoriya","Leksiya zali"]); capacity=c4.number_input("Sig‘imi",min_value=1,max_value=1000,value=30)
            if st.form_submit_button("Xona qo‘shish"):
                try: run("INSERT INTO rooms(code,building,kind,capacity) VALUES(?,?,?,?)",(code,building,kind,capacity)); st.success("Xona qo‘shildi.")
                except: st.error("Xona kodi takrorlangan.")
    elif page=="Dars jadvali":
        st.title("Dars jadvalini boshqarish")
        with st.form("add_schedule"):
            c1,c2=st.columns(2); group= c1.text_input("Guruh",value="IE-21"); sem=c2.selectbox("Semestr",list(range(1,9)),index=2)
            courses=q("SELECT id,name FROM courses WHERE semester=?",(sem,))
            course=c1.selectbox("Fan",courses,format_func=lambda x:x["name"]) if courses else None
            rooms=q("SELECT id,code,kind FROM rooms")
            room=c2.selectbox("Xona",rooms,format_func=lambda x:f"{x['code']} · {x['kind']}") if rooms else None
            c3,c4,c5=st.columns(3); day=c3.selectbox("Kun",["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba"]); start=c4.text_input("Boshlanish",value="09:00"); end=c5.text_input("Tugash",value="10:30")
            teacher=st.text_input("O‘qituvchi")
            if st.form_submit_button("Jadvalga qo‘shish"):
                if course and room:
                    run("INSERT INTO schedule(year,semester,group_name,day,start_time,end_time,course_id,room_id,teacher) VALUES(?,?,?,?,?,?,?,?,?)",(sem//2+1,sem,group,day,start,end,course["id"],room["id"],teacher))
                    st.success("Dars jadvaliga qo‘shildi.")
                else: st.error("Avval fan va xona yarating.")
        rows=q("""SELECT s.id,s.group_name,s.day,s.start_time,s.end_time,c.name course,r.code room,s.teacher FROM schedule s JOIN courses c ON c.id=s.course_id JOIN rooms r ON r.id=s.room_id ORDER BY s.group_name,s.day,s.start_time""")
        st.dataframe([dict(r) for r in rows],use_container_width=True,hide_index=True)
    elif page=="Baholar":
        st.title("Talaba baholarini boshqarish")
        students=q("SELECT id,full_name,student_id FROM users WHERE role='student'")
        if students:
            student=st.selectbox("Talaba",students,format_func=lambda x:f"{x['full_name']} · {x['student_id']}")
            courses=q("SELECT id,name FROM courses ORDER BY semester,name")
            if courses:
                course=st.selectbox("Fan",courses,format_func=lambda x:x["name"])
                score=st.number_input("Ball (0–100)",min_value=0.0,max_value=100.0,value=85.0,step=1.0)
                if st.button("Bahoni saqlash"):
                    letter="A" if score>=90 else "B" if score>=80 else "C" if score>=70 else "D" if score>=60 else "F"
                    run("""INSERT INTO grades(user_id,course_id,score,letter,updated) VALUES(?,?,?,?,?)
                    ON CONFLICT(user_id,course_id) DO UPDATE SET score=excluded.score,letter=excluded.letter,updated=excluded.updated""",(student["id"],course["id"],score,letter,datetime.now().strftime("%Y-%m-%d")))
                    st.success("Baho saqlandi.")
            rows=q("""SELECT c.name,c.semester,g.score,g.letter,g.updated FROM grades g JOIN courses c ON c.id=g.course_id WHERE g.user_id=?""",(student["id"],))
            st.dataframe([dict(r) for r in rows],use_container_width=True,hide_index=True)
        else: st.info("Hali talabalar qo‘shilmagan.")

st.divider()
st.caption("JIDU Digital University · Demo versiya · Ma’lumotlar namuna sifatida kiritilgan")
