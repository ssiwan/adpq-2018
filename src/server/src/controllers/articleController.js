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
            articleobj['sharedCount'] = art.sharedUsers.length; 

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
            articleobj['sharedCount'] = art.sharedUsers.length; 

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
                articleobj['approvedBy'] =  art.approvedBy; 
                articleobj['description'] = art.description;
                articleobj['attachments'] = art.attachments;
                articleobj['comments'] = art.comments;  
                articleobj['views'] = art.views;
                articleobj['sharedCount'] = art.sharedUsers.length;
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
        tagpreArray.forEach(function (tid) {
            tagArray.push(mongoose.Types.ObjectId(tid)); 
        });    
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
        tags: tagArray,
        description: req.body.longDesc,
        attachments: attachmentsArray,       
        //approvedBy: mongoose.Types.ObjectId('none'),
        views: 0,//default fields
        sharedUsers: [],
        comments: [],
        articleEdits: [],
        createdAt: Date.now(),
        status: 0,
        type: 0 // dud for now
    });

    var prom = newArticle.save();

    prom.then(function(artreturn) {
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
                returnCount += ret.sharedUsers.length; 
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
    var promiseArray = [];  

    //shares query 
    var sharesQuery = article.aggregate([
        {
            $match: {
                status: 1,
                role: {$lte: parseInt(req.userRole)}
            }
        },
        {'$project': {
            'shareCount': {'$size': '$sharedUsers'}
        }},
        {'$sort': {'shareCount': -1}},
        {'$limit': 1}
    ]).then(function(sharesResult){
        if (sharesResult != null && sharesResult.length > 0) {
            return sharesResult[0]._id.toString();
        }
        else {
            return null;
        }
    });
    promiseArray.push(sharesQuery); 

    //tags query 
    var tagsQuery = article.aggregate([
        {
            $match: {
                status: 1,
                role: {$lte: parseInt(req.userRole)}
            }
        },
        {'$project': {
            'tagCount': {'$size': '$tags'}
        }},
        {'$sort': {'shareCount': -1}},
        {'$limit': 2}
    ]).then(function(tagsResult){
        if (tagsResult != null && tagsResult.length > 0) {
            var tagsObj = [];
            if (tagsResult[0] != null) {
                tagsObj.push(tagsResult[0]._id.toString());

                if (tagsResult[1] != null) {
                    tagsObj.push(tagsResult[1]._id.toString()); 
                }
            }
            return tagsObj; 
        }
        else {
            return null;
        } 
    });
    promiseArray.push(tagsQuery);

    //viewQuery
    var viewsQueryParams = {}; 
    viewsQueryParams.status = 1;
    var sortObj = {}; 
    sortObj['views'] = -1;  
    var viewsQuery = article.find(viewsQueryParams)
        .lte('role', parseInt(req.userRole))
        .populate('createdBy').populate('agency').populate('tags').sort(sortObj).limit(3)
        .then(function(vqResult) {
            return vqResult; 
        });
    promiseArray.push(viewsQuery); 

    Promise.all(promiseArray).then(function(values) {
        var sharedArticleId = values[0];
        var tagsArticleIds = values[1];//could have zero one or two
        var viewsArticles = values[2];         
        var searchIds = []; 
        var returnArticles = {}; 
        var prefilteredArticles = []; 
        var sharedarticleidstring = "";
        var tagarticleidstring = "";  
        var viewarticle = null; 
        
        //input shared article Id to be searched
        if (sharedArticleId == null) {
            returnArticles.mostShared = {}; 
        }
        else {
            sharedarticleidstring = sharedArticleId.toString(); 
            searchIds.push(new ObjectId(sharedarticleidstring)); 
        }

        //input views article id to be searched
        if (tagsArticleIds == null) {
            returnArticles.mostTagged = {};
        }       
        else {
            if (tagsArticleIds[0].toString() != sharedarticleidstring) {
                tagarticleidstring = tagsArticleIds[0].toString();
                searchIds.push(new ObjectId(tagarticleidstring));
            }
            else if (tagsArticleIds[1] != null) {
                tagarticleidstring = tagsArticleIds[1].toString();
                searchIds.push(new ObjectId(tagarticleidstring)); 
            }
            else {
                returnArticles.mostTagged = {}; 
            }
        }

        if (viewsArticles == null) {
            returnArticles.mostViewed = {};             
        }
        else {
            if (viewsArticles[0]._id.toString() != sharedarticleidstring && viewsArticles[0]._id.toString() != tagarticleidstring) {
                viewarticle = viewsArticles[0];
            }
            else if (viewsArticles[1] != null 
                        && viewsArticles[1]._id.toString() != sharedarticleidstring 
                        && viewsArticles[1]._id.toString() != tagarticleidstring) {

            }
            else if (viewsArticles[2] != null) {
                viewarticle = viewsArticles[2]; 
            }
            else {
                returnArticles.mostViewed = {}; 
            }  
        }

        if (searchIds.length > 0) {
            var queryParams = {};         
            var query = article.find().in('_id', searchIds).populate('createdBy').populate('agency').populate('tags'); 

            query.exec().then(function(arts) {
                if (viewarticle != null) {
                    arts.push(viewarticle)
                }
                arts.forEach(function(indart) {
                    var articleobj = {};
                    articleobj['id'] = indart._id.toString();
                    articleobj['title'] = indart.title;
                    articleobj['summary'] = indart.summary;
                    articleobj['tags'] = getTagNames(indart.tags);
                    articleobj['tagCount'] = indart.tags.length;  
                    articleobj['lastUpdatedAt'] = indart.createdAt; //to be replaced after ArticleEdit
                    articleobj['createdAt'] = indart.createdAt;
                    articleobj['createdBy'] = indart.createdBy; 
                    articleobj['agency'] = indart.agency.value;
                    articleobj['status'] = indart.status;
                    articleobj['approvedBy'] =  indart.approvedBy; 
                    articleobj['description'] = indart.description;
                    articleobj['attachments'] = indart.attachments;
                    articleobj['views'] = indart.views;
                    articleobj['sharedCount'] = indart.sharedUsers.length;

                    if (indart.id.toString() == sharedarticleidstring) {
                        returnArticles.mostShared = articleobj; 
                    }
                    else if (indart.id.toString() == tagarticleidstring){
                        returnArticles.mostTagged = articleobj; 
                    }
                    else {
                        returnArticles.mostViewed = articleobj; 
                    }
                });
                return res.json({data: returnArticles});  
            });
        }        
    })
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
                articleobj['sharedCount'] = art.sharedUsers.length;
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