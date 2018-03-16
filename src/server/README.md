# Server
This folder contains the back-end and front-end code used for the project.

# Getting Started

## Requirements
![](https://img.shields.io/badge/node-v9.2.0-blue.svg)
![](https://img.shields.io/badge/npm-v5.5.1-blue.svg)
![](https://img.shields.io/badge/docker-v17.12.0-blue.svg)
![](https://img.shields.io/badge/dockercompose-v1.18.0-blue.svg)

- Supports any Operating System
- Install Node.js v9.5.0  
- Install NPM v5.5.1
- Install [docker](https://docs.docker.com/get-started/) v17.12.0
- Install [docker-compose](https://docs.docker.com/compose/gettingstarted/) v1.18.0

## Project Configuration
To keep our sensitive information secure we have bundled any important variables in a config.json file which resides in the following directory:
```
<project-root>/src/server/src/config.json
```
Please add the config.json we have supplied to the above directory before executing any scripts.

## Quick Start
Add the supplied config.json to the following path:
```
<project-root>/src/server/src/config.json
```
Run the following command:
```
npm install && 
npm start
```
The `npm start:local` command will build and deploy local containers of the website, api and database. Once running your default browser will automatically open to the ADPQ Knowledge Base website.

## Run Tests
To run unit tests simply execute the following command from this directory:
```
npm test
```

## Running Locally

Running locally will create local instances of the API, website and a MongoDB instance. It is easiest to run against staging but if you wish to run a truely local environment please do the following:

The `npm run start:local` command will build and deploy local containers of the website, api and database. Once running your default browser will automatically open to the ADPQ Knowledge Base website. Additional database setup WILL be required. Please use the `mongorestore` command to upload some initial "seed" data into the database. Data can be found here:
```
cd <project-root>/src/devops/utilities/database/backup
```
Please ask one of our developers for any assistance in configuring a local database.

Once ready execute the following command:
```
cd <project-root>/src/server

npm run start:local
```

The following docker containers will be running detached:<br>

- **Website & API:** http://localhost:3001<br>
- **MongoDB:** http://localhost:27017

## Deploy to Staging

When ready to deploy your code to staging please create a pull request via GitHub to merge your current branch into the staging branch. A reviewer will analyze your updates ASAP and approve or deny the request. Merges into staging will automatically trigger the build and deployment process to the staging servers.

## Deploy to Production

When ready to deploy a new build to production please confirm with the team that the current staging branch is up to date with the latest code and has no critical issues present. Tag the commit with the relevant version number and create a pull request to have a reviewer analyze the updates and approve or deny the request. Once merged into master our team lead will use the following commands to deploy to staging:
```
cd <project-root>/src/devops/scripts
sh deployProduction.sh <version-number>
```
NOTE - In order to deploy to production make sure you have the correct AWS credentials saved to the default configuration path specified by AWS. (Please speak with a team lead about production deployment) 

### Additional Installation
For additional scripts, instructions and configuration of your development environment please refer to the following documentation:<br>
- [Package.json](package.json)<br>
- [API Docs](http://adpq-docs.hotbsoftware.com)<br>