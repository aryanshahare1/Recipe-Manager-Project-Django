from django.contrib import admin
from django.urls import path
from home.views import home  
from vege.views import recipes, add_recipe, update_recipe, delete_recipe, login_page, register_page, logout_page
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name= 'home'),  
    path('recipes/', recipes, name='recipes'),
    path('add-recipe/', add_recipe, name='add_recipe'),
    path('delete-recipe/<id>/', delete_recipe, name='delete_recipe'),
    path('update-recipe/<id>/', update_recipe, name='update_recipe'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    path('register/', register_page, name='register_page'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()
