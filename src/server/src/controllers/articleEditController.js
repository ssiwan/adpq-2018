'use strict';

var mongoose = require('mongoose'),
    articleEdit = mongoose.model('articleEdit'),
    articleController = require('./articleController');

var ObjectId = mongoose.Types.ObjectId; 

exports.editArticle = function(req, res) {
    if (req.userRole == '0') {//will need to change to 2 later
        return res.json({error: 'User not permitted'});
    }

    var articleId = req.body.articleId;
    var articleObj = {};
    articleObj.title = req.body.title; 
    articleObj.agencyId = req.body.agencyId; 
    articleObj.role = req.body.audience; 
    articleObj.shortDesc = req.body.shortDesc; 
    articleObj.longDesc = req.body.longDesc; 
    articleObj.attachments = req.body.attachments; 
    articleObj.status = req.body.status; 
    //tag feature later on

    var newEdit = new articleEdit({
        createdBy: new ObjectId(req.userId),
        articleId: new ObjectId(req.body.articleId),
        status: req.body.status,
        createdAt: Date.now()
    }); 

    var prom = newEdit.save();

    prom.then(function(editreturn) {
        articleController.editArticle(articleId, editreturn._id.toString(), articleObj); 
        return res.json({status: 'saved!'});
    })
    .catch(function(err) {
        return res.json({'error': err.toString() });
    });  
}

exports.publishArticle = function(req, res) {
    //create one last edit 
    //increment agency 
    //increment tags
}