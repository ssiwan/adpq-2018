# Quality Assurance

This folder contains the python code used to run automated unit tests against local, staging and production environments. 

# Getting Started

## Requirements
![](https://img.shields.io/badge/python-v3.3+-blue.svg)
![](https://img.shields.io/badge/requests-v2.18.4-blue.svg)
![](https://img.shields.io/badge/unittest-v2.1.1-blue.svg)
![](https://img.shields.io/badge/docker-v17.12.0-blue.svg)


# Installation Instructions

Tests may be executed via python or docker. 

## Docker Installation Instructions

- Install Docker v.17.12.0<br>
- Build a Docker image using the following command:<br>
```
docker build ./src/qa –t adpq+tests
```
- Execute tests using the following command: <br>
docker run –e Environment=staging
- Handle Docker cleanup by removing the stopped container and its image:
```
docker rm adpq_tests && docker rmi adpq_tests
```

OR

- Navigate to the Server directory:
```
cd <projectroot>/src/server
```
- Run npm test:
```
npm test
```

## Python Installation Instructions

- Install Python v3.3 or greater<br>
- Use pip to install requests<br>
- Use pip to install unittest-xml-reporting<br>
- Navigate to the following directory:<br>
```
cd <projectroot>/src/qa
```
- Run the following command using python (Please make sure your py PATH is set correctly):<br>
```
py runner.py
```


