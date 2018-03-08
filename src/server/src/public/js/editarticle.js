$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    var articleId = getParameterByName("articleId"); // gets articleId from the URL querystring
    var agencyid = sessionStorage.getItem("agencyid");
   /* console.log(role);
    console.log(token);
    console.log(articleId);*/

    if(!isEmpty(role) && !isEmpty(token) && !isEmpty(articleId))
 {
         /*    if (role === "admin") {
                $("#adminsettingsbtn").show();
            } */
           
           
            
        
            var attachments = [];
            var FileJSON = { "mime":"","name":""};
            var options = "";
            LoadTags();
            LoadData();
            function LoadTags() {
            
                $.ajax({
                    url: APIURL + "suggestedTags",
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

            function UploadToS3() {
                var x = document.getElementById("fileattachments");
                console.log(x.files.length);

                for (var file, i = 0; i < x.files.length; i++) {
                    file = x.files[i];
                    //console.log(x.files[i].type);
                    //console.log(x.files[i].name);
                    FileJSON.mime = x.files[i].type;
                    FileJSON.name = x.files[i].name;
                    attachments.push(x.files[i].name);
                    $.ajax({
                        url : APIURL + "preS3",
                        data: JSON.stringify(FileJSON),
                        type : "POST",
                        dataType : "json",
                        headers:{
                            'Authorization':token,
                            'Content-Type' :'application/json'
                        }
                    })
                    .done(function(s3presignedUrl) {
                        console.log(s3presignedUrl);
                        //console.log(file.type);
                        //console.log(file);
                    $.ajax({
                            url : s3presignedUrl.url,
                            method : 'PUT',
                            data : file,
                            headers: {'Content-Type': ''},
                            processData:false
                        })
                        .done(function(){
                            console.log("Success file uploaded " + file.name);
                            
                        })
                        .fail(function(){
                            console.log("S3 file upload failed" + file.name);
                        })
                    })
                }
            }
            

        $('#tags').tagsInput({
            width: 'auto'
        });

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
                //console.log(JSON.parse(response.data.description));
                if (!isEmpty(response.data)) {
                    $("#title").val(response.data.title);                    
                    $("#agency").val(response.data.agencyName);
                    document.getElementById("audience").value = response.data.role;
                    $("#shortdesc").val(response.data.summary);
                    quill.setContents(JSON.parse(response.data.description),'api');
                    article.tags = $("#tags").val(); // need to uncomment once create article endpoint accepts tags
                    var tgs = "";
                    for (let index = 0; index < response.data.tags.length; index++) {
                        tgs += response.data.tags[index] + ",";
                    }
                    tgs = tgs.substring(0, tgs.length - 1)
                    $('#tags').importTags(tgs);
                    $('#dynamictable').append('<table class="table table-stripped"><thead><tr>Attachments</tr></thead></table>');
                    var table = $('#dynamictable').children();    
                    var j = 0;
                    for (let index = 0; index < response.data.attachments.length; index++) {
                        j++;
                        table.append("<tbody><tr><td>Attachment " + j +"</td><td><a href="+response.data.attachments[index]+">View</a></td><td><button type='button' class='btn' onclick='DeleteAttachments(" + response.data.attachments[index]  +")'>Delete</button></td></tr>");
                    }
                    table.append("</tbody>");
                }

            })
            .fail(function(data, textStatus, xhr) {
                alert(data.responseJSON.Error);
            });
        }

        var deleteAtts = {
            articleId:"",
            attachmentUrl:""
        }

       function DeleteAttachments(attachmentUrl) 
       {
        deleteAtts.articleId = articleId;
        deleteAtts.attachmentUrl = attachmentUrl;

        console.log(JSON.stringify(deleteAtts));
           if (!isEmpty(attachmentUrl)) 
           {
                $.ajax({
                    url: APIURL + "deleteAttachment",
                    type: 'PATCH',
                    dataType: 'json',
                    headers:{
                        'Authorization':token,
                        'Content-Type':'application/json'
                    },
                    data: JSON.stringify(deleteAtts)
                })
                .done(function(response) {
                    console.log(response);
                    //console.log(isEmpty(response.status));
                    if (!isEmpty(response.status)) {
                        if (response.status === "saved!") {
                        alert("Attachment deleted.");
                        }
                    }
                    else{
                        alert("There seems to be a problem with deleting attachments.Please try again.");
                    }
                })
                .fail(function(data, textStatus, xhr) {
                    alert(data.responseJSON.Error);
                });
           }        
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
            article.agencyId = agencyid;
            article.audience = $("#audience").val();
           
            article.shortDesc = $("#shortdesc").val();
            article.longDesc = JSON.stringify(quill.getContents());
            article.tags = $("#tags").val();
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

            UploadToS3();
            article.attachments = attachments;

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
                       //window.location.href = "dashboard-staff.html";
                       alert("Article edited successfully.")
                       setTimeout(function(){ window.location.href = "dashboard-staff.html"; }, 2000);
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

        $("#logout").click(function() {
            sessionStorage.clear();
            window.location.href = "index.html";
        })

        $("#btnCancel").click(function() {
            window.location.href = "dashboard-staff.html";
        });

 }
else {
    window.location.href = "index.html";
}

});