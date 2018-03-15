# Server
[insert description]

# Getting Started
Don't Panic.
## Requirements
![](https://img.shields.io/badge/node-v9.2.0-blue.svg)
![](https://img.shields.io/badge/npm-v5.5.1-blue.svg)
![](https://img.shields.io/badge/docker-v17.12.0-blue.svg)
![](https://img.shields.io/badge/dockercompose-v1.18.0-blue.svg)

- Supports any Operating System
- Install Node.js v9.5.0  
- Install NPM v5.5.1
- Install [docker](http://insertlink) v17.12.0
- Install [docker-compose](http://insertlink) v1.18.0

## Quick Start
Add the supplied config.json to the following path:
```
/src/server/src/config.json
```
Run the following command:
```
npm install && 
SET Environment=local &&
npm start
```

The `npm start` command will build and deploy local containers of the website, api and database. Once running your default browser will automatically open to the ADPQ Knowledge Base website.

The following docker containers will be running detached:<br>

- **Website:** http://localhost:80<br>
- **API:** http://localhost:3001<br>
- **MongoDB:** http://localhost:3002


### Additional Installation
For additional scripts, instructions and configuration of your development environment please refer to the following documentation:<br>
- [Package.json](https://www.kualo.co.uk/404)<br>
- [API Docs](http://adpq-docs.hotbsoftware.com)<br>
- [Server Readme](https://www.kualo.co.uk/404)<br>
- [Additional Guides](https://www.kualo.co.uk/404)