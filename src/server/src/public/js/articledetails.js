$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    var articleId = getParameterByName("articleId"); // gets articleId from the URL querystring

    console.log(role);
    console.log(token);
    console.log(articleId);

    if(!isEmpty(role) && !isEmpty(token) && !isEmpty(articleId))
 {
            if (role === "admin") {
                $("#adminsettingsbtn").show();
            }

            $("#articleeditlnk").attr("href","edit-article.html?articleId="+articleId);


            LoadData();



        function LoadData() {
            $.ajax({
                url: APIURL + "articles/" + articleId,
                type: 'GET',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                }
            })
            .done(function(response) {
                console.log(response);
                if (!isEmpty(response.data)) {
                    $("#agency").append("Agency - " + response.data.agencyName);
                    $("#description").append(response.data.summary);
                    var tgs = "";
                    for (let index = 0; index < response.data.tags.length; index++) {
                        tgs += response.data.tags[index] + ",";
                    }
                    tgs = tgs.substring(0, tgs.length - 1)
                    $('#tags').append(tgs);
                    $("#author").append(response.data.createdBy.name.first + "  " + response.data.createdBy.name.last);
                    //$("#reviewby").append(response.data.summary);
                    $("#publishdate").append(convertToLocalDate(response.data.createdAt));
                    //$("#lastupdate").append(response.data.summary);

                    $("#tagcount").append(response.data.tags.length);
                    $("#views").append(response.data.views);
                    $("#shares").append(response.data.sharedCount);
                    if (response.data.status === 0) {
                        $("#status").append("New/In Review");  
                    }

                    if (response.data.status === 1) {
                        $("#status").append("Published");  
                    }
                    if (response.data.status === 2) {
                        $("#status").append("Declined");  
                    }
                    var commentstr = "";
                    for (let index = 0; index < response.data.comments.length; index++) {
                        commentstr += "<div class='comments-inner-wrap'><div class='commenter-icon'></div><div class='commenter-author-wrap'><div class='commenter-author-name'>"+ response.data.comments[index].commenter.name.first + "  " + response.data.comments[index].commenter.name.last  +"</div><div class='comment-published'>Published:  " + convertToLocalDate(response.data.comments[index].createdAt)  +"</div><div class='commenters-comment'>" + response.data.comments[index].comment   +"</div></div></div>";
                    }
                    $("#comments").append(commentstr);
                    $("#commentcount").append(response.data.comments.length);

                }

            })
            .fail(function(data, textStatus, xhr) {
                alert(data.responseJSON.Error);
            });
        }



        var article = {
            title:"",
            agencyId:"",
            audience:"",
            shortDesc: "",
            longDesc:"",
            tags: "", 
            attachments:"",
            articleId:""
        }


        $("#btnSave").click(function(){

            article.title = $("#title").val();
            article.agencyId = $("#agency").val();
            article.audience = $("#audience").val();
            article.type = $("#articletype").val();
            article.shortDesc = $("#shortdesc").val();
            article.longDesc = JSON.stringify(quill.getContents());
            //article.tags = $("#tags").val(); // need to uncomment once create article endpoint accepts tags
            article.attachments = attachments;
            article.articleId = articleId;

            // Validation
            var errors = "";
            if (isEmpty(article.title)) {
                errors+= "Title is required. \r\n";
            }
            if (isEmpty(article.shortDesc)) {
                errors+= "Short Description is required. \r\n";
            }
            if (isEmpty(article.longDesc)) {
                errors+= "Long Description is required. \r\n";
            }

            if (!isEmpty(errors)) {
                alert(errors);
                return;
            }

            if (!isEmpty(article.attachments)) {
                UploadToS3();
            }

        console.log("Request JSON" + JSON.stringify(article));
            
            $.ajax({
                url: APIURL + "editArticle",
                type: 'POST',
                dataType: 'json',
                headers:{
                    'Authorization':token,
                    'Content-Type':'application/json'
                },
                data: JSON.stringify(article)
            })
            .done(function(response) {
                console.log(response);
                console.log(isEmpty(response.status));
                if (!isEmpty(response.status)) {
                    if (response.status === "saved!") {
                        alert("Saved Successfully");
                        setTimeout(function(){  window.location.href = "dashboard.html"; }, 3000);
                    }
                }
                else{
                    alert("There seems to be a problem with saving.Please try again.");
                }
            })
            .fail(function(data, textStatus, xhr) {
                alert(data.responseJSON.Error);
            });


        });

        $("#btnCancel").click(function() {
            window.location.href = "dashboard.html";
        });

 }
else {
    window.location.href = "index.html";
}

});