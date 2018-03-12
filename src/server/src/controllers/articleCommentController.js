'use strict';

var mongoose = require('mongoose'),
    articleComment = mongoose.model('articleComment'),
    articleController = require('./articleController');
mongoose.Promise = Promise;

var ObjectId = mongoose.Types.ObjectId;

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
        var jsonreturn = {
            status: 'saved!',
            articleId: savedComment.articleId.toString()
        };     
        return res.json(jsonreturn); 
    })
    .catch(function(err) {
        res.status(400); 
        return res.json({'error': err.toString() });
    });
}

//*******************************INTERNAL API FUNCTIONS*********************//

exports.deleteArticleComments = function(articleId) {
    var articleObjId = new ObjectId(articleId); 
    articleComment.deleteMany({'articleId': articleObjId}).exec();     
}