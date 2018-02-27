'use strict';
var express = require('express'),
    jwt = require('jsonwebtoken'),
    AWS = require('aws-sdk');
var router = express.Router();

module.exports = function (app, apiParseKey, AWSKeys) {

//***********CONTROLLERS****************************//
    var tagsController = require('./controllers/tagsController');
    var agencyController = require('./controllers/agencyController');
    var articleController = require('./controllers/articleController');
    var userController = require('./controllers/userController'); 
    var articleCommentController = require('./controllers/articleCommentController');
    var articleEditController = require('./controllers/articleEditController');  

//***********ROUTES****************************//

// User Authentification check
    router.use(function(req, res, next) {
        //routes allowed 
        const permissibleRoutes = ['/user/signIn', 
                                    '/articles', 
                                    '/tags', 
                                    '/agencies', 
                                    '/searchArticles']; //(permissibleRoutes.indexOf(req.url) < 0)

        var token = req.header('Authorization');         

        if (token && token.length > 0) {
            jwt.verify(token, apiParseKey, function(err, decoded) {
                if (err) {                    
                    return res.json({error: 'Failed to authenticate token'});
                }
                else {
                    req.userRole = decoded.role;
                    req.userId = decoded.userId;
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
        router.get('/articles/:articleId', articleController.getArticleDetails);
        router.get('/articles', articleController.getArticles);        

    //POST
        router.post('/articles', articleController.createArticle);

//articleEditRoutes
    //POST
        router.post('/editArticle', articleEditController.editArticle); 

//articleCommentRoutes
    //POST
        router.post('/articleComment', articleCommentController.createArticleComment);

//userRoutes
    //POST
        router.post('/user/signIn', userController.signIn);

//UTILIES - will create utility file if need grows
//presigned s3 url
    //GET
        router.post('/preS3', function(req, res) {
            
            var filename = req.body.name; 

            function guid() {
                function s4() {
                    return Math.floor((1 + Math.random()) * 0x10000)
                        .toString(16)
                        .substring(1);
                    }
                return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
            }

            var tempKey = guid(); 

            AWS.config.update({accessKeyId: AWSKeys.AccessKey, secretAccessKey: AWSKeys.SecretAccessKey});
            var s3 = new AWS.S3({
                signature: 'v2'
            }); 

            var myBucket = 'adpq-assets';
            var signedUrlExpireSeconds = 60 * 30;

            var params = {
                Bucket: myBucket,
                Key: filename,
                Expires: signedUrlExpireSeconds,
                ACL: 'public-read'
            };            

            var url = s3.getSignedUrl('putObject', params, function(err, url) {
                return res.json({'url':url, 'fileKey': tempKey});
            });
        });

//**************MOUNT ROUTER********************//
    app.use('/api/v1', router); 
};