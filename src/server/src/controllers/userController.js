'use strict';

var mongoose = require('mongoose'),
    bcrypt = require('bcrypt'),
    jwt = require('jsonwebtoken'), 
    users = mongoose.model('user');

var ObjectId = mongoose.Types.ObjectId; 
const saltRounds = 2; 

//temp function 
exports.signIn = function(req, res) {
    var userEmail = req.body.email;
    var textpassword = req.body.password;  
    var queryParams = {};
    queryParams.email = userEmail;
    var query = users.findOne(queryParams).populate('agency');

    query.exec()
        .catch(function (err) {
            res.send(err);
        });  
    
    query.then(function(user) {
        if (!user) {
            return res.json({error: 'User not found'});          
        }
        else {
            bcrypt.compare(textpassword, user.hashedPassword, function(err, match) {
                if (match) {
                    var roleString = "admin";
                    if (user.role == 1) {
                        roleString = "staff"; 
                    }
                    var jsonresult = {
                        token: jwt.sign({exp: Math.floor(Date.now() / 1000) + ( 7 * 24 * 60 * 60), userId: user._id.toString(), role: user.role}, req.PK),
                        id: user._id.toString(),
                        role: roleString, 
                        agencyName: user.agency.value,
                        agencyId: user.agency._id.toString()
                    }
                    res.json(jsonresult);
                    //set token expiring at a week 
                }
                else {
                    res.json({error: 'Invalid password'});
                }
            });
            
        }
    });  
}

exports.createUser = function(req, res) {
    if (parseInt(req.userRole) != 2) {
        return res.json({error: 'User not allowed'}); 
    }

    var firstName = req.body.firstName; 
    var lastName = req.body.lastName; 
    var newEmail = req.body.email; 
    var newPhone = req.body.phone; 
    var newAgencyId = req.body.agencyId; 
    var newAllowUploads = req.body.allowUploads; 
    var plainpassword = req.body.password; 

    bcrypt.hash(plainpassword, saltRounds, function(err, newHashedPassword) {
        if (err) {
            return res.json({error: err.toString()}); 
        }

        var newUser = new users({
            name: {
                first: firstName, 
                last: lastName
            },
            createdAt: Date.now(),
            updatedAt: Date.now(),
            email: newEmail,
            agency: new ObjectId(newAgencyId),
            hashedPassword: newHashedPassword, 
            phone: newPhone,
            allowUploads: newAllowUploads, 
            role: 1
        });

        var prom = newUser.save(); 
        prom.then(function(userreturn){
            var jsonreturn = {
                status: 'saved!',
                userId: userreturn._id.toString(),
                pswd: newHashedPassword  
            }; 
            return res.json(jsonreturn);
        }).catch(function(err) {
            return res.json({'error': err.toString() });
        });

    });

}

exports.getUsers = function(req, res) {
    if (parseInt(req.userRole) != 2) {
        return res.json({error: 'User not allowed'}); 
    }

    var queryParams = {};
    queryParams.role = 1; 

    var query = users.find(queryParams); 
    var sortObj = {};
    sortObj['email'] = -1; 

    query.exec().catch(function(err){
        return res.json({error:err.toString()});
    });

    query.then(function(returnusers) {
        var returnlist = []; 
        if (returnusers != null) {
            returnusers.forEach(function(returnuser) {
                var returnobj = {}; 
                returnobj.userId = returnuser._id.toString(); 
                returnobj.name = returnuser.name.first + " " + returnuser.name.last; 
                returnobj.email = returnuser.email; 
                returnobj.phone = returnuser.phone; 
                returnlist.push(returnobj); 
            });
        }
        res.json({data:returnlist}); 
    });
}

exports.deleteUser = function(req, res) {
    if (parseInt(req.userRole) != 2) {
        return res.json({error: 'User not allowed'}); 
    }

    if (req.params.userId == null) {
        return res.json({error: 'Please submit a user to delete'}); 
    }

    var userobjid = new ObjectId(req.params.userId); 

    var queryParams = {}; 
    queryParams._id = userobjid; 

    var query = users.find(queryParams).remove().exec(); 

    query.catch(function(err) {
        return res.json({error: err.toString()});
    });

    query.then(function(returnuser) {
        return res.json({data:'user removed!'}); 
    });
}

exports.getUserDetails = function(req, res) {
    var userobjid = new ObjectId(req.params.userId); 
    var queryParams = {}; 
    queryParams._id = userobjid; 

    var query = users.findOne(queryParams).populate('agency'); 

    query.exec().catch(function(err) {
        return res.json({error: err.toString()}); 
    }); 

    query.then(function(returnuser) {
        var returnobj = {}; 
        if (returnuser != null) {
            returnobj.userId = returnuser._id.toString(); 
            returnobj.name = returnuser.name.first + " " + returnuser.name.last; 
            returnobj.email = returnuser.email; 
            returnobj.phone = returnuser.phone;
            returnobj.agencyName = returnuser.agency.value; 
            returnobj.agencyId = returnuser.agency._id.toString(); 
            returnobj.allowUploads = returnuser.allowUploads;  
        }
        return res.json({data:returnobj}); 
    }); 
}

// exports.editUser = function(req, res) {
//     if ((req.body.userId == req.userId) || parseInt(req.userRole) == 2) {

//         var textpassword 

//         bcrypt.hash(plainpassword, saltRounds, function(err, newHashedPassword) {

//         });
//     }
//     else {
//         res.json({error:'Not allowed to edit this user'}); 
//     }
// }

