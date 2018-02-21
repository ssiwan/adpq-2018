'use strict';
var express = require('express');
var router = express.Router();

module.exports = function (app, apiKey) {

//***********CONTROLLERS****************************//
    var tagsController = require('./controllers/tagsController');
    var agencyController = require('./controllers/agencyController');
    var articleController = require('./controllers/articleController');


//***********ROUTES****************************//

//apiKey check 
    router.use(function(req, res, next) {
        if (req.header('apiKey') != apiKey) {
            res.send({'error': 'Invalid api key'}); 
        }
        else {             
            next();
        }
    });

//tagRoutes
    //GET    
        router.get('/tags', tagsController.getTags); 

    //POST

    //PUT

    //DELETE

//agencyRoutes
    //GET
        router.get('/agencies', agencyController.getAgencies);
    
    //POST

    //PUT

    //DELETE

//articleRoutes
    //GET
        router.get('/searchArticles', articleController.search);
        router.get('/articles', articleController.getArticles);
        router.get('/articleDetails', articleController.getArticleDetails); 

    //POST

    //PUT

    //DELETE

//**************MOUNT ROUTER********************//
    app.use('/api/v1', router); 
};