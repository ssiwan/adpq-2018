'use strict';

var mongoose = require('mongoose'),
    article = mongoose.model('article'),
    users = mongoose.model('user'); 
    

var ObjectId = mongoose.Types.ObjectId; 

//GET /searchArticles
exports.search = function (req, res) {
    var keyword = req.query.keyword;
    var returnlist = []; 
    var queryParams = {};

    //if keyword exists in any title or description
    if (keyword != null && keyword.length > 0) {
        queryParams.title = {'$regex': keyword, '$options': 'i'};
        //queryParams.description = {'$regex': {value: keyword}, '$options': 'i'};
    }

    queryParams.role = {"$lte": parseInt(req.userRole)};

    var query = article.find().or([queryParams, {createdBy: new ObjectId(req.userId)}])
                            .populate('createdBy').populate('agency').populate('tags');

    //if keyword exists in any tags

    query.exec()
        .catch(function (err) {
            res.send(err);
        });  
    
    query.then(function(articles) {
        articles.forEach(function (art, index) {
            var articleobj = {};
            articleobj['id'] = art._id.toString();
            articleobj['title'] = art.title;
            articleobj['summary'] = art.summary;
            articleobj['tags'] = getTagNames(art.tags);
            articleobj['lastUpdatedAt'] = art.createdAt; //to be replaced after ArticleEdit 
            articleobj['createdAt'] = art.createdAt;
            articleobj['createdBy'] = art.createdBy; 
            articleobj['agency'] = art.agency.value;
            articleobj['status'] = art.status;
            articleobj['approvedBy'] =  art.approvedBy; 
            articleobj['description'] = art.description;
            articleobj['attachments'] = art.attachments;
            articleobj['views'] = art.views;

            returnlist.push(articleobj);   
        }); 
        res.json({'data':returnlist}); 
    });      
};

//GET /articles
exports.getArticles = function(req, res, next) {
    var returnlist = []; 
    var queryParams = {};

    var sortField = req.query.sort;
    var orderString = req.query.order;
    var limitString = req.query.limit;
    var agencyId = req.query.agencyId;
    var tagId = req.query.tagId;
    var startDateString = req.query.dateStart;//mm-dd-yyyy
    var endDateString = req.query.dateEnd;        

    queryParams.role = {"$lte": parseInt(req.userRole)}; //set logic to less than 

    // if filtering by start date and/or end date
    var startDate = null;
    var endDate = null; 

    if (startDateString != null) {
        var tempArray = startDateString.split('-');
        startDate = new Date(parseInt(tempArray[2]), parseInt(tempArray[0])-1, parseInt(tempArray[1]));
    }

    if (endDateString != null) {
        var tempArray = endDateString.split('-');
        endDate = new Date(parseInt(tempArray[2]), parseInt(tempArray[0])-1, parseInt(tempArray[1]));
    }

    if (startDate != null && endDate != null) {
        queryParams.createdAt = {"$gt": startDate, "$lt": endDate}
    }
    else if (startDate != null && endDate == null) {
        queryParams.createdAt = {"$gt": startDate}     
    }
    else if (startDate == null && endDate != null) {
        queryParams.createdAt = {"$lt": endDate}     
    }


    //if filtering by enddate
    if (agencyId != null && agencyId != '') {
        queryParams.agency = new ObjectId(agencyId); 
    }


    //if filtering by tag
    if (tagId != null && tagId != '') {//automatically searches array.contains
        queryParams.tags = new ObjectId(tagId); 
    }
    
    var query = article.find().or([queryParams, {createdBy: new ObjectId(req.userId)}])
                            .populate('createdBy').populate('agency').populate('tags');
    

    //if filtering by sort and order 
    if (orderString != null) {
        var order = parseInt(orderString);
        
        if (!isNaN(order)) {
            if (sortField != null) {
                var sortObj = {};
                sortObj[sortField] = order;
                query.sort(sortObj)
            }
        }
    }


    //if filtering by limit
    if (limitString != null) {
        var limit = parseInt(limitString);

        if (!isNaN(limit)) {
            query.limit(limit); 
        }
    }

    //execute query
    query.exec()
        .catch(function (err) {
            res.send(err);
        });  

    query.then(function(articles) {
        articles.forEach(function (art, index) {
            var articleobj = {};
            articleobj['id'] = art._id.toString();
            articleobj['title'] = art.title;
            articleobj['summary'] = art.summary;
            articleobj['tags'] = getTagNames(art.tags); 
            articleobj['lastUpdatedAt'] = art.createdAt; //to be replaced after ArticleEdit
            articleobj['createdAt'] = art.createdAt;
            articleobj['createdBy'] = art.createdBy; 
            articleobj['agency'] = art.agency.value;
            articleobj['status'] = art.status;
            articleobj['approvedBy'] =  art.approvedBy; 
            articleobj['description'] = art.description;
            articleobj['attachments'] = art.attachments;
            articleobj['views'] = art.views;

            returnlist.push(articleobj);   
        }); 
        res.json({'data':returnlist}); 
    });

}

