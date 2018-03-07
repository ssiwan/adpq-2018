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
    articleObj.status = 0;

    var tagArray = [];  
    if (req.body.tags != null && req.body.tags.length > 0) {
        var tagpreArray = (req.body.tags).split(','); //hopefully will be a string of tagIds
        tagpreArray.forEach(function(tg) {
            if (!tagArray.includes(tg.toLowerCase())) {
                tagArray.push(tg.toLowerCase()); 
            }
        }); 
    }

    articleObj.tags = tagArray; 

    //tag feature later on

    var newEdit = new articleEdit({
        createdBy: new ObjectId(req.userId),
        articleId: new ObjectId(req.body.articleId),
        status: 0,
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
    if (req.userRole != '2') {//will need to change to 2 later
        return res.json({error: 'User not permitted'});
    }

    var newEdit = new articleEdit({
        createdBy: new ObjectId(req.userId),
        articleId: new ObjectId(req.body.articleId),
        status: 1,
        createdAt: Date.now()
    }); 
    
    var prom = newEdit.save();

    prom.then(function(editreturn) {
        articleController.publishOrDeclineArticle(req.body.articleId, editreturn._id.toString(), 1); 
        return res.json({status: 'saved!'});
    })
    .catch(function(err) {
        return res.json({'error': err.toString() });
    });
}

exports.declineArticle = function(req, res) {
    if (parseInt(req.userRole) != 2) {
        return res.json({error: 'User not permitted'});
    }

    var newEdit = new articleEdit({
        createdBy: new ObjectId(req.userId),
        articleId: new ObjectId(req.body.articleId),
        status: 2,
        createdAt: Date.now()
    }); 
    
    var prom = newEdit.save();

    prom.then(function(editreturn) {
        articleController.publishOrDeclineArticle(req.body.articleId, editreturn._id.toString(), 2); 
        return res.json({status: 'saved!'});
    })
    .catch(function(err) {
        return res.json({'error': err.toString() });
    });
}

//********************************* INTERNAL API FUNCTION**************//
exports.deleteArticleEdits = function(articleId) {
    var articleObjId = new ObjectId(articleId); 
    articleEdit.deleteMany({'articleId': articleObjId}).exec();     
}