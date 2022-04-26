from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path(
        "detail/<uuid:uuid>/checkout/",
        views.ProjectCheckoutView.as_view(),
        name="checkout",
    ),
    path(
        "detail/<uuid:uuid>/portal/",
        views.ProjectPortalView.as_view(),
        name="portal",
    ),
    path(
        "detail/<uuid:uuid>/terms/",
        views.ProjectTermsView.as_view(),
        name="terms",
    ),
    path(
        "detail/<uuid:uuid>/keys/",
        views.ProjectKeysView.as_view(),
        name="keys",
    ),
    path("create/", views.ProjectCreateView.as_view(), name="create"),
    path("", views.ProjectListView.as_view(), name="list"),
]
