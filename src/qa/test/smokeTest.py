import sys, unittest, QaAdpqShell, requests

## @package smoke test
#

'''
    ADPQ v1 - All end points.
    
    Purpose - Will test all end points for their status. 200 status 
              indicates that the end point is active and running 
              properly. 

    Test cases
        Test end point GetAgencies by extracting a status code.
        Test end point GetTags by extracting a status code.
        Test end point GetArticles by extracting a status code.
        Test end point SearchArticles by extracting a status code.
        Test end point UserSignIn by extracting a status code.
'''
class SmokeTest(unittest.TestCase):
    title = 'Department of funky beats'
    agencyId = '5a8b73f94212d1f20f847b9a'
    audience = 0
    shortDesc = 'short description here'
    longDesc = 'This is a longer description'
    tags = '5a8b55bca2d13ad4ba5369ef'
    attachments = ["url1"]
    status = 0

    @classmethod
    def setUpClass(cls):
        try:
            # Make a class object user.
            cls.user = QaAdpqShell.QaADPQShell()
            # Create shell BaseURL class object (version appended).
            cls.BaseUrl = QaAdpqShell.QaADPQShell.setEnv
            # SignIn a user. 
            cls.user.sign_in(email = QaAdpqShell.QaADPQShell.testEmail)
            assert(cls.BaseUrl != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            raise

     
     
    ## Get the status of the get agencies end point.
    def test_GetAgenciesStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.GetAgencies
        
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        # Assign the body parameters.
        body = {}
        
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
        
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_GetAgenciesStatus assert#1 failed.')
         
         
         
    ## Get the status of the get tags end point.
    def test_GetTagStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.GetTags
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_GetTagStatus assert#1 failed.')
         
         
         
    ## Get the status of the get articles end point.
    def test_GetArticleStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.Articles
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_GetArticleStatus assert#1 failed.')
          
          
          
    ## Get the status of the search articles end point.
    def test_GetSearchArticleStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.SearchArticles 
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_GetSearchArticleStatus assert#1 failed.')
         
         
         
    ## Get the status of the SignIn end point.
    def test_UserSignInStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.UsersSignIn 
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
         
        # Assign the body parameters.
        body = {'email':'jlennon@hotbsoftware.com'}
         
        # Make the call and return the save the results.
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_UserSignInStatus assert#1 failed.')
        
        
        
    ## Get the status of the GetArticleDetails end point.
    def test_GetArticleDetailsStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.Articles 
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_GetArticleDetailsStatus assert#1 failed.')
        
        
        
    ## Get the status of the GetArticleDetails end point.
    def test_CreateArticleStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.Articles 
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('POST', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_CreateArticleStatus assert#1 failed.')
        
        
        
    ## Get the status of the dashboard_analytics end point.
    def test_DashboardAnalyticsStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.DashAnalytics 
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache',
            'Authorization': str(self.user.GetAuthKey())
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_DashboardAnalyticsStatus assert#1 failed.')
        
        
        
    ## Get the status of the dashboard_trending end point.
    def test_DashboardTrendingStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.DashTrending 
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache',
            'Authorization': str(self.user.GetAuthKey())
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_DashboardTrendingStatus assert#1 failed.')
        
        
        
    ## Get the status of the dashboard_pubArticles end point.
    def test_DashboardPubArticlesStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.DashPubArticles 
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache',
            'Authorization': str(self.user.GetAuthKey())
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_DashboardPubArticlesStatus assert#1 failed.')
        
        
        
    ## Get the status of the dashboard_workflow end point.
    def test_DashboardWorkflowStatus(self):
        # Build the URL for this end point.
        url = self.BaseUrl + QaAdpqShell.QaADPQShell.DashWorkflow 
         
        # Assign the header parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache',
            'Authorization': str(self.user.GetAuthKey())
        }
         
        # Assign the body parameters.
        body = {}
         
        # Make the call and return the save the results.
        response = requests.request('GET', url, json=body, 
                                    headers=headers, verify=False)
         
        # Ensure that the end point is live.
        self.assertEqual(response.status_code, 200, 
                         msg='test_DashboardWorkflowStatus assert#1 failed.')
        
        
        
    ## Get the status of the Edit Article end point.
    def test_EditArticleStatus(self):
        status = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                        articleId = '5a907847ca13999bc0d11d92', 
                                        title = SmokeTest.title,
                                        agencyId = "5a8b73f94212d1f20f847b9c", 
                                        audience = SmokeTest.audience, 
                                        shortDesc = SmokeTest.shortDesc, 
                                        longDesc = SmokeTest.longDesc, 
                                        tags = SmokeTest.tags, 
                                        attachments = SmokeTest.attachments, 
                                        status = SmokeTest.status,
                                        return_status=True)
        
        # Ensure that the end point is live.
        self.assertEqual(status.status_code, 200, msg='test_EditArticleStatus assert#1 failed.')
        
        
        
    ## Get the status of the Comment Article end point.
    def test_CommentArticleeStatus(self):
        status = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                           articleId = '5a907847ca13999bc0d11d92', 
                                           comment = "comments", return_status=True)
        
        # Ensure that the end point is live.
        self.assertEqual(status.status_code, 200, msg='test_CommentArticleeStatus assert#1 failed.')
        
        
        
    ## Get the status of the Presigned S3 end point.
    def test_PresignedS3Status(self):
        status = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                           name = 'puppy.jpeg', return_status=True)
        
        # Ensure that the end point is live.
        self.assertEqual(status.status_code, 200, msg='test_PresignedS3Status assert#1 failed.')



    
    
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(SmokeTest('test_GetAgenciesStatus'))
    suite.addTest(SmokeTest('test_GetTagStatus'))
    suite.addTest(SmokeTest('test_GetArticleStatus'))
    suite.addTest(SmokeTest('test_GetSearchArticleStatus'))
    suite.addTest(SmokeTest('test_UserSignInStatus'))
    suite.addTest(SmokeTest('test_GetArticleDetailsStatus'))
    suite.addTest(SmokeTest('test_CreateArticleStatus'))
    suite.addTest(SmokeTest('test_DashboardAnalyticsStatus'))
    suite.addTest(SmokeTest('test_DashboardTrendingStatus'))
    suite.addTest(SmokeTest('test_DashboardPubArticlesStatus'))
    suite.addTest(SmokeTest('test_DashboardWorkflowStatus'))
    suite.addTest(SmokeTest('test_EditArticleStatus'))
    suite.addTest(SmokeTest('test_CommentArticleeStatus'))
    suite.addTest(SmokeTest('test_PresignedS3Status'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())