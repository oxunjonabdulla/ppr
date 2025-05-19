from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# ✅ API routes should not be localized
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    # API routes (no /uz/ prefix)
    path("api/", include("apps.users.api.urls")),
    path("api/", include("apps.companies.api.urls")),
    path("api/", include("apps.equipment.api.urls")),
    path("api/", include("apps.maintenance.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# ✅ Only admin and frontend routes get language prefix
urlpatterns += i18n_patterns(
    path(settings.ADMIN_URL, admin.site.urls),
    prefix_default_language=True,
)

# Static/media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Debug URLs
if settings.DEBUG:
    # Error page testing
    from django.views import defaults as default_views

    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied!")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page Not Found!")},
        ),
        path("500/", default_views.server_error),
    ]

    # Debug toolbar
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls))
        ] + urlpatterns
