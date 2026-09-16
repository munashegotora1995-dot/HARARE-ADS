import sqlite3, os, uuid, base64, requests, streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Harare Hub", page_icon="🇿🇼", layout="wide")
st.markdown("""
<style>
.hero{background:#0B8A42;color:white;padding:28px;border-radius:12px;text-align:center}
.price{color:#0B8A42;font-weight:800;font-size:1.4rem}
.wa{display:block;background:#25D366;color:white!important;text-align:center;padding:12px;border-radius:8px;text-decoration:none;font-weight:700;margin-top:10px}
#MainMenu,footer{visibility:hidden}
</style>
<div class="hero"><h1>🇿🇼 Harare Hub</h1><p style='color:#FFC700;font-weight:700'>Harare #1 Marketplace</p></div>
""", unsafe_allow_html=True)

BASE=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(BASE,"harare.db")
IMG_DIR=os.path.join(BASE,"images")
os.makedirs(IMG_DIR,exist_ok=True)

def fmt_wa(n):
    d=''.join(filter(str.isdigit,str(n)))
    if d.startswith("0"): d="263"+d[1:]
    if not d.startswith("263"): d="263"+d[-9:]
    return d

def save_img(file):
    if not file: return ""
    try:
        key=st.secrets.get("IMGBB_API_KEY","")
        if key:
            b64=base64.b64encode(file.getvalue()).decode()
            r=requests.post("https://api.imgbb.com/1/upload",data={"key":key,"image":b64},timeout=15)
            j=r.json()
            if j.get("success"): return j["data"]["url"]
    except: pass
    p=os.path.join(IMG_DIR,f"{uuid.uuid4().hex}_{file.name}")
    with open(p,"wb") as f: f.write(file.getvalue())
    return p

def show_img(p):
    if not p: return
    if p.startswith("http"): st.image(p,use_container_width=True)
    elif os.path.exists(p): st.image(p,use_container_width=True)

with sqlite3.connect(DB) as c:
    c.execute("CREATE TABLE IF NOT EXISTS ads(id INTEGER PRIMARY KEY AUTOINCREMENT,business TEXT,title TEXT,cat TEXT,price REAL,loc TEXT,desc TEXT,wa TEXT,wa_clean TEXT,img TEXT,pay TEXT,pkg TEXT,days INT,status TEXT DEFAULT 'Active',posted TEXT,expiry TEXT)")
    c.execute("UPDATE ads SET status='Expired' WHERE status='Active' AND expiry <= ?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))

CATS=["Cars","Property for Rent","Property for Sale","Jobs","Phones & Electronics","Services","Other"]
LOCS=["CBD","Avondale","Borrowdale","Budiriro","Chitungwiza","Highfield","Warren Park","Other"]

menu=st.sidebar.radio("Menu",["🛍️ Buy Products","💼 Post Ad"])

if menu=="🛍️ Buy Products":
    c1,c2,c3=st.columns([2,1,1])
    with c1: q=st.text_input("🔍 Search").lower()
    with c2: fc=st.selectbox("Category",["All"]+CATS)
    with c3: fl=st.selectbox("Location",["All"]+LOCS)
    with sqlite3.connect(DB) as conn:
        conn.row_factory=sqlite3.Row
        rows=conn.execute("SELECT * FROM ads WHERE status='Active' ORDER BY id DESC").fetchall()
    filtered=[]
    for r in rows:
        if fc!="All" and r["cat"]!=fc: continue
        if fl!="All" and r["loc"]!=fl: continue
        if q and q not in (r
