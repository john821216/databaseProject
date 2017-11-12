$('#bid').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New Item');
  //modal.find('.modal-body input').val(recipient);
})
enter=false;
var pp=[];
function addMessage(tag,name,msg){
	console.log(tag+ " " + name +" " + msg);
	if(tag == "<msg>" && msg != "" && enter == true){
		console.log("Mes+" + msg);
		$("#messageBoard").append( "<div class='row message-bubble'><p class='text-muted'>" +name+" : </p><p>"+msg+"</p></div>" );
		$("#mes" ).val("")
	} else if(tag=="<bid>"){
		var otherRoom = msg.split(" ")[0];
		var user = name;
		var myRoom = document.URL.split("biddingRoom/")[1];
		if(myRoom== otherRoom){
			pp.push(user);
			var users=""
			for(var i = 0 ; i < pp.length ; i++){
				if(i==0){
					users = pp[i];
				} else{
					users += " " + pp[i];
				}
			}
			var socket = io.connect('http://' + document.domain + ':' + "5000");
			socket.on('connect', function() {
				socket.send("<bidUpdate> " + myRoom+" " + users);
			});
		}
	} else if(tag=="<bidUpdate>"){
		var otherRoom = name;
		$("#currentPP").text("Current People: ");
		pp=[];
		for(var i =0 ; i < msg.split(" ").length ; i++){
			$("#currentPP").append(msg.split(" ")[i] +" ");
			pp.push(msg.split(" ")[i]);
		}	
		console.log(pp);
	}
}

$(document).ready(function() {
	var socket = io.connect('http://' + document.domain + ':' + "5000");
	var currentRoom = document.URL.split("biddingRoom/")[1];
	socket.on('connect', function() {
		socket.send("<bid> " + $('#username').text()+" " + currentRoom);
	});
	socket.on('message', function(msg) {
		var tag = msg.split(" ")[0]
		var name = msg.split(" ")[1];
		var mes="";
		for(var i = 2 ; i < msg.split(" ").length ; i++){
			mes += msg.split(" ")[i]+" ";
		}
		addMessage(tag,name,mes);
		console.log('Received message');
	});
});
