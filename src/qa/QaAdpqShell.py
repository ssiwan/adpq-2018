import requests, os

environmentBody = { 'staging':'http://adpq-staging-loadbalancer-777882718.us-west-1.elb.amazonaws.com',
                    'production':'http://adpq-production-loadbalancer-557804625.us-west-1.elb.amazonaws.com/'
                  }
setEnv = ''



# Set API Development Environment
if 'Environment' not in os.environ.keys():
    print('\n[AutoScript] Defaulting to staging.\n')
    setEnv = environmentBody['staging']
else:
    print('\n[AutoScript] Setting environment to', os.environ['Environment'], '\n')
    #setEnv = os.environ['Environment']
    if os.environ['Environment'] == 'local':
        setEnv = 'http://localhost:3001'
    elif os.environ['Environment'] == 'staging':
        setEnv = 'http://adpq-staging-loadbalancer-777882718.us-west-1.elb.amazonaws.com'
    elif os.environ['Environment'] == 'prod':
        setEnv = 'http://adpq-production-loadbalancer-557804625.us-west-1.elb.amazonaws.com'
 
setEnv.strip()


## @class ADPQ Test Automation Shell 
# This shell provides a mechanism from which to run python3 unittest 
# scripts. The user has absolute control over the header & body 
# parameters. Body & header Parameters can be left out of any call or be 
# assigned any values, including null. Class is called from an external 
# script which has inherited from unittest.TestCase
#
class QaADPQShell:
    
    ## @var Test variables which are used by calling unittest scripts.
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
    
    ## @var URL end point completions.
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
    
    ## Save a BaseURL without API Version
    BaseURL = setEnv
    
    ## Set API Version
    setEnv = setEnv + '/api/v1/'
    
    ## Variables that can be appended at the end of URL end point calls.
    articleSort = 'sort=createdAt&'
    articleLimit = 'limit=1&'
    articleDateStart = 'dateStart=02-01-2018&'
    articleDateEnd = 'dateEnd=03-01-2018&'
    articleAgencyId = 'agencyId=5a8b73f94212d1f20f847b9a&'
    agencyTagId = 'tagId=5a8b55bca2d13ad4ba5369ef&'
    
        
        
    ## @fn __init__ : Class initializations.
    def __init__(self, env=setEnv):
        # Essential information used to successfully run calling scripts.
        self.ClientID = QaADPQShell.ClientId
#         self.apiKey = data['api_key']
        self.UserNetwork = ''
        self.AuthKey = ''
        self.UserID = ''
        self.email = ''
        self.password = ''
        self.placeId = []
        self.groupId = []
        self.environment = env
        self.role = ''
        self.agencyId = []
        self.articleId = []
        
        
        

    ## @fn get_agency_list : Will return a list of all agencies.
    # :required - api_key
    #
    def get_agencies(self):
        # URL end point.
        url = self.environment + QaADPQShell.GetAgencies

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
        
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\nget_agencies\n', responseBody)
        print('response.status_code: ', response.status_code)
        
