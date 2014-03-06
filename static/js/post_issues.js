function getIssuesFromTable(){
	issue_rows = $("#issues tbody tr")
	issues = []

	if (issue_rows.length == 0){
		return issues;
	}

	
	$.each(issue_rows, function(i, issue_row) {

		type = $(issue_row).find(".issue_type img").attr("title");
		id = $(issue_row).find(".issue_id").html();
		summary = $(issue_row).find(".issue_summary").html();
		publicize = $(issue_row).find(".issue_publicize").is(':checked');

		if (publicize){
			issues.push({type:type, id:id, summary:summary,publize:publicize});	
		}
	});
	return issues
}


function postIssuesToTwitterAndGetsat(form){

	
	issues = getIssuesFromTable();
	console.log("POSTING ISSUES:");
	console.log(issues);
	console.log(issues.length);

	form_failed = false;
	if (issues.length == 0){
		form_failed=true;
	 	
	}else if ($(form).find('#version_no').val() == ''){
		form_failed=true;
	} 
	if (form_failed){
		$(form).effect('shake');
		return false;
	}

	ajaxLoading();
	$.ajax({
	    url: "/post_issues_to_twitter_and_getsat",
	    data: {
	    	issues: JSON.stringify(issues)
	    },
	    type: "POST",
	    dataType : "json",

	    success: function( json ) {

	    },

	    error:ajaxError
	});
	

}