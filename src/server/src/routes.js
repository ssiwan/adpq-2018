'use strict';
var express = require('express'),
    jwt = require('jsonwebtoken');
var router = express.Router();

module.exports = function (app, apiParseKey) {

//***********CONTROLLERS****************************//
    var tagsController = require('./controllers/tagsController');
    var agencyController = require('./controllers/agencyController');
    var articleController = require('./controllers/articleController');
    var userController = require('./controllers/userController'); 

//***********ROUTES****************************//

// User Authentification check
    router.use(function(req, res, next) {
        //routes allowed 
        const permissibleRoutes = ['/user/signIn', 
                                    '/articles', 
                                    //'/tags', 
                                    '/agencies', 
                                    '/searchArticles']; //(permissibleRoutes.indexOf(req.url) < 0)

        var token = req.header('Authentication');         

        if (token && token.length > 0) {
            jwt.verify(token, apiParseKey, function(err, decoded) {
                if (err) {                    
                    return res.json({error: 'Failed to authenticate token'});
                }
                else {
                    req.userRole = decoded.role; 
                    next(); 
                }
            });
        }
        else if (permissibleRoutes.includes(req.path)) {             
            req.userRole = 0; 
            if (permissibleRoutes.indexOf(req.path) == 0) {//sign in
                req.PK = apiParseKey; 
            }
            next(); 
        }
        else {
            return res.json({error: 'Please provide an authentication token'}); 
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
        //router.get('/createTempArticle', articleController.createTempArticle);  

    //POST

    //PUT

    //DELETE

//userRoutes
    //GET 

    //POST
        router.post('/user/signIn', userController.signIn);
    //PUT

    //DELETE

//**************MOUNT ROUTER********************//
    app.use('/api/v1', router); 
};