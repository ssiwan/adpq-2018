'use strict'

// Constants
var http = require("https");

// Request Parameters
var options = {
  "method": "POST",
  "hostname": "hooks.slack.com",
  "port": null,
  "path": "/services/T0DD4DR5G/B9CHWRD9V/tSqTrOH8OXfGaw2xcjshJse7",
  "headers": {
    "content-type": "application/x-www-form-urlencoded",
    "cache-control": "no-cache"
  }
};

// Create Request
var req = http.request(options, function (res) {
  var chunks = [];

  res.on("data", function (chunk) {
    chunks.push(chunk);
  });

  res.on("end", function () {
    var body = Buffer.concat(chunks);
  });
});

// Define Arguments
var type = process.argv[2];
var message = process.argv[3];
var additionalArgs = process.argv[4];

// Create Payload
var payload;
if (type == "SUCCESS") {
		payload = {
				text: message,
				attachments: [
						{
								color: "#00ff00",
								fields: [
										{
												title: "Success",
												value: additionalArgs,
												short: false
										}
								]
						}
				]
		}
} else {
		payload = {
				text: message,
				attachments: [
						{
								color: "#D00000",
								fields: [
										{
												title: "Failure",
												value: additionalArgs,
												short: false
										}
								]
						}
				]
		}
}

req.write(JSON.stringify(payload));
req.end();