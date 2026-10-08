from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'maintenance/',
        views.maintenance_list,
        name='maintenance_list'
    ),

    path(
        'maintenance/add/',
        views.maintenance_create,
        name='maintenance_create'
    ),

    path(
        'maintenance/<int:id>/',
        views.maintenance_detail,
        name='maintenance_detail'
    ),

    path(
        'maintenance/<int:id>/edit/',
        views.maintenance_edit,
        name='maintenance_edit'
    ),

    path(
        'maintenance/<int:id>/delete/',
        views.maintenance_delete,
        name='maintenance_delete'
    ),

    path(
        'cost-summary/',
        views.cost_summary,
        name='cost_summary'
    ),
]