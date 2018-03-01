import sys, unittest, QaAdpqShell

'''
    ADPQ v1 - Create Articles end point.
    
    Purpose - Allows an existing user to create an article
    
    Method signature:
        create_article(Authorization='', title='', agencyId='', audience=0,
                       shortDesc='', longDesc='', tags='', attachments=[],
                       AuthorizationExclude=False, titleExclude=False,
                       agencyIdExclude=False, audienceExclude=False,
                       shortDescExclude=False, longDescExclude=False, 
                       tagsExclude=False, attachmentsExclude=False):
    
    Required:
        Authorization
        title
        agencyId
        audience
        shortDesc
        lognDesc
        tags
        attachments

    Test cases
        Successfully create an article.
        
        Authorization missing from request call.
        Null Authorization value. 
        Int Authorization value.    
        Float Authorization value.   
        String Authorization value.
        Array Authorization value.  
        
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
'''
class TestCreateArticles(unittest.TestCase):
    title = 'Department of funky beats'
    agencyId = '5a8b73f94212d1f20f847b9a'
    audience = 0
    shortDesc = 'short description here'
    longDesc = 'This is a longer description'
    tags = '5a8b55bca2d13ad4ba5369ef'
    attachments = ["url1"]
    
    @classmethod
    def setUpClass(cls):
        try:
            # Create user object.
            cls.user = QaAdpqShell.QaADPQShell()
            
            # SignIn the user. 
            cls.user.sign_in(email = QaAdpqShell.QaADPQShell.testEmail)
            
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            raise

    
    
    # Test successfully creating a new article.
    def test_success(self):
        # Create article.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        # GetArticleIds() returns a list of all ids.
        articleIds = self.user.GetArticleIds()
        
        # If successful, list will not be empty.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_Success assert#1 has failed.')
        
        
        # Now ensure that the article data was successfully created & saved.
        responseBody = self.user.get_articles_details(Authorization = self.user.GetAuthKey(), 
                                                      articleId = self.user.GetArticleIds())
         
        # Ensure all data persists.
        if articleIds != []:
            self.assertEqual(responseBody['data']['id'], articleIds[0],
                              msg='test_Success assert#2 has failed.') 
        
        self.assertEqual(responseBody['data']['title'], TestCreateArticles.title,
                          msg='test_Success assert#3 has failed.') 
        
        self.assertEqual(responseBody['data']['summary'], TestCreateArticles.shortDesc,
                          msg='test_Success assert#4 has failed.') 
        
        self.assertEqual(responseBody['data']['description'], TestCreateArticles.longDesc,
                          msg='test_Success assert#5 has failed.') 
        
        ## THIS IS HARD CODED CURRENTLY. WHEN THIS IS PATCHED, THIS TEST
        # WILL FAIL.
        self.assertEqual(responseBody['data']['tags'], ['Auto'],
                          msg='test_Success assert#6 has failed.') 
         
         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        # Missing Authorization value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(),
                                              AuthorizationExclude=True)
        
        # Currently passing. 
        self.assertEqual(responseBody['error'], 'User not permitted',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        # Null Authorization value.
        responseBody = self.user.create_article(Authorization = '')
        
        # Currently passing. 
        self.assertEqual(responseBody['error'], 'User not permitted',
                          msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    def test_intAuthorization(self):
        # Int Authorization value.
        responseBody = self.user.create_article(Authorization = 8523154687)
        
        # Currently passing. 
        self.assertEqual(responseBody['data'], [],
                          msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    def test_floatAuthorization(self):
        # Float Authorization value.
        responseBody = self.user.create_article(Authorization = -852315.4687)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        # String Authorization value.
        responseBody = self.user.create_article(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    def test_arrayAuthorization(self):
        # Array Authorization value.
        responseBody = self.user.create_article(Authorization = ['hodl', 666, [.6, 0], {}])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Title tests                                *
    # *********************************************************************
    
    
        
    # Missing Title information from request call.
    def test_missingTitle(self):
        # Missing Title value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments,
                                                titleExclude=True)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingTitle assert#1 has failed.')
        
        
        
    # Test a null Title.
    def test_nullTitle(self):
        # Null Title value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = '', 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullTitle assert#1 has failed.')



    # Test a int Title.
    def test_intTitle(self):
        # Int Title value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = 666, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intTitle assert#1 has failed.')



    # Test a float Title.
    def test_floatTitle(self):
        # Float Title value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = 6.66, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatTitle assert#1 failed.')
        
        
        
    # Test a string Title value call.
    def test_stringTitle(self):
        # String Title value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringTitle assert#1 failed.')



    # Test an array Title value call.
    def test_arrayTitle(self):
        # Array Title value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ['hodl', 666, [.6, 0], {}], 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayTitle assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        AgencyId tests                             *
    # *********************************************************************
    
    
        
    # Missing AgencyId information from request call.
    def test_missingAgencyId(self):
        # Missing AgencyId value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments,
                                                agencyIdExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAgencyId assert#1 has failed.')
        
        
        
    # Test a null AgencyId.
    def test_nullAgencyId(self):
        # Null AgencyId value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = '',
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAgencyId assert#1 has failed.')



    # Test a int AgencyId.
    def test_intAgencyId(self):
        # Int AgencyId value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = 666,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAgencyId assert#1 has failed.')



    # Test a float AgencyId.
    def test_floatAgencyId(self):
        # Float AgencyId value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = -.369,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAgencyId assert#1 failed.')
        
        
        
    # Test a string AgencyId value call.
    def test_stringAgencyId(self):
        # String AgencyId value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = "';:.>,</?]}[{!@#$%^&*()-_=+|\"",
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringAgencyId assert#1 failed.')



    # Test an array AgencyId value call.
    def test_arrayAgencyId(self):
        # Array AgencyId value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = ['hodl', 666, [.6, 0], {}],
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayAgencyId assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Audience tests                             *
    # *********************************************************************
    
    
        
    # Missing Audience information from request call.
    def test_missingAudience(self):
        # Missing Audience value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments,
                                                audienceExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAudience assert#1 has failed.')
        
        
        
    # Test a null Audience.
    def test_nullAudience(self):
        # Null Audience value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = '', 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAudience assert#1 has failed.')



    # Test a int Audience.
    def test_intAudience(self):
        # Int Audience value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = 666, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAudience assert#1 has failed.')



    # Test a float Audience.
    def test_floatAudience(self):
        # Float Audience value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = .281354, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAudience assert#1 failed.')
        
        
        
    # Test a string Audience value call.
    def test_stringAudience(self):
        # String Audience value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertIn('error', responseBody.keys(), msg='test_stringAudience assert#1 failed.')



    # Test an array Audience value call.
    def test_arrayAudience(self):
        # Array Audience value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = ['hodl', 666, [.6, 0], {}], 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertIn('error', responseBody.keys(), msg='test_arrayAudience assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        ShortDesc tests                            *
    # *********************************************************************
    
    
        
    # Missing ShortDesc information from request call.
    def test_missingShortDesc(self):
        # Missing ShortDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments,
                                                shortDescExclude=True)
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingShortDesc assert#1 has failed.')
        
        
        
    # Test a null ShortDesc.
    def test_nullShortDesc(self):
        # Null ShortDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = '', 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullShortDesc assert#1 has failed.')



    # Test a int ShortDesc.
    def test_intShortDesc(self):
        # Int ShortDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = 666, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intShortDesc assert#1 has failed.')



    # Test a float ShortDesc.
    def test_floatShortDesc(self):
        # Float ShortDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = -3.3, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatShortDesc assert#1 failed.')
        
        
        
    # Test a string ShortDesc value call.
    def test_stringShortDesc(self):
        # String ShortDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringShortDesc assert#1 failed.')



    # Test an array ShortDesc value call.
    def test_arrayShortDesc(self):
        # Array ShortDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = ['hodl', 666, [.6, 0], {}], 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayShortDesc assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        LongDesc tests                             *
    # *********************************************************************
    
    
        
    # Missing LongDesc information from request call.
    def test_missingLongDesc(self):
        # Missing LongDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments,
                                                longDescExclude=True)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingLongDesc assert#1 has failed.')
        
        
        
    # Test a null LongDesc.
    def test_nullLongDesc(self):
        # Null LongDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = '', 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullLongDesc assert#1 has failed.')



    # Test a int LongDesc.
    def test_intLongDesc(self):
        # Int LongDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = 123, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intLongDesc assert#1 has failed.')



    # Test a float LongDesc.
    def test_floatLongDesc(self):
        # Float LongDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = 32.1, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatLongDesc assert#1 failed.')
        
        
        
    # Test a string LongDesc value call.
    def test_stringLongDesc(self):
        # String LongDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringLongDesc assert#1 failed.')



    # Test an array LongDesc value call.
    def test_arrayLongDesc(self):
        # Array LongDesc value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = ['hodl', 666, [.6, 0], {}], 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayLongDesc assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                           Tags tests                              *
    # *********************************************************************
    
    
        
    # Missing Tags information from request call.
    def test_missingTags(self):
        # Missing Tags value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments,
                                                tagsExclude=True)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingTags assert#1 has failed.')
        
        
        
    # Test a null Tags.
    def test_nullTags(self):
        # Null Tags value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = '', 
                                                attachments = TestCreateArticles.attachments)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullTags assert#1 has failed.')



    # Test a int Tags.
    def test_intTags(self):
        # Int Tags value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = 666, 
                                                attachments = TestCreateArticles.attachments)
        
        # Currently passing. 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intTags assert#1 has failed.')



    # Test a float Tags.
    def test_floatTags(self):
        # Float Tags value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = .3, 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatTags assert#1 failed.')
        
        
        
    # Test a string Tags value call.
    def test_stringTags(self):
        # String Tags value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringTags assert#1 failed.')



    # Test an array Tags value call.
    def test_arrayTags(self):
        # Array Tags value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = ['hodl', 666, [.6, 0], {}], 
                                                attachments = TestCreateArticles.attachments)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayTags assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Attachments tests                          *
    # *********************************************************************
    
    
        
    # Missing Attachments information from request call.
    def test_missingAttachments(self):
        # Missing Attachments value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = TestCreateArticles.attachments,
                                                attachmentsExclude=True)
 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAttachments assert#1 has failed.')
        
        
        
    # Test a null Attachments.
    def test_nullAttachments(self):
        # Null Attachments value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = '')
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAttachments assert#1 has failed.')



    # Test a int Attachments.
    def test_intAttachments(self):
        # Int Attachments value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = 1)
 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAttachments assert#1 has failed.')



    # Test a float Attachments.
    def test_floatAttachments(self):
        # Float Attachments value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = 1.1)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAttachments assert#1 failed.')
        
        
        
    # Test a string Attachments value call.
    def test_stringAttachments(self):
        # String Attachments value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringAttachments assert#1 failed.')



    # Test an array Attachments value call.
    def test_arrayAttachments(self):
        # Array Attachments value.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = TestCreateArticles.title, 
                                                agencyId = TestCreateArticles.agencyId,
                                                audience = TestCreateArticles.audience, 
                                                shortDesc = TestCreateArticles.shortDesc, 
                                                longDesc = TestCreateArticles.longDesc, 
                                                tags = TestCreateArticles.tags, 
                                                attachments = ['hodl', 666, [.6, 0], {}])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayAttachments assert#1 failed.')
        
        
        
        
        
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
    
    suite.addTest(TestCreateArticles('test_success'))
  
    suite.addTest(TestCreateArticles('test_missingAuthorization'))
    suite.addTest(TestCreateArticles('test_nullAuthorization'))
