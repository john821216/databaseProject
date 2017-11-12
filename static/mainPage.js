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
	//var mes = $( "#mes" ).val();
	console.log(enter);
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

function addItem(){
	var itemName = $( "#item-name" ).val();
	var itemCategory = $( "#item-category" ).val();
	var itemPrice = $( "#item-price" ).val();
	var durationFrom = $("#item-du-from").datepicker('getDate').toString().split(" ")[1] +" "+ $("#item-du-from").datepicker('getDate').toString().split(" ")[2] +" "+  $("#item-du-from").datepicker('getDate').toString().split(" ")[3]
	var durationTo = $("#item-du-to").datepicker('getDate').toString().split(" ")[1] +" "+ $("#item-du-from").datepicker('getDate').toString().split(" ")[2] +" "+  $("#item-du-to").datepicker('getDate').toString().split(" ")[3]
	console.log(itemName+" "+ itemCategory+" "+ itemPrice +" " + durationFrom +" " + durationTo);
	//console.log($('#item-du-to').datepicker('getDate'));
	$("#room-group").append("<a href='#'' class='list-group-item list-group-item-action flex-column align-items-start'><div class='d-flex w-100 justify-content-between'><h5 id="+'itemName'+itemCount+">"+itemName+"</h5><small id="+'itemTime'+ itemCount+"> From: " + durationFrom + " To: " + durationTo+"</small>"+"</div><p id=" + 'itemPrice' +itemCount +">"+itemPrice+"</p></a>");                           
	$('#addItem').modal('hide')
	$( "#item-name" ).val("");
 	$( "#item-category" ).val("");
  	$( "#item-price" ).val("");
  	itemCount++;
}

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
		var name = msg.split(" ")[1];
		var mes="";
		for(var i = 2 ; i < msg.split(" ").length ; i++){
			mes += msg.split(" ")[i]+" ";
		}
		addMessage(tag,name,mes);
		console.log('Received message');
	});
	$('#mesSend').on('click', function() {
		socket.send("<msg>" + " " + $('#username').text()+" " +$('#mes').val());
		$('#mes').val('');
	});
});