import sys, unittest, ADPQShell
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

    @classmethod
    def setUpClass(cls):
        try:
            cls.user = ADPQShell.ADPQ()
            # Create shell BaseURL class object (version appended).
            cls.BaseUrl = ADPQShell.ADPQ.setEnv
            cls.user.sign_in(email = ADPQShell.data['testEmail'],
                             password = ADPQShell.data['testPassword'])
            assert(cls.BaseUrl != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])

     
     
    ## Get the status of the get agencies end point.
    def test_GetAgenciesStatus(self):
        status = self.user.get_agencies(return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_GetAgenciesStatus assert#1 failed.')
         
         
         
    ## Get the status of the get tags end point.
    def test_GetTagStatus(self):
        status = self.user.get_tags(return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_GetTagStatus assert#1 failed.')
         
         
         
    ## Get the status of the get articles end point.
    def test_GetArticleStatus(self):
        status = self.user.get_articles(Authorization = self.user.GetAuthKey(),
                                        sortUrl=True, limitUrl=True, tagIdUrl=True,
                                        return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_GetArticleStatus assert#1 failed.')
          
          
          
    ## Get the status of the search articles end point.
    def test_GetSearchArticleStatus(self):
        status = self.user.search_articles(return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_GetSearchArticleStatus assert#1 failed.')
         
         
         
    ## Get the status of the SignIn end point.
    def test_UserSignInStatus(self):
        status = self.user.sign_in(email = ADPQShell.data['testEmail'], 
                                   password = ADPQShell.data['testPassword'], 
                                   return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_UserSignInStatus assert#1 failed.')
        
        
        
    ## Get the status of the GetArticleDetails end point.
    def test_GetArticleDetailsStatus(self):
        status = self.user.get_articles_details(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_GetArticleDetailsStatus assert#1 failed.')
        
        
         
    ## Get the status of the CreateArticle end point.
    def test_CreateArticleStatus(self):
        status = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                        title = ADPQShell.data['testTitle'], 
                                        agencyId = ADPQShell.data['testAgencyId'],
                                        audience = ADPQShell.data['testAudience'], 
                                        shortDesc = ADPQShell.data['testShortDesc'], 
                                        longDesc = ADPQShell.data['testLongDesc'], 
                                        tags = ADPQShell.data['testTags'], 
                                        attachments = ADPQShell.data['testAttachments'],
                                        return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_CreateArticleStatus assert#1 failed.')
        
        
    ## Get the status of the dashboard_analytics end point.
    def test_DashboardAnalyticsStatus(self):
        status = self.user.dashboard_analytics(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_DashboardAnalyticsStatus assert#1 failed.')
        
        

    ## Get the status of the dashboard_trending end point.
    def test_DashboardTrendingStatus(self):
        status = self.user.dashboard_trending(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_DashboardTrendingStatus assert#1 failed.')
        
        
    ## Get the status of the dashboard_pubArticles end point.
    def test_DashboardPubArticlesStatus(self):
        status = self.user.dashboard_pubArticles(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_DashboardPubArticlesStatus assert#1 failed.')
        
        
        
    ## Get the status of the dashboard_workflow end point.
    def test_DashboardWorkflowStatus(self):
        status = self.user.dashboard_workflow(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_DashboardWorkflowStatus assert#1 failed.')
        
        
        
    ## Get the status of the Edit Article end point.
    def test_EditArticleStatus(self):
        status = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                          articleId = self.user.GetArticleIds(), 
                                          title = ADPQShell.data['testTitle'],
                                          agencyId = ADPQShell.data['testAgencyId'], 
                                          audience = ADPQShell.data['testAudience'], 
                                          shortDesc = ADPQShell.data['testShortDesc'], 
                                          longDesc = ADPQShell.data['testLongDesc'], 
                                          tags = ADPQShell.data['testTags'], 
                                          attachments = ADPQShell.data['testAttachments'], 
                                          status = ADPQShell.data['testStatus'],
                                          return_status = True)
        self.assertEqual(status.status_code, 200, msg='test_EditArticleStatus assert#1 failed.')
        self.user.delete_article(Authorization = self.user.GetAuthKey(), 
                                    articleId = self.user.GetArticleIds())
        
        
        
    ## Get the status of the Comment Article end point.
    def test_CommentArticleeStatus(self):
        status = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                           articleId = '5a907847ca13999bc0d11d92', 
                                           comment = "comments", return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_CommentArticleeStatus assert#1 failed.')
        
        
        
    ## Get the status of the Presigned S3 end point.
    def test_PresignedS3Status(self):
        status = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                           name = 'puppy.jpeg', return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_PresignedS3Status assert#1 failed.')
    
    
    
    ## Get the status of the AdminDashboard end point.
    def test_AdminDashboardsStatus(self):
        status = self.user.admin_dashboard_decline(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_AdminDashboardStatus assert#1 failed.')
        
        status = self.user.admin_dashboard_approved(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_AdminDashboardStatus assert#2 failed.')
        
        status = self.user.admin_dashboard_pending(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_AdminDashboardStatus assert#3 failed.')


    
    
    
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
    suite.addTest(SmokeTest('test_AdminDashboardsStatus'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())