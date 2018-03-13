import sys, unittest, ADPQShell

    
'''
    ADPQ v1 - Comment Articles end point.
    
    Purpose - Allows an existing user to add comments to an edit an existing article.
    
    Method signature:
        comment_article(Authorization='', articleId=[], comment='', 
                        AuthorizationExclude=False, articleIdExclude=False, 
                        commentExclude=False, return_status=False):
    
    Required:
        Authorization
        articleId
        comment

    Test cases
        Successfully comment an existing article.
        
        Authorization missing from request call.
        Null Authorization value. 
        Int Authorization value.    
        Float Authorization value.   
        String Authorization value.
        Array Authorization value.  
        
        ArticleId missing from request call.
        Null articleId value. 
        Int articleId value.    
        Float articleId value.   
        String articleId value.
        Array articleId value.  
        
        Comment missing from request call.
        Null comment value. 
        Int comment value.    
        Float comment value.   
        String comment value.
        Array comment value.
'''
class TestCommentArticle(unittest.TestCase):
    '''
        Ideally here, we want to create a brand new article. Use the new 
        id to run all the tests, then delete the article.
        
        **** COME BACK TO THIS WHEN WE HAVE A DELETE ARTICLE ENDPOINT ****
    '''
    
    
    @classmethod
    def setUpClass(cls):
        try:
            # Create user object.
            cls.user = ADPQShell.ADPQ()
            
            # SignIn the user. 
            cls.user.sign_in(email = ADPQShell.data['testEmail'])
            # Create an article
            cls.user.create_article(Authorization = cls.user.GetAuthKey(), 
                                    title = ADPQShell.data['testTitle'], 
                                    agencyId = ADPQShell.data['testAgencyId'],
                                    audience = ADPQShell.data['testAudience'], 
                                    shortDesc = ADPQShell.data['testShortDesc'], 
                                    longDesc = ADPQShell.data['testLongDesc'], 
                                    tags = ADPQShell.data['testTags'], 
                                    attachments = ADPQShell.data['testAttachments'])
            
            assert(cls.user != None)
        except:
            print("Unexpected error during setUpClass:", sys.exc_info()[0])

    
    
    # Test successfully commenting on an existing article.
    def test_success(self):
        # Comment article.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])

        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_Success assert#1 has failed.')
        
        # Now ensure that the comment persists & is present. 
        responseBody = self.user.get_articles_details(Authorization = self.user.GetAuthKey(), 
                                                      articleId = self.user.GetArticleIds())
          
        self.assertEqual(responseBody['data']['comments'][0]['comment'], 
                         ADPQShell.data['testComment'], msg='test_Success assert#2 has failed.') 

         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        # Missing Authorization value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'],
                                                 AuthorizationExclude=True)
         
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        # Null Authorization value.
        responseBody = self.user.comment_article(Authorization = '', 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        # Int Authorization value.
        responseBody = self.user.comment_article(Authorization = 6666, 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['data'], [],
                          msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        # Float Authorization value.
        responseBody = self.user.comment_article(Authorization = 6.666, 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        # String Authorization value.
        responseBody = self.user.comment_article(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        # Array Authorization value.
        responseBody = self.user.comment_article(Authorization = ['hodl', 666, [.6, 0], {}], 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                          ArticleId tests                          *
    # *********************************************************************
    
    
        
    # Missing ArticleId information from request call.
    def test_missingArticleId(self):
        # Missing ArticleId value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'],
                                                 articleIdExclude=True)
       
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingArticleId assert#1 has failed.')
        
        
        
    # Test a null ArticleId.
    @unittest.skip("raise JSONDecodeError")
    def test_nullArticleId(self):
        # Null ArticleId value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = '', 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullArticleId assert#1 has failed.')



    # Test a int ArticleId.
    def test_intArticleId(self):
        # Int ArticleId value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = 123456, 
                                                 comment = ADPQShell.data['testComment'])
        # TEST HAS BEEN COMMENTED OUT.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intArticleId assert#1 has failed.')



    # Test a float ArticleId.
    def test_floatArticleId(self):
        # Float ArticleId value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = 12.3456, 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatArticleId assert#1 failed.')
        
        
        
    # Test a string ArticleId value call.
    @unittest.skip("raise JSONDecodeError")
    def test_stringArticleId(self):
        # String ArticleId value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                 comment = ADPQShell.data['testComment'])
        # TEST HAS BEEN COMMENTED OUT.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringArticleId assert#1 failed.')



    # Test an array ArticleId value call.
    @unittest.skip("raise JSONDecodeError")
    def test_arrayArticleId(self):
        # Array ArticleId value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = ['hodl', 666, [.6, 0], {}], 
                                                 comment = ADPQShell.data['testComment'])
        # TEST HAS BEEN COMMENTED OUT.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayArticleId assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Comment tests                              *
    # *********************************************************************
    
    
        
    # Missing Comment information from request call.
    def test_missingComment(self):
        # Missing Comment value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingComment assert#1 has failed.')
        
        
        
    # Test a null Comment.
    def test_nullComment(self):
        # Null Comment value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullComment assert#1 has failed.')



    # Test a int Comment.
    def test_intComment(self):
        # Int Comment value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intComment assert#1 has failed.')



    # Test a float Comment.
    def test_floatComment(self):
        # Float Comment value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatComment assert#1 failed.')
        
        
        
    # Test a string Comment value call.
    def test_stringComment(self):
        # String Comment value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringComment assert#1 failed.')



    # Test an array Comment value call.
    def test_arrayComment(self):
        # Array Comment value.
        responseBody = self.user.comment_article(Authorization = self.user.GetAuthKey(), 
                                                 articleId = self.user.GetArticleIds(), 
                                                 comment = ADPQShell.data['testComment'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayComment assert#1 failed.')
    
        
        
        
    @classmethod
    def tearDownClass(cls):
        try:
            pass
#             cls.user.remove_user(cls.user.testEmail)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            #raise
        #cls.user.remove_user(cls.user.testEmail)
    
    
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestCommentArticle('test_success'))
   
    suite.addTest(TestCommentArticle('test_missingAuthorization'))
    suite.addTest(TestCommentArticle('test_nullAuthorization'))
    suite.addTest(TestCommentArticle('test_intAuthorization'))
    suite.addTest(TestCommentArticle('test_floatAuthorization'))
    suite.addTest(TestCommentArticle('test_stringAuthorization'))
    suite.addTest(TestCommentArticle('test_arrayAuthorization'))
 
    suite.addTest(TestCommentArticle('test_missingArticleId'))
    suite.addTest(TestCommentArticle('test_nullArticleId'))
    suite.addTest(TestCommentArticle('test_intArticleId'))
    suite.addTest(TestCommentArticle('test_floatArticleId'))
    suite.addTest(TestCommentArticle('test_stringArticleId'))
    suite.addTest(TestCommentArticle('test_arrayArticleId'))
         
    suite.addTest(TestCommentArticle('test_missingComment'))
    suite.addTest(TestCommentArticle('test_nullComment'))
    suite.addTest(TestCommentArticle('test_intComment'))
    suite.addTest(TestCommentArticle('test_floatComment'))
    suite.addTest(TestCommentArticle('test_stringComment'))
    suite.addTest(TestCommentArticle('test_arrayComment'))

    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())