
var config = require('./config');
var express = require('express'),
    app = express(),
    mongoose = require('mongoose'),
    bodyParser = require('body-parser'),
    //tag = require('./models/tag');
    port = process.env.port || 3001;

//connect to db
mongoose.Promise = global.Promise;

    // const options = {
    //     user: config.dbUser,
    //     pass: config.dbPassword,
    //     auth: {
    //         authdb: 'admin'
    //     }
    // }

//mongoose.connect(config.dbUrl, options);
mongoose.connect(config.dbUrl);
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

//models
require('./models/tag');
require('./models/agency');
require('./models/article');

//body parser
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json()); 

//routes
var routes = require('./routes'); //import routes
routes(app);

app.get('/', (req, res) => res.send('Hello Server Test!'))

app.listen(port);
console.log('Server listening on port 3001'); 