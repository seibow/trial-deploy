from django.urls import path
from . import views

app_name = "steps"

urlpatterns = [
    path("<int:goal_id>/create/", views.step_create, name="step_create"),
    path("<int:step_id>/delete/", views.step_delete, name="step_delete"),
    path("<int:step_id>/complete/", views.complete_step, name="complete_step"),
]
