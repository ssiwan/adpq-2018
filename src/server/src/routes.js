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
    var emailController = require('./controllers/emailController');   

//***********ROUTES****************************//

// User Authentification check
    router.use(function(req, res, next) {
        //routes allowed 
        const permissibleRoutes = ['/user', 
                                    '/articles', 
                                    '/tags', 
                                    '/agencies', 
                                    '/searchArticles',
                                    '/incrementViews',
                                    '/incrementShares',
                                    '/suggestedTags',
                                    '/sendTestEmail']; 

        var token = req.header('Authorization');

        if (token == undefined) {
            token = ""; 
        }
        var reqpaths = req.path.split('/');  
        var reqbase = '/' + reqpaths[1]; 

        if (token && token.length > 0) {
            jwt.verify(token, apiParseKey, function(err, decoded) {
                if (err) {
                    //console.log(err);
                    res.status(401);                     
                    return res.json({error: 'Failed to authenticate token'});
                }
                else {
                    req.userRole = decoded.role;
                    req.userId = decoded.userId;
                    next(); 
                }
            });
        }
        else if (permissibleRoutes.includes(reqbase)) {             
            req.userRole = 0; 
            if (permissibleRoutes.indexOf(reqbase) == 0) {//sign in
                req.PK = apiParseKey; 
            }
            next(); 
        }
        else {
            res.status(401);  
            return res.json({error: 'Please provide an authentication token'}); 
        }

    });

//tagRoutes
    //GET    
        router.get('/tags', tagsController.getTags);
        router.get('/suggestedTags', tagsController.getSuggestedTags); 

//agencyRoutes
    //GET
        router.get('/agencies', agencyController.getAgencies);

//articleRoutes
    //GET
        router.get('/searchArticles', articleController.search);
        router.get('/articles/:articleId', articleController.getArticleDetails);
        router.get('/articles', articleController.getArticles);  
        router.get('/staffArticles', articleController.getStaffArticles); 

    //POST
        router.post('/articles', articleController.createArticle);
    
    //PATCH
        router.patch('/incrementViews/:articleId', articleController.incrementViews); 
        router.patch('/incrementShares/:articleId', articleController.incrementShares);
        router.patch('/deleteAttachment/', articleController.deleteAttachment);  

    //DELETE
        router.delete('/articles/:articleId', articleController.deleteArticle); 

//articleEditRoutes
    //POST
        router.post('/editArticle', articleEditController.editArticle);
        router.post('/publishArticle', articleEditController.publishArticle); 
        router.post('/declineArticle', articleEditController.declineArticle); 

//articleCommentRoutes
    //POST
        router.post('/articleComment', articleCommentController.createArticleComment);

//userRoutes
    //GET
        router.get('/user', userController.getUsers);
        router.get('/user/:userId', userController.getUserDetails);  

    //POST
        router.post('/user/signIn', userController.signIn);
        router.post('/user', userController.createUser);

    //PATCH
        router.patch('/user', userController.editUser); 
        router.patch('/user/editProfile', userController.editProfile); 

    //DELETE
        router.delete('/user/:userId', userController.deleteUser); 

//Dashboard
    //GET 
        router.get('/dashboardAnalytics', articleController.dashboardAnalytics);
        router.get('/dashboardTrending', articleController.dashboardTrending);  
        router.get('/dashboardMyPublished', articleController.dashboardPublishedArticles);
        router.get('/dashboardWorkflow', articleController.dashboardWorkflow);
        router.get('/adminDashboardDeclined', articleController.admindbdeclined);
        router.get('/adminDashboardPending', articleController.admindbpending);
        router.get('/adminDashboardApproved', articleController.admindbapproved);      

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