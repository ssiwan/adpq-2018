$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    var articleId = getParameterByName("articleId"); // gets articleId from the URL querystring

    if(!isEmpty(role) && !isEmpty(token) && !isEmpty(articleId))
 {
            if (role === "admin") {
                $("#adminsettingsbtn").show();
            }

            $("#articleeditlnk").attr("href","edit-article.html?articleId="+articleId);
            LoadAgencies();
            //SuggestedTitles();
            
        
            var options = "";
            LoadTags();
            LoadData();
            function LoadTags() {
            
                $.ajax({
                    url: APIURL + "tags",
                    type: 'GET',
                    dataType: 'json',
                    cache:false
                })
                .done(function(response) {
                    if (!isEmpty(response.data)) {
                        for (let index = 0; index < response.data.length; index++) {
                            options += response.data[index].name + ",";
                        }
                        options = options.substring(0, options.length - 1)
                        //console.log(options);
                        $('#suggestedtags').importTags(options);
                    }
                    else
                    {
                        alert(response.error);
                    }
            
                })
                .fail(function(xhr) {
                    console.log('error', xhr);
                });
            }


        function LoadData() {
            //generateTable();
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
                //console.log(JSON.parse(response.data.description));
                if (!isEmpty(response.data)) {
                    $("#title").val(response.data.title);
                    //article.agencyId = $("#agency").val();
                    //article.audience = $("#audience").val();
                    //article.type = $("#articletype").val();
                    $("#shortdesc").val(response.data.summary);
                    quill.setContents(JSON.parse(response.data.description),'api');
                    //article.tags = $("#tags").val(); // need to uncomment once create article endpoint accepts tags
                    var tgs = "";
                    for (let index = 0; index < response.data.tags.length; index++) {
                        tgs += response.data.tags[index] + ",";
                    }
                    tgs = tgs.substring(0, tgs.length - 1)
                    $('#tags').importTags(tgs);
                    $('#dynamictable').append('<table class="table table-stripped"><thead><tr>Existing Attachments</tr></thead></table>');
                    var table = $('#dynamictable').children();    

                    for (let index = 0; index < response.data.attachments.length; index++) {
                        table.append("<tbody><tr><td>" +response.data.attachments[index]+"</td><td><button type='button' class='btn'>Delete</button></td></tr>");
                       
                        
                    }
                    table.append("</tbody>");
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