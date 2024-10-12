from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import authView, home, logout_view,  details, Addbook, insert_book,approvebook,rejectbook,btech,insertData,book_details,view_cart,save_note,delete_note

urlpatterns = [
    path("", home, name="home"),

    path("insert/", insertData, name="insertData"),
    path("signup/", authView, name="authView"),
    path("details/", details, name="details"),
    path("logout/", logout_view, name="logout"),
    path("addbook/", Addbook, name="Addbook"),
    path("btech/",btech,name="btech"),
    path("insert_book/", insert_book, name="insert_book"),
    path('insert/', insertData, name='insert_data'),
    path('view_cart/' ,view_cart,name="view_cart"),
    
    
    # Include Django's built-in authentication URLs
    path("accounts/", include("django.contrib.auth.urls")),
    
     #path("btech/<int:id>/", btech_detail, name="btech_detail"),
    
     path('approve/<uuid:token>/',approvebook, name='approve_book'),
    path('reject/<uuid:token>/', rejectbook, name='reject_book'),
    
     path('book/<int:pk>/',book_details, name='book_details'),
     
     
      path('save-note/<int:book_id>/', save_note, name='save-note'),
      path('delete-note/<int:book_id>/', delete_note, name='delete-note'),
   
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