//GET /articleDetails
exports.getArticleDetails = function(req, res) {
    var articleId = req.params.articleId; 
    var userRole = parseInt(req.userRole); 
    //param check
    if (articleId == null || articleId == '') {
        return res.send({'error': 'Please submit an articleId'});
    }

    var queryParams = {};
    queryParams._id = new ObjectId(articleId); 

    var query = article.findOne(queryParams).populate('tags')
                                            .populate('createdBy')
                                            .populate('agency')
                                            .populate({path: 'articleEdits', populate: {path: 'createdBy', model: 'user'}})
                                            .populate({path: 'comments', populate: {path: 'commenter', model: 'user'}});
    //query.limit(1);

    query.exec()
        .catch(function (err) {
            res.send(err);
        });
    
    query.then(function(art) {
        var articleobj = {};
        if (art != null) {
            if ((art.createdBy._id.toString() == req.userId || art.role <= userRole)) {
                articleobj['id'] = art._id.toString();
                articleobj['title'] = art.title;
                articleobj['summary'] = art.summary;
                articleobj['tags'] = getTagNames(art.tags);
                articleobj['createdAt'] = art.createdAt;
                articleobj['createdBy'] = art.createdBy; 
                articleobj['agencyId'] = art.agency._id.toString();
                articleobj['agencyName'] = art.agency.value;
                articleobj['status'] = art.status;
                articleobj['description'] = art.description;
                articleobj['attachments'] = art.attachments;
                articleobj['comments'] = art.comments;  
                articleobj['views'] = art.views;
                articleobj['sharedCount'] = art.shares; 
                articleobj['lastUpdated'] = getLastUpdated(art.articleEdits);
                articleobj['approvedBy'] = getApprover(art.articleEdits); 
            }
        }
        res.json({'data': articleobj}); 
    }); 
}

//tempcreate not actually going to be a GET - will convert to Post /createArticle
exports.createArticle = function(req, res) {

    if (req.userRole == '0') {
        return res.json({error: 'User not permitted'});
    }
    var userRole = parseInt(req.userRole); 

    var tagArray = []; 
    if (req.body.tags != null && req.body.tags.length > 0) {
        var tagpreArray = (req.body.tags).split(','); //hopefully will be a string of tagIds
        //tag functionality here    
    }

    var attachmentsArray = []; 
    var baseUrl = 'https://s3-us-west-1.amazonaws.com/adpq-assets/'; 
    if (req.body.attachments != null && req.body.attachments.length > 0) {
        req.body.attachments.forEach(function(atchmt) {
            attachmentsArray.push(baseUrl + atchmt); 
        });
    }

    //turn tag stringIds into objectIds 

    var newArticle = new article({
        createdBy: mongoose.Types.ObjectId(req.userId),
        agency: mongoose.Types.ObjectId(req.body.agencyId),
        role: req.body.audience,     
        title: req.body.title,
        summary: req.body.shortDesc,       
        tags: [],
        description: req.body.longDesc,
        attachments: attachmentsArray,       
        views: 0,//default fields
        shares: 0,
        comments: [],
        articleEdits: [],
        createdAt: Date.now(),
        status: 0,
        trendingScore: 0,
        type: 0 // dud for now
    });

    var prom = newArticle.save();

    prom.then(function(artreturn) {
        //add tags that don't exist
        var jsonreturn = {
            status: 'saved!',
            articleId: artreturn._id.toString() 
        }
        res.json(jsonreturn);
    })
    .catch(function(err) {
        res.json({'error': err.toString() });
    });
}    

