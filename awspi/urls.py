from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'awspi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^hour/plus/(\d{1,2})$','awspi.views.HoursLater', name='HoursLater'),
    #url(r'^current_time/$', 'awspi.views.current_time', name='current_time'),
    #url(r'^show_users/$', 'awspi.views.show_users', name='show_users'),
    
    url(r'^user_data/$', 's3pi.views.user_data', name='user_data'),
    url(r'^s3list/$', 's3pi.views.s3list', name='s3list'),
    url(r'^listbucket/$', 's3pi.views.get_object', name='get_object'),
    url(r'^listinstance/$', 'ec2pi.views.ListInstances', name='ListInstances'),
    url(r'^listvolume/$', 'ec2pi.views.ListVolumes', name='ListVolumes'),
    url(r'^listip/$', 'ec2pi.views.ListIP', name='ListIP'),
]
