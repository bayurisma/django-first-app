from django.urls import path
from wishlist.views import show_wishlist
from wishlist.views import return_xml
from wishlist.views import return_json
from wishlist.views import return_json_by_id
from wishlist.views import return_xml_by_id

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('xml/', return_xml, name='return_xml'),
    path('json/', return_json, name='return_json'),
    path('json/<int:id>', return_json_by_id, name='return_json_by_id'),
    path('xml/<int:id>', return_xml_by_id, name='return_xml_by_id'),
]