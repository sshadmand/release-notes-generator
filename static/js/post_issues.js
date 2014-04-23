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

function formFailed(form, message){
	$("#post-release-error-message").html(message).show().delay(3000).fadeOut(200);
	$(form).effect('shake');
}

function getIssuesToPost(form){
	issues = getIssuesFromTable();
	console.log("POSTING ISSUES:");
	console.log(issues);
	console.log(issues.length);

	form_failed = false;
	message = "";

	version_no = $(form).find('#version_no').val();

	if (issues.length == 0){
	 	message = "You must have issues selected to publish them as a release."
	 	formFailed(form, message);
	 	return false;
	}
	
	return issues
}

function getReleaseNameToPost(form){
	release_name = $("#release_name").val();
	if (release_name == ''){
		message = "You must enter a release name to post. Example: LAPI - v2.2"
		formFailed(form, message);
		return false;
	}
	return release_name;
}



function postIssuesToTwitterAndGetsat(form){
	
	issues = getIssuesToPost(form);
	release_name = getReleaseNameToPost(form);
	if (!issues || !release_name){
		return false;
	}


	ajaxLoading();
	$.ajax({
	    url: "/post_issues_to_twitter_and_getsat",
	    data: {
	    	issues: JSON.stringify(issues),
	    	release_name: release_name,
	    },
	    type: "POST",
	    dataType : "json",

	    success: function( json ) {
		  	ajaxSuccess();
	    },

	    error:ajaxError
	});
	
}

function createMessageFromIssues(issues){
   message = "All,%0A%0D%0A%0DHere are some recent releases:%0A%0D%0A%0D";
   for(i=0;i<issues.length;i++){
		type = issues[i].type;
		id = issues[i].id;
		summary = issues[i].summary;
		message += "  " + i + ". [" + type + "] - " + id + " : " + summary + "%0A%0D";
		message += "       Link: https://sharethis.atlassian.net/browse/" + id;
		message += "%0A%0D";
   }
   return message;
}

function getMessageSubject(release_name){
	subject = "Release%20Update";
	if (release_name != ""){
		subject += ":%20" + release_name;
	}
	console.log(subject);
	return subject;
}

function postIssuesToEmail(form){
	ajaxLoading();

	//get data from form
	issues = getIssuesToPost(form);
	release_name = getReleaseNameToPost(form);

	//trigger errors
	if ( !issues || !release_name){
		ajaxError();
		return false;
	}

	//create email
	issues_body = createMessageFromIssues(issues);
	subject = getMessageSubject(release_name);
	window.open("mailto:dev%40sharethis.com?subject=" + subject + "%20&body=" + issues_body);
	ajaxSuccess();
	

}













