import os
from flask import Flask, request, session, redirect, jsonify, render_template_string
from supabase import create_client

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY","bagar100")
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

HTML="""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>BAGAR BILLIIII 100</title>
<style>body{background:#0a0a0f;color:#fff;font-family:Arial;margin:0}
.card{background:#15151f;padding:15px;border-radius:15px;margin:10px auto;max-width:430px;border:1px solid #222}
input,button{padding:12px;width:88%;margin:6px;border-radius:10px;border:none}
button{background:#ffcc00;font-weight:bold}
.tab{display:inline-block;padding:8px 12px;margin:2px;background:#1c1c2b;border-radius:8px;font-size:13px}
.active{background:#ffcc00;color:#000}</style></head><body>
<h2 style="text-align:center">😾 BAGAR BILLIIII - 100 USERS</h2>
{% if not user %}
<div class="card"><h3>Login</h3><form method="post" action="/login"><input name="username" placeholder="Username" required><input name="password" type="password" placeholder="Password" required><button>GO</button></form><p style="font-size:11px">Demo: Jadugarni / 123</p></div>
{% else %}
<div style="text-align:center"><span class="tab active" onclick="location.reload()">Friends</span><span class="tab" onclick="document.getElementById('c').style.display='block'">Chat</span><span class="tab" onclick="document.getElementById('k').style.display='block'">Khusrish</span><span class="tab" onclick="document.getElementById('m').style.display='block'">Gana</span><span class="tab" onclick="document.getElementById('s').style.display='block'">Syiim Portal</span> <a href="/logout" style="color:#ffcc00">Logout ({{user}})</a></div>

<div class="card"><h3>Pending Requests</h3><div id="reqs"></div><h3>All Users</h3><div id="users"></div></div>
<div id="c" class="card" style="display:none"><h3>Chat: <span id="chatWith">-</span></h3><div id="chatBox" style="height:200px;overflow:auto;background:#000;padding:8px;border-radius:8px"></div><input id="chatMsg"><button onclick="sendMsg()">Send</button></div>
<div id="k" class="card" style="display:none"><h3>Khusrish</h3><input id="img" placeholder="Image URL"><input id="cap" placeholder="Caption"><button onclick="postStory()">Post</button><div id="stories"></div></div>
<div id="m" class="card" style="display:none"><h3>Gana Suno</h3><audio id="player" controls style="width:100%"></audio><div id="songs"></div><input id="sTitle" placeholder="Title"><input id="sUrl" placeholder="MP3 URL"><button onclick="addSong()">Add</button></div>
<div id="s" class="card" style="display:none;background:#2a104a"><h3>🪄 Syiim Portal</h3><button onclick="document.getElementById('sOut').innerText='Love Spell ❤️'">Love Spell</button><button onclick="document.getElementById('sOut').innerText='MEOW 😾'">Billi Spell</button><button onclick="document.getElementById('sOut').innerText='Tight Hug 🤗'">Hug Spell</button><button onclick="document.getElementById('sOut').innerText='Tu hi sab kuch hai'">Sach Spell</button><p id="sOut" style="background:#000;padding:10px;border-radius:8px"></p></div>

<script>
let cur=null;
async function loadUsers(){let r=await fetch('/api/users');let d=await r.json();document.getElementById('users').innerHTML=d.map(u=>`${u.username} <button onclick="reqF('${u.username}')">Add</button> <button onclick="openC('${u.username}')">Chat</button><br>`).join('');let r2=await fetch('/api/friends');let d2=await r2.json();document.getElementById('reqs').innerHTML=d2.map(f=>`${f.sender} <button onclick="acc('${f.id}')">Accept</button><br>`).join('')||'No req'}
async function reqF(u){await fetch('/api/friend',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({receiver:u})});alert('Sent')}
async function acc(id){await fetch('/api/friends/accept',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});loadUsers()}
function openC(u){cur=u;document.getElementById('chatWith').innerText=u;document.getElementById('c').style.display='block';loadC()}
async function loadC(){if(!cur)return;let r=await fetch('/api/messages?with='+cur);let d=await r.json();document.getElementById('chatBox').innerHTML=d.map(m=>`<b>${m.sender}:</b> ${m.msg}<br>`).join('')}
async function sendMsg(){let m=document.getElementById('chatMsg').value;await fetch('/api/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({receiver:cur,msg:m})});document.getElementById('chatMsg').value='';loadC()}
async function loadS(){let r=await fetch('/api/stories');let d=await r.json();document.getElementById('stories').innerHTML=d.map(s=>`<p><b>${s.username}</b>: ${s.caption}<br><img src="${s.image_url}" style="width:100%;border-radius:8px"></p>`).join('')}
async function postStory(){await fetch('/api/stories',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image_url:document.getElementById('img').value,caption:document.getElementById('cap').value})});loadS()}
async function loadSongs(){let r=await fetch('/api/songs');let d=await r.json();document.getElementById('songs').innerHTML=d.map(s=>`<p><a href="#" onclick="document.getElementById('player').src='${s.url}';document.getElementById('player').play()" style="color:#ffcc00">${s.title}</a></p>`).join('')}
async function addSong(){await fetch('/api/songs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:document.getElementById('sTitle').value,url:document.getElementById('sUrl').value})});loadSongs()}
setInterval(()=>{if(cur)loadC()},3000);loadUsers();loadS();loadSongs();
</script>
{% endif %}
</body></html>
"""
@app.route("/")
def home(): return render_template_string(HTML,user=session.get("user"))
@app.route("/login",methods=["POST"])
def login():
    u=request.form.get("username").strip();p=request.form.get("password").strip()
    res=supabase.table("users").select("*").eq("username",u).execute()
    if res.data:
        if res.data[0]["password"]!=p: return "Wrong pass <a href='/'>back</a>"
    else: supabase.table("users").insert({"username":u,"password":p}).execute()
    session["user"]=u;return redirect("/")
