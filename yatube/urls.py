from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
#для загрузки пользователем изображений
from django.conf import settings
from django.conf.urls.static import static


handler404 = "posts.views.page_not_found" #Страницы ошибок 
handler500 = "posts.views.server_error"    #Страницы ошибок

urlpatterns = [
    #  обработчик для главной страницы ищем в urls.py приложения posts
    path("", include("posts.urls")),

    #  регистрация и авторизация
    path("auth/", include("users.urls")),

    #  если нужного шаблона для /auth не нашлось в файле users.urls — 
    #  ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),

    #  раздел администратора
    path("admin/", admin.site.urls),

    # flatpage
    path('about/', include('django.contrib.flatpages.urls')),

    
]

urlpatterns += [
        path('about-author/', views.flatpage, {'url': '/about-us/'}, name='about-author'),

]

#позволяет обращаться файлам в директории, указанной в MEDIA_ROOT по имени, через префикс MEDIA_URL.
#только в режиме разработки
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)