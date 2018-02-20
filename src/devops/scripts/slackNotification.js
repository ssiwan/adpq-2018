var http = require("https");

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

var req = http.request(options, function (res) {
  var chunks = [];

  res.on("data", function (chunk) {
    chunks.push(chunk);
  });

  res.on("end", function () {
    var body = Buffer.concat(chunks);
    console.log(body.toString());
  });
});

var type = process.argv[2];
var message = process.argv[3];
var testList = process.argv[4];

var payload;
if (type == "SUCCESS") {
	payload = {
	    text: message
	}
} else {
	payload = {
	    text: message,
	    attachments: [
		{
	   	    color: "#D00000",
	  	    fields: [
			{
		            title: "Failed Tests:",
		            value: testList,
		            short: false
			}
		    ]
		}
	    ]
	}
}

req.write(JSON.stringify(payload));
req.end();