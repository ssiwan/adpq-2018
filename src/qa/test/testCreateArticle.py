import sys, unittest, ADPQShell

'''
    ADPQ v1 - Create Articles end point.
    
    Purpose - Allows an existing user to create an article
    
    Method signature:
        create_article(Authorization='', title='', agencyId='', audience=0,
                       shortDesc='', longDesc='', tags='', attachments=[],
                       AuthorizationExclude=False, titleExclude=False,
                       agencyIdExclude=False, audienceExclude=False,
                       shortDescExclude=False, longDescExclude=False, 
                       tagsExclude=False, attachmentsExclude=False, 
                       return_status=False):
    
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
    @classmethod
    def setUpClass(cls):
        try:
            cls.user = ADPQShell.ADPQ()
            # Only role 1/staff can create articles. Sign in with role 1.
            cls.user.sign_in(email = ADPQShell.data['testEmailRole1'],
                             password = ADPQShell.data['testPassword'])
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            raise

    
    
    # Test successfully creating a new article.
    def test_success(self):
        # Create article.
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        # If successful, list will not be empty.
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_Success assert#1 has failed.')
        
        
        # Now ensure that the article data was successfully created & saved.
        responseBody = self.user.get_articles_details(Authorization = self.user.GetAuthKey(), 
                                                      articleId = self.user.GetArticleIds())
         
        # Ensure all data persists.
        self.assertEqual(responseBody['data']['title'], ADPQShell.data['testTitle'],
                          msg='test_Success assert#2 has failed.') 
        
        self.assertEqual(responseBody['data']['summary'], ADPQShell.data['testShortDesc'],
                          msg='test_Success assert#3 has failed.') 
        
        self.assertEqual(responseBody['data']['description'], ADPQShell.data['testLongDesc'],
                          msg='test_Success assert#4 has failed.') 
        
        self.assertEqual(responseBody['data']['tags'], [ADPQShell.data['testTags']],
                          msg='test_Success assert#5 has failed.') 
         
         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(),
                                                AuthorizationExclude=True)
        
        self.assertEqual(responseBody['error'], 'User not permitted',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        responseBody = self.user.create_article(Authorization = '')
        
        self.assertEqual(responseBody['error'], 'User not permitted',
                         msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        responseBody = self.user.create_article(Authorization = 8523154687)
        
        self.assertEqual(responseBody['data'], [], msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        responseBody = self.user.create_article(Authorization = -852315.4687)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        responseBody = self.user.create_article(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        responseBody = self.user.create_article(Authorization = ['hodl', 666, [.6, 0], {}])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Title tests                                *
    # *********************************************************************
    
    
        
    # Missing Title information from request call.
    def test_missingTitle(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'],
                                                titleExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingTitle assert#1 has failed.')
        
        
        
    # Test a null Title.
    def test_nullTitle(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = '', 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullTitle assert#1 has failed.')



    # Test a int Title.
    def test_intTitle(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = 666, 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intTitle assert#1 has failed.')



    # Test a float Title.
    def test_floatTitle(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = 6.66, 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatTitle assert#1 failed.')
        
        
        
    # Test a string Title value call.
    def test_stringTitle(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringTitle assert#1 failed.')



    # Test an array Title value call.
    def test_arrayTitle(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ['hodl', 666, [.6, 0], {}], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayTitle assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        AgencyId tests                             *
    # *********************************************************************
    
    
        
    # Missing AgencyId information from request call.
    def test_missingAgencyId(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'],
                                                agencyIdExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAgencyId assert#1 has failed.')
        
        
        
    # Test a null AgencyId.
    def test_nullAgencyId(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = '',
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAgencyId assert#1 has failed.')



    # Test a int AgencyId.
    def test_intAgencyId(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = 666,
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAgencyId assert#1 has failed.')



    # Test a float AgencyId.
    def test_floatAgencyId(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = -.369,
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAgencyId assert#1 failed.')
        
        
        
    # Test a string AgencyId value call.
    def test_stringAgencyId(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = "';:.>,</?]}[{!@#$%^&*()-_=+|\"",
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringAgencyId assert#1 failed.')



    # Test an array AgencyId value call.
    def test_arrayAgencyId(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ['hodl', 666, [.6, 0], {}],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayAgencyId assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Audience tests                             *
    # *********************************************************************
    
    
        
    # Missing Audience information from request call.
    def test_missingAudience(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'],
                                                audienceExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAudience assert#1 has failed.')
        
        
        
    # Test a null Audience.
    def test_nullAudience(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = '', 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAudience assert#1 has failed.')



    # Test a int Audience.
    def test_intAudience(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = 666, 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAudience assert#1 has failed.')



    # Test a float Audience.
    def test_floatAudience(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = .281354, 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAudience assert#1 failed.')
        
        
        
    # Test a string Audience value call.
    def test_stringAudience(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertIn('error', responseBody.keys(), msg='test_stringAudience assert#1 failed.')



    # Test an array Audience value call.
    def test_arrayAudience(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ['hodl', 666, [.6, 0], {}], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertIn('error', responseBody.keys(), msg='test_arrayAudience assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        ShortDesc tests                            *
    # *********************************************************************
    
    
        
    # Missing ShortDesc information from request call.
    def test_missingShortDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'],
                                                shortDescExclude=True)
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingShortDesc assert#1 has failed.')
        
        
        
    # Test a null ShortDesc.
    def test_nullShortDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = '', 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullShortDesc assert#1 has failed.')



    # Test a int ShortDesc.
    def test_intShortDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = 666, 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intShortDesc assert#1 has failed.')



    # Test a float ShortDesc.
    def test_floatShortDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = -3.3, 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatShortDesc assert#1 failed.')
        
        
        
    # Test a string ShortDesc value call.
    def test_stringShortDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringShortDesc assert#1 failed.')



    # Test an array ShortDesc value call.
    def test_arrayShortDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ['hodl', 666, [.6, 0], {}], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayShortDesc assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        LongDesc tests                             *
    # *********************************************************************
    
    
        
    # Missing LongDesc information from request call.
    def test_missingLongDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'],
                                                longDescExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingLongDesc assert#1 has failed.')
        
        
        
    # Test a null LongDesc.
    def test_nullLongDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = '', 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullLongDesc assert#1 has failed.')



    # Test a int LongDesc.
    def test_intLongDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = 123, 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intLongDesc assert#1 has failed.')



    # Test a float LongDesc.
    def test_floatLongDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = 32.1, 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatLongDesc assert#1 failed.')
        
        
        
    # Test a string LongDesc value call.
    def test_stringLongDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringLongDesc assert#1 failed.')



    # Test an array LongDesc value call.
    def test_arrayLongDesc(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ['hodl', 666, [.6, 0], {}], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayLongDesc assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                           Tags tests                              *
    # *********************************************************************
    
    
        
    # Missing Tags information from request call.
    def test_missingTags(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'],
                                                tagsExclude=True)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingTags assert#1 has failed.')
        
        
        
    # Test a null Tags.
    def test_nullTags(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = '', 
                                                attachments = ADPQShell.data['testAttachments'])
         
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullTags assert#1 has failed.')



    # Test a int Tags.
    def test_intTags(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = 666, 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intTags assert#1 has failed.')



    # Test a float Tags.
    def test_floatTags(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = .3, 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatTags assert#1 failed.')
        
        
        
    # Test a string Tags value call.
    def test_stringTags(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringTags assert#1 failed.')



    # Test an array Tags value call.
    @unittest.skip("JSONDecodeError")
    def test_arrayTags(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ['hodl', 666, [.6, 0], {}], 
                                                attachments = ADPQShell.data['testAttachments'])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayTags assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                        Attachments tests                          *
    # *********************************************************************
    
    
        
    # Missing Attachments information from request call.
    def test_missingAttachments(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ADPQShell.data['testAttachments'],
                                                attachmentsExclude=True)
 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_missingAttachments assert#1 has failed.')
        
        
        
    # Test a null Attachments.
    def test_nullAttachments(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = '')
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_nullAttachments assert#1 has failed.')



    # Test a int Attachments.
    @unittest.skip("attachments - int value")
    def test_intAttachments(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = 1)
 
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_intAttachments assert#1 has failed.')



    # Test a float Attachments.
    @unittest.skip("attachments - float value")
    def test_floatAttachments(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = 1.1)
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_floatAttachments assert#1 failed.')
        
        
        
    # Test a string Attachments value call.
    @unittest.skip("JSONDecodeError")
    def test_stringAttachments(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_stringAttachments assert#1 failed.')



    # Test an array Attachments value call.
    def test_arrayAttachments(self):
        responseBody = self.user.create_article(Authorization = self.user.GetAuthKey(), 
                                                title = ADPQShell.data['testTitle'], 
                                                agencyId = ADPQShell.data['testAgencyId'],
                                                audience = ADPQShell.data['testAudience'], 
                                                shortDesc = ADPQShell.data['testShortDesc'], 
                                                longDesc = ADPQShell.data['testLongDesc'], 
                                                tags = ADPQShell.data['testTags'], 
                                                attachments = ['hodl', 666, [.6, 0], {}])
        
        self.assertEqual(responseBody['status'], "saved!",
                          msg='test_arrayAttachments assert#1 failed.')
        
        
            
            
    def tearDown(self):
        self.user.delete_article(Authorization = self.user.GetAuthKey(), 
                                 articleId = self.user.GetArticleIds())
    
    
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestCreateArticles('test_success'))
  
    suite.addTest(TestCreateArticles('test_missingAuthorization'))
    suite.addTest(TestCreateArticles('test_nullAuthorization'))
    suite.addTest(TestCreateArticles('test_intAuthorization'))
    suite.addTest(TestCreateArticles('test_floatAuthorization'))
    suite.addTest(TestCreateArticles('test_stringAuthorization'))
    suite.addTest(TestCreateArticles('test_arrayAuthorization'))
        
    suite.addTest(TestCreateArticles('test_missingTitle'))
    suite.addTest(TestCreateArticles('test_nullTitle'))
    suite.addTest(TestCreateArticles('test_intTitle'))
    suite.addTest(TestCreateArticles('test_floatTitle'))
    suite.addTest(TestCreateArticles('test_stringTitle'))
    suite.addTest(TestCreateArticles('test_arrayTitle'))
       
#     suite.addTest(TestCreateArticles('test_missingAgencyId'))
#     suite.addTest(TestCreateArticles('test_nullAgencyId'))
#     suite.addTest(TestCreateArticles('test_intAgencyId'))
#     suite.addTest(TestCreateArticles('test_floatAgencyId'))
#     suite.addTest(TestCreateArticles('test_stringAgencyId'))
#     suite.addTest(TestCreateArticles('test_arrayAgencyId'))
       
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
    suite.addTest(TestCreateArticles('test_stringTags'))
    suite.addTest(TestCreateArticles('test_arrayTags'))
      
    suite.addTest(TestCreateArticles('test_missingAttachments'))
    suite.addTest(TestCreateArticles('test_nullAttachments'))
    suite.addTest(TestCreateArticles('test_intAttachments'))
    suite.addTest(TestCreateArticles('test_floatAttachments'))
    suite.addTest(TestCreateArticles('test_stringAttachments'))
    suite.addTest(TestCreateArticles('test_arrayAttachments'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())