exports.dashboardAnalytics = function(req, res) {
    //if userRole == 2, then add total users query 
    var objuserId = new ObjectId(req.userId); 
    var promiseArray = []; 

    //Articles Published Count  
    var queryParams = {}; 
    queryParams.createdBy = objuserId;  
    queryParams.status = 1; 
    var query = article.count(queryParams); 

    promiseArray.push(query); 

    //Articles In Review Count
    var queryParams2 = {};
    queryParams2.createdBy = objuserId; 
    queryParams2.status = 0; 
    var query2 = article.count(queryParams2); 

    promiseArray.push(query2); 

    //Articles Declined Count
    var queryParams3 = {};
    queryParams3.createdBy = objuserId; 
    queryParams3.status = 2; 
    var query3 = article.count(queryParams3); 

    promiseArray.push(query3);

    //Views Count - from only published
    var queryParams4 = {};
    queryParams4.createdBy = objuserId; 
    queryParams4.status = 1; 
    var query4 = article.find(queryParams4).then(function(result) {
        var returnCount = 0; 
        if (result != null) {
            result.forEach(function(ret) {
                returnCount += ret.views; 
            });
        }
        return returnCount;  
    }); 

    promiseArray.push(query4);

    //Share Count - from only published
    var queryParams5 = {};
    queryParams5.createdBy = objuserId; 
    queryParams5.status = 1; 
    var query5 = article.find(queryParams5).then(function(result) {
        var returnCount = 0; 
        if (result != null) {
            result.forEach(function(ret) {
                returnCount += ret.shares; 
            });
        }
        return returnCount;  
    }); 

    promiseArray.push(query5); 

    //User Count - if admin
    if (req.userRole == 2) {
        var query6 = users.count(); 
        promiseArray.push(query6); 
    }   


    Promise.all(promiseArray).then(function(values) {
        var returndata = {};
        returndata.publishCount = values[0];
        returndata.reviewCount = values[1]; 
        returndata.declineCount = values[2]; 
        returndata.viewCount = values[3];
        returndata.shareCount = values[4];
        if (req.userRole == 2) {
            returndata.userCount = values[5]; 
        }
        return res.json({'data': returndata}); 
    });
}

exports.dashboardTrending = function(req, res) {
    var objuserId = new ObjectId(req.userId);
    var limit = 0; 
    if (req.query.limit != null) {
        limit = parseInt(req.query.limit);  
    }  
    var queryParams = {}; 
    queryParams.role = {"$lte": parseInt(req.userRole)};
    var query = article.find().or([queryParams, {createdBy: objuserId}])
                                .populate('createdBy').populate('agency').populate('tags');    
    var sortObj = {};
    sortObj['trendingScore'] = -1;
    query.sort(sortObj); 
    if (limit != 0) {
        query.limit(limit); 
    }

    query.exec().catch(function(err) {
        return res.json({error: err.toString()}); 
    });

    query.then(function(arts) {
        var returnlist = []; 
        if (arts != null) {
            arts.forEach(function(art) {
                var articleobj = {};
                articleobj['id'] = art._id.toString();
                articleobj['title'] = art.title;
                articleobj['summary'] = art.summary;
                articleobj['tags'] = getTagNames(art.tags); 
                articleobj['lastUpdatedAt'] = art.createdAt; //to be replaced after ArticleEdit
                articleobj['createdAt'] = art.createdAt;
                articleobj['createdBy'] = art.createdBy; 
                articleobj['agency'] = art.agency.value;
                articleobj['status'] = art.status;
                articleobj['description'] = art.description;
                articleobj['views'] = art.views;
                articleobj['shares'] = art.shares; 

                returnlist.push(articleobj);   
            }); 
        }
        return res.json({'data': returnlist}); 
    }); 

    //or([queryParams, {createdBy: new ObjectId(req.userId)}])
}

exports.dashboardPublishedArticles = function(req, res) {
    var userobjid = new ObjectId(req.userId);
    var limit = 0; 
    if (req.query.limit != null) {
        limit = parseInt(req.query.limit); 
    }

    var queryParams = {};
    queryParams.createdBy = userobjid; 
    queryParams.status = 1; 

    var query = article.find(queryParams).populate('createdBy').populate('agency').populate('tags').populate('articleEdits');
    var sortObj = {};
    sortObj['createdAt'] = -1;
    query.sort(sortObj);  
    if (limit != 0) {
        query.limit(limit); 
    }

    query.exec().catch(function(err) {
        return res.json({error: err.toString()}); 
    });

    query.then(function(arts) {
        var returnArticles = []; 
        if (arts != null) {
            arts.forEach(function(art) {
                var articleobj = {}; 
                articleobj['id'] = art._id.toString();
                articleobj['title'] = art.title;
                articleobj['summary'] = art.summary;
                articleobj['tags'] = getTagNames(art.tags); 
                articleobj['createdAt'] = art.createdAt;
                articleobj['createdBy'] = art.createdBy; 
                articleobj['agency'] = art.agency.value;
                articleobj['status'] = art.status;
                articleobj['approvedBy'] =  art.approvedBy; 
                articleobj['description'] = art.description;
                articleobj['attachments'] = art.attachments;
                articleobj['views'] = art.views;
                articleobj['sharedCount'] = art.shares;
                articleobj['lastUpdated'] = getLastUpdated(art.articleEdits); 

                returnArticles.push(articleobj);
            });
        }
        return res.json({data: returnArticles}); 
    })
}

