# HOTB Software - ADPQ Knowledge Base

## Links
**ADPQ Knowledge Articles Website:**<br>
https://adpq.hotbsoftware.com<br>

## User Accounts

**Staff Account**<br>
**Username:** adpq-staff@hotbsoftware.com<br>
**Password:** Hotb&2018

**Admin Account**<br>
**Username:** adpq-admin@hotbsoftware.com<br>
**Password:** Hotb&2018

# TECHNICAL APPROACH
HOTB Software Solutions developed the ADPQ Knowledge Management System Prototype in response to the California Department of Technology ADPQ Vendor Pool RFI Submission due on March 16, 2018.<br><br>
Our technical approach was based on HOTB’s agile development process that utilizes Scrum Methodology focused on short, iterative sprints to deliver functional components that are evolved based on user feedback. We started with the concept of delivering a functional prototype that would provide authorized users with the ability to create Knowledge Articles. This primary use case was expanded to include administrative features like User Creation and Article Approval workflow. In subsequent iterations we introduced the ability to share articles (while being mindful of role-based access) and began to capture those metrics to identify trending articles, tags and topics that were used to prompt the user to create new or similar articles.<br><br>
Our design process incorporated several user-centric design methodologies that provided feedback which was incorporated into our subsequent design iterations. Our goal was to build a prototype with a clear and intuitive design that was driven by user feedback and delivered in an agile software development environment.<br><br>
We chose a modern technology stack that utilized open source technologies and implemented those using a continuous integration and continuous deployment methodology based on Docker containers and Jenkins. Automated tests scripts were written in Python and executed against the prototype during the development process.<br><br>
The project team met daily to review project status, action items and deliverables. Progress was tracked using Aha!, our internal project management and ticketing system, and we relied upon Slack as our collaboration tool. All code updates were committed to Github along with our agile process documentation, design iterations and test scripts.<br><br>
Further information about our process can be found in the [California RFI Process Documentation attached](http://google.com) and in our responses below.

# ARCHITECTURAL FLOW
[insert description]

# US DIGITAL SERVICES PLAYBOOK
We followed the US Digital Services Playbook. Our responses to each can be found [here](src/administration/U.S.%20Digital%20Services%20Playbook/US%20Digital%20Services%20Playbook.pdf).

# OTHER REQUESTED ITEMS

## a) Assigned one (1) leader and gave that person authority and responsibility and held that person accountable for the quality of the prototype submitted
We assigned the role of Project Lead to Jason Connolly. Jason acted as the Business Owner and established project priorities and acted as the primary leader taking accountability for all phases of the project.

## b) Assembled a multidisciplinary and collaborative team that includes, at a minimum, five (5) of the labor categories as identified in Attachment B: PQVP DS-AD Labor Category Descriptions
- **Project Lead** – Jason Connolly<br>
- **Product Manager** – Mark Witte<br>
- **Technical Architect** – Mike Firoved<br>
- **Interaction Designer/User Researcher/Usability Tester** – Tracie DePietro<br>
- **Visual Designer** – Ken Baker<br>
- **Front End Web Developer** – Raghu Jonnala<br>
- **Backend Web Developer** – Noel Eom<br>
- **Quality Assurance Engineer** - Luis Escobar<br>
- **DevOps Engineer** – Eric Dobyns<br>

## c) Understood what people needed, by including people in the prototype development and design process
During our initial discovery process we utilized surveys and questionnaires conducted with prospective users which helped shape our understanding of user requirements and key features. We also conducted interviews with KMT providers and super users. Their experience and insights were extremely valuable in shaping the features and functions of the prototype.<br><br>
We constructed an initial user survey to get feedback on general user experience with Knowledge Management Tools. Results of the survey are included [here](http://www.google.com).<br><br>
We also had users provide feedback following a user session with a clickable prototype. A sample of those responses can be found [here](http://www.google.com).<br><br>
Interview Notes can be found [here](http://www.google.com).

## d) Used at least a minimum of three (3) “user-centric design” techniques and/or tools
We used at least three (3) user centric design techniques that included: Key Experience Pillar Documents, Online Survey, User Interviews following a clickable prototype review and phone interviews with subject matter experts.<br><br>
In addition to the surveys and interviews above, we created Key Experience Pillar documents to define user stories and use cases. Those can be found [here](http://www.google.com).

## e) Used GitHub to document code commits
A GitHub repository was setup to capture code commits for each developer. We also included agile process documentation, design changes and automated testing scripts. We utilized version control by separating branches for each developer as well as managed code merges through individual pull requests.

## f) Used Swagger to document the RESTful API, and provided a link to the Swagger API
OpenAPI v3.0.0 (Swagger) was used to document our RESTful APIs and other technical documentation.

**API Docs**<br>
http://adpq-docs.hotbsoftware.com

**API Documentation hosted on SwaggerHub**<br>
https://app.swaggerhub.com/apis/HOTB-Software/adpq_knowledge_base

**OpenAPI v3.0.0 Code**<br>
[JSON](src/documentation/swagger/api-docs.json) | [YAML](src/documentation/swagger/api-docs.yaml)

## g) Complied with Section 508 of the Americans with Disabilities Act and WCAG 2.0
We created our and implemented our designs and user experience in accordance with standards outlined in Section 508 of the ADA and WCAG 2.0.

## h) Created or used a design style guide and/or a pattern library
Following the initial wireframe creation, we created a [style guide and color palette](http://www.google.com) that was used throughout the application for consistency and uniformity.

## i) Performed usability tests with people
We conducted usability tests with prospective users who provided relevant feedback that sharpened our focus and improved our design and system features.

## j) Used an iterative approach, where feedback informed subsequent work or versions of the prototype
Our initial designs were based on [Key Experience Pillars documents](http://www.google.com). These documents were created and based on feedback we received from our initial consumer survey. We made adjustments to the design and system features following feedback from user testing and interviews.

## k) Created a prototype that works on multiple devices, and presents a responsive design
The prototype works across multiple devices (phones, tablets and PCs) and is supported by multiple browsers and is responsive to the specific device.

## l) Used at least five (5) modern and open-source technologies, regardless of architectural layer (frontend, backend, etc.)
We used at least five (5) modern and open-source technologies including:

### Front-End
- HTML/CSS
- Bootstrap
- Javascript
- jQuery

### API/Back-End
- Node.js/Express.js
- MongoDB

### Dev-Ops
- Jenkins
- Docker

### QA
- Python
- Unittest

## m) Deployed the prototype on an Infrastructure as a Service (IaaS) or Platform as Service (PaaS) provider, and indicated which provider they used
Our website and API are built with Node.js and are deployed as a containerized solution on AWS ECS. ECS instances are monitored using AWS Cloudwatch and automatically scale up or down based on defined Cloudwatch alarms. All incoming traffic is passed through an elastic load balancer (AWS ELB) which automatically distributes traffice across multiple ECS instances.<br>

Our production databases are typically comprised of a MongoDB cluster with a minimum of three replica sets to ensure high availability in case one of the servers goes down. When necessary we are able to configure additional database sharding to increase the write throughput of the existing database.

## n) Developed automated unit tests for their code
We developed automated unit tests written in Python which are automated through Jenkins following the automated build and deployment process. Automated unit tests run nightly and developers may manually run tests at any time.

## o) Setup or used a continuous integration system to automate the running of tests and continuously deployed their code to their IaaS or PaaS provider
We have in place automated deployment scripts that handle actions based off of git commits to specific remote branches. Our build server utilizes the CI/CD software "Jenkins" to accept incoming SQS messages from Github and kick off automated scripts to test, build and deploy the project to AWS. Additional Jenkins jobs consist of nightly automated tests and nightly backups of our production database. Automated tests built with Python are run each night as well manually by back-end developers and quality assurance engineers. Our automated tests our monitored daily and manually adjusted whenever necessary.

## p) Setup or used configuration management
Jenkins and Docker were used to automatically configure environment variables for each environment. Please refer to the [server documentation](src/server/README.md) for configuration instructions.

## q) Setup or used continuous monitoring
AWS Cloudwatch was setup to monitor the ECS servers, application availability and general system performance.

## r) Deployed their software in an open source container, such as Docker (i.e., utilized operating-system-level virtualization)
Both our web and back-end solutions are containerized via Docker. Docker images are uploaded to AWS ECR and then deployed on AWS ECS clusters for scalability.

## s) Provided sufficient documentation to install and run their prototype on another machine
Please refer to the [server documentation](src/server/README.md) for additional installation instructions.

## t) Prototype and underlying platforms used to create and run the prototype are openly licensed and free of charge.
All components used to deliver and run the prototype are openly licensed and free of charge.


# License 
[The MIT License](https://opensource.org/licenses/MIT)

Copyright (c) 2018 Homeowners Toolbox Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

<br>Have a great day!<br>(っˆڡˆς)