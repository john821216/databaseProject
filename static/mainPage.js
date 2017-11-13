var itemCount = 0;
var enter = false;
document.getElementById("enterRoom").addEventListener("click", enterRoomFunc);
document.getElementById("leaveRoom").addEventListener("click", leaveRoomFunc);

function enterRoomFunc() {
    enter = true;
    alert("Enter chat room successfully");
}

function leaveRoomFunc(){
	enter = false;
	alert("Leave chat room successfully");
}

function addMessage(tag,name,msg){
	if(tag == "<msg>" && msg != "" && enter == true){
		console.log("Mes+" + msg);
		$("#messageBoard").append( "<div class='row message-bubble'><p class='text-muted'>" +name+" : </p><p>"+msg+"</p></div>" );
		$("#mes" ).val("")
	}
}

$('#addItem').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New Item');
  //modal.find('.modal-body input').val(recipient);
})

$('#addSet').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New Setting');
  //modal.find('.modal-body input').val(recipient);
})

$('#modSet').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('Modify Setting');
  //modal.find('.modal-body input').val(recipient);
})

$('#delSet').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('Delete Setting');
  //modal.find('.modal-body input').val(recipient);
})

$('#changeSet').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('Change Room Setting');
  //modal.find('.modal-body input').val(recipient);
})

$("#enterRoom").click(function(){
    $.ajax({
	  type: 'get',
	  url: "/enterRoom",
	  data: "postedData",
	  dataType: 'json',
      success: function(response) {
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
});

$("#leaveRoom").click(function(){
    $.ajax({
	  type: 'get',
	  url: "/leaveRoom",
	  data: "postedData",
	  dataType: 'json',
      success: function(response) {
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
});


$(document).ready(function() {
	var socket = io.connect('http://' + document.domain + ':' + "5000");
	socket.on('connect', function() {
		socket.send("<msg> Admin " + $('#username').text()+' has connected!');
	});
	socket.on('message', function(msg) {
		var tag = msg.split(" ")[0]
		if(tag=="<msg>"){
			var name = msg.split(" ")[1];
			var mes="";
			for(var i = 2 ; i < msg.split(" ").length ; i++){
				mes += msg.split(" ")[i]+" ";
			}
			addMessage(tag,name,mes);
			console.log('Received message');
		} else if(tag=="<mainPagePP>"){
			var numberOfPeople = msg.split(" ")[1];
			var roomNumber = msg.split(" ")[2];
			var maxPeople = 4;
			$("#item" + roomNumber+ "Curpeople").text("Current People: " + numberOfPeople +"/"+ maxPeople );
		}
	});
	$('#mesSend').on('click', function() {
		socket.send("<msg>" + " " + $('#username').text()+" " +$('#mes').val());
		$('#mes').val('');
	});
});