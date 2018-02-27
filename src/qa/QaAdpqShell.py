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

#     # Set API Version
#     setEnv = setEnv + '/api/v1/'
 
setEnv.strip()


## @class ADPQ Test Automation Shell 
# This shell provides a mechanisms from which to run python3 unittest 
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
    
    # Save a BaseURL without API Version
    BaseURL = setEnv
    
    # Set API Version
    setEnv = setEnv + '/api/v1/'
    
    articleSort = 'sort='
    articleLimit = 'limit='
    articleDateStart = 'dateStart='
    articleDateEnd = 'dateEnd='
    articleAgencyId = 'agencyId='
    agencyTagId = 'tagId='
    
        
        
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
    
    
    
    ## @fn get_article : Will 
    # :required - api_key
    #
    def articles(self, api_key='', apiKeyExclude=False, 
                 Authorization='', AuthorizationExclude=False):
        # URL end point.
        url = self.environment + QaADPQShell.Articles

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        # Add the api_key header parameter.
        if apiKeyExclude == True:
            pass
        elif api_key != '':
            headers['api_key'] = api_key
        else:
            headers['api_key'] = ''
            
        # Add the Authorization header parameter.
        if AuthorizationExclude == True:
            pass
        elif Authorization != '':
            headers['Authorization'] = Authorization
        else:
            headers['Authorization'] = ''
        
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
        
#         # Add the network body parameter.
#         if networkExclude == True:
#             pass
#         elif network != '':
#             body['network'] = network
#         else:
#             body['network'] = ''
#             
#         # Add the email body parameter.
#         if emailExclude == True:
#             pass
#         elif email != '':
#             body['email'] = email
#         else:
#             body['email'] = ''
#             
#         # Add the password body parameter.
#         if passwordExclude == True:
#             pass
#         elif password != '':
#             body['password'] = password
#         else:
#             body['password'] = ''
            
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
    
    

    def GetRole(self):
        return self.role
    
    def GetAuthKey(self):
        return self.AuthKey
    
    def GetUserId(self):
        return self.UserID
    
    

## @fn Test_Class()  
# Test_Class function allows the user to 'test drive' every class 
# method above. This function provides example calls. 
# Above each class method call is the method signature.
# 
#     
def Test_Class():
    # Declare class objects. Create class instance. DONE
    user = QaADPQShell()
    
    
    # Method signature. WORKIGN ON THIS
    # sign_in(self, email='', emailExclude=False):
    user.sign_in(email = QaADPQShell.testEmail)
    
    
#     # Method signature. DONE
#     # get_agencies():
#     user.get_agencies()
    
    
#     # Method signature. DONE
#     # get_tags():
#     user.get_tags()
     
     
#     # Method signature. 
#     # articles(self, api_key='', apiKeyExclude=False, 
#     #             Authorization='', AuthorizationExclude=False):
#     user.articles(api_key = user.GetApiKey(), apiKeyExclude=True, 
#                   Authorization = user.GetAuthKey(), AuthorizationExclude=False)
     
     
#     # Method signature. DONE
#     # search_articles():
#     user.search_articles()
    
    
#     # Method signature. MAY NOT BE NEEDED
#     # remove_user(self, email=''):
#     user.remove_user(user.testEmail)
    
    
    
# Test_Class()