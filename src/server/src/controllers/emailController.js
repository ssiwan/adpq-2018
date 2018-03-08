'use strict';
var sendmail = require('sendmail')({silent: true});


//INTERNAL API
exports.sendNotificationEmail = function() {
	var message  = {
		to:      'adpq-admin@hotbsoftware.com',
		from:    'noreply@adpq.com',
		subject: 'Subject',
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