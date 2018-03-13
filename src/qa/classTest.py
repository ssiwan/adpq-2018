def Test_Class():
    # Declare class objects. Create class instance. DONE
    user = ADPQ()
    
    
    # Method signature. DONE
    # sign_in(self, email='', emailExclude=False, return_status=False):
    user.sign_in(email = data['testEmail'])
    
    
#     # Method signature. DONE
#     # get_agencies(return_status=False):
#     user.get_agencies()
    
    
#     # Method signature. DONE
#     # get_tags(return_status=False):
#     user.get_tags()
     
     
#     # Method signature. DONE
#     # get_articles(Authorization='', AuthorizationExclude=False, sortUrl=False,
#     #              limitUrl=False, dateStartURL=False, dateEndUrl=False,
#     #              agencyIdUrl=False, tagIdUrl=False, return_status=False):
#     user.get_articles(Authorization = user.GetAuthKey(), AuthorizationExclude=False,
#                       sortUrl=False, limitUrl=True, dateStartURL=False, dateEndUrl=False,
#                       agencyIdUrl=False, tagIdUrl=True, return_status=False)
     
     
#     # Method signature. DONE
#     # search_articles(return_status=False):
#     user.search_articles()

    
#     # Method signature. DONE
#     # create_article(Authorization='', title='', agencyId='', audience=0,
#     #                shortDesc='', longDesc='', tags='', attachments=[],
#     #                AuthorizationExclude=False, titleExclude=False,
#     #                agencyIdExclude=False, audienceExclude=False,
#     #                shortDescExclude=False, longDescExclude=False, 
#     #                tagsExclude=False, attachmentsExclude=False, return_status=False):
#     user.create_article(user.GetAuthKey(), 'Department of funky beats', '5a8b73f94212d1f20f847b9a',
#                         0, 'short desc', 'loonngg desc', '5a8b55bca2d13ad4ba5369ef', ["url1"])
    
    
#     # Method signature. DONE
#     # get_articles_details(Authorization='', AuthorizationExclude=False,
#     #                      articleId=[], return_status=False):
#     user.get_articles_details(user.GetAuthKey(), articleId = user.GetArticleIds())
    
    
#     # Method signature. DONE
#     # dashboard_analytics(self, Authorization='', AuthorizationExclude=False,
#                           return_status=False): 
#     user.dashboard_analytics(user.GetAuthKey())
#     
#     
#     # Method signature. DONE
#     # dashboard_trending(self, Authorization='', AuthorizationExclude=False,
#                           return_status=False):  
#     user.dashboard_trending(user.GetAuthKey())
#     
#     
#     # Method signature. DONE
#     # dashboard_pubArticles(self, Authorization='', AuthorizationExclude=False,
#                           return_status=False): 
#     user.dashboard_pubArticles(user.GetAuthKey())
#     
#     
#     # Method signature. DONE
#     # dashboard_workflow(self, Authorization='', AuthorizationExclude=False,
#                           return_status=False): 
#     user.dashboard_workflow(user.GetAuthKey())


#     # Method signature. DONE
#     # edit_article(Authorization='', articleId=[], title='', agencyId='', audience=0,
#     #              shortDesc='', longDesc='', tags='', attachments=[], status=0,
#     #              AuthorizationExclude=False, articleIdExclude=False, titleExclude=False,
#     #              agencyIdExclude=False, audienceExclude=False,
#     #              shortDescExclude=False, longDescExclude=False, 
#     #              tagsExclude=False, attachmentsExclude=False, statusExclude=False,
#     #              return_status=False)
#     user.edit_article(user.GetAuthKey(), user.GetArticleIds(), "Department of funky beats",
#                       '5a8b73f94212d1f20f847b9a', 0, 'short desc', 'long desc',
#                       'tags', ['pdf1, 666'], 0)
    
    
#     # Method signature. DONE
#     # comment_article(Authorization='', articleId=[], comment='', 
#     #                 AuthorizationExclude=False, articleIdExclude=False, 
#     #                   commentExclude=False, return_status=False):
#     user.comment_article(user.GetAuthKey(), user.GetArticleIds(), 'COMMENTS')
    
    
#     # Method signature. DONE
#     # get_presignedS3(Authorization='', name='', AuthorizationExclude=False, 
#     #                 nameExclude=False, return_status=False):
#     user.get_presignedS3(user.GetAuthKey(), 'file.txt')
    
    
Test_Class()