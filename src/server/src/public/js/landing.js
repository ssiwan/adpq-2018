
// GET ALL AGENCIES
$(document).ready(function(){
    $("#btnArticles").click(function(){
        sessionStorage.removeItem("searchValue");
        window.location.href = "articles.html";
    });

    $("#btnsearch").click(function(){
        if (typeof(Storage) !== "undefined") {
            sessionStorage.setItem("searchValue", $("#txtsearch").val());
        }
        window.location.href = "articles.html";
    });   
});