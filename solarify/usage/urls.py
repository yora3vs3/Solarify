from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="usage"),
    path('add-usage', views.add_usage, name="add-usage"),
    path('edit-usage/<int:id>', views.usage_edit, name="usage-edit"),
    path('usage-delete/<int:id>', views.delete_usage, name="usage-delete"),
    path('search-usage', csrf_exempt(views.search_usage),
         name="search_usage"),
    path('usage_category_summary', views.usage_category_summary,
         name="usage_category_summary"),
    path('stats', views.stats_view,
         name="stats")
]
