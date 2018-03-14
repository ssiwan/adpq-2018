import sys, unittest, requests, ADPQShell

'''
    ADPQ v1 - Search Articles end point.
    
    Purpose - Returns a list of all articles in the db.
    
    Method signature:
        search_articles(self, Authorization='', AuthorizationExclude=False, 
                        return_status=False):
    
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
        status = self.user.search_articles(return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_liveEndPoint assert#1 failed.')
        
        
        
    # Test successfully calling the end point and getting a list of articles.
    def test_success(self):
        responseBody = self.user.search_articles()
           
        self.assertNotEqual(responseBody['data'], [], msg='test_Success assert#1 has failed.')
    
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSearchArticles('test_liveEndPoint'))
    suite.addTest(TestSearchArticles('test_success'))
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())