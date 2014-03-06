function ajaxError(xhr, status, error ){
	$(".ajax-indicator .loading").hide();
    $(".ajax-indicator .error").show().fadeOut("slow");    
}

function ajaxLoading(){
	$(".ajax-indicator .loading").show();
}

function ajaxSuccess(){
	$(".ajax-indicator .loading").hide();
	$(".ajax-indicator .complete").show().fadeOut("slow");
}
