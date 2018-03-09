'use strict';
var sendmail = require('sendmail')({silent: true});


//INTERNAL API
exports.sendNotificationEmail = function() {
	var message  = {
		to:      'adpq-admin@hotbsoftware.com',
		from:    'noreply-adpq@hotbsoftware.com',
		subject: 'New Article',
		html:    '<b>A NEW ARTICLE HAS BEEN CREATED!</b>'
	} 
	sendmail(
		message, 
		function(sendEmailErr, sendEmailReply){
			console.log("sendEmail: " + "Email sent to " + message.to);
		}
	);
    return;
}

exports.sendWelcomeEmail = function(email) {
	var message  = {
		to:      email,
		from:    'noreply-adpq@hotbsoftware.com',
		subject: 'Welcome to ADPQ!',
		html:    '<b>WELCOME TO ADPQ</b>'
	} 
	sendmail(
		message, 
		function(sendEmailErr, sendEmailReply){
			console.log("sendEmail: " + "Email sent to " + message.to);
		}
	);
    return;
}