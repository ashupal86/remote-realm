from flask import Flask, request, render_template, redirect, url_for,session
from flask_socketio import SocketIO, emit,join_room, leave_room,send
from flask_session import Session
import random
from string import ascii_uppercase
from colorama import Fore,Style

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SESSION_TYPE']='filesystem'
app.config['SESSION_PERMANANT']=False
Session(app)
socketio = SocketIO(app)
rooms={}
roles={}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

def random_role(players):
    roles=['King','Minister','Soldier','Thief']
    random.shuffle(roles)
    role={players[i]:roles[i] for i in range(len(players))}
    return role

def assign_role(players):
    role=random_role(players)
    roles[session.get('roomid')]=role
    session['roles']=roles[session.get('roomid')]




@app.route('/',methods=['GET','POST'])
def home():
    session.clear()
    if request.method == 'POST':
        uname=request.form['username']
        roomid=request.form['roomid']
        join=request.form.get('join',False)
        create=request.form.get('create',False)
        
        if join != False and not roomid:
            return render_template("index.html", error="Please enter a room code.")
        if create!=False:
            roomid = generate_unique_code(4)
            rooms[roomid] = {'players':0,'total':[]}
            session['room']=rooms[roomid]
            print(rooms)
        elif roomid not in rooms:
            return render_template('index.html',error="Room not found")

        session['roomid']=roomid
        session['username']=uname
        return redirect(url_for('room'))
    

    return render_template('index.html')

@app.route("/room")
def room():
    room = session.get("roomid")
    uname = session.get("username")
    if room is None or session.get("username") is None or room not in rooms :
        return redirect(url_for("home"))
    return render_template("room.html", code=room)



@app.route('/game/<roomid>')
def game(roomid):
    if roomid not in rooms:
        return redirect(url_for('home'))
    else:
        role=roles.get(session.get('roomid'))
        print(Fore.BLACK+Style.BRIGHT,role,Fore.WHITE+Style.RESET_ALL)
        return render_template('game.html',roomid=roomid,username=session.get('username'),roles=role)    



@socketio.on("start")
def start(data):
    print(Fore.BLACK+Style.BRIGHT,"start the game",Fore.WHITE+Style.RESET_ALL)
    assign_role(rooms[session.get('roomid')]['total'])
    print(Fore.BLACK+Style.BRIGHT,session['roles'],Fore.WHITE+Style.RESET_ALL)
    redirect(url_for('game',roomid=str(session.get('roomid'))))
    emit('start','ready',to=session.get('roomid'))

@socketio.on("connect")
def connect(auth):
    room = session.get("roomid")
    name = session.get("username")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    rooms[room]["players"] += 1
    rooms[room]["total"].append(name)
    emit('join',{'name':name,'players':rooms[room]['players'],"total":rooms[room]['total'],'roomid':session['roomid']},to=room,broadcast=True)
    print(Fore.BLUE+Style.BRIGHT,f"{name} joined room {room}",Fore.WHITE+Style.RESET_ALL)


@socketio.on("disconnect")
def disconnect():
    room = session.get("roomid")
    name = session.get("username")

    if room in rooms:
        rooms[room]["players"] -= 1
        rooms[room]["total"].remove(name)
        if rooms[room]["players"] <= 0:
            del rooms[room]
    
    # emit('leave',{'name':name,'players':rooms[room]['players'],"total":rooms[room]['total'],'roomid':session['roomid']},to=room,broadcast=True)
    leave_room(room)

    print(Fore.RED+Style.BRIGHT,f"{name} has left the room {room}",Fore.WHITE+Style.RESET_ALL)



if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=3000)