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

//***********ROUTES****************************//

// User Authentification check
    router.use(function(req, res, next) {
        //routes allowed 
        const permissibleRoutes = ['/user/signIn', 
                                    '/articles', 
                                    '/tags', 
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
        router.get('/articles', articleController.getArticles);
        //router.get('/articleDetails', articleController.getArticleDetails);         

    //POST
        router.post('/articles', articleController.createArticle); 

    //PUT

    //DELETE

//articleCommentRoutes
    //GET

    //POST
        //articleComment

//userRoutes
    //GET 

    //POST
        router.post('/user/signIn', userController.signIn);
    //PUT

    //DELETE

//UTILIES - will create utility file if need grows
//presigned s3 url
    //GET
        router.get('/preS3', function(req, res) {
            AWS.config.update({accessKeyId: AWSKeys.AccessKey, secretAccessKey: AWSKeys.SecretAccessKey});
            var s3 = new AWS.S3(); 

            var myBucket = 'adpq-assets';
            var myKey = AWSKeys.MySecretKey;
            var signedUrlExpireSeconds = 60 * 30;

            var params = {
                Bucket: myBucket,
                Key: myKey,
                Expires: signedUrlExpireSeconds
            }; 

            var url = s3.getSignedUrl('putObject', params, function(err, url) {
                return res.json({'url':url, 'fileKey': AWSKeys.FileKey});
            });
        });

//**************MOUNT ROUTER********************//
    app.use('/api/v1', router); 
};