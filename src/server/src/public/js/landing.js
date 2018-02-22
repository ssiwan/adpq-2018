
// GET ALL AGENCIES
$(document).ready(function(){
    $("#btnArticles").click(function(){
        window.location.href = "articles.html";
    });

    $("#btnsearch").click(function(){
        if (typeof(Storage) !== "undefined") {
            sessionStorage.setItem("searchValue", $("#txtsearch").val());
        }
        window.location.href = "articles.html";
    });   
});