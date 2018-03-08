import requests, os, json


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
if 'TESTOUTPUT' not in os.environ.keys():
    TestOutput = False
else:
    TestOutput = bool(os.environ['TESTOUTPUT'])
    
# Get all necessary data.
with open('data.json') as data_file:    
    data = json.load(data_file)
# print(data)
    

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
        
        
        
    ## @fn create_user : Will create a user with role 1.
    #
    def create_user(self, Authorization='', firstName='', lastName='', email='',
                    phone='', agencyId=[], AuthorizationExclude=False,  
                    fNameExclude=False, lNameExclude=False, emailExclude=False,
                    phoneExclude=False, agencyIdExclude=False, return_status=False):
        
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
            
        response = requests.request('POST', url, json={}, headers=headers, verify=False)
    
        responseBody = response.json()
        
        if TestOutput == True:
            print('\ncreate_user\n', responseBody)
            print('response.status_code: ', response.status_code)
            print('body:', body)
            print('headers:', headers)
        
        # Delete the articleId if successful.
        if response.status_code == 200 and "error" not in responseBody.keys():
            del self.articleId[0]
            
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
    
    
    
    ## @fn search_articles : Get all articles within the db.
    #
    def search_articles(self, return_status=False):

        url = self.environment + data['SearchArticles']
        
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
            
        # If triggered, will return request object instead of json object.
        if return_status == True:
            return response
        
        return responseBody
    
    
    
    ## @fn sign_in : Allows an existing user to log into their account. 
    # :required - email
    #
    def sign_in(self, email='', emailExclude=False):

        url = self.environment + data['UsersSignIn']
        
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
    
        responseBody = response.json()
        
        # Only if request was successful, save critical user data.
        if 'token' in responseBody.keys():
            if response.status_code == 200 and responseBody['token'] != None:
                self.AuthKey = responseBody['token']
                self.role = responseBody['role']
                self.UserID = responseBody['id']
        
        if TestOutput == True:
            print('\nsign_in\n', responseBody)
            print('response.status_code: ', response.status_code)
        
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
            print('response.status_code: ', response.status_code)
            
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
            
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
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
            
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
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
        
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
    
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
        
        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
    
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
    
    
    
    
    
    
def Test_Class():
    # Declare class objects. Create class instance. DONE
    user = ADPQ()

    
    # Method signature. DONE
    # create_user(Authorization='', firstName='', lastName='', email='',
    #             phone='', agencyId=[], AuthorizationExclude=False,  
    #             fNameExclude=False, lNameExclude=False, emailExclude=False,
    #             phoneExclude=false, agencyIdExclude=False, return_status=False):
    user.create_user(data['testFirstName'], data['testLastName'], data['testEmail'],
                     data['testPhone'], data['testAgencyId'])
    
    
#     # Method signature. DONE
#     # sign_in(self, email='', emailExclude=False, return_status=False):
#     user.sign_in(email = data['testEmail'])
    
    
#     # Method signature. DONE
#     # get_agencies(return_status=False):
#     user.get_agencies()
    
    
#     # Method signature. DONE
#     # get_tags(return_status=False):
#     user.get_tags()
     
     
#     # Method signature. DONE
#     # get_articles(Authorization='', AuthorizationExclude=False, sortUrl=False,
#     #              limitUrl=False, dateStartURL=False, dateEndUrl=False,
#     #              agencyIdUrl=False, tagIdUrl=False, return_status=False):
#     user.get_articles(Authorization = user.GetAuthKey(), AuthorizationExclude=False,
#                       sortUrl=False, limitUrl=True, dateStartURL=False, dateEndUrl=False,
#                       agencyIdUrl=False, tagIdUrl=True, return_status=False)
     
     
#     # Method signature. DONE
#     # search_articles(return_status=False):
#     user.search_articles()

    
    # Method signature. DONE
    # create_article(Authorization='', title='', agencyId='', audience=0,
    #                shortDesc='', longDesc='', tags='', attachments=[],
    #                AuthorizationExclude=False, titleExclude=False,
    #                agencyIdExclude=False, audienceExclude=False,
    #                shortDescExclude=False, longDescExclude=False, 
    #                tagsExclude=False, attachmentsExclude=False, return_status=False):
    user.create_article(user.GetAuthKey(), "Ministry of Truth", '5a8b73f94212d1f20f847b9a',
                        '0', 'short desc', 'loonngg desc', 'LSDog', ["url1"])
    
    
