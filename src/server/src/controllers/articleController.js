'use strict';

var mongoose = require('mongoose'),
    article = mongoose.model('article');

//GET /searchArticles
exports.search = function (req, res) {
    var keyword = req.query.keyword;
    var returnlist = []; 
    var role = 0;
    var query = {};

    if (keyword != null && keyword.length > 0) {
        query.title = {'$regex': keyword, '$options': 'i'};
    }

    query.role = role;

    var prom = article.find(query);
    
    prom.exec()
        .catch(function (err) {
            res.send(err);
        });  
    
    prom.then(function(articles) {
        articles.forEach(function (art, index) {
            var articleobj = {};
            articleobj['title'] = art.title;
            articleobj['summary'] = art.summary;
            articleobj['tags'] = art.tags;
            articleobj['createdAt'] = art.createdAt;
            articleobj['createdBy'] = getAuthorName('tempAuthorName'); 
            articleobj['agency'] = getAgencyName('tempName');
            articleobj['status'] = art.status;
            articleobj['approvedBy'] =  getApproverName('tempApproverName'); 
            articleobj['description'] = art.description[role];
            articleobj['attachments'] = art.attachments[role];
            articleobj['views'] = art.views;
            articleobj['sharedCount'] = 12;//art.sharedUsers.length; 

            returnlist.push(articleobj);   
        }); 
        res.json({'data':returnlist}); 
    });      
};

//Get /articles
exports.getArticles = function(req, res) {
    //sort, order, limit
    var sortField = req.query.sort;
    var orderString = req.query.order;
    var limitString = req.query.limit;
    
    //to be modified - get user role 
    var role = 0; 

    var returnlist = []; 
    var queryParams = {};
    
    var query = article.find(queryParams);
    
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
            articleobj['title'] = art.title;
            articleobj['summary'] = art.summary;
            articleobj['tags'] = art.tags;
            articleobj['createdAt'] = art.createdAt;
            articleobj['createdBy'] = getAuthorName('tempAuthorName'); 
            articleobj['agency'] = getAgencyName('tempName');
            articleobj['status'] = art.status;
            articleobj['approvedBy'] =  getApproverName('tempApproverName'); 
            articleobj['description'] = art.description[role];
            articleobj['attachments'] = art.attachments[role]; 
            articleobj['views'] = art.views;
            articleobj['sharedCount'] = 12;//art.sharedUsers.length;  

            returnlist.push(articleobj);   
        }); 
        res.json({'data':returnlist}); 
    });

}

//tempcreate not actually going to be a GET - will convert to Post /createArticle
exports.createTempArticle = function(req, res) {
    var tagArray = ['fire'];
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
        agency: mongoose.Types.ObjectId('5a84ad66cb1d2c84e88d5132'),
        role: 1,
        status: 0,
        title: 'Fire article #2 role 1',
        summary: 'summary for Fire article 2',
        approvedBy: mongoose.Types.ObjectId('5a84ad66cb1d2c84e88d5132'),
        tags: tagArray,
        views: 0,
        description: descriptionArray,
        attachments: attachmentArray
    });
    var prom = tempArticle.save();
    prom.then(function() {
        res.send('saved!');
    })
    .catch(function(err) {
        res.json({'error': err.toString() });//will standardize return types next sprint
    });
}    

function getAgencyName(name) {
    return name; 
}

function getAuthorName(name) {
    return name; 
}

function getApproverName(name) {
    return name; 
}