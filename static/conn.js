import "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.js";
import "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js";

var socketio = io('http://'+window.location.host);
  const roomid='';
  const data={
    
  }

 socketio.on('join', (data) => {
    console.log(data.name,data.total,data.players);
    $('#count').text(data.players);
    $('#players').text(data.total);
    $('#name').text(data.name);
    data.name=data.name;
    data.players=data.players;
    data.total=data.total;
   
    
   
 });
 socketio.on('leave',(data)=>{
   console.log(data.name,data.total,data.players);
   $('#count').text(data.players);
    $('#players').text(data.total);
    
 });

    socketio.on('start',()=>{
        alert("game");
        window.location.href = '/game/'+$('#code').text();
    });
    
function start(){
    if($('#count').text()>=4){
        socketio.emit('start',{'count':data.players,'total':data.total});
        console.log('start');
    }
    else{
        alert('need 4 players to start the game');
    }
    
};
window.onbeforeunload = function(e) {    
    alert('leaveing the room');
    socketio.emit('disconnect',{'name':data.name,'total':data.total});
    e.preventDefault();
    socketio.disconnect();
    return e.returnValue = "Are you sure you want to leave the page?";

};
const onConfirmRefresh = function (event) {
  event.preventDefault();
  return event.returnValue = "Are you sure you want to leave the page?";
}

window.addEventListener("beforeunload", onConfirmRefresh, { capture: false });