@app.route("/logout")
def logout(): session.clear();return redirect("/")
@app.route("/api/users")
def au(): r=supabase.table("users").select("username").execute(); return jsonify([x for x in r.data if x["username"]!=session.get("user")])
@app.route("/api/friends")
def gf(): r=supabase.table("friends").select("*").eq("receiver",session["user"]).eq("status","pending").execute(); return jsonify(r.data)
@app.route("/api/friend",methods=["POST"])
def rf(): supabase.table("friends").insert({"sender":session["user"],"receiver":request.json["receiver"],"status":"pending"}).execute(); return jsonify({"ok":True})
@app.route("/api/friends/accept",methods=["POST"])
def af(): supabase.table("friends").update({"status":"accepted"}).eq("id",request.json["id"]).execute(); return jsonify({"ok":True})
@app.route("/api/messages",methods=["GET","POST"])
def am():
    if request.method=="POST": supabase.table("messages").insert({"sender":session["user"],"receiver":request.json["receiver"],"msg":request.json["msg"]}).execute(); return jsonify({"ok":True})
    o=request.args.get("with");me=session["user"];r=supabase.table("messages").select("*").or_(f"and(sender.eq.{me},receiver.eq.{o}),and(sender.eq.{o},receiver.eq.me)").order("created_at").execute();return jsonify(r.data[-50:])
@app.route("/api/stories",methods=["GET","POST"])
def ast():
    if request.method=="POST": supabase.table("stories").insert({"username":session["user"],"image_url":request.json["image_url"],"caption":request.json["caption"]}).execute();return jsonify({"ok":True})
    r=supabase.table("stories").select("*").order("created_at",desc=True).limit(50).execute();return jsonify(r.data)
@app.route("/api/songs",methods=["GET","POST"])
def aso():
    if request.method=="POST": supabase.table("songs").insert({"title":request.json["title"],"url":request.json["url"]}).execute();return jsonify({"ok":True})
    r=supabase.table("songs").select("*").execute();return jsonify(r.data)
if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
