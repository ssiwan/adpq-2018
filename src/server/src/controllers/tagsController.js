'use strict';

var mongoose = require('mongoose'),
    tags = mongoose.model('tags'),
    articleController = require('./articleController');
mongoose.Promise = Promise;

var ObjectId = mongoose.Types.ObjectId; 

//GET /tags
exports.getTags = function (req, res) {
    var returnlist = [];  
    var query = tags.find();
    
    query.exec().catch(function (err) {
        res.json({'error':'Query error'});
    });  
    
    query.then(function(tgs, blah) {
        tgs.forEach(function(tg) {
                var obj = {};
                obj["id"] = tg._id.toString(); 
                obj["name"] = tg.value;
                returnlist.push(obj);
            });
        res.json({'data': returnlist}); 
    });
};

exports.getSuggestedTags = function(req, res) {    
    var returnlist = []; 
    
    var limit = 0; 
    if (req.query.limit != null) {
        limit = parseInt(req.query.limit); 
    }

    var query = tags.find(); 
    var sortObj = {}; 
    sortObj['articleCount'] = -1; 

    query.sort(sortObj); 

    if (limit > 0) {
        query.limit(limit); 
    }

    query.exec().catch(function (err) {
        res.json({'error':'Query error'});
    });  
    
    query.then(function(tgs, blah) {
        tgs.forEach(function(tg) {
                var obj = {};                
                obj["id"] = tg._id.toString(); 
                obj["name"] = tg.value;
                obj["articleCount"] = tg.articleCount; 
                returnlist.push(obj);
            });
        res.json({'data': returnlist}); 
    });
}

//*******************************INTERNAL API FUNCTIONS ************************//

exports.convertTags = function(tagStringArray, articleId) {
    var query = tags.find().in('value', tagStringArray);
    var tagsToAddToDB = []; 
    var tagIdArray = []; 

    query.exec().then(function(tgs) {
        if (tgs != null) {
            tgs.forEach(function(tg) {
                tagIdArray.push(new ObjectId(tg._id.toString()));
                if (tagStringArray.includes(tg.value)) {
                    for (var i=tagStringArray.length-1; i>=0; i--) { //remove from tagstringarray
                        if (tagStringArray[i] === tg.value) {
                            tagStringArray.splice(i, 1);
                            break; 
                        }
                    }
                } 
            });            
        }

        tagStringArray.forEach(function(tgta) {
            var newtag = new tags({
                value: tgta,
                articleCount: 0
            });
            tagsToAddToDB.push(newtag); 
        });

        tags.insertMany(tagsToAddToDB)
            .then(function(returntags) {
                if (returntags != null) {
                    returntags.forEach(function(returntag) {
                        tagIdArray.push(new ObjectId(returntag._id.toString())); 
                    });
                }
                articleController.addTagIdsToArticle(tagIdArray, articleId); 
                return; 
            }); 
        return; 
    }); 
};    

exports.incrementTagArticleCounts = function(tagIds) {
    //maybe not necessary but just in case
    var tagObjectIds = []; 

    tagIds.forEach(function(tagid) {
        tagObjectIds.push(new ObjectId(tagid.toString())); 
    });

    var queryParams =  {'_id': { $in: tagObjectIds}};

    tags.update(queryParams, { $inc: { articleCount: 1}}, { multi: true }, 
                                function(err, returnvals) {
                                    return; 
                                });
}