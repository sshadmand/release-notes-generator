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

		function search(){
			$(".ajax-indicator .loading").show();
			// Using the core $.ajax() method
			$.ajax({
			    // the URL for the request
			    url: "/get_issues",
			 
			    // the data to send (will be converted to a query string)
			    data: {
			        jql: encodeURIComponent($("#jql-search-str").val())
			    },
			 
			    // whether this is a POST or GET request
			    type: "GET",
			 
			    // the type of data we expect back
			    dataType : "json",
			 
			    // code to run if the request succeeds;
			    // the response is passed to the function
			    success: function( json ) {
					  if (json.errorMessages){
					  	handleError();
					  	$("#jql-error-query-message").show().html(json.errorMessages[0]).delay(3000).fadeOut(200);
					  	
					  }else{
					  	clearResults();
					  	jQuery.each(json.issues, function(i, issue) {
	 				  		  //console.log(issue.key + " " + issue.self + " " + issue.fields.summary)
							  key = "<td><a href='" + issue.self + "'>" + issue.key + "</a></td>"
							  summary = "<td>" + issue.fields.summary + "</td>"
							  publicize = "<td><input type=\"checkbox\" checked=checked></td>"
							  
							  $('#issues tbody:last').append('<tr>' + key + summary + publicize + '</tr>');
						  });
					  	$(".ajax-indicator .loading").hide();
			    		$(".ajax-indicator .complete").show().fadeOut("slow");
					  }
			    },
			    // code to run regardless of success or failure
			    // complete: function( xhr, status ) {
			    // 	$(".ajax-indicator .loading").hide();
			    // 	$(".ajax-indicator .complete").show().fadeOut("slow");
			    // },
			    // code to run if the request fails; the raw request and
			    // status codes are passed to the function
			    error:handleError
			});
			
			function handleError(xhr, status, error ){
				
			    	$(".ajax-indicator .loading").hide();
			        $(".ajax-indicator .error").show().fadeOut("slow");
			    
			}
		}