#         # Iterate through the list items (items are dicts)
#         for i in range(len(responseBody['data'])):
#             # Iterate through the dicts within the list.
#             for keys in responseBody['data'][i]:
#                 print(keys) 

        return responseBody
    
    
    

    ## @fn get_tagst : Will 
    #
    def get_tags(self):
        # URL end point.
        url = self.environment + QaADPQShell.GetTags

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
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
        
        # Optional URL additions.
        if sortUrl == True:
            url = url + QaADPQShell.articleSort
        if limitUrl == True:
            url = url + QaADPQShell.articleLimit
        if dateStartURL == True:
            url = url + QaADPQShell.articleDateStart
            dateEndUrl
        if limitUrl == True:
            url = url + QaADPQShell.articleDateEnd
        if agencyIdUrl == True:
            url = url + QaADPQShell.articleAgencyId
        if tagIdUrl == True:
            url = url + QaADPQShell.agencyTagId

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\nget_article_list\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn get_search : Will return a list of all articles.
    #
    def search_articles(self):#, api_key='', apiKeyExclude=False):
        # URL end point.
        url = self.environment + QaADPQShell.SearchArticles

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\nsearch_articles\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn user_login : Will 
    # :required - email
    #
    def sign_in(self, email='', emailExclude=False):
        # URL end point.
        url = self.environment + QaADPQShell.UsersSignIn

        # HTTP Action.
        HTTP_action = 'POST'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
        
        # Add the network body parameter.
        if emailExclude == True:
            pass
        elif email != '':
            body['email'] = email
        else:
            body['email'] = ''
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\nsign_in\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        # Only if request was successful, save critical user data.
        if 'token' in responseBody.keys():
            if response.status_code == 200 and responseBody['token'] != None:
                self.AuthKey = responseBody['token']
                self.role = responseBody['role']
                self.UserID = responseBody['id']
        
        return responseBody
    
    
    
    ## @fn get_articles_details : Will get details of any passed in article, 
    #                             article ID must be appended to end of the url.
    # :optional - Authorization
    #
    def get_articles_details(self, Authorization='', AuthorizationExclude=False,
                             articleId=[]):
        # If articleId list is not empty, grab the first item. Else, if 
        # the value is empty, make the ID a default article id.
        if articleId != '' and articleId != []:
            if type(articleId) == list:
                ID = articleId[0]
            else:
                ID = articleId
        else:
            ID = '5a907847ca13999bc0d11d92'
            
        # URL end point.
        url = self.environment + 'articles/' + ID

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\nget_articles_details\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn create_article : Will get details of any passed in article, 
    #                             article ID must be appended to end of the url.
    # :required - Authorization
    # :required - title
    # :required - Authorization
    # :required - audience
    # :required - shortDesc
    # :required - longDesc
    # :required - tags
    # :required - attachments
    #
    def create_article(self, Authorization='', title='', agencyId='', audience=0,
                       shortDesc='', longDesc='', tags='', attachments=[],
                       AuthorizationExclude=False, titleExclude=False,
                       agencyIdExclude=False, audienceExclude=False,
                       shortDescExclude=False, longDescExclude=False, 
                       tagsExclude=False, attachmentsExclude=False):
        # URL end point.
        url = self.environment + QaADPQShell.Articles

        # HTTP Action.
        HTTP_action = 'POST'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        body = {}
        
        # Add the title body parameter.
        if titleExclude == True:
            pass
        elif title != '':
            body['title'] = title
        else:
            body['title'] = ''
            
        # Add the agencyId body parameter.
        if agencyIdExclude == True:
            pass
        elif agencyId != '':
            body['agencyId'] = agencyId
        else:
            body['agencyId'] = ''
            
        # Add the audience body parameter.
        if audienceExclude == True:
            pass
        elif audience != '':
            body['audience'] = audience
        else:
            body['audience'] = ''
            
        # Add the shortDesc body parameter.
        if shortDescExclude == True:
            pass
        elif shortDesc != '':
            body['shortDesc'] = shortDesc
        else:
            body['shortDesc'] = ''
            
        # Add the longDesc body parameter.
        if longDescExclude == True:
            pass
        elif longDesc != '':
            body['longDesc'] = longDesc
        else:
            body['longDesc'] = ''
            
        # Add the tags body parameter.
        if tagsExclude == True:
            pass
        elif tags != '':
            body['tags'] = tags
        else:
            body['tags'] = ''
            
        # Add the attachments body parameter.
        if attachmentsExclude == True:
            pass
        elif attachments != '' and attachments != []:
            body['attachments'] = attachments
        else:
            body['attachments'] = ''
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        if 'status' in responseBody.keys():
            if responseBody['status'] == 'saved!':
                self.articleId.append(responseBody['articleId']) 
        
        # ~~ TESTING ~~
        print('\ncreate_article\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn edit_article : Will edit specified article.
    # :required - Authorization
    # :required - articleId
    # :required - title
    # :required - agencyId
    # :required - audience
    # :required - shortDesc
    # :required - longDesc
    # :required - tags
    # :required - attachments
    # :required - status
    #
    def edit_article(self, Authorization='', articleId=[], title='', agencyId='', 
                     audience=0, shortDesc='', longDesc='', tags='', 
                     attachments=[], status=0, AuthorizationExclude=False, 
                     articleIdExclude=False, titleExclude=False, 
                     agencyIdExclude=False, audienceExclude=False,
                     shortDescExclude=False, longDescExclude=False, 
                     tagsExclude=False, attachmentsExclude=False, statusExclude=False,
                     return_status=False):
        # URL end point.
        url = self.environment + QaADPQShell.EditArticles

        # HTTP Action.
        HTTP_action = 'POST'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        body = {}
        
        # Add the articleId body parameter.
        if articleIdExclude == True:
            pass
        elif articleId != '' and articleId != []:
            if type(articleId) == list: 
                body['articleId'] = articleId[0]
            else:
                body['articleId'] = articleId
        else:
            body['articleId'] = ''
        
        # Add the title body parameter.
        if titleExclude == True:
            pass
        elif title != '':
            body['title'] = title
        else:
            body['title'] = ''
            
        # Add the agencyId body parameter.
        if agencyIdExclude == True:
            pass
        elif agencyId != '':
            body['agencyId'] = agencyId
        else:
            body['agencyId'] = ''
            
        # Add the audience body parameter.
        if audienceExclude == True:
            pass
        elif audience != '':
            body['audience'] = audience
        else:
            body['audience'] = ''
            
        # Add the shortDesc body parameter.
        if shortDescExclude == True:
            pass
        elif shortDesc != '':
            body['shortDesc'] = shortDesc
        else:
            body['shortDesc'] = ''
            
        # Add the longDesc body parameter.
        if longDescExclude == True:
            pass
        elif longDesc != '':
            body['longDesc'] = longDesc
        else:
            body['longDesc'] = ''
            
        # Add the tags body parameter.
        if tagsExclude == True:
            pass
        elif tags != '':
            body['tags'] = tags
        else:
            body['tags'] = ''
            
        # Add the attachments body parameter.
        if attachmentsExclude == True:
            pass
        elif attachments != '' and attachments != []:
            body['attachments'] = attachments
        else:
            body['attachments'] = ''
            
        # Add the status body parameter.
        if statusExclude == True:
            pass
        elif status != '':
            body['status'] = status
        else:
            body['status'] = ''
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\nEdit_article\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn dashboard_analytics : Will get the analytics of the user such as
    #                            review, public, decline, etc counts.
    # :required - Authorization
    #
    def dashboard_analytics(self, Authorization='', AuthorizationExclude=False):  
        # URL end point.
        url = self.environment + QaADPQShell.DashAnalytics

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\ndashboard_analytics\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn dashboard_trending : Will get all trending articles.
    # :required - Authorization
    #
    def dashboard_trending(self, Authorization='', AuthorizationExclude=False):  
        # URL end point.
        url = self.environment + QaADPQShell.DashTrending

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\ndashboard_trending\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn dashboard_pubArticles : Will get all the users published articles.
    # :required - Authorization
    #
    def dashboard_pubArticles(self, Authorization='', AuthorizationExclude=False):  
        # URL end point.
        url = self.environment + QaADPQShell.DashPubArticles + QaADPQShell.articleLimit

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
        print('\ndashboard_pubArticles\n', responseBody)
        print('response.status_code: ', response.status_code)
        
        return responseBody
    
    
    
    ## @fn dashboard_workflow : Will get the workflow on the dashboard.
    # :required - Authorization
    #
    def dashboard_workflow(self, Authorization='', AuthorizationExclude=False):  
        # URL end point.
        url = self.environment + QaADPQShell.DashWorkflow

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
    
        # Return requests object of json data.
        responseBody = response.json()
        
        # ~~ TESTING ~~
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
    
    

## @fn Test_Class()  
# Test_Class function allows the user to 'test drive' every class 
# method above. This function provides example calls. 
# Above each class method call is the method signature.
# 
#     
def Test_Class():
    # Declare class objects. Create class instance. DONE
    user = QaADPQShell()
    
    
    # Method signature. DONE
    # sign_in(self, email='', emailExclude=False):
    user.sign_in(email = QaADPQShell.testEmail)
    
    
#     # Method signature. DONE
#     # get_agencies():
#     user.get_agencies()
    
    
#     # Method signature. DONE
#     # get_tags():
#     user.get_tags()
     
     
#     # Method signature. DONE
#     # get_articles(Authorization='', AuthorizationExclude=False, sortUrl=False,
#     #              limitUrl=False, dateStartURL=False, dateEndUrl=False,
#     #              agencyIdUrl=False, tagIdUrl=False):
#     user.get_articles(Authorization = user.GetAuthKey(), AuthorizationExclude=False,
#                       sortUrl=False, limitUrl=True, dateStartURL=False, dateEndUrl=False,
#                       agencyIdUrl=False, tagIdUrl=True)
     
     
#     # Method signature. DONE
#     # search_articles():
#     user.search_articles()

    
    # Method signature. DONE
    # create_article(Authorization='', title='', agencyId='', audience=0,
    #                shortDesc='', longDesc='', tags='', attachments=[],
    #                AuthorizationExclude=False, titleExclude=False,
    #                agencyIdExclude=False, audienceExclude=False,
    #                shortDescExclude=False, longDescExclude=False, 
    #                tagsExclude=False, attachmentsExclude=False):
    user.create_article(user.GetAuthKey(), 'Department of funky beats', '5a8b73f94212d1f20f847b9a',
                        0, 'short desc', 'loonngg desc', '5a8b55bca2d13ad4ba5369ef', ["url1"])
    
    
#     # Method signature. DONE
#     # get_articles_details(Authorization='', AuthorizationExclude=False,
#     #                      articleId=[]):
#     user.get_articles_details(user.GetAuthKey(), articleId = user.GetArticleIds())
    
    
#     # Method signature. DONE
#     # dashboard_analytics(self, Authorization='', AuthorizationExclude=False): 
#     user.dashboard_analytics(user.GetAuthKey())
    
    
#     # Method signature. DONE
#     # dashboard_trending(self, Authorization='', AuthorizationExclude=False): 
#     user.dashboard_trending(user.GetAuthKey())
    
    
#     # Method signature. DONE
#     # dashboard_pubArticles(self, Authorization='', AuthorizationExclude=False):
#     user.dashboard_pubArticles(user.GetAuthKey())
    
    
#     # Method signature. DONE
#     # dashboard_workflow(self, Authorization='', AuthorizationExclude=False):
#     user.dashboard_workflow(user.GetAuthKey())


    # Method signature. DONE
    # edit_article(Authorization='', articleId=[], title='', agencyId='', audience=0,
    #              shortDesc='', longDesc='', tags='', attachments=[], status=0,
    #              AuthorizationExclude=False, articleIdExclude=False, titleExclude=False,
    #              agencyIdExclude=False, audienceExclude=False,
    #              shortDescExclude=False, longDescExclude=False, 
    #              tagsExclude=False, attachmentsExclude=False, statusExclude=False,
    #              return_status=False)
    user.edit_article(user.GetAuthKey(), user.GetArticleIds(), "Department of funky beats",
                      '5a8b73f94212d1f20f847b9a', 0, 'short desc', 'long desc',
                      'tags', ['pdf1, 666'], 0)
     
    user.get_articles_details(user.GetAuthKey(), articleId = user.GetArticleIds())
    
    
Test_Class()