#     suite.addTest(TestCreateArticles('test_intAuthorization'))
#     suite.addTest(TestCreateArticles('test_floatAuthorization'))
    suite.addTest(TestCreateArticles('test_stringAuthorization'))
#     suite.addTest(TestCreateArticles('test_arrayAuthorization'))
       
    suite.addTest(TestCreateArticles('test_missingTitle'))
    suite.addTest(TestCreateArticles('test_nullTitle'))
    suite.addTest(TestCreateArticles('test_intTitle'))
    suite.addTest(TestCreateArticles('test_floatTitle'))
    suite.addTest(TestCreateArticles('test_stringTitle'))
    suite.addTest(TestCreateArticles('test_arrayTitle'))
      
#     suite.addTest(TestCreateArticles('test_missingAgencyId'))
# #     suite.addTest(TestCreateArticles('test_nullAgencyId'))
#     suite.addTest(TestCreateArticles('test_intAgencyId'))
#     suite.addTest(TestCreateArticles('test_floatAgencyId'))
# #     suite.addTest(TestCreateArticles('test_stringAgencyId'))
# #     suite.addTest(TestCreateArticles('test_arrayAgencyId'))
      
#     suite.addTest(TestCreateArticles('test_missingAudience'))
#     suite.addTest(TestCreateArticles('test_nullAudience'))
#     suite.addTest(TestCreateArticles('test_intAudience'))
#     suite.addTest(TestCreateArticles('test_floatAudience'))
#     suite.addTest(TestCreateArticles('test_stringAudience'))
#     suite.addTest(TestCreateArticles('test_arrayAudience'))
      
    suite.addTest(TestCreateArticles('test_missingShortDesc'))
    suite.addTest(TestCreateArticles('test_nullShortDesc'))
    suite.addTest(TestCreateArticles('test_intShortDesc'))
    suite.addTest(TestCreateArticles('test_floatShortDesc'))
    suite.addTest(TestCreateArticles('test_stringShortDesc'))
    suite.addTest(TestCreateArticles('test_arrayShortDesc'))
      
    suite.addTest(TestCreateArticles('test_missingLongDesc'))
    suite.addTest(TestCreateArticles('test_nullLongDesc'))
    suite.addTest(TestCreateArticles('test_intLongDesc'))
    suite.addTest(TestCreateArticles('test_floatLongDesc'))
    suite.addTest(TestCreateArticles('test_stringLongDesc'))
    suite.addTest(TestCreateArticles('test_arrayLongDesc'))
      
    suite.addTest(TestCreateArticles('test_missingTags'))
    suite.addTest(TestCreateArticles('test_nullTags'))
    suite.addTest(TestCreateArticles('test_intTags'))
    suite.addTest(TestCreateArticles('test_floatTags'))
#     suite.addTest(TestCreateArticles('test_stringTags'))
#     suite.addTest(TestCreateArticles('test_arrayTags'))
     
    suite.addTest(TestCreateArticles('test_missingAttachments'))
    suite.addTest(TestCreateArticles('test_nullAttachments'))
    suite.addTest(TestCreateArticles('test_intAttachments'))
    suite.addTest(TestCreateArticles('test_floatAttachments'))
#     suite.addTest(TestCreateArticles('test_stringAttachments'))
    suite.addTest(TestCreateArticles('test_arrayAttachments'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())