from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Apps
    path('api/auth/', include('users.api.urls')),
    path('api/departments/', include('departments.api.urls')),
    path('api/teachers/', include('teachers.api.urls')),
    path('api/students/', include('students.api.urls')),
    path('api/courses/', include('courses.api.urls')),
    path('api/attendance/', include('attendance.api.urls')),
    path('api/results/', include('results.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
