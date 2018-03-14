import sys, unittest, ADPQShell
'''
    ADPQ v1 - Smoke test
    
    Purpose - performed after software build to ascertain that the critical 
              functionalities of the program are working fine.

    Test cases
        Admin dashboard
        Dashboard
        Get agencies
        Get articles
        Get tags
        Sign in
        Create article
        Edit article
        Comment article
        Delete article
'''
class SmokeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.user = ADPQShell.ADPQ()
            cls.user.sign_in(email = ADPQShell.data['testEmail'], 
                              password = ADPQShell.data['testPassword'])   # Role 2.
            
            cls.role1 = ADPQShell.ADPQ()
            cls.role1.sign_in(email = ADPQShell.data['testEmailRole1'],
                              password = ADPQShell.data['testPassword']) # Role 1.
            
        except:
            print("Unexpected error during setUpClass:", sys.exc_info()[0])

    
    
    def test_AdminDashboardSmokeTest(self):
        status = self.user.admin_dashboard_decline(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_AdminDashboardSmokeTest assert#1 has failed.')
        
        
        status = self.user.admin_dashboard_approved(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_AdminDashboardSmokeTest assert#2 has failed.')
        
        
        status = self.user.admin_dashboard_pending(self.user.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_AdminDashboardSmokeTest assert#3 has failed.')
        
     
     
    def test_DashBoard(self):
        status = self.role1.dashboard_analytics(self.role1.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_DashBoard assert#1 failed.')
        
        status = self.role1.dashboard_trending(self.role1.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_DashBoard assert#2 failed.')
        
        status = self.role1.dashboard_pubArticles(self.role1.GetAuthKey(), return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_DashBoard assert#3 failed.')
        
        
        
    def test_GetAgencies(self):
        responseBody = self.user.get_agencies()
        self.assertNotEqual(responseBody['data'], [], msg='test_GetAgencies assert#1 has failed.')
        
        
        
    def test_GetArticles(self):
        responseBody = self.user.get_articles(Authorization = self.user.GetAuthKey())
        self.assertNotEqual(responseBody['data'], [], msg='test_GetArticles assert#1 has failed.')
        
        
        
    def test_GetTags(self):
        responseBody = self.user.get_tags()
        self.assertNotEqual(responseBody['data'], [], msg='test_GetTags assert#1 has failed.')
        
        
    
    def test_Signin(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'],
                                         password = ADPQShell.data['testPassword'])
        self.assertEqual(responseBody['token'], self.user.GetAuthKey(),
                          msg='test_Signin assert#1 has failed.')
        self.assertEqual(responseBody['role'], self.user.GetRole(),
                            msg='test_Signin assert#2 has failed.')
        self.assertEqual(responseBody['id'], self.user.GetUserId(),
                          msg='test_Signin assert#3 has failed.')
        
        
    
    def test_CreateArticle(self):
        # Create article.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!", msg='test_CreateArticle assert#1 has failed.')
        
        
        # Now ensure that the article data was successfully created & saved.
        responseBody = self.user.get_articles_details(Authorization = self.user.GetAuthKey(), 
                                                      articleId = self.user.GetArticleIds())
         
        # Ensure all data persists.
        self.assertEqual(responseBody['data']['title'], ADPQShell.data['testTitle'],
                          msg='test_CreateArticle assert#2 has failed.') 
        
        self.assertEqual(responseBody['data']['summary'], ADPQShell.data['testShortDesc'],
                          msg='test_CreateArticle assert#3 has failed.') 
        
        self.assertEqual(responseBody['data']['description'], ADPQShell.data['testLongDesc'],
                          msg='test_CreateArticle assert#4 has failed.') 
        
        self.assertEqual(responseBody['data']['tags'], [ADPQShell.data['testTags']],
                          msg='test_CreateArticle assert#5 has failed.') 
        
        
        
    def test_EditArticle(self):
        responseBody = self.user.edit_article(Authorization = self.role1.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = ADPQShell.data['testTitle'],
                                              agencyId = ADPQShell.data['testAgencyId'], 
                                              audience = ADPQShell.data['testAudience'], 
                                              shortDesc = ADPQShell.data['testShortDesc'], 
                                              longDesc = ADPQShell.data['testLongDesc'], 
                                              tags = ADPQShell.data['testTags'], 
                                              attachments = ADPQShell.data['testAttachments'], 
                                              status = ADPQShell.data['testStatus'])
        
        # GetArticleIds() returns a list of all ids.
        articleIds = self.user.GetArticleIds()
 
        # If successful, list will not be empty.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_EditArticle assert#1 has failed.')
         
        # Now ensure that all data was successfully updated & saved.
        responseBody = self.user.get_articles_details(Authorization = self.user.GetAuthKey(), 
                                                      articleId = self.user.GetArticleIds())
          
        # Ensure all data persists.
        if articleIds != []:
            self.assertEqual(responseBody['data']['id'], articleIds[0],
                              msg='test_EditArticle assert#2 has failed.') 
         
        self.assertEqual(responseBody['data']['title'], ADPQShell.data['testTitle'],
                          msg='test_EditArticle assert#3 has failed.') 
         
        self.assertEqual(responseBody['data']['summary'], ADPQShell.data['testShortDesc'],
                          msg='test_EditArticle assert#4 has failed.') 
         
        self.assertEqual(responseBody['data']['description'], ADPQShell.data['testLongDesc'],
                          msg='test_EditArticle assert#5 has failed.') 
         
        self.assertEqual(responseBody['data']['status'], ADPQShell.data['testStatus'],
                          msg='test_EditArticle assert#6 has failed.') 
         
        self.assertEqual(responseBody['data']['tags'], [ADPQShell.data['testTags']],
                          msg='test_EditArticle assert#7 has failed.') 
        
        
        

    def test_CommentArticle(self):
        # Comment article.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])

        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_CommentArticle assert#1 has failed.')
        
        # Now ensure that the comment persists & is present. 
        responseBody = self.user.get_articles_details(Authorization = self.user.GetAuthKey(), 
                                                      articleId = self.user.GetArticleIds())
          
        self.assertEqual(responseBody['data']['comments'][0]['comment'], 
                         ADPQShell.data['testComment'], msg='test_Success assert#2 has failed.')
        
        
        
    def test_DeleteArticle(self):
        self.user.delete_article(Authorization = self.user.GetAuthKey(), 
                                 articleId = self.user.GetArticleIds())
    
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(SmokeTest('test_AdminDashboardSmokeTest'))
    suite.addTest(SmokeTest('test_DashBoard'))
    suite.addTest(SmokeTest('test_GetAgencies'))
    suite.addTest(SmokeTest('test_GetArticles'))
    suite.addTest(SmokeTest('test_GetTags'))
    suite.addTest(SmokeTest('test_Signin'))
    suite.addTest(SmokeTest('test_CreateArticle'))
    suite.addTest(SmokeTest('test_EditArticle'))
    suite.addTest(SmokeTest('test_CommentArticle'))
    suite.addTest(SmokeTest('test_DeleteArticle'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())