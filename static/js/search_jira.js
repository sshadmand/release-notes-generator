function populate_sz_web(){
	search_str = 'Sprint="Sprint 146" AND status=accepted AND project=SWEB'
	$("#jql-search-str").val(search_str);
}

function populate_sz_api(){
	search_str = 'Sprint="Sprint 146" AND status=accepted AND project=SAPI'
	$("#jql-search-str").val(search_str);
}

function clearResults(){
	$('#issues tbody').html("");
}

function createIssueTableRows(issues){
  	jQuery.each(issues, function(i, issue) {
  		
  		
  		
  		type = "<td class='issue_type'><img title='" + issue.fields.issuetype.name + "' src='" + issue.fields.issuetype.iconUrl + "'></td>"
		key = "<td><a class='issue_id' href='" + issue.self + "'>" + issue.key + "</a></td>"
		summary = "<td class='issue_summary'>" + issue.fields.summary + "</td>"
		publicize = "<td><input class='issue_publicize' type=\"checkbox\" checked=checked></td>"
		  
		$('#issues tbody:last').append('<tr>' + type + key + summary + publicize + '</tr>');
		  
  	});
}

function search(){
	ajaxLoading();

	$.ajax({
	    url: "/get_issues",
	    data: {jql: encodeURIComponent($("#jql-search-str").val())},
	    type: "GET",
	    dataType : "json",

	    success: function( json ) {
			  if (json.errorMessages){
			  	handleError();
			  	$("#jql-error-query-message").show().html(json.errorMessages[0]).delay(3000).fadeOut(200);
			  	
			  }else{
			  	clearResults();
			  	createIssueTableRows(json.issues);
			  	ajaxSuccess();
			  }
	    },
	    error:ajaxError
	});
	

}