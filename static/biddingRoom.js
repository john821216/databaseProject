$('#bid').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New Item');
})

var socket;
var numberOfPeople;
function leave(){
	if($('#role').text() != 'seller'){
		var currentRoom = document.URL.split("biddingRoom/")[1];
		socket.send("<mainPagePP> " + (numberOfPeople-1)+" " + currentRoom);
	}
	socket.send("<bidLeave> " +$('#role').text() +" " +$('#id').text()+" " + currentRoom);
	var millisecondsToWait = 1500;
	setTimeout(function() {
			window.location = "http://" + document.URL.split("http://")[1].split("/")[0]
	}, millisecondsToWait);
}

enter=false;
function addMessage(tag,id,msg){
	if(tag == "<msg>" && msg != "" && enter == true){
		console.log("Mes+" + msg);
		$("#messageBoard").append( "<div class='row message-bubble'><p class='text-muted'>" +name+" : </p><p>"+msg+"</p></div>" );
		$("#mes" ).val("")
	} else if(tag=="<bid>"){
		$("#currentPP").text("Current Bidder: ");
		for(var i =0 ; i < id.length ; i++){
			$("#currentPP").append(id[i] +" ");
		}	
	} else if(tag=="<bidMoney>"){
		$("#currentPrice").text("Current Price: " + id);
	}
}

function bidding(){
	if($("#role").text() != "seller"){
		var price = $("#item-price").val();
		if(parseInt(price) === parseInt(price, 10)){
			var currentRoom = document.URL.split("biddingRoom/")[1];
			socket.send("<bidMoney> " + price+" " + currentRoom);
			$('#addBid').modal('hide');

			var currentRoom = document.URL.split("biddingRoom/")[1];
			var d = $('#bidPriceForm').serializeArray();
			d.push({name: 'room', value: currentRoom});
			d.push({name: 'cbid', value: $('#id').text()})
			$.ajax({
		        url: '/bid',
		        data: d,
		        type: 'POST',
		        success: function(response) {
		            //console.log(response);
		        },
		        error: function(error) {
		            //console.log(error);
		        }
		    });		
		}
		else{
		    alert("price is not an integer")
		}
		
	} else{
		alert("Seller is not allowed bidding");
	}
}



$(document).ready(function() {
	socket = io.connect('http://' + document.domain + ':' + "5000");
	var currentRoom = document.URL.split("biddingRoom/")[1];
	socket.on('connect', function() {
		socket.send("<bid> " + $('#role').text() + " " +$('#id').text()+" " + currentRoom);
	});

	socket.on('message', function(msg) {
		var tag = msg.split(" ")[0];
		if(tag == "<bid>"){
			var maxPP =  msg.split(" ")[1];
			var roomNumber = msg.split(" ")[2];
			var id = [];
			if(roomNumber == currentRoom){
				for(var i = 3 ; i < msg.split(" ").length ; i++){
					id.push(msg.split(" ")[i]);
				}
				addMessage(tag,id,"");
				console.log('Received message');
				numberOfPeople = id.length-1;
				if(numberOfPeople > maxPP){
					alert("Too many people");
					window.location = "http://" + document.URL.split("http://")[1].split("/")[0]
				}
				//send the length of room
				socket.send("<mainPagePP> " + numberOfPeople+" " + currentRoom);
			}
			console.log(id.length);

		} else if(tag =="<bidMoney>"){
			var roomNumber = msg.split(" ")[2];
			var price = msg.split(" ")[1];
			//send the length of room
			socket.send("<mainPagePM> " + price+" " + roomNumber);
			if(roomNumber == currentRoom){
				addMessage(tag,price,"");
			}
		} 
	});
});
