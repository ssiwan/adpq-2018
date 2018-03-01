import sys, unittest, QaAdpqShell

'''
    ADPQ v1 - Edit Articles end point.
    
    Purpose - Allows an existing user to edit an existing article.
    
    Method signature:
        edit_article(Authorization='', articleId=[], title='', agencyId='', audience=0,
                     shortDesc='', longDesc='', tags='', attachments=[], status=0,
                     AuthorizationExclude=False, articleIdExclude=False, titleExclude=False,
                     agencyIdExclude=False, audienceExclude=False,
                     shortDescExclude=False, longDescExclude=False, 
                     tagsExclude=False, attachmentsExclude=False, statusExclude=False):
    
    Required:
        Authorization
        articleId
        title
        agencyId
        audience
        shortDesc
        lognDesc
        tags
        attachments
        status

    Test cases
        Successfully edit an existing article.
        
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
        
        Title missing from request call.
        Null title value. 
        Int title value.    
        Float title value.   
        String title value.
        Array title value.
        
        AgencyId missing from request call.
        Null agencyId value. 
        Int agencyId value.    
        Float agencyId value.   
        String agencyId value.
        Array agencyId value.
        
        Audience missing from request call.
        Null audience value. 
        Int audience value.    
        Float audience value.   
        String audience value.
        Array audience value.
        
        ShortDesc missing from request call.
        Null shortDesc value. 
        Int shortDesc value.    
        Float shortDesc value.   
        String shortDesc value.
        Array shortDesc value.
        
        LongDesc missing from request call.
        Null longDesc value. 
        Int longDesc value.    
        Float longDesc value.   
        String longDesc value.
        Array longDesc value.
        
        Tags missing from request call.
        Null tags value. 
        Int tags value.    
        Float tags value.   
        String tags value.
        Array tags value.
        
        Attachments missing from request call.
        Null attachments value. 
        Int attachments value.    
        Float attachments value.   
        String attachments value.
        Array attachments value.
        
        Status missing from request call.
        Null status value. 
        Int status value.    
        Float status value.   
        String status value.
        Array status value.
'''
class TestEditArticle(unittest.TestCase):
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
            # Create user object.
            cls.user = QaAdpqShell.QaADPQShell()
            
            # SignIn the user. 
            cls.user.sign_in(email = QaAdpqShell.QaADPQShell.testEmail)
            # Create an article
            cls.user.create_article(Authorization = cls.user.GetAuthKey(), 
                                    title = TestEditArticle.title, 
                                    agencyId = TestEditArticle.agencyId,
                                    audience = TestEditArticle.audience, 
                                    shortDesc = TestEditArticle.shortDesc, 
                                    longDesc = TestEditArticle.longDesc, 
                                    tags = TestEditArticle.tags, 
                                    attachments = TestEditArticle.attachments)
            
            assert(cls.user != None)
        except:
            print("Unexpected error during setUpClass:", sys.exc_info()[0])
            raise

    
    
    # Test successfully editing an existing article.
    def test_success(self):
        # Edit article.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        # GetArticleIds() returns a list of all ids.
        articleIds = self.user.GetArticleIds()

        # If successful, list will not be empty.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_Success assert#1 has failed.')
        
        # Now ensure that all data was successfully updated & saved.
        responseBody = self.user.get_articles_details(Authorization = self.user.GetAuthKey(), 
                                                      articleId = self.user.GetArticleIds())
         
        # Ensure all data persists.
        if articleIds != []:
            self.assertEqual(responseBody['data']['id'], articleIds[0],
                              msg='test_Success assert#2 has failed.') 
        
        self.assertEqual(responseBody['data']['title'], TestEditArticle.title,
                          msg='test_Success assert#3 has failed.') 
        
        self.assertEqual(responseBody['data']['summary'], TestEditArticle.shortDesc,
                          msg='test_Success assert#4 has failed.') 
        
        self.assertEqual(responseBody['data']['description'], TestEditArticle.longDesc,
                          msg='test_Success assert#5 has failed.') 
        
        self.assertEqual(responseBody['data']['status'], TestEditArticle.status,
                          msg='test_Success assert#6 has failed.') 
        
        ## THIS IS HARD CODED CURRENTLY. WHEN THIS IS PATCHED, THIS TEST
        # WILL FAIL.
        self.assertEqual(responseBody['data']['tags'], ['Auto'],
                          msg='test_Success assert#7 has failed.') 
         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        # Missing Authorization value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              AuthorizationExclude=True)
         
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        # Null Authorization value.
        responseBody = self.user.edit_article(Authorization = '', 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    def test_intAuthorization(self):
        # Int Authorization value.
        responseBody = self.user.edit_article(Authorization = 1, 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['data'], [],
                          msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    def test_floatAuthorization(self):
        # Float Authorization value.
        responseBody = self.user.edit_article(Authorization = 1.1, 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        # String Authorization value.
        responseBody = self.user.edit_article(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    def test_arrayAuthorization(self):
        # Array Authorization value.
        responseBody = self.user.edit_article(Authorization = ['hodl', 666, [.6, 0], {}], 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                          ArticleId tests                          *
    # *********************************************************************
    
    
        
    # Missing ArticleId information from request call.
    def test_missingArticleId(self):
        # Missing ArticleId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              articleIdExclude=True)
       
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingArticleId assert#1 has failed.')
        
        
        
    # Test a null ArticleId.
    def test_nullArticleId(self):
        # Null ArticleId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = '', 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullArticleId assert#1 has failed.')



    # Test a int ArticleId.
    def test_intArticleId(self):
        # Int ArticleId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = 123456789, 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        # TEST HAS BEEN COMMENTED OUT.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intArticleId assert#1 has failed.')



    # Test a float ArticleId.
    def test_floatArticleId(self):
        # Float ArticleId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = 12345.6789, 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatArticleId assert#1 failed.')
        
        
        
    # Test a string ArticleId value call.
    def test_stringArticleId(self):
        # String ArticleId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        # TEST HAS BEEN COMMENTED OUT.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringArticleId assert#1 failed.')



    # Test an array ArticleId value call.
    def test_arrayArticleId(self):
        # Array ArticleId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = ['hodl', 666, [.6, 0], {}], 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        # TEST HAS BEEN COMMENTED OUT.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayArticleId assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Title tests                                *
    # *********************************************************************
    
    
        
    # Missing Title information from request call.
    def test_missingTitle(self):
        # Missing Title value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              titleExclude=True)
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingTitle assert#1 has failed.')
        
        
        
    # Test a null Title.
    def test_nullTitle(self):
        # Null Title value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = '',
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullTitle assert#1 has failed.')



    # Test a int Title.
    def test_intTitle(self):
        # Int Title value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = 123456798,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intTitle assert#1 has failed.')



    # Test a float Title.
    def test_floatTitle(self):
        # Float Title value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = 1.23456798,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatTitle assert#1 failed.')
        
        
        
    # Test a string Title value call.
    def test_stringTitle(self):
        # String Title value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = "';:.>,</?]}[{!@#$%^&*()-_=+|\"",
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringTitle assert#1 failed.')



    # Test an array Title value call.
    def test_arrayTitle(self):
        # Array Title value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = ['hodl', 666, [.6, 0], {}],
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayTitle assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        AgencyId tests                             *
    # *********************************************************************
    
    
        
    # Missing AgencyId information from request call.
    def test_missingAgencyId(self):
        # Missing AgencyId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              agencyIdExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAgencyId assert#1 has failed.')
        
        
        
    # Test a null AgencyId.
    def test_nullAgencyId(self):
        # Null AgencyId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = '', 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAgencyId assert#1 has failed.')



    # Test a int AgencyId.
    def test_intAgencyId(self):
        # Int AgencyId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = 963852741, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAgencyId assert#1 has failed.')



    # Test a float AgencyId.
    def test_floatAgencyId(self):
        # Float AgencyId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = -63852.741, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAgencyId assert#1 failed.')
        
        
        
    # Test a string AgencyId value call.
    def test_stringAgencyId(self):
        # String AgencyId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringAgencyId assert#1 failed.')



    # Test an array AgencyId value call.
    def test_arrayAgencyId(self):
        # Array AgencyId value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = ['hodl', 666, [.6, 0], {}], 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayAgencyId assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Audience tests                             *
    # *********************************************************************
    
    
        
    # Missing Audience information from request call.
    def test_missingAudience(self):
        # Missing Audience value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              audienceExclude=False)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAudience assert#1 has failed.')
        
        
        
    # Test a null Audience.
    def test_nullAudience(self):
        # Null Audience value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = '', 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAudience assert#1 has failed.')



    # Test a int Audience.
    def test_intAudience(self):
        # Int Audience value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = 123456789, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAudience assert#1 has failed.')



    # Test a float Audience.
    def test_floatAudience(self):
        # Float Audience value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = 123456.789, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAudience assert#1 failed.')
        
        
        
    # Test a string Audience value call.
    def test_stringAudience(self):
        # String Audience value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertIn('error', responseBody.keys(), msg='test_stringAudience assert#1 failed.')



    # Test an array Audience value call.
    def test_arrayAudience(self):
        # Array Audience value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = ['hodl', 666, [.6, 0], {}], 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertIn('error', responseBody.keys(), msg='test_arrayAudience assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        ShortDesc tests                            *
    # *********************************************************************
    
    
        
    # Missing ShortDesc information from request call.
    def test_missingShortDesc(self):
        # Missing ShortDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              shortDescExclude=True)
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingShortDesc assert#1 has failed.')
        
        
        
    # Test a null ShortDesc.
    def test_nullShortDesc(self):
        # Null ShortDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = '', 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullShortDesc assert#1 has failed.')



    # Test a int ShortDesc.
    def test_intShortDesc(self):
        # Int ShortDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = 666666666666, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intShortDesc assert#1 has failed.')



    # Test a float ShortDesc.
    def test_floatShortDesc(self):
        # Float ShortDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = 66666666666.6, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatShortDesc assert#1 failed.')
        
        
        
    # Test a string ShortDesc value call.
    def test_stringShortDesc(self):
        # String ShortDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringShortDesc assert#1 failed.')



    # Test an array ShortDesc value call.
    def test_arrayShortDesc(self):
        # Array ShortDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = ['hodl', 666, [.6, 0], {}], 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayShortDesc assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        LongDesc tests                             *
    # *********************************************************************
    
    
        
    # Missing LongDesc information from request call.
    def test_missingLongDesc(self):
        # Missing LongDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              longDescExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingLongDesc assert#1 has failed.')
        
        
        
    # Test a null LongDesc.
    def test_nullLongDesc(self):
        # Null LongDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = '', 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullLongDesc assert#1 has failed.')



    # Test a int LongDesc.
    def test_intLongDesc(self):
        # Int LongDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = 321456987, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intLongDesc assert#1 has failed.')



    # Test a float LongDesc.
    def test_floatLongDesc(self):
        # Float LongDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = 32145698.7, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatLongDesc assert#1 failed.')
        
        
        
    # Test a string LongDesc value call.
    def test_stringLongDesc(self):
        # String LongDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringLongDesc assert#1 failed.')



    # Test an array LongDesc value call.
    def test_arrayLongDesc(self):
        # Array LongDesc value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = ['hodl', 666, [.6, 0], {}], 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayLongDesc assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                           Tags tests                              *
    # *********************************************************************
    
    
        
    # Missing Tags information from request call.
    def test_missingTags(self):
        # Missing Tags value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              tagsExclude=True)

        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingTags assert#1 has failed.')
        
        
        
    # Test a null Tags.
    def test_nullTags(self):
        # Null Tags value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = '', 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)

        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullTags assert#1 has failed.')



    # Test a int Tags.
    def test_intTags(self):
        # Int Tags value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = 123456852, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)

        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intTags assert#1 has failed.')



    # Test a float Tags.
    def test_floatTags(self):
        # Float Tags value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = 12345.6852, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatTags assert#1 failed.')
        
        
        
    # Test a string Tags value call.
    def test_stringTags(self):
        # String Tags value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringTags assert#1 failed.')



    # Test an array Tags value call.
    def test_arrayTags(self):
        # Array Tags value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = ['hodl', 666, [.6, 0], {}], 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayTags assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Attachments tests                          *
    # *********************************************************************
    
    
        
    # Missing Attachments information from request call.
    def test_missingAttachments(self):
        # Missing Attachments value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              attachmentsExclude=True)
 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAttachments assert#1 has failed.')
        
        
        
    # Test a null Attachments.
    def test_nullAttachments(self):
        # Null Attachments value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = '', 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAttachments assert#1 has failed.')



    # Test a int Attachments.
    def test_intAttachments(self):
        # Int Attachments value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = 666, 
                                              status = TestEditArticle.status)
 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAttachments assert#1 has failed.')



    # Test a float Attachments.
    def test_floatAttachments(self):
        # Float Attachments value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = 66.6, 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAttachments assert#1 failed.')
        
        
        
    # Test a string Attachments value call.
    def test_stringAttachments(self):
        # String Attachments value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['error'], "TypeError: articleObj.attachments.forEach is not a function",
                          msg='test_stringAttachments assert#1 failed.')



    # Test an array Attachments value call.
    def test_arrayAttachments(self):
        # Array Attachments value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = ['hodl', 666, [.6, 0], {}], 
                                              status = TestEditArticle.status)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayAttachments assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                            Status tests                           *
    # *********************************************************************
    
    
        
    # Missing Status information from request call.
    def test_missingStatus(self):
        # Missing Status value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = TestEditArticle.status,
                                              statusExclude=True)
 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingStatus assert#1 has failed.')
        
        
        
    # Test a null Status.
    def test_nullStatus(self):
        # Null Status value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = '')
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullStatus assert#1 has failed.')



    # Test a int Status.
    def test_intStatus(self):
        # Int Status value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = 666)
 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intStatus assert#1 has failed.')



    # Test a float Status.
    def test_floatStatus(self):
        # Float Status value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = -.666)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatStatus assert#1 failed.')
        
        
        
    # Test a string Status value call.
    def test_stringStatus(self):
        # String Status value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['status'], 'saved!',
                          msg='test_stringStatus assert#1 failed.')



    # Test an array Status value call.
    def test_arrayStatus(self):
        # Array Status value.
        responseBody = self.user.edit_article(Authorization = self.user.GetAuthKey(), 
                                              articleId = self.user.GetArticleIds(), 
                                              title = TestEditArticle.title,
                                              agencyId = TestEditArticle.agencyId, 
                                              audience = TestEditArticle.audience, 
                                              shortDesc = TestEditArticle.shortDesc, 
                                              longDesc = TestEditArticle.longDesc, 
                                              tags = TestEditArticle.tags, 
                                              attachments = TestEditArticle.attachments, 
                                              status = ['hodl', 666, [.6, 0], {}])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayStatus assert#1 failed.')
        
        
        
        
        
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
    
    suite.addTest(TestEditArticle('test_success'))
  
    suite.addTest(TestEditArticle('test_missingAuthorization'))
    suite.addTest(TestEditArticle('test_nullAuthorization'))
