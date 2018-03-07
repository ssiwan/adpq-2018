'use strict';

var mongoose = require('mongoose'),
    article = mongoose.model('article'),
    users = mongoose.model('user'),
    tagController = require('./tagsController'),
    agencyController = require('./agencyController'); 
    
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
    queryParams.status = 1; 

    var query = article.find().or([queryParams, {createdBy: new ObjectId(req.userId), status: 1}])
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
            articleobj['shares'] = art.shares; 

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
    queryParams.status = 1; 

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
    
    var query = article.find().or([queryParams, {createdBy: new ObjectId(req.userId), status: 1}])
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
            articleobj['shares'] = art.shares; 

            returnlist.push(articleobj);   
        }); 
        res.json({'data':returnlist}); 
    });

}

//GET /articleDetails
exports.getArticleDetails = function(req, res) {
    var articleId = req.params.articleId;
    var userRole = 0;
    if (req.userRole != null) { 
        userRole = parseInt(req.userRole);
    }
    //param check
    if (articleId == null || articleId == '') {
        return res.send({'error': 'Please submit an articleId'});
    }

    var queryParams = {};

    if (userRole == 0) {
        queryParams.status = 1; 
    }

    queryParams._id = new ObjectId(articleId); 

    var query = article.findOne(queryParams).populate('tags')
                                            .populate('createdBy')
                                            .populate('agency')
                                            .populate({path: 'articleEdits', populate: {path: 'createdBy', model: 'user'}})
                                            .populate({path: 'comments', populate: {path: 'commenter', model: 'user'}});

    query.exec()
        .catch(function (err) {
            res.send(err);
        });
    
    query.then(function(art) {
        var articleobj = {};
        if (art != null) {
            if ((art.status == 1 && art.role <= userRole ) || (art.createdBy._id.toString() == req.userId || userRole == 2)) {
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
                articleobj['role'] = art.role; 
                articleobj['shares'] = art.shares; 
                articleobj['lastUpdated'] = getLastUpdatedDate(art.articleEdits);
                if (art.status == 1) {
                    articleobj['approvedBy'] = getApprover(art.articleEdits);
                }
                articleobj['history'] = art.articleEdits;  
            }
        }
        res.json({'data': articleobj}); 
    }); 
}

//POST /articles
exports.createArticle = function(req, res) {

    if (req.userRole == '0') {
        return res.json({error: 'User not permitted'});
    }
    var userRole = parseInt(req.userRole); 

    var tagArray = []; 
    if (req.body.tags != null && req.body.tags.length > 0) {
        var tagpreArray = (req.body.tags).split(','); //hopefully will be a string of tagIds
        tagpreArray.forEach(function(tg) {
            if (!tagArray.includes(tg.toLowerCase())) {
                tagArray.push(tg.toLowerCase()); 
            }
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
        tagController.convertTags(tagArray, artreturn._id.toString()); 
        var jsonreturn = {
            status: 'saved!',
            articleId: artreturn._id.toString() 
        }; 
        res.json(jsonreturn);
    })
    .catch(function(err) {
        res.json({'error': err.toString() });
    });
}    

//GET /dashboardAnalytics
exports.dashboardAnalytics = function(req, res) {
    //if userRole == 2, then add total users query 
    var objuserId = new ObjectId(req.userId); 
    var role = parseInt(req.userRole);
    var isStaff = (role == 1);  
    var promiseArray = []; 

    //Articles Published Count  
    var queryParams = {}; 
    if (isStaff) {
        queryParams.createdBy = objuserId;
    }  
    queryParams.status = 1; 
    var query = article.count(queryParams); 

    promiseArray.push(query); 

    //Articles In Review Count
    var queryParams2 = {};
    if (isStaff) {
        queryParams2.createdBy = objuserId;
    } 
    queryParams2.status = 0; 
    var query2 = article.count(queryParams2); 

    promiseArray.push(query2); 

    //Articles Declined Count
    var queryParams3 = {};
    if (isStaff) {
        queryParams3.createdBy = objuserId;
    } 
    queryParams3.status = 2; 
    var query3 = article.count(queryParams3); 

    promiseArray.push(query3);

    //Views Count - from only published
    var queryParams4 = {};
    if (isStaff) {
        queryParams4.createdBy = objuserId;
    } 
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
    if (isStaff) {
        queryParams5.createdBy = objuserId;
    } 
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
    if (!isStaff) {
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

//GET /dashboardTrending
exports.dashboardTrending = function(req, res) {
    var objuserId = new ObjectId(req.userId);
    var limit = 0; 
    if (req.query.limit != null) {
        limit = parseInt(req.query.limit);  
    }  
    var queryParams = {}; 
    queryParams.status = 1; 
    queryParams.role = {"$lte": parseInt(req.userRole)};
    var query = article.find().or([queryParams, {createdBy: objuserId, status: 1}])
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

//GET /dashboardMyPublished
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
                articleobj['shares'] = art.shares;
                articleobj['lastUpdated'] = getLastUpdatedDate(art.articleEdits); 

                returnArticles.push(articleobj);
            });
        }
        return res.json({data: returnArticles}); 
    });
}

//GET /dashboardWorkflow
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
                articleobj['shares'] = art.shares;

                returnArticles.push(articleobj);
            });
        }
        return res.json({data: returnArticles}); 
    })
}

//GET /adminDashboardDeclined
exports.admindbdeclined = function(req, res) {
    if (parseInt(req.userRole) != 2) {
        return res.json({error: 'User not permitted'}); 
    }
    var limit = 0; 
    if (req.query.limit != null) {
        limit = parseInt(req.query.limit); 
    }

    var queryParams = {}; 
    queryParams.status = 2;

    var query = article.find(queryParams).populate('createdBy').populate('agency').populate('tags');; 

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
                articleobj['shares'] = art.shares;
                articleobj['lastUpdated'] = getLastUpdatedDate(art.articleEdits); 

                returnArticles.push(articleobj);
            });
        }
        return res.json({data: returnArticles}); 
    });
}

