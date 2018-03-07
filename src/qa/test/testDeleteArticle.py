import sys, unittest, ADPQShell

'''
    ADPQ v1 Delete Article end point.
    
    Purpose - Will delete an article. ArticleId is appended to the end of
              the url end point.
    
    Method signature:
        delete_article(Authorization='', articleId=[],
                       AuthorizationExclude=False,  articleIdExclude=False,
                       return_status=False):
        
    Required:
        Authorization
        Appended articleId to the end point.

    Test cases
        Successfully delete an article.
        Attempt to delete a non-existant article.
        Attempt to delete with users that did not create the article & have lower roles.
        
        ApiKey missing from request call.
        Null ApiKey value. 
        Int ApiKey value.    
        Float ApiKey value.  
        String ApiKey value.
        Array ApiKey value. 
'''
class TestDeleteArticle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.user = ADPQShell.ADPQ()
            cls.user.sign_in(email = ADPQShell.data['testEmail']) # Role 2.
            cls.user.create_article(Authorization = cls.user.GetAuthKey(), 
                                    title = ADPQShell.data['testTitle'], 
                                    agencyId = ADPQShell.data['testAgencyId'],
                                    audience = ADPQShell.data['testAudience'], 
                                    shortDesc = ADPQShell.data['testShortDesc'], 
                                    longDesc = ADPQShell.data['testLongDesc'], 
                                    tags = ADPQShell.data['testTags'], 
                                    attachments = ADPQShell.data['testAttachments'])
            
            cls.role1 = ADPQShell.ADPQ()
            cls.role1.sign_in(email = 'pmccartney@hotbsoftware.com') # Role 1.
            
            cls.role0 = ADPQShell.ADPQ()
            cls.role0.sign_in(email = 'jlennon@hotbsoftware.com')    # Role 0.
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])

    
    
    # Test successfully deleting an article.
    def test_success(self):
        responseBody = self.user.delete_article(Authorization = self.user.GetAuthKey(), 
                                                articleId = self.user.GetArticleIds())
        
        self.assertEqual(responseBody['data'], "article removed!",
                          msg='test_Success assert#1 has failed.')
        
        
    
    # Test  deleting an article that does not exist.
    def test_doesNotExist(self):
        responseBody = self.user.delete_article(Authorization = self.user.GetAuthKey(), 
                                                articleId = self.user.GetArticleIds())
        
        self.assertEqual(responseBody['error'], "article not found",
                          msg='test_doesNotExist assert#1 has failed.')
        
        
        
    # Test attempting to delete with an invalid role.
    def test_UserRoleInvalid(self):
        self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                title = ADPQShell.data['testTitle'], 
                                agencyId = ADPQShell.data['testAgencyId'],
                                audience = ADPQShell.data['testAudience'], 
                                shortDesc = ADPQShell.data['testShortDesc'], 
                                longDesc = ADPQShell.data['testLongDesc'], 
                                tags = ADPQShell.data['testTags'], 
                                attachments = ADPQShell.data['testAttachments'])
        
        responseBody = self.role1.delete_article(Authorization = self.role1.GetAuthKey(), 
                                                 articleId = self.role1.GetArticleIds())
        
        self.assertEqual(responseBody['error'], "article not found",
                          msg='test_UserRoleInvalid assert#1 has failed.')
        
        
        responseBody = self.role0.delete_article(Authorization = self.role0.GetAuthKey(), 
                                                 articleId = self.role0.GetArticleIds())
        
        self.assertEqual(responseBody['error'], "article not found",
                          msg='test_UserRoleInvalid assert#2 has failed.')
        
        self.user.delete_article(Authorization = self.user.GetAuthKey(), 
                                articleId = self.user.GetArticleIds())
        
        
        
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        responseBody = self.user.delete_article(Authorization = self.user.GetAuthKey(), 
                                                articleId = self.user.GetArticleIds(),
                                                AuthorizationExclude=True)
        
        self.assertEqual(responseBody['error'], 'Role not allowed',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        responseBody = self.user.delete_article(Authorization = '', 
                                                articleId = self.user.GetArticleIds())
        
        self.assertEqual(responseBody['error'], 'Role not allowed',
                         msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        responseBody = self.user.delete_article(Authorization = 123456789, 
                                                articleId = self.user.GetArticleIds())
        
        self.assertEqual(responseBody['data'], [], msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        responseBody = self.user.delete_article(Authorization = 12.3456789, 
                                                articleId = self.user.GetArticleIds())
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        responseBody = self.user.delete_article(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                articleId = self.user.GetArticleIds())
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        responseBody = self.user.delete_article(Authorization = ['hodl', 666, [.6, 0], {}], 
                                                articleId = self.user.GetArticleIds())
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
        
        
        
        
    @classmethod
    def tearDownClass(cls):
        try:
            pass
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
        
        
        

    
    
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestDeleteArticle('test_success'))
    suite.addTest(TestDeleteArticle('test_doesNotExist'))
    suite.addTest(TestDeleteArticle('test_UserRoleInvalid'))
    
    suite.addTest(TestDeleteArticle('test_missingAuthorization'))
    suite.addTest(TestDeleteArticle('test_nullAuthorization'))
    suite.addTest(TestDeleteArticle('test_intAuthorization'))
    suite.addTest(TestDeleteArticle('test_floatAuthorization'))
    suite.addTest(TestDeleteArticle('test_stringAuthorization'))
    suite.addTest(TestDeleteArticle('test_arrayAuthorization'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())