#     suite.addTest(TestEditArticle('test_intAuthorization'))
#     suite.addTest(TestEditArticle('test_floatAuthorization'))
    suite.addTest(TestEditArticle('test_stringAuthorization'))
#     suite.addTest(TestEditArticle('test_arrayAuthorization'))

    suite.addTest(TestEditArticle('test_missingArticleId'))
#     suite.addTest(TestEditArticle('test_nullArticleId'))
    suite.addTest(TestEditArticle('test_intArticleId'))
    suite.addTest(TestEditArticle('test_floatArticleId'))
#     suite.addTest(TestEditArticle('test_stringArticleId'))
#     suite.addTest(TestEditArticle('test_arrayArticleId'))
        
    suite.addTest(TestEditArticle('test_missingTitle'))
    suite.addTest(TestEditArticle('test_nullTitle'))
    suite.addTest(TestEditArticle('test_intTitle'))
    suite.addTest(TestEditArticle('test_floatTitle'))
    suite.addTest(TestEditArticle('test_stringTitle'))
    suite.addTest(TestEditArticle('test_arrayTitle'))
        
#     suite.addTest(TestEditArticle('test_missingAgencyId'))
#     suite.addTest(TestEditArticle('test_nullAgencyId'))
#     suite.addTest(TestEditArticle('test_intAgencyId'))
#     suite.addTest(TestEditArticle('test_floatAgencyId'))
#     suite.addTest(TestEditArticle('test_stringAgencyId'))
#     suite.addTest(TestEditArticle('test_arrayAgencyId'))
#        
#     suite.addTest(TestEditArticle('test_missingAudience'))
#     suite.addTest(TestEditArticle('test_nullAudience'))
#     suite.addTest(TestEditArticle('test_intAudience'))
#     suite.addTest(TestEditArticle('test_floatAudience'))
#     suite.addTest(TestEditArticle('test_stringAudience'))
#     suite.addTest(TestEditArticle('test_arrayAudience'))
       
    suite.addTest(TestEditArticle('test_missingShortDesc'))
    suite.addTest(TestEditArticle('test_nullShortDesc'))
    suite.addTest(TestEditArticle('test_intShortDesc'))
    suite.addTest(TestEditArticle('test_floatShortDesc'))
    suite.addTest(TestEditArticle('test_stringShortDesc'))
    suite.addTest(TestEditArticle('test_arrayShortDesc'))
       
    suite.addTest(TestEditArticle('test_missingLongDesc'))
    suite.addTest(TestEditArticle('test_nullLongDesc'))
    suite.addTest(TestEditArticle('test_intLongDesc'))
    suite.addTest(TestEditArticle('test_floatLongDesc'))
    suite.addTest(TestEditArticle('test_stringLongDesc'))
    suite.addTest(TestEditArticle('test_arrayLongDesc'))
       
    suite.addTest(TestEditArticle('test_missingTags'))
    suite.addTest(TestEditArticle('test_nullTags'))
    suite.addTest(TestEditArticle('test_intTags'))
    suite.addTest(TestEditArticle('test_floatTags'))
    suite.addTest(TestEditArticle('test_stringTags'))
    suite.addTest(TestEditArticle('test_arrayTags'))
      
    suite.addTest(TestEditArticle('test_missingAttachments'))
    suite.addTest(TestEditArticle('test_nullAttachments'))
    suite.addTest(TestEditArticle('test_intAttachments'))
    suite.addTest(TestEditArticle('test_floatAttachments'))
    suite.addTest(TestEditArticle('test_stringAttachments'))
    suite.addTest(TestEditArticle('test_arrayAttachments'))

    suite.addTest(TestEditArticle('test_missingStatus'))
    suite.addTest(TestEditArticle('test_nullStatus'))
    suite.addTest(TestEditArticle('test_intStatus'))
    suite.addTest(TestEditArticle('test_floatStatus'))
    suite.addTest(TestEditArticle('test_stringStatus'))
    suite.addTest(TestEditArticle('test_arrayStatus'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())