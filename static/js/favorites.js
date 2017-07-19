$(function() {


$(".favorite_star").on('click', function (evt) {

	$( this ).toggleClass("favorited");
	var is_favorite = $( this ).hasClass('favorited');
	var trip_id = $( this ).data('trip-id');

	$.post('/favorite.json', { trip_id: trip_id, favorited: is_favorite }, giveStatus); 	

	console.log("clicked");
});

function giveStatus(result) {
	console.log(result['status'])
	console.log(result['trip_id'])
};

});