'use strict';

var mongoose = require('mongoose'),
    articleComment = mongoose.model('articleComment'),
    articleController = require('./articleController');;
mongoose.Promise = Promise;

exports.createArticleComment = function(req, res) {

    var newComment = new articleComment({
        commenter: mongoose.Types.ObjectId(req.userId),
        articleId: mongoose.Types.ObjectId(req.body.articleId),
        comment: req.body.comment,
        createdAt: Date.now() 
    }); 

    var prom = newComment.save(); 

    prom.then(function(savedComment) {
        //update article object, can run async
        articleController.addCommentToArticle(savedComment.articleId.toString(), savedComment._id.toString()); 
        return res.send('saved!');
    })
    .catch(function(err) {
        return res.json({'error': err.toString() });
    });
}