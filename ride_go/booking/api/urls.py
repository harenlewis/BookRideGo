from django.conf.urls import url

from .views.ride_schedule_view import RideScheduleAPIView


urlpatterns = [
    
    url(r'^users/(?P<user_id>[^/]+)/ride/(?P<ride_id>[^/]+)/schedule?/?$',
        RideScheduleAPIView.as_view(), name='schedule-ride-api'),

]