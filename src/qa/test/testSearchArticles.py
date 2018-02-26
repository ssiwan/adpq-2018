import sys, unittest, QaAdpqShell, requests

'''
    ADPQ v1 - Search Articles end point.
    
    Purpose - Returns a list of all articles in the db.
    
    Method signature:
        search_articles(self):
    
    Required:
        <none>

    Test cases
        Ensure the end point is live.
        Successfully execute a search and get the results.
'''
class TestSearchArticles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            # Create user object.
            cls.user = QaAdpqShell.QaADPQShell()
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            raise


    
    # Make sure the end point is live.
    def test_liveEndPoint(self):
        # URL end point.
        url = QaAdpqShell.QaADPQShell.BaseURL + QaAdpqShell.QaADPQShell.SearchArticles

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
        
        # Ensure end point is live.
        self.assertEqual(response.status_code, 200, msg='test_liveEndPoint assert#1 has failed.')
        
        
        
    # Test successfully calling the end point and getting a list of articles.
    def test_success(self):
        # Attempt to get a list of articles.
        responseBody = self.user.search_articles()
           
        # Ensure that articles are present.
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_Success assert#1 has failed.')
        
        
        
        
    @classmethod
    def tearDownClass(cls):
        try:
            pass
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
    
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSearchArticles('test_liveEndPoint'))
    suite.addTest(TestSearchArticles('test_success'))
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())