exports.dashboardWorkflow = function(req, res) {
    var userobjid = new ObjectId(req.userId);
    var limit = 0; 
    if (req.query.limit != null) {
        limit = parseInt(req.query.limit); 
    }

    var queryParams = {};
    queryParams.createdBy = userobjid; 
    queryParams.status = 0; 

    var query = article.find(queryParams).populate('createdBy').populate('agency').populate('tags');
    var sortObj = {};
    sortObj['createdAt'] = -1;
    query.sort(sortObj);  
    if (limit != 0) {
        query.limit(limit); 
    }

    query.exec().catch(function(err) {
        return res.json({error: err.toString()}); 
    });

    query.then(function(arts) {
        var returnArticles = []; 
        if (arts != null) {
            arts.forEach(function(art) {
                var articleobj = {}; 
                articleobj['id'] = art._id.toString();
                articleobj['title'] = art.title;
                articleobj['summary'] = art.summary;
                articleobj['tags'] = getTagNames(art.tags); 
                articleobj['createdAt'] = art.createdAt;
                articleobj['createdBy'] = art.createdBy; 
                articleobj['agency'] = art.agency.value;
                articleobj['status'] = art.status;
                articleobj['approvedBy'] =  art.approvedBy; 
                articleobj['description'] = art.description;
                articleobj['attachments'] = art.attachments;
                articleobj['views'] = art.views;
                articleobj['sharedCount'] = art.sharedUsers.length;

                returnArticles.push(articleobj);
            });
        }
        return res.json({data: returnArticles}); 
    })
}

exports.shareArticle = function(req, res) {
    
}

exports.viewArticle = function(req, res) {

}

exports.publishArticle = function(req, res) {

}

//*****************************API internal functions****************//

exports.addCommentToArticle = function(articleId, commentId) {
    var queryParams = {};
    queryParams._id = new ObjectId(articleId);
    
    var query = article.findOne(queryParams);
    query.exec()
        .catch(function (err) {
            res.send(err);
        });
    
    query.then(function(art) {
        art.comments.push(new ObjectId(commentId)); 
        art.save();
        return;  
    });
}

exports.editArticle = function(articleId, articleEditId, articleObj) {
    var attachmentsArray = []; 
    var baseUrl = 'https://s3-us-west-1.amazonaws.com/adpq-assets/'; 
    if (articleObj.attachments != null && articleObj.attachments.length > 0) {
        articleObj.attachments.forEach(function(atchmt) {
            attachmentsArray.push(baseUrl + atchmt); 
        });
    }

        var queryParams = {};
    queryParams._id = new ObjectId(articleId); 

    var query = article.findOne(queryParams);
    query.exec()
        .catch(function (err) {
            res.send(err);
        });
    
    query.then(function(art) {
        art.articleEdits.push(new ObjectId(articleEditId)); 
        art.title = articleObj.title;
        art.agency = new ObjectId(articleObj.agencyId);
        art.role = articleObj.role; 
        art.summary = articleObj.shortDesc;
        art.description = articleObj.longDesc;
        art.attachments = attachmentsArray; 
        art.status = articleObj.status; 
        art.save();
        return; 
    }); 
}

function getTagNames(tags) {
    var returnarray = []; 
    tags.forEach(function(tag) {
        returnarray.push(tag.value); 
    })
    return returnarray; 
}; 

function getLastUpdated(edits) {
    
    if (edits != null && edits.length > 0) {
        var recentEdit = edits[edits.length - 1];
        return recentEdit.createdAt; 
    }
    else {
        return {}; 
    }
}

function getApprover(edits) {
    if (edits != null && edits.length > 0) {
        var recentEdit = edits[edits.length - 1];
        return (recentEdit.createdBy.name.first + " " + recentEdit.createdBy.name.last); 
    }
    else {
        return ""; 
    }
}