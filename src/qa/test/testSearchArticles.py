import sys, unittest, requests, ADPQShell

'''
    ADPQ v1 - Search Articles end point.
    
    Purpose - Returns a list of all articles in the db.
    
    Method signature:
        search_articles(self, return_status=False):
    
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
            cls.user = ADPQShell.ADPQ()
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])


    
    # Make sure the end point is live.
    def test_liveEndPoint(self):
        url = ADPQShell.ADPQ.setEnv + ADPQShell.data['SearchArticles']
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        response = requests.request('GET', url, json={}, headers=headers, verify=False)
        
        self.assertEqual(response.status_code, 200, msg='test_liveEndPoint assert#1 has failed.')
        
        
        
    # Test successfully calling the end point and getting a list of articles.
    def test_success(self):
        responseBody = self.user.search_articles()
           
        self.assertNotEqual(responseBody['data'], [], msg='test_Success assert#1 has failed.')
        
        
        
        
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