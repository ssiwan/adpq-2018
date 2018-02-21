'use strict';

var mongoose = require('mongoose'),
    article = mongoose.model('article');
var agencyController = require('./agencyController');

var ObjectId = mongoose.Types.ObjectId; 
var userRole = 0; //to be modified - get user role 

//GET /searchArticles
exports.search = function (req, res) {
    var keyword = req.query.keyword;
    var returnlist = []; 
    var query = {};

    if (keyword != null && keyword.length > 0) {
        query.title = {'$regex': keyword, '$options': 'i'};
    }

    query.role = userRole;

    var prom = article.find(query).populate('agency').populate('tags');
    
    prom.exec()
        .catch(function (err) {
            res.send(err);
        });  
    
    prom.then(function(articles) {
        articles.forEach(function (art, index) {
            var articleobj = {};

            articleobj['id'] = art._id.toString();
            articleobj['title'] = art.title;
            articleobj['summary'] = art.summary;
            articleobj['tags'] = getTagNames(art.tags); 
            articleobj['createdAt'] = art.createdAt;
            articleobj['createdBy'] = getAuthorName('tempAuthorName'); 
            articleobj['agency'] = art.agency.value;
            articleobj['status'] = art.status;
            articleobj['approvedBy'] =  getApproverName('tempApproverName'); 
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
exports.getArticles = function(req, res) {
    //sort, order, limit
    var sortField = req.query.sort;
    var orderString = req.query.order;
    var limitString = req.query.limit;
    var agencyId = req.query.agencyId;
    var tagId = req.query.tagId; 

    var returnlist = []; 
    var queryParams = {};
    
    if (agencyId != null && agencyId != '') {
        queryParams.agency = new ObjectId(agencyId); 
    }

    if (tagId != null && tagId != '') {//automatically searches array.contains
        queryParams.tags = new ObjectId(tagId); 
    }
    
    var query = article.find(queryParams).populate('agency').populate('tags');
    
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

    if (limitString != null) {
        var limit = parseInt(limitString);

        if (!isNaN(limit)) {
            query.limit(limit); 
        }
    }

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
            articleobj['createdAt'] = art.createdAt;
            articleobj['createdBy'] = getAuthorName('tempAuthorName'); 
            articleobj['agency'] = art.agency.value;
            articleobj['status'] = art.status;
            articleobj['approvedBy'] =  getApproverName('tempApproverName'); 
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
    var articleId = req.query.articleId; 

    //param check
    if (articleId == null || articleId == '') {
        res.send({'error': 'Please submit an articleId'});
    }

    var queryParams = {};
    queryParams._id = new ObjectId(articleId); 

    var query = article.find(queryParams);
    query.limit(1);

    query.exec()
        .catch(function (err) {
            res.send(err);
        });
    
    query.then(function(art) {
        var articleobj = {};
        articleobj['id'] = art._id.toString();
        articleobj['title'] = art.title;
        articleobj['summary'] = art.summary;
        articleobj['tags'] = getTagNames('');
        articleobj['createdAt'] = art.createdAt;
        articleobj['createdBy'] = getAuthorName('tempAuthorName'); 
        articleobj['agency'] = getAgencyName('tempName');
        articleobj['status'] = art.status;
        articleobj['approvedBy'] =  getApproverName('tempApproverName'); 
        articleobj['description'] = art.description[userRole];
        articleobj['attachments'] = art.attachments[userRole]; 
        articleobj['views'] = art.views;
        articleobj['sharedCount'] = art.sharedUsers.length;

        res.json({'data': articleobj}); 
    }); 
}

//tempcreate not actually going to be a GET - will convert to Post /createArticle
exports.createTempArticle = function(req, res) {
    var tag1 = new ObjectId('5a8b55bca2d13ad4ba5369e3');
    var tag2 = new ObjectId('5a8b55bca2d13ad4ba5369ef'); 
    var tagArray = [tag1];

    var sharedUsersArray = [tag1]; 

    var descriptionArray = [
        {
            role: 0,
            value: 'role 0 description'
        },
        {
            role: 1,
            value: 'role 1 description'
        },
        {
            role: 2,
            value: 'role 2 description'
        },
        {
            role: 3,
            value: 'role 3 description'
        },
        {
            role: 4,
            value: 'role 4 description'
        }
    ];
    var attachmentArray = [
        {
            role: 0,
            value: ['role 0 attachment 1', 'role 0 attachment 2']
        },
        {
            role: 1,
            value: ['role 1 attachment 1', 'role 1 attachment 2']
        },
        {
            role: 2,
            value: ['role 2 attachment 1', 'role 2 attachment 2']
        },
        {
            role: 3,
            value: ['role 3 attachment 1', 'role 3 attachment 2']
        },
        {
            role: 4,
            value: ['role 4 attachment 1', 'role 4 attachment 2']
        }
    ]; 

    var tempArticle = new article({
        createdAt: Date.now(),
        createdBy: mongoose.Types.ObjectId('5a84ad66cb1d2c84e88d5132'),
        agency: mongoose.Types.ObjectId('5a8b73f94212d1f20f847b9d'),
        role: 0,
        status: 0,
        title: 'Test Article 5',
        summary: 'Test Article 5 Summary',
        approvedBy: mongoose.Types.ObjectId('5a84ad66cb1d2c84e88d5132'),
        tags: tagArray,
        views: 15,
        description: descriptionArray,
        attachments: attachmentArray,
        sharedUsers: sharedUsersArray
    });
    var prom = tempArticle.save();
    prom.then(function() {
        res.send('saved!');
    })
    .catch(function(err) {
        res.json({'error': err.toString() });
    });
}    

//*****************************API internal functions****************//

function getTagNames(tags) {
    var returnarray = []; 
    tags.forEach(function(tag) {
        returnarray.push(tag.value); 
    })
    return returnarray; 
}

function getAuthorName(name) {
    return name; 
}

function getApproverName(name) {
    return name; 
}