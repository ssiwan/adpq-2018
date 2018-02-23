'use strict';

var mongoose = require('mongoose'),
    articleComment = mongoose.model('articleComment');
mongoose.Promise = Promise;

exports.createArticleComment = function(req, res) {
    //req.userId

    var newComment = new articleComment({
        commenterId: mongoose.Types.ObjectId(req.userId),
        articleId: "",
        comment: "",
        createdAt: Date.now() 
    }); 
}