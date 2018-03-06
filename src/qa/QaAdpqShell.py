import requests, os


# Set API Development Environment.
setEnv = ''
if 'Environment' not in os.environ.keys():
    print('\n[AutoScript] Defaulting to staging.\n')
    setEnv = 'http://adpq-staging-loadbalancer-777882718.us-west-1.elb.amazonaws.com'
else:
    print('\n[AutoScript] Setting environment to', os.environ['Environment'], '\n')
    if os.environ['Environment'] == 'local':
        setEnv = 'http://localhost:3001'
    elif os.environ['Environment'] == 'staging':
        setEnv = 'http://adpq-staging-loadbalancer-777882718.us-west-1.elb.amazonaws.com'
    elif os.environ['Environment'] == 'prod':
        setEnv = 'http://adpq-production-loadbalancer-557804625.us-west-1.elb.amazonaws.com'
setEnv.strip()


# Set test output flag.
# True  - Test print statements will output to console.
# False - No console output.
if 'TestOutput' not in os.environ.keys():
    TestOutput = False
else:
    TestOutput = os.environ['TestOutput']
    

'''
    ADPQ Test Automation Shell 
    
    Shell provides a platform to run unittest scripts against. 
    
    Each class method corresponds to an end point. 
    
    Each method contains header/body dictionaries. Dict pairs can be
    entirely excluded or assigned any values, including null.
    
    example(email='', emailExclude=False)
    
    If emailExclude flag is set to True during the method call, the value 
    will not be included in the request.
'''
class QaADPQShell:
    
    ## @var Test variables used by unittest scripts.
    testEmail = 'jlennon@hotbsoftware.com'
    testPassword = 'p@assw0rd1!'
    testFirstName = 'Ragnar'
    testLastName = 'Lothbrok'
    testGender = 'Viking Male'
    testStatus = 'Still alive'
    testAge = '55'
    testOrientation = 'Viking'
    testEducation = 'UCI'
    testFcmId = "abc123321bca"
    ClientId = 'ffcc8.4b0-and-??v27-93ae-92.361f002671'
    testArticleId = '5a98378b47c4e20019ac0f86'
    
    ## @var End point completions.
    GetAgencies = 'agencies'
    GetTags = 'tags'
    Articles = 'articles?'
    SearchArticles = 'searchArticles'
    UsersSignIn = 'user/signIn'
    DashAnalytics = 'dashboardAnalytics'
    DashTrending = 'dashboardTrending'
    DashPubArticles = 'dashboardMyPublished?'
    DashWorkflow = 'dashboardWorkflow'
    EditArticles = 'editArticle'
    ArticleComment = 'articleComment'
    PreS3 = 'preS3'
    
    ## @var Save a BaseURL without API Version.
    BaseURL = setEnv
    
    ## @var Set API Version.
    setEnv = setEnv + '/api/v1/'
    
    ## @var Variables that can be appended at the end of URL end point calls.
    articleSort = 'sort=createdAt&'
    articleLimit = 'limit=1&'
    articleDateStart = 'dateStart=02-01-2018&'
    articleDateEnd = 'dateEnd=03-01-2018&'
    articleAgencyId = 'agencyId=5a8b73f94212d1f20f847b9a&'
    agencyTagId = 'tagId=5a8b55bca2d13ad4ba5369ef&'
    
        
        
    ## @fn __init__ : Class initializations.
    def __init__(self, env=setEnv):
        self.ClientID = QaADPQShell.ClientId
        self.AuthKey = ''
        self.UserID = ''
        self.email = ''
        self.environment = env
        self.role = ''
        self.agencyId = []
        self.articleId = []
        
        

    ## @fn get_agency_list : Will return a list of all agencies.
    # :required - api_key
    #
    def get_agencies(self):

        url = self.environment + QaADPQShell.GetAgencies
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
        
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nget_agencies\n', responseBody)
            print('response.status_code: ', response.status_code)

        return responseBody
    
    
    

    ## @fn get_tagst : Will return a list of all tags.
    #
    def get_tags(self):

        url = self.environment + QaADPQShell.GetTags
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Make HTTPS Request.
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nget_tags\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    


    
    ## @fn get_article : Will get a list of articles given the users permissions. 
    # :required - Authorization
    #
    def get_articles(self, Authorization='', AuthorizationExclude=False, sortUrl=False,
                     limitUrl=False, dateStartURL=False, dateEndUrl=False,
                     agencyIdUrl=False, tagIdUrl=False):
        # URL end point.
        url = self.environment + QaADPQShell.Articles

        # End point options which can be appended to the end of the url.
        # ?example=100&
        if sortUrl == True:
            url = url + QaADPQShell.articleSort
        if limitUrl == True:
            url = url + QaADPQShell.articleLimit
        if dateStartURL == True:
            url = url + QaADPQShell.articleDateStart
        if dateEndUrl == True:
            url = url + QaADPQShell.articleDateEnd
        if agencyIdUrl == True:
            url = url + QaADPQShell.articleAgencyId
        if tagIdUrl == True:
            url = url + QaADPQShell.agencyTagId
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:# Dont include in call.
            pass                                     
        elif Authorization != '':       # Assign value.
            headers['Authorization'] = Authorization 
        else:                           # Assign nullptr.
            headers['Authorization'] = ''            
            
        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nget_article_list\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn search_articles : Get all articles within the db.
    #
    def search_articles(self):

        url = self.environment + QaADPQShell.SearchArticles
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nsearch_articles\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn sign_in : Allows an existing user to log into their account. 
    # :required - email
    #
    def sign_in(self, email='', emailExclude=False):

        url = self.environment + QaADPQShell.UsersSignIn
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        body = {}
        
        # Network body parameter.
        if emailExclude == True:
            pass
        elif email != '':
            body['email'] = email
        else:
            body['email'] = ''
            
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nsign_in\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        # Only if request was successful, save critical user data.
        if 'token' in responseBody.keys():
            if response.status_code == 200 and responseBody['token'] != None:
                self.AuthKey = responseBody['token']
                self.role = responseBody['role']
                self.UserID = responseBody['id']
        
        return responseBody
    
    
    
    ## @fn get_articles_details : Gets details of all articles. If an articleId 
    #                             is appended to url, then only details returned
    #                             are for specified article.
    #                             
    def get_articles_details(self, Authorization='', AuthorizationExclude=False,
                             articleId=[]):

        # If articleId isnt an empty string or list.
        if articleId != '' and articleId != []:
            # If articleId is a list.
            if type(articleId) == list:
                # Grab the first articleId and append to the url.
                url = self.environment + 'articles/' + articleId[0]
            # If articleId is a string.
            else:
                # Append to the url.
                url = self.environment + 'articles/' + articleId
        # Append nothing to the url, no specified articleId.
        else:
            url = self.environment + 'articles/'
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
            
        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nget_articles_details\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn create_article : Creates an article.
    #
    def create_article(self, Authorization='', title='', agencyId='', audience=0,
                       shortDesc='', longDesc='', tags='', attachments=[],
                       AuthorizationExclude=False, titleExclude=False,
                       agencyIdExclude=False, audienceExclude=False,
                       shortDescExclude=False, longDescExclude=False, 
                       tagsExclude=False, attachmentsExclude=False):

        url = self.environment + QaADPQShell.Articles
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        body = {}
        
        # title body parameter.
        if titleExclude == True:
            pass
        elif title != '':
            body['title'] = title
        else:
            body['title'] = ''
            
        # agencyId body parameter.
        if agencyIdExclude == True:
            pass
        elif agencyId != '':
            body['agencyId'] = agencyId
        else:
            body['agencyId'] = ''
            
        # audience body parameter.
        if audienceExclude == True:
            pass
        elif audience != '':
            body['audience'] = audience
        else:
            body['audience'] = ''
            
        # shortDesc body parameter.
        if shortDescExclude == True:
            pass
        elif shortDesc != '':
            body['shortDesc'] = shortDesc
        else:
            body['shortDesc'] = ''
            
        # longDesc body parameter.
        if longDescExclude == True:
            pass
        elif longDesc != '':
            body['longDesc'] = longDesc
        else:
            body['longDesc'] = ''
            
        # tags body parameter.
        if tagsExclude == True:
            pass
        elif tags != '':
            body['tags'] = tags
        else:
            body['tags'] = ''
            
        # attachments body parameter.
        if attachmentsExclude == True:
            pass
        # Attachments can be a string or list, assignment works different, check.
        elif attachments != '' and attachments != []:
            if type(attachments) == list:
                body['attachments'] = attachments[0]
            else:
                body['attachments'] = attachments
        else:
            body['attachments'] = ''
            
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if 'status' in responseBody.keys():
            if responseBody['status'] == 'saved!':
                self.articleId.append(responseBody['articleId']) 
        
        if TestOutput == True:
            print('\ncreate_article\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn edit_article : Will edit specified article.
    #
    def edit_article(self, Authorization='', articleId=[], title='', agencyId='', 
                     audience=0, shortDesc='', longDesc='', tags='', 
                     attachments=[], status=0, AuthorizationExclude=False, 
                     articleIdExclude=False, titleExclude=False, 
                     agencyIdExclude=False, audienceExclude=False,
                     shortDescExclude=False, longDescExclude=False, 
                     tagsExclude=False, attachmentsExclude=False, statusExclude=False,
                     return_status=False):
        
        url = self.environment + QaADPQShell.EditArticles
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        body = {}
        
        # articleId body parameter.
        if articleIdExclude == True:
            pass
        elif articleId != '' and articleId != []:
            if type(articleId) == list: 
                body['articleId'] = articleId[0]
            else:
                body['articleId'] = articleId
        else:
            body['articleId'] = ''
        
        # title body parameter.
        if titleExclude == True:
            pass
        elif title != '':
            body['title'] = title
        else:
            body['title'] = ''
            
        # agencyId body parameter.
        if agencyIdExclude == True:
            pass
        elif agencyId != '':
            body['agencyId'] = agencyId
        else:
            body['agencyId'] = ''
            
        # audience body parameter.
        if audienceExclude == True:
            pass
        elif audience != '':
            body['audience'] = audience
        else:
            body['audience'] = ''
            
        # shortDesc body parameter.
        if shortDescExclude == True:
            pass
        elif shortDesc != '':
            body['shortDesc'] = shortDesc
        else:
            body['shortDesc'] = ''
            
        # longDesc body parameter.
        if longDescExclude == True:
            pass
        elif longDesc != '':
            body['longDesc'] = longDesc
        else:
            body['longDesc'] = ''
            
        # tags body parameter.
        if tagsExclude == True:
            pass
        elif tags != '':
            body['tags'] = tags
        else:
            body['tags'] = ''
            
        # attachments body parameter.
        if attachmentsExclude == True:
            pass
        elif attachments != '' and attachments != []:
            body['attachments'] = attachments
        else:
            body['attachments'] = ''
            
        # status body parameter.
        if statusExclude == True:
            pass
        elif status != '':
            body['status'] = status
        else:
            body['status'] = ''
            
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nEdit_article\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn comment_article : Will add comments to the specified article.
    #
    def comment_article(self, Authorization='', articleId=[], comment='', 
                        AuthorizationExclude=False, articleIdExclude=False, 
                        commentExclude=False, return_status=False):
        
        url = self.environment + QaADPQShell.ArticleComment
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        body = {}
        
        # articleId body parameter.
        if articleIdExclude == True:
            pass
        elif articleId != '' and articleId != []:
            if type(articleId) == list: 
                body['articleId'] = articleId[0]
            else:
                body['articleId'] = articleId
        else:
            body['articleId'] = ''
        
        # comment body parameter.
        if commentExclude == True:
            pass
        elif comment != '':
            body['comment'] = comment
        else:
            body['comment'] = ''
            
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ncomment_article\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn get_presignedS3 : Will......
    #
    def get_presignedS3(self, Authorization='', name='', AuthorizationExclude=False, 
                        nameExclude=False, return_status=False):
        
        url = self.environment + QaADPQShell.PreS3
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        body = {}
        
        # name body parameter.
        if nameExclude == True:
            pass
        elif name != '':
            body['name'] = name
        else:
            body['name'] = ''
        
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nget_presignedS3\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn dashboard_analytics : Will get the analytics of the user such as
    #                            review, public, decline, etc counts.
    #
    def dashboard_analytics(self, Authorization='', AuthorizationExclude=False):  

        url = self.environment + QaADPQShell.DashAnalytics
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ndashboard_analytics\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn dashboard_trending : Will get all trending articles.
    #
    def dashboard_trending(self, Authorization='', AuthorizationExclude=False):  

        url = self.environment + QaADPQShell.DashTrending
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
            
        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ndashboard_trending\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn dashboard_pubArticles : Will get all the users published articles.
    #
    def dashboard_pubArticles(self, Authorization='', AuthorizationExclude=False):  

        url = self.environment + QaADPQShell.DashPubArticles + QaADPQShell.articleLimit
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''

        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ndashboard_pubArticles\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn dashboard_workflow : Will get the workflow on the dashboard.
    #
    def dashboard_workflow(self, Authorization='', AuthorizationExclude=False):  

        url = self.environment + QaADPQShell.DashWorkflow
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
            
        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ndashboard_workflow\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        return responseBody
    
    

    def GetRole(self):
        return self.role
    
    def GetAuthKey(self):
        return self.AuthKey
    
    def GetUserId(self):
        return self.UserID
    
    def GetArticleIds(self):
        return self.articleId