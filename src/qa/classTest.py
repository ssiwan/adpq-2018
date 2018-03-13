# def Test_Class():
#     # Declare class objects. Create class instance. DONE
#     user = ADPQ()
#     
#     # Method signature. DONE
#     # sign_in(email='', password='', emailExclude=False, passwordExclude=False,
#     #         return_status=False):
#     user.sign_in(data['testEmail'], data['testPassword'])
#     
#     
# #     # Method signature. DONE
# #     # create_user(Authorization='', firstName='', lastName='', email='',
# #     #             phone='', password='', agencyId=[], allowUploads=0, AuthorizationExclude=False,  
# #     #             fNameExclude=False, lNameExclude=False, emailExclude=False,
# #     #             phoneExclude=False, agencyIdExclude=False, passwordExclude=False,
# #     #             allowUploadsExclude=False, return_status=False):
# #     user.create_user(user.GetAuthKey(), "Vladimir", "Putin", 
# #                      "vPutin@hotbsoftware.com", data['testPhone'], data['testPassword'], 
# #                      data['testAgencyId'], 1)
#     
#     
# #     # Method signature. DONE
# #     # get_agencies(return_status=False):
# #     user.get_agencies()
#     
#     
# #     # Method signature. DONE
# #     # get_tags(return_status=False):
# #     user.get_tags()
#      
#      
# #     # Method signature. DONE
# #     # get_articles(Authorization='', AuthorizationExclude=False, sortUrl=False,
# #     #              limitUrl=False, dateStartURL=False, dateEndUrl=False,
# #     #              agencyIdUrl=False, tagIdUrl=False, return_status=False):
# #     user.get_articles(Authorization = user.GetAuthKey(), AuthorizationExclude=False,
# #                       sortUrl=False, limitUrl=True, dateStartURL=False, dateEndUrl=False,
# #                       agencyIdUrl=False, tagIdUrl=True, return_status=False)
#      
#      
#     # Method signature. DONE
#     # search_articles(self, Authorization='', AuthorizationExclude=False, 
#     #                    return_status=False):
#     user.search_articles()
# 
# 
# #     # Method signature. DONE
# #     # create_article(Authorization='', title='', agencyId='', audience=0,
# #     #                shortDesc='', longDesc='', tags='', attachments=[],
# #     #                AuthorizationExclude=False, titleExclude=False,
# #     #                agencyIdExclude=False, audienceExclude=False,
# #     #                shortDescExclude=False, longDescExclude=False, 
# #     #                tagsExclude=False, attachmentsExclude=False, return_status=False):
# #     user.create_article(user.GetAuthKey(), "Ministry of Truth", '5a8b73f94212d1f20f847b9a',
# #                         '0', 'short desc', 'loonngg desc', 'LSDog', ["url1"])
#     
#     
# #     # Method signature. DONE
# #     # get_articles_details(Authorization='', AuthorizationExclude=False,
# #     #                      articleId=[], return_status=False):
# #     user.get_articles_details(user.GetAuthKey(), articleId = user.GetArticleIds())
#     
#     
# #     # Method signature. DONE
# #     # dashboard_analytics(self, Authorization='', AuthorizationExclude=False,
# #                           return_status=False): 
# #     user.dashboard_analytics(user.GetAuthKey())
# #     
# #     
# #     # Method signature. DONE
# #     # dashboard_trending(self, Authorization='', AuthorizationExclude=False,
# #                           return_status=False):  
# #     user.dashboard_trending(user.GetAuthKey())
# #     
# #     
# #     # Method signature. DONE
# #     # dashboard_pubArticles(self, Authorization='', AuthorizationExclude=False,
# #                           return_status=False): 
# #     user.dashboard_pubArticles(user.GetAuthKey())
# #     
# #     
# #     # Method signature. DONE
# #     # dashboard_workflow(self, Authorization='', AuthorizationExclude=False,
# #                           return_status=False): 
# #     user.dashboard_workflow(user.GetAuthKey())
# 
# 
# #     # Method signature. DONE
# #     # admin_dashboard_decline(Authorization='', AuthorizationExclude=False, 
# #     #                         return_status=False):
# #     user.admin_dashboard_decline(user.GetAuthKey())
# #     
# #     
# #     # Method signature. DONE
# #     # admin_dashboard_approved(Authorization='', AuthorizationExclude=False, 
# #     #                          return_status=False):  
# #     user.admin_dashboard_approved(user.GetAuthKey())
# #     
# #     
# #     # Method signature. DONE
# #     # admin_dashboard_pending(Authorization='', AuthorizationExclude=False, 
# #     #                         return_status=False):
# #     user.admin_dashboard_pending(user.GetAuthKey()) 
#     
# 
# #     # Method signature. DONE
# #     # edit_article(Authorization='', articleId=[], title='', agencyId='', audience=0,
# #     #              shortDesc='', longDesc='', tags='', attachments=[], status=0,
# #     #              AuthorizationExclude=False, articleIdExclude=False, titleExclude=False,
# #     #              agencyIdExclude=False, audienceExclude=False,
# #     #              shortDescExclude=False, longDescExclude=False, 
# #     #              tagsExclude=False, attachmentsExclude=False, statusExclude=False,
# #     #              return_status=False)
# #     user.edit_article(user.GetAuthKey(), user.GetArticleIds(), "Department of funky beats",
# #                       '5a8b73f94212d1f20f847b9a', 0, 'short desc', 'long desc',
# #                       'tags', ['pdf1, 666'], 0)
#     
#     
# #     # Method signature. DONE
# #     # comment_article(Authorization='', articleId=[], comment='', 
# #     #                 AuthorizationExclude=False, articleIdExclude=False, 
# #     #                   commentExclude=False, return_status=False):
# #     user.comment_article(user.GetAuthKey(), user.GetArticleIds(), 'COMMENTS')
#     
#     
# #     # Method signature. DONE
# #     # get_presignedS3(Authorization='', name='', AuthorizationExclude=False, 
# #     #                 nameExclude=False, return_status=False):
# #     user.get_presignedS3(user.GetAuthKey(), 'file.txt')
# 
# 
# #     # Method signature. START HERE SCRIPT ALREADY NON FILE
# #     # delete_article(Authorization='', articleId=[],
# #     #                AuthorizationExclude=False,  articleIdExclude=False,
# #     #                return_status=False):
# #     user.delete_article(user.GetAuthKey(), user.GetArticleIds())
#     
#     
# #     # Method signature
# #     # delete_user(Authorization='', userId='',
# #     #             AuthorizationExclude=False,  userIdExclude=False,
# #     #             return_status=False):
# #     user.delete_user(user.GetAuthKey(), user.GetNewUserIds())
#     
#     
# # Test_Class()