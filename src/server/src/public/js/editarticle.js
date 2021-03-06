var articleId = getParameterByName("articleId"); // gets articleId from the URL querystring
var token = sessionStorage.getItem("token");
var role = sessionStorage.getItem("role");
var agencyid = sessionStorage.getItem("agencyid");
var userid = sessionStorage.getItem("id");
$(document).ready(function(){

   
   /* console.log(role);
    console.log(token);
    console.log(articleId);*/

    if(!isEmpty(role) && !isEmpty(token) && !isEmpty(articleId))
 {
         /*    if (role === "admin") {
                $("#adminsettingsbtn").show();
            } */
           
            if (role === "admin") {
                $("#adminprofile").attr("href","edit-profile-admin.html?userId="+ userid);
            }
            else{
                $("#adminprofile").attr("href","edit-profile-staff.html?userId="+ userid); 
            }
           
        
            var attachments = [];
            var FileJSON = { "mime":"","name":""};
            var options = "";
            var allowUploads = "0";
            getUserDetails();
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

            function getUserDetails() {
                $.ajax({
                    url: APIURL + "user/" + userid,
                    type: 'GET',
                    dataType: 'json',
                    headers:{
                        'Authorization':token,
                        'Content-Type':'application/json'
                    }
                })
                .done(function(response) {
                    console.log(response);
                    if (response.data.allowUploads === 1) {
                        allowUploads = "1";
                        $("#divfileattachments").show();  
                    }
                })
                .fail(function( jqXHR, textStatus, errorThrown) {
                    alert(jqXHR.responseJSON.error);
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
                        .fail(function( jqXHR, textStatus, errorThrown) {
                            alert(jqXHR.responseJSON.error);
                        });
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
                //console.log(response);
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
                    console.log("Allow Uploads " + allowUploads);
                    if (allowUploads === "1") {
                        $('#dynamictable').append('<table class="table table-stripped"><thead><tr>Attachments</tr></thead></table>');
                        var table = $('#dynamictable').children();    
                        var j = 0; //onclick='DeleteAttachments("+response.data.attachments[index]+")'
                        for (let index = 0; index < response.data.attachments.length; index++) {
                            j++;
                            table.append("<tbody><tr><td>Attachment " + j +"</td><td><a href="+encodeURI(response.data.attachments[index])+">View</a></td><td><button type='button' class='btn' onclick=\"DeleteAttachments('"+encodeURI(response.data.attachments[index])+"')\">Delete</button></td></tr>");
                        }
                        table.append("</tbody>");
                    }
                   
                }

            })
            .fail(function( jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseJSON.error);
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
            article.agencyId = agencyid;
            article.audience = $("#audience").val();
           
            article.shortDesc = $("#shortdesc").val();
            article.longDesc = JSON.stringify(quill.getContents());
            article.tags = $("#tags").val();
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

            if (allowUploads === "1") {
                UploadToS3();
                article.attachments = attachments;
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
                       //window.location.href = "dashboard-staff.html";
                       alert("Article edited successfully.")
                       setTimeout(function(){ window.location.href = "dashboard-staff.html"; }, 2000);
                    }
                }
                else{
                    alert("There seems to be a problem with saving.Please try again.");
                }
            })
            .fail(function( jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseJSON.error);
            });


        });

        $("#logout").click(function() {
            sessionStorage.clear();
            window.location.href = "index.html";
        })

        $("#btnCancel").click(function() {
            window.location.href = "dashboard-staff.html";
        });

        // Accessibility adding labels
        var x = document.getElementById("tags_tag");
        //console.log(x);  
        x.setAttribute('aria-label', 'input tags');
        $(".ql-preview").attr('aria-label', 'long description preview');

        $("input[data-video$='URL']").attr('aria-label', 'long description preview');


 }
else {
    window.location.href = "index.html";
}

});

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
            if (!isEmpty(response.data)) {
                if (response.data === "saved!") {
                   alert("Attachment deleted.");
                   setTimeout(function(){ window.location.href = "dashboard-staff.html"; }, 1000);
                }
            }
            else{
                alert("There seems to be a problem with deleting attachments.Please try again.");
            }
        })
        .fail(function( jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseJSON.error);
        });
   }        
}