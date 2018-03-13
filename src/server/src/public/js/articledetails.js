$(document).ready(function(){

    var role = sessionStorage.getItem("role");
    var token = sessionStorage.getItem("token");
    var articleId = getParameterByName("articleId"); // gets articleId from the URL querystring
    var userid = sessionStorage.getItem("id");

    //console.log(role);
    //console.log(token);
    //console.log(articleId);
    var socialmediaurl = SocialMediaURL+"articles-details-admin-history.html?articleId="+articleId;
    if (isEmpty(token)) {
        token = " ";
    }

    if(!isEmpty(articleId)) 
 {
                            switch (role) {
                            case "admin":
                                $("#btnhistory").show();
                                $("#commentsection").show();
                                $("#comments").show();
                                $("#adminsettingsbtn").show();
                                $("#admincssmenu").show();
                                $("#adminprofile").attr("href","edit-profile-admin.html?userId="+ userid);                 
                                break;
                                case "staff":
                                $("#btnhistory").show();
                                $("#commentsection").show();
                                $("#comments").show();
                                $("#staffcssmenu").show();
                                $("#staffprofile").attr("href","edit-profile-staff.html?userId="+ userid); 
                                break;
                    
                            default: // public
                                break;
                        }
                
                        $("#articleeditlnk").click(function() {
                            window.location.href = "edit-article.html?articleId="+articleId;
                        });
                        
                        incrementViews();
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
                                $("#title").append(response.data.title);
                                $("#description").append(response.data.summary);
                               
                                var longdesc = JSON.parse(response.data.description);
                                console.log(longdesc);
                                var desc = "";
                                for (let index = 0; index < longdesc.ops.length; index++) {
                                    desc += longdesc.ops[index].insert;
                                }
                                $('#longdescription').append(desc);
                                var tgs = "";
                                for (let index = 0; index < response.data.tags.length; index++) {
                                    tgs += response.data.tags[index] + ",";
                                }
                                tgs = tgs.substring(0, tgs.length - 1)
                                $('#tags').append(tgs);
                                $("#author").append(response.data.createdBy.name.first + "  " + response.data.createdBy.name.last);
                                $("#reviewby").append(response.data.approvedBy);
                                $("#publishdate").append(convertToLocalDate(response.data.createdAt));
                                $("#lastupdate").append(convertToLocalDate(response.data.lastUpdated));

                                $('#dynamictable').append('<table class="table table-stripped"></table>');
                                var table = $('#dynamictable').children();    
                                var j = 0;
                                for (let index = 0; index < response.data.attachments.length; index++) {
                                    j++;
                                    table.append("<tbody><tr><td>Attachment " + j +"</td><td><a href="+response.data.attachments[index]+">View</a></td></tr>");
                                }
                                table.append("</tbody>");

                                $('#historytable').append('<table width="860" border="0" class="history-table"><tr><th>Created On</th><th>Last Updated</th><th>Edit By</th><th>Change</th></tr></table>');
                                var table = $('#historytable').children();    
                                for (let index = 0; index < response.data.history.length; index++) {
                                    var status = "";
                                    if (response.data.history[index].status === 0) {
                                        status = "pending"
                                    }
                                    if (response.data.history[index].status === 1) {
                                        status = "published"
                                    }
                                    if (response.data.history[index].status === 2) {
                                        status = "declined"
                                    }
                                    table.append("<tbody><tr><td>"+convertToLocalDate(convertToLocalDate(response.data.createdAt))+"</td><td>" + convertToLocalDate(response.data.history[index].createdAt)+"</td><td>" +response.data.history[index].createdBy.name.first + " " + response.data.history[index].createdBy.name.last +"</td><td>Status: " +status +"</td></tr>");
                                }
                                table.append("</tbody>");

                                $("#tagcount").append(response.data.tags.length);
                                $("#views").append(response.data.views);
                                $("#shares").append(response.data.shares);

                                /*if (response.data.role === 0) { // public role
                                
                                }*/

                                if (response.data.status === 0) { // pending
                                    $("#status").append("pending");
                                    if (role === "staff") {
                                        $("#articleeditlnk").show();
                                        $("#articledelete").show();
                                    }
                                    if (role === "admin") {
                                        $("#btndecline").show();
                                        $("#btnapprove").show();
                                        $("#articledelete").show();
                                    }
                                }

                                if (response.data.status === 1) { // published (Share icons should not show up until article is approved)
                                    $("#shareicons").show();
                                    $("#status").append("published"); 
                                    $("#btndecline").hide();
                                    $("#btnapprove").hide();
                                } 
                                if (response.data.status === 2) { // declined
                                    $("#status").append("declined");
                                    $("#btndecline").hide();
                                    $("#btnapprove").hide();
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

            $("#addbtn").click(function() {
                $("#addcomment").show();
                
            });



            var articlecomment = {
                articleId:" ",
                comment:" "
            };


            var articleapprove = {
                articleId:" "
            };

            var articledecline = {
                articleId:" "
            };



            $("#btnSave").click(function() {
                articlecomment.articleId = articleId;
                articlecomment.comment = $("#txtcomment").val();
                if (isEmpty($("#txtcomment").val())) {
                  alert("Please enter a comment");
                  return;   
                }


                $.ajax({
                    url: APIURL + "articleComment",
                    type: 'POST',
                    dataType: 'json',
                    headers:{
                        'Authorization':token,
                        'Content-Type':'application/json'
                    },
                    data: JSON.stringify(articlecomment)
                })
                .done(function(response) {
                    console.log(response);
                    //console.log(isEmpty(response.status));
                    if (!isEmpty(response.status)) {
                        if (response.status === "saved!") {
                            //alert("Comment Added Successfully");
                            window.location.reload(true);
                        }
                    }
                    else{
                        alert("There seems to be a problem with saving the comment.Please try again.");
                    }
                })
                .fail(function(data, textStatus, xhr) {
                    alert(data.responseJSON.Error);
                });
                
            });

            $("#btnapprove").click(function() {
                articleapprove.articleId = articleId;
                $.ajax({
                    url: APIURL + "publishArticle",
                    type: 'POST',
                    dataType: 'json',
                    headers:{
                        'Authorization':token,
                        'Content-Type':'application/json'
                    },
                    data: JSON.stringify(articleapprove)
                })
                .done(function(response) {
                    console.log(response);
                    //console.log(isEmpty(response.status));
                    if (!isEmpty(response.status)) {
                        if (response.status === "saved!") {
                            if (role === "admin") {
                                window.location.href = "dashboard-admin.html";
                            }
                        }
                    }
                    else{
                        alert("There seems to be a problem with approving the article.Please try again.");
                    }
                })
                .fail(function(data, textStatus, xhr) {
                    alert(data.responseJSON.Error);
                });
                
            });

            $("#btndecline").click(function() {
                articledecline.articleId = articleId;
                $.ajax({
                    url: APIURL + "declineArticle",
                    type: 'POST',
                    dataType: 'json',
                    headers:{
                        'Authorization':token,
                        'Content-Type':'application/json'
                    },
                    data: JSON.stringify(articledecline)
                })
                .done(function(response) {
                    console.log(response);
                    //console.log(isEmpty(response.status));
                    if (!isEmpty(response.status)) {
                        if (response.status === "saved!") {
                            if (role === "admin") {
                                window.location.href = "dashboard-admin.html";
                            }
                        }
                    }
                    else{
                        alert("There seems to be a problem with declining the article.Please try again.");
                    }
                })
                .fail(function(data, textStatus, xhr) {
                    alert(data.responseJSON.Error);
                });
                
            });


            $("#articledelete").click(function() {
                $.ajax({
                    url: APIURL + "articles/" + articleId,
                    type: 'DELETE',
                    headers:{
                        'Authorization':token,
                        'Content-Type':'application/json'
                    }
                })
                .done(function(response) {
                    console.log(response);
                    //console.log(isEmpty(response.status));
                    if (!isEmpty(response.data)) {
                        if (response.data === "article removed!") {
                            if (role === "staff") {
                                window.location.href = "dashboard-staff.html";
                            }

                            if (role === "admin") {
                                window.location.href = "dashboard-admin.html";
                            }
                           
                        }
                    }
                    else{
                        alert("There seems to be a problem with deleting the article.Please try again.");
                    }
                })
                .fail(function(data, textStatus, xhr) {
                    alert("Error with deleting an article endpoint.");
                });
                
            });

            $("#btnhistory").click(function() {

                $("#historywrap").show();
                

                
            });

            $("#sharefb").click(function() {
                var title = $("#title").text();
                window.open("https://www.facebook.com/sharer/sharer.php?title=+" + title +"&u="+socialmediaurl, "pop", "width=600, height=400, scrollbars=no");
                //console.log(url);
                incrementShares();
            });

            $("#sharetw").click(function() {
                window.open("https://twitter.com/intent/tweet?text="+$("#title").text()+"&url="+socialmediaurl);
                incrementShares();
            });

            $("#shareemail").click(function() {
                var emailTo = "testuser@gmail.com";
                window.open("mailto:"+emailTo+'?subject='+$("#title").text()+'&body='+socialmediaurl, '_self');
                //console.log()
                incrementShares();
            });

            $("#logoutadmin").click(function() {
                sessionStorage.clear();
                window.location.href = "index.html";
            })

            $("#logoutstaff").click(function() {
                sessionStorage.clear();
                window.location.href = "index.html";
            })


            function incrementShares() {
                $.ajax({
                    url: APIURL + "incrementShares/"+ articleId,
                    type: 'PATCH'
                    })
                .done(function(response) {
                })
                .fail(function(data, textStatus, xhr) {
                    alert(data.responseJSON.Error);
                });
            }

            function incrementViews() {
                $.ajax({
                    url: APIURL + "incrementViews/"+ articleId,
                    type: 'PATCH'
                    })
                .done(function(response) {
                    //console.log(response);
                })
                .fail(function(data, textStatus, xhr) {
                    alert(data.responseJSON.Error);
                });
            }

            $("#btnCancel").click(function() {
                window.location.reload(true);
            });    

 }
else {
    window.location.href = "index.html";
}

});