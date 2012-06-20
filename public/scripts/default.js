var host = window.location.host;
if( host.substr(-1) !== "/" ) host += '/';

/* when page is ready */
$(document).ready(function(){



});



// helper: block UI
function blockUI(text){
	if (text == undefined) text = '<h1 style="font-size:18px;color: #fff">Please, wait a moment...</h1>';
	$.blockUI({
		message: text,
		css: { 
			border: 'none', 
			padding: '15px', 
			backgroundColor: '#000', 
			'-webkit-border-radius': '10px', 
			'-moz-border-radius': '10px', 
			'-o-border-radius': '10px', 
			opacity: .5, 
			color: '#fff' 
		}, 
		baseZ: 3000, 
	}); 
}

// helper: unblock UI
function unblockUI(){
	$.unblockUI();
}


// helper: htmllEncode
function htmlEncode(value){
	return $('<div/>').text(value).html();
}

// helper: htmllDecode
function htmlDecode(value){
	return $('<div/>').html(value).text();
}


// helper: goto element by scrolling
function goToByScroll(where){
	$('html,body').animate({scrollTop: where.offset().top},'slow');
}

