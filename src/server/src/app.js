var config = require('./config'),
    express = require('express'),
    app = express(),
    mongoose = require('mongoose'),
    bodyParser = require('body-parser'),
    dns = require('dns'),
    winston = require('winston'),
    expressWinston = require('express-winston'),
    expressBrute = require('express-brute'),
    MongooseStore = require('express-brute-mongoose'),
    healthCheck = require('express-healthcheck'), 
    BruteForceModel = require('./models/bruteforce'),
    port = process.env.port || 3001;

require('winston-mongodb'); 

var cors = require('cors');

//email
dns.setServers(['8.8.8.8', '8.8.4.4']);

process.on('unhandledRejection', (reason, p) => {
    console.log('Unhandled Rejection at: Promise', p, 'reason:', reason)
})

// Configure Request Logging
app.use(expressWinston.logger({
    transports: [
        new winston.transports.MongoDB({
            db: config.logsDatabaseURL,
            collection: 'Requests',
            expireAfterSeconds: 30 * 24 * 60 * 60, // One Month
            username: config.dbUser,
            password: config.dbPassword
        })
    ],
    meta: true, // optional: control whether you want to log the meta data about the request (default to true)
    msg: '{{ req.headers[\'x-forwarded-for\'] || req.connection.remoteAddress }}', 
    address: '{{ req.headers[\'x-forwarded-for\'] || req.connection.remoteAddress }}',
    colorize: true,
    ignoreRoute: function (req) { 
        if (req.url == '/favicon.ico') { // skip logs for favicon.ico
            return true
        } else {
            return false
        }
    }
}));

//connect to db
mongoose.Promise = global.Promise;

const options = {
    user: config.dbUser,
    pass: config.dbPassword,
    auth: {
        authdb: 'admin'
    }
};

mongoose.connect(config.dbUrl, process.env.NODE_ENV == 'local' ? null : options).then(() => {
    var db = mongoose.connection;
    db.on('error', console.error.bind(console, 'MongoDB connection error:'));
    
    //models
    require('./models/tag');
    require('./models/user');
    require('./models/agency');
    require('./models/articleComment');
    require('./models/articleEdit');
    require('./models/article');

    //cors 
    app.use(cors()); 

    //body parser
    app.use(bodyParser.urlencoded({ extended: true }));
    app.use(bodyParser.json()); 

    // Setup brute force MongoDB store
    var store = new MongooseStore(BruteForceModel); 
    // Setup brute force configuration for all endpoints
    var bruteforceAll = new expressBrute(store, {
        freeRetries: 1000, // Per Hour
        refreshTimeoutOnRequest: false,
        minWait: 15 * 1000,
        maxWait: 61*60*1000,
        lifetime: 60*60,
        failCallback: (req,resp,next,nextValidRequestDate) => {
            resp.status(429)
            resp.json({
                error: 'Too many requests',
                nextValidRequest: nextValidRequestDate
            })
        }
    });
    // Apply brute force configuration for all endpoints
    app.all('/*', bruteforceAll.prevent, (req, res, next) => {
        next()
    });
    
    //routes
    var routes = require('./routes'); //import routes
    routes(app, config.apiParseKey, config.AWSKeys);

    app.use(express.static(require('path').join(__dirname, 'public')));

    app.get('/healthcheck', healthCheck({
        healthy: function() {
            return {status: "Ok", version: config.version}; 
        }
    }));

    app.get('/', (req, res) => {
        res.sendFile('/index.html', {root : __dirname + 'public'})
    });

    app.use(expressWinston.errorLogger({
        transports: [
            new winston.transports.MongoDB({
                db: config.logsDatabaseURL,
                collection: 'Errors',
                expireAfterSeconds: 30 * 24 * 60 * 60, // One Month
                username: config.dbUser,
                password: config.dbPassword
            })
        ],
        meta: true, // optional: control whether you want to log the meta data about the request (default to true)
        msg: '{{ req.headers[\'x-forwarded-for\'] || req.connection.remoteAddress }}', // optional: customize the default logging message. E.g. "{{res.statusCode}} {{req.method}} {{res.responseTime}}ms {{req.url}}"
        colorize: true
    }));

    // Handle Invalid Routes
    app.use((req, res) => {
        res.status(404)
        res.send({
            error: 'Invalid url'
        })
    });

    app.listen(port, () => {
        console.log('Server listening on port 3001')
    });
    
}, error => {
    console.log(error);
});