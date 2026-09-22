from flask import Flask, request, redirect
import os, json
from datetime import datetime

app = Flask(__name__)

BUSINESSES_FILE = "/tmp/businesses.json"

def load_businesses():
    if os.path.exists(BUSINESSES_FILE):
        try:
            with open(BUSINESSES_FILE, 'r') as f:
                return json.load(f)
        except: pass
    return []

def save_businesses(data):
    with open(BUSINESSES_FILE, 'w') as f:
        json.dump(data, f)

# Your businesses here - I will include a sample so it works
DEFAULT = [{"name":"Test Business","whatsapp":"+263713504734","category":"Demo"}]

@app.route('/')
def home():
    businesses = load_businesses()
    if not businesses: businesses = DEFAULT
    html = """
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{background:#0a0a0a;color:white;font-family:sans-serif;padding:20px;text-align:center}
    .card{background:#1a1a1a;padding:15px;margin:10px;border-radius:10px}
    .wa{color:#25D366}</style></head>
    <body><h1>HARARE PROMO</h1><p>🔥 #1 Harare Business Hub</p>
    """
    for b in businesses:
        html+= f"<div class='card'><h3>{b['name']}</h3><p class='wa'>{b['whatsapp']}</p></div>"
    html+= "<br><p>WhatsApp: +263713504734 for ads</p><p><a href='/submit' style='color:#25D366'>+ Add Business</a> | <a href='/admin?password=harare2024' style='color:orange'>Admin</a></p></body></html>"
    return html

@app.route('/submit')
def submit():
    return """
    <html><body style='background:#0a0a0a;color:white;padding:20px;font-family:sans-serif'>
    <h2>Submit Business</h2>
    <form action='/add' method='post'>
    <input name='name' placeholder='Business Name' required style='width:100%;padding:10px;margin:5px'><br>
    <input name='whatsapp' placeholder='+263...' required style='width:100%;padding:10px;margin:5px'><br>
    <input name='category' placeholder='Category' style='width:100%;padding:10px;margin:5px'><br>
    <button type='submit' style='background:#25D366;color:white;padding:12px;width:100%;border:none;border-radius:8px'>Submit</button>
    </form></body></html>
    """

@app.route('/add', methods=['POST'])
def add():
    data = load_businesses()
    data.append({"name":request.form.get('name'),"whatsapp":request.form.get('whatsapp'),"category":request.form.get('category'),"date":str(datetime.now())})
    save_businesses(data)
    return redirect('/')

@app.route('/admin')
def admin():
    if request.args.get('password')!='harare2024': return 'Wrong password. Use ?password=harare2024'
    businesses = load_businesses()
    return f"<body style='background:black;color:white;padding:20px'>Admin - {len(businesses)} businesses<br><br>{str(businesses)[:2000]}</body>"

if __name__ == '__main__':
    app.run()
