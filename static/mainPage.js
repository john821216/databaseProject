var itemCount = 0;

function addMessage(msg){
	//var mes = $( "#mes" ).val();
	if(msg != ""){
		console.log("Mes+" + msg);
		$("#messageBoard").append( "<div class='row message-bubble'><p class='text-muted'>A: </p><p>"+msg+"</p></div>" );
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


$(document).ready(function() {
	var socket = io.connect('http://' + document.domain + ':' + "5000");
	socket.on('connect', function() {
		socket.send('User has connected!');
	});
	socket.on('message', function(msg) {
		//$("#messages").append('<li>'+msg+'</li>');
		addMessage(msg);
		console.log('Received message');
	});
	$('#mesSend').on('click', function() {
		socket.send($('#mes').val());
		$('#mes').val('');
	});
});