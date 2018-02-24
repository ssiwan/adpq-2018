'use strict';

var mongoose = require('mongoose'),
    article = mongoose.model('article'); 

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

    var query = article.find(queryParams).populate('createdBy').populate('agency').populate('tags');

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
    
    var query = article.find(queryParams).populate('agency').populate('tags').populate('createdBy');
    

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

    //param check
    if (articleId == null || articleId == '') {
        return res.send({'error': 'Please submit an articleId'});
    }

    var queryParams = {};
    queryParams._id = new ObjectId(articleId); 
    queryParams.role = {"$lte": parseInt(req.userRole)};

    var query = article.findOne(queryParams).populate('tags')
                                            .populate('createdBy')
                                            .populate({path: 'comments', populate: {path: 'commenter', model: 'user'}});
    //query.limit(1);

    query.exec()
        .catch(function (err) {
            res.send(err);
        });
    
    query.then(function(art) {
        var articleobj = {};
        if (art != null) {
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
            articleobj['comments'] = art.comments;  
            articleobj['views'] = art.views;
            articleobj['sharedCount'] = art.sharedUsers.length;
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
    var tagpreArray = (req.body.tags).split(','); //hopefully will be a string of tagIds
    tagpreArray.forEach(function (tid) {
        tagArray.push(mongoose.Types.ObjectId(tid)); 
    });    

    //turn tag stringIds into objectIds 

    var newArticle = new article({
        createdBy: mongoose.Types.ObjectId(req.userId),
        agency: mongoose.Types.ObjectId(req.body.agencyId),
        role: req.body.audience,     
        title: req.body.title,
        summary: req.body.shortDesc,       
        tags: tagArray,
        description: req.body.longDesc,
        attachments: req.body.attachments,       
        //approvedBy: mongoose.Types.ObjectId('none'),
        views: 0,//default fields
        sharedUsers: [],
        comments: [],
        createdAt: Date.now(),
        status: 0,
        type: 0 // dud for now
    });

    var prom = newArticle.save();

    prom.then(function() {
        res.send('saved!');
    })
    .catch(function(err) {
        res.json({'error': err.toString() });
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

function getTagNames(tags) {
    var returnarray = []; 
    tags.forEach(function(tag) {
        returnarray.push(tag.value); 
    })
    return returnarray; 
}; 