#     # Method signature. DONE
#     # get_articles_details(Authorization='', AuthorizationExclude=False,
#     #                      articleId=[], return_status=False):
#     user.get_articles_details(user.GetAuthKey(), articleId = user.GetArticleIds())
    
    
#     # Method signature. DONE
#     # dashboard_analytics(self, Authorization='', AuthorizationExclude=False,
#                           return_status=False): 
#     user.dashboard_analytics(user.GetAuthKey())
#     
#     
#     # Method signature. DONE
#     # dashboard_trending(self, Authorization='', AuthorizationExclude=False,
#                           return_status=False):  
#     user.dashboard_trending(user.GetAuthKey())
#     
#     
#     # Method signature. DONE
#     # dashboard_pubArticles(self, Authorization='', AuthorizationExclude=False,
#                           return_status=False): 
#     user.dashboard_pubArticles(user.GetAuthKey())
#     
#     
#     # Method signature. DONE
#     # dashboard_workflow(self, Authorization='', AuthorizationExclude=False,
#                           return_status=False): 
#     user.dashboard_workflow(user.GetAuthKey())


#     # Method signature. DONE
#     # admin_dashboard_decline(Authorization='', AuthorizationExclude=False, 
#     #                         return_status=False):
#     user.admin_dashboard_decline(user.GetAuthKey())
#     
#     
#     # Method signature. DONE
#     # admin_dashboard_approved(Authorization='', AuthorizationExclude=False, 
#     #                          return_status=False):  
#     user.admin_dashboard_approved(user.GetAuthKey())
#     
#     
#     # Method signature. DONE
#     # admin_dashboard_pending(Authorization='', AuthorizationExclude=False, 
#     #                         return_status=False):
#     user.admin_dashboard_pending(user.GetAuthKey()) 
    

#     # Method signature. DONE
#     # edit_article(Authorization='', articleId=[], title='', agencyId='', audience=0,
#     #              shortDesc='', longDesc='', tags='', attachments=[], status=0,
#     #              AuthorizationExclude=False, articleIdExclude=False, titleExclude=False,
#     #              agencyIdExclude=False, audienceExclude=False,
#     #              shortDescExclude=False, longDescExclude=False, 
#     #              tagsExclude=False, attachmentsExclude=False, statusExclude=False,
#     #              return_status=False)
#     user.edit_article(user.GetAuthKey(), user.GetArticleIds(), "Department of funky beats",
#                       '5a8b73f94212d1f20f847b9a', 0, 'short desc', 'long desc',
#                       'tags', ['pdf1, 666'], 0)
    
    
#     # Method signature. DONE
#     # comment_article(Authorization='', articleId=[], comment='', 
#     #                 AuthorizationExclude=False, articleIdExclude=False, 
#     #                   commentExclude=False, return_status=False):
#     user.comment_article(user.GetAuthKey(), user.GetArticleIds(), 'COMMENTS')
    
    
#     # Method signature. DONE
#     # get_presignedS3(Authorization='', name='', AuthorizationExclude=False, 
#     #                 nameExclude=False, return_status=False):
#     user.get_presignedS3(user.GetAuthKey(), 'file.txt')


    # Method signature. START HERE SCRIPT ALREADY NON FILE
    # delete_article(Authorization='', articleId=[],
    #                AuthorizationExclude=False,  articleIdExclude=False,
    #                return_status=False):
    user.delete_article(user.GetAuthKey(), user.GetArticleIds())
    
    
Test_Class()