//GET /adminDashboardPending
exports.admindbpending = function(req, res) {
    if (parseInt(req.userRole) != 2) {
        return res.json({error: 'User not permitted'}); 
    }
    var limit = 0; 
    if (req.query.limit != null) {
        limit = parseInt(req.query.limit); 
    }

    var queryParams = {}; 
    queryParams.status = 0;

    var query = article.find(queryParams).populate('createdBy').populate('agency').populate('tags');; 

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
                articleobj['shares'] = art.shares;
                articleobj['lastUpdated'] = getLastUpdatedDate(art.articleEdits); 

                returnArticles.push(articleobj);
            });
        }
        return res.json({data: returnArticles}); 
    });
}

//GET /adminDashboardApproved
exports.admindbapproved = function(req, res) {
    if (parseInt(req.userRole) != 2) {
        return res.json({error: 'User not permitted'}); 
    }
    var limit = 0; 
    if (req.query.limit != null) {
        limit = parseInt(req.query.limit); 
    }

    var queryParams = {}; 
    queryParams.status = 1;

    var query = article.find(queryParams).populate('createdBy').populate('agency').populate('tags');; 

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
                articleobj['shares'] = art.shares;
                articleobj['lastUpdated'] = getLastUpdatedDate(art.articleEdits); 

                returnArticles.push(articleobj);
            });
        }
        return res.json({data: returnArticles}); 
    });
}

//PATCH /incrementViews
exports.incrementViews = function(req, res) {
    var articleobjId = new ObjectId(req.params.articleId);

    var queryParams = {}; 
    queryParams._id = articleobjId; 

    var query = article.findOne(queryParams);
    query.exec().then(function(art) {
        if (art.status == 1) {
            art.views = art.views + 1;
            art.trendingScore = art.trendingScore + 1;  
            art.save(); 
        }
        return res.send('saved!'); 
    });
}

//PATCH /incrementShares
exports.incrementShares = function(req, res) {
    var articleobjId = new ObjectId(req.params.articleId);

    var queryParams = {}; 
    queryParams._id = articleobjId; 

    var query = article.findOne(queryParams);
    query.exec().then(function(art) {
        if (art.status == 1) {
            art.shares = art.shares + 1;
            art.trendingScore = art.trendingScore + 3;  
            art.save(); 
        }
        return res.send('saved!'); 
    });
}

//DELETE /deleteArticle
exports.deleteArticle = function(req, res) {
    if (req.params.articleId == null) {
        return res.json({error: 'Please submit an article id to delete'}); 
    }
    var userRole = parseInt(req.userRole); 

    if (userRole == 0) {
        return res.json({error: 'Role not allowed'}); 
    }

    var userobjid = new ObjectId(req.userId); 

    var articleobjid = new ObjectId(req.params.articleId); 

    var queryParams = {}; 
    queryParams._id = articleobjid; 
    var query = article.findOne(queryParams); 
    query.catch(function(err) {
        return res.json({error: err.toString()}); 
    }); 
    query.then(function(returnarticle) {    
        if (returnarticle != null) {
            if ((userRole == 2) || ((returnarticle.status == 0) && (returnarticle.createdBy.toString() == req.userId))) {
                if (returnarticle.status == 1) {
                    tagController.decrementTagArticleCounts(returnarticle.tags);
                    agencyController.decrementAgencyArticleCount(returnarticle.agency.toString()); 
                }

                var deleteQuery = article.find(queryParams).remove().exec();
                deleteQuery.then(function(ret){
                    return res.json({data:'article removed!'}); 
                }) 
            }
            else {
                return res.json({error: 'Delete is not permitted'}); 
            }
        }
        else {
            return res.json({error: 'article not found'}); 
        }
    }); 
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
        if (art.status == 0) {
            tagController.convertTags(articleObj.tags, articleId); 
            art.articleEdits.push(new ObjectId(articleEditId)); 
            art.title = articleObj.title;
            art.agency = new ObjectId(articleObj.agencyId);
            art.role = articleObj.role; 
            art.summary = articleObj.shortDesc;
            art.description = articleObj.longDesc;
            art.attachments = attachmentsArray; 
            art.status = articleObj.status; 
            art.save();
        }
        return; 
        
    }); 
}

exports.publishOrDeclineArticle = function(articleId, articleEditId, status) {
    var queryParams = {};
    queryParams._id = new ObjectId(articleId);

    var query = article.findOne(queryParams);
    query.exec()
        .catch(function (err) {
            res.send(err);
        });
    
    query.then(function(art) {
        if (status == 1) { 
            agencyController.incrementAgencyArticleCount(art.agency.toString()); 
            tagController.incrementTagArticleCounts(art.tags);
        }
        art.articleEdits.push(new ObjectId(articleEditId)); 
        art.status = status; 
        art.save();
        return; 
    });  
}

exports.addTagIdsToArticle = function(tagsIdArray, articleId) {
     var queryParams = {};
     queryParams._id = new ObjectId(articleId);  
     var query = article.findOne(queryParams); 

     query.exec().then(function(art) {
         art.tags = tagsIdArray;
         art.save(); 
     });
}; 

function getTagNames(tags) {
    var returnarray = []; 
    tags.forEach(function(tag) {
        returnarray.push(tag.value); 
    })
    return returnarray; 
}; 

function getLastUpdatedDate(edits) {
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