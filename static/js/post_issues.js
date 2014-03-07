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
	message = "";

	version_no = $(form).find('#version_no').val();

	if (issues.length == 0){
		form_failed=true;
	 	message = "You must have issues selected to publish them as a release."
	
	}else if (release_name == ''){
		form_failed=true;
		message = "You must enter a release name to post. Example: LAPI - v2.2"
	} 
	
	if (form_failed){
		$("#post-release-error-message").html(message).show().delay(3000).fadeOut(200);
		$(form).effect('shake');
		return false;
	}

	ajaxLoading();
	$.ajax({
	    url: "/post_issues_to_twitter_and_getsat",
	    data: {
	    	issues: JSON.stringify(issues),
	    	release_name: $("#release_name").val(),
	    },
	    type: "POST",
	    dataType : "json",

	    success: function( json ) {
		  	ajaxSuccess();
	    },

	    error:ajaxError
	});
	

}