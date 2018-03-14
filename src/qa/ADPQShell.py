import requests, os, json

requests.packages.urllib3.disable_warnings()

# Set API Development Environment.
setEnv = ''
if 'Environment' not in os.environ.keys():
    print('\n[AutoScript] Defaulting to staging.\n')
    setEnv = 'https://adpq-staging.hotbsoftware.com'
else:
    print('\n[AutoScript] Setting environment to', os.environ['Environment'], '\n')
    if os.environ['Environment'] == 'local':
        setEnv = 'http://localhost:3001'
    elif os.environ['Environment'] == 'staging':
        setEnv = 'https://adpq-staging.hotbsoftware.com'
    elif os.environ['Environment'] == 'prod':
        setEnv = 'https://adpq.hotbsoftware.com'
setEnv.strip()


# Set test output flag.
# True  - Test print statements will output to console.
# False - No console output.
if 'TESTOUTPUT' not in os.environ.keys():
    TestOutput = False
else:
    TestOutput = bool(os.environ['TESTOUTPUT'])
    
# Get all necessary data.
with open('data.json') as data_file:    
    data = json.load(data_file)

    

'''
    ADPQ Test Automation Shell 
    
    Shell provides a platform to run unittest scripts against. 
    
    Each class method corresponds to an end point. 
    
    Each method contains header/body dictionaries. Dict pairs can be
    entirely excluded or assigned any values, including null.
    
    example(email='', emailExclude=False)
    
    If emailExclude flag is set to True during the method call, the keypair 
    will not be included in the request.
'''
class ADPQ:
    ## @var Save a BaseURL without API Version.
    BaseURL = setEnv
    
    ## @var Set API Version.
    setEnv = setEnv + '/api/v1/'
        
    ## @fn __init__ : Class initializations.
    def __init__(self, env=setEnv):
        self.ClientID = data['ClientId']
        self.AuthKey = ''
        self.UserID = ''
        self.email = ''
        self.environment = env
        self.role = ''
        self.agencyId = []
        self.articleId = []
        self.newUserIds = []
        
        
        
    ## @fn create_user : Will create a user with role 1.
    #
    def create_user(self, Authorization='', firstName='', lastName='', email='',
                    phone='', password='', agencyId=[], allowUploads=0, AuthorizationExclude=False,  
                    fNameExclude=False, lNameExclude=False, emailExclude=False,
                    phoneExclude=False, agencyIdExclude=False, passwordExclude=False,
                    allowUploadsExclude=False, return_status=False):
        
        url = self.environment + data["CreateUser"]
        
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
        
        # firstName body parameter.
        if fNameExclude == True:
            pass
        elif firstName != '':
            body['firstName'] = firstName
        else:
            body['firstName'] = ''
            
        # lastName body parameter.
        if lNameExclude == True:
            pass
        elif lastName != '':
            body['lastName'] = lastName
        else:
            body['lastName'] = ''
            
        # email body parameter.
        if emailExclude == True:
            pass
        elif email != '':
            body['email'] = email
        else:
            body['email'] = ''
            
        # phone body parameter.
        if phoneExclude == True:
            pass
        elif phone != '':
            body['phone'] = phone
        else:
            body['phone'] = ''
            
        # password body parameter.
        if passwordExclude == True:
            pass
        elif password != '':
            body['password'] = password
        else:
            body['password'] = ''
        
        # agencyId body parameter.
        if agencyIdExclude == True:
            pass
        elif agencyId != '' and agencyId != []:
            if type(agencyId) == list: 
                body['agencyId'] = agencyId[0]
            else:
                body['agencyId'] = agencyId
        else:
            body['agencyId'] = ''
            
        # allowUploads body parameter.
        if allowUploadsExclude == True:
            pass
        elif password != '':
            body['allowUploads'] = allowUploads
        else:
            body['allowUploads'] = ''
            
        response = requests.request('POST', url, json=body, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ncreate_user\n', responseBody)
            print('responseBody: ', response.status_code)
            print('body:', body)
            print('headers:', headers)
            print('url:', url)
        
        # Append the new user id.
        if 'status' in responseBody.keys():
            if responseBody['status'] == 'saved!':
                self.newUserIds.append(responseBody['userId'])
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn delete_user : Will 
    #
    def delete_user(self, Authorization='', userId=[],
                       AuthorizationExclude=False,  userIdExclude=False,
                       return_status=False):
        
        url = self.environment + data['DeleteUser']
        
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
        if userIdExclude == True:
            pass
        elif userId != '' and userId != []:
            if type(userId) == list: 
                body['userId'] = userId[0]
            else:
                body['userId'] = userId
        else:
            body['userId'] = ''
        
        # Delete the article at this dict value.
        url = url + body['userId']
            
        response = requests.request('DELETE', url, json={}, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ndelete_user\n', responseBody)
            print('response.status_code: ', response.status_code)
            print('headers: ', headers)
            print('url: ', url)
        
        # Delete the articleId if successful.
        if response.status_code == 200 and "error" not in responseBody.keys():
            self.UserID = ''
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
        
        
    
    ## @fn delete_article : Will add comments to the specified article.
    #
    def delete_article(self, Authorization='', articleId=[],
                       AuthorizationExclude=False,  articleIdExclude=False,
                       return_status=False):
        
        url = self.environment + data['DeleteArticle']
        
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
            body['articleId'] = '5a9f3382724638000fcf011a'
        
        # Delete the article at this dict value.
        url = url + body['articleId']
            
        response = requests.request('DELETE', url, json={}, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ndelete_article\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        # Delete the articleId if successful.
        if response.status_code == 200 and "error" not in responseBody.keys():
            del self.articleId[0]
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn get_agency_list : Will return a list of all agencies.
    # :required - api_key
    #
    def get_agencies(self, return_status=False):

        url = self.environment + data['GetAgencies']
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
        
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nget_agencies\n', responseBody)
            print('response.status_code: ', response.status_code)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response

        return responseBody
    
    
    

    ## @fn get_tagst : Will return a list of all tags.
    #
    def get_tags(self, return_status=False):

        url = self.environment + data['GetTags']
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nget_tags\n', responseBody)
            print('response.status_code: ', response.status_code)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    


    
    ## @fn get_article : Will get a list of articles given the users permissions. 
    # :required - Authorization
    #
    def get_articles(self, Authorization='', AuthorizationExclude=False, sortUrl=False,
                     limitUrl=False, dateStartURL=False, dateEndUrl=False,
                     agencyIdUrl=False, tagIdUrl=False, return_status=False):

        url = self.environment + data['Articles']

        # End point options which can be appended to the end of the url.
        # ?example=100&
        if sortUrl == True:
            url = url + data['articleSort']
        if limitUrl == True:
            url = url + data['articleLimit']
        if dateStartURL == True:
            url = url + data['articleDateStart']
        if dateEndUrl == True:
            url = url + data['articleDateEnd']
        if agencyIdUrl == True:
            url = url + data['articleAgencyId']
        if tagIdUrl == True:
            url = url + data['agencyTagId']
        
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
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn search_articles : Get all articles within the db with 
    #                        keyword health.
    #
    def search_articles(self, Authorization='', AuthorizationExclude=False, 
                        return_status=False):

        url = self.environment + 'searchArticles?keyword=health'
        
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
            
        response = requests.request('GET', url, json={},  headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nsearch_articles\n', responseBody)
            print('response.status_code: ', response.status_code)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn sign_in : Allows an existing user to log into their account. 
    # :required - email
    # :required - password
    #
    def sign_in(self, email='', password='', emailExclude=False, passwordExclude=False,
                return_status=False):

        url = self.environment + data['UsersSignIn']
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        body = {}
        
        # email body parameter.
        if emailExclude == True:
            pass
        elif email != '':
            body['email'] = email
        else:
            body['email'] = ''
            
        # password body parameter.
        if passwordExclude == True:
            pass
        elif password != '':
            body['password'] = password
        else:
            body['password'] = ''
            
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
        responseBody = response.json()
        
        # Only if request was successful, save critical user data.
        if 'token' in responseBody.keys():
            if response.status_code == 200 and responseBody['token'] != None:
                self.AuthKey = responseBody['token']
                self.role = responseBody['role']
                self.UserID = responseBody['id']
        
        if TestOutput == True:
            print('\nsign_in\n', responseBody)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn get_articles_details : Gets details of all articles. If an articleId 
    #                             is appended to url, then only details returned
    #                             are for specified article.
    #                             
    def get_articles_details(self, Authorization='', AuthorizationExclude=False,
                             articleId=[], return_status=False):
        
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
            url = self.environment + 'articles/' + ''
        
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
            
        response = requests.request('GET', url, headers=headers, verify=False)
        
        if TestOutput == True:
            print('\nresponse.status_code:', response.status_code)
            print('response:', response)
            print('url: ', url)
            print('headers: ', headers)
            
        responseBody = response.json()
        
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn create_article : Creates an article.
    #
    def create_article(self, Authorization='', title='', agencyId='', audience='',
                       shortDesc='', longDesc='', tags='', attachments=[],
                       AuthorizationExclude=False, titleExclude=False,
                       agencyIdExclude=False, audienceExclude=False,
                       shortDescExclude=False, longDescExclude=False, 
                       tagsExclude=False, attachmentsExclude=False, return_status=False):

        url = self.environment + data['Articles']
        
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
                body['attachments'] = list(attachments[0])
            else:
                body['attachments'] = list(attachments)
        else:
            body['attachments'] = list('')
            
        response = requests.request('POST', url, json=body, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if 'status' in responseBody.keys():
            if responseBody['status'] == 'saved!':
                self.articleId.append(responseBody['articleId']) 
        
        if TestOutput == True:
            print('\ncreate_article\n', responseBody)
            print('self.articleId: ', self.articleId)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
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
        
        url = self.environment + data['EditArticles']
        
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
            
        response = requests.request('POST', url, json=body, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nEdit_article\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn comment_article : Will add comments to the specified article.
    #
    def comment_article(self, Authorization='', articleId=[], comment='', 
                        AuthorizationExclude=False, articleIdExclude=False, 
                        commentExclude=False, return_status=False):
        
        url = self.environment + data['ArticleComment']
        
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
            
        response = requests.request('POST', url, json=body, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ncomment_article\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn get_presignedS3 : Will......
    #
    def get_presignedS3(self, Authorization='', name='', AuthorizationExclude=False, 
                        nameExclude=False, return_status=False):
        
        url = self.environment + data['PreS3']
        
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
        
        response = requests.request('POST', url, json=body, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nget_presignedS3\n', responseBody)
            print('response.status_code: ', response.status_code)
        
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn dashboard_analytics : Will get the analytics of the user such as
    #                            review, public, decline, etc counts.
    #
    def dashboard_analytics(self, Authorization='', AuthorizationExclude=False, 
                            return_status=False):  

        url = self.environment + data['DashAnalytics']
        
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
        
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ndashboard_analytics\n', responseBody)
            print('response.status_code: ', response.status_code)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn dashboard_trending : Will get all trending articles.
    #
    def dashboard_trending(self, Authorization='', AuthorizationExclude=False, 
                            return_status=False):   

        url = self.environment + data['DashTrending']
        
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
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn dashboard_pubArticles : Will get all the users published articles.
    #
    def dashboard_pubArticles(self, Authorization='', AuthorizationExclude=False, 
                            return_status=False):    

        url = self.environment + data['DashPubArticles'] + data['articleLimit']
        
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
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn dashboard_workflow : Will get the workflow on the dashboard.
    #
    def dashboard_workflow(self, Authorization='', AuthorizationExclude=False, 
                            return_status=False):    

        url = self.environment + data['DashWorkflow']
        
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
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn admin_dashboard_decline : Will get the analytics of the user such as
    #                            review, public, decline, etc counts.
    #
    def admin_dashboard_decline(self, Authorization='', AuthorizationExclude=False, 
                                return_status=False):  

        url = self.environment + data['AdminDashDecline']
        
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
        
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nadmin_dashboard_decline', responseBody)
            print('response.status_code: ', response.status_code)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn admin_dashboard_approved : Will get the analytics of the user such as
    #                            review, public, decline, etc counts.
    #
    def admin_dashboard_approved(self, Authorization='', AuthorizationExclude=False, 
                                return_status=False):  

        url = self.environment + data['AdminDashApproved']
        
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
        
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nadmin_dashboard_approved', responseBody)
            print('response.status_code: ', response.status_code)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn admin_dashboard_pending : Will get the analytics of the user such as
    #                            review, public, decline, etc counts.
    #
    def admin_dashboard_pending(self, Authorization='', AuthorizationExclude=False, 
                                return_status=False):  
        
        url = self.environment + data['AdminDashPending']
        
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
        
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\nadmin_dashboard_pending', responseBody)
            print('response.status_code: ', response.status_code)
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    

    def GetRole(self):
        return self.role
    
    def GetAuthKey(self):
        return self.AuthKey
    
    def GetUserId(self):
        return self.UserID
    
    def GetArticleIds(self):
        return self.articleId
    
    def GetNewUserIds(self):
        return self.newUserIds