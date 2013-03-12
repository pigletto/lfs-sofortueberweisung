# django imports
from django.conf.urls.defaults import *


urlpatterns = patterns('lfs_sofortueberweisung.views',
                       url(r'^notification_url/(?P<order_id>\d*)/(?P<security_hash>).*?/$',
                           "success_notification", name="lfs_sofortueberweisung_notification"),
)
