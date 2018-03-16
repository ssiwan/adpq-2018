'use strict';
var sendmail = require('sendmail')({silent: true});

//INTERNAL API
exports.sendNotificationEmail = function() {
	var message  = {
		to:      'adpq-admin@hotbsoftware.com',
		from:    'noreply-adpq@hotbsoftware.com',
		subject: 'New Article',
		html:    '<!doctype html>'+
					'<div class="dddd">'+
					'  <html lang="en">'+
					'  <head>'+
					'  <meta charset="utf-8">'+
					'  <title>Untitled Document</title>'+
					'  <style type="text/css">'+
					'body {'+
					'    margin: 0px;'+
					'    padding: 0px;'+
					'}'+
					'.welcome-header {'+
					'    background-color: #046b99;'+
					'    margin: 0px;'+
					'    padding: 0px;'+
					'    float: left;'+
					'    height: 50px;'+
					'    width: 100%;'+
					'    border-bottom: 5px solid #e9911b;'+
					'    border-top-style: none;'+
					'    position: absolute;'+
					'    top: 0px;'+
					'}'+
					'.adpq-content {'+
					'    display: block;'+
					'    padding: 25px;'+
					'    height: 600px;'+
					'    width: 700px;'+
					'    margin-top: 75px;'+
					'    margin-right: auto;'+
					'    margin-bottom: 50px;'+
					'    margin-left: auto;'+
					'    position: relative;'+
					'}'+
					'	'+
					'.dddd {'+
					'      font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;'+
					'    font-size: 24px;'+
					'    font-style: normal;'+
					'    font-weight: normal;'+
					'    color: #000;'+
					'}'+
					'.userpass {'+
					'    font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;'+
					'    font-size: 24px;'+
					'    font-style: normal;'+
					'    line-height: 29px;'+
					'    text-align: left;'+
					'    vertical-align: middle;'+
					'    display: block;'+
					'    height: 300px;'+
					'    width: 400px;'+
					'    margin-top: 50px;'+
					'    margin-right: auto;'+
					'    margin-left: auto;'+
					'    position: relative;'+
					'}'+
					'  </style>'+
					'  </head>'+
					'    '+
					'  <body>'+
					'  <div class="fluid_wrap">'+
					'    <header class="welcome-header"></header>'+
					'    <div class="adpq-content">'+
					'      '+
					'      <p> A new article has been created on the Knowledge Articles Application.  Please login and review.</p>  '+
					''+
					'<p>Thank you.</p>'+
					'		'+
					'    </div>'+
					'  </div>'+
					'  </body>'+
					'  </html>'+
					'</div>'
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
		html:    '<!doctype html>'+
					'<div class="dddd">'+
					'  <html lang="en">'+
					'  <head>'+
					'  <meta charset="utf-8">'+
					'  <title>Untitled Document</title>'+
					'  <style type="text/css">'+
					'body {'+
					'    margin: 0px;'+
					'    padding: 0px;'+
					'}'+
					'.welcome-header {'+
					'    background-color: #046b99;'+
					'    margin: 0px;'+
					'    padding: 0px;'+
					'    float: left;'+
					'    height: 50px;'+
					'    width: 100%;'+
					'    border-bottom: 5px solid #e9911b;'+
					'    border-top-style: none;'+
					'    position: absolute;'+
					'    top: 0px;'+
					'}'+
					'.adpq-content {'+
					'    display: block;'+
					'    padding: 25px;'+
					'    height: 600px;'+
					'    width: 700px;'+
					'    margin-top: 75px;'+
					'    margin-right: auto;'+
					'    margin-bottom: 50px;'+
					'    margin-left: auto;'+
					'    position: relative;'+
					'}'+
					'	'+
					'.dddd {'+
					'      font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;'+
					'    font-size: 24px;'+
					'    font-style: normal;'+
					'    font-weight: normal;'+
					'    color: #000;'+
					'}'+
					'.userpass {'+
					'    font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;'+
					'    font-size: 24px;'+
					'    font-style: normal;'+
					'    line-height: 29px;'+
					'    text-align: left;'+
					'    vertical-align: middle;'+
					'    display: block;'+
					'    height: 300px;'+
					'    width: 400px;'+
					'    margin-top: 50px;'+
					'    margin-right: auto;'+
					'    margin-left: auto;'+
					'    position: relative;'+
					'}'+
					'  </style>'+
					'  </head>'+
					'    '+
					'  <body>'+
					'  <div class="fluid_wrap">'+
					'    <header class="welcome-header"></header>'+
					'    <div class="adpq-content">'+
					'      <h1>Welcome to ADPQ Knowledge Articles Application.</h1>'+
					'      <p> Feel free to create, view, and comment on any articles! Thank you.</p>'+
					'		'+
					'    </div>'+
					'  </div>'+
					'  </body>'+
					'  </html>'+
					'</div>'
	} 
	sendmail(
		message, 
		function(sendEmailErr, sendEmailReply){
			console.log("sendEmail: " + "Email sent to " + message.to);
		}
	);
    return;
}