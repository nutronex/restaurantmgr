from django.conf.urls import url,include
from django.conf.urls.static import  static
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from restaurant import settings

from food.views import FoodCategoryCreateView
from food.views import AccountCreateView
from food.views import delete_account_view
from food.views import AccountListView
from food.views import MenuItemCreateView
from food.views import FoodCategoryUpdateView
from food.views import FoodCategoryDeleteView
from food.views import FoodCategoryListView
from food.views import FoodCategoryDetailView
from food.views import menu_item_update_mini_view
from food.views import bill_payment_view

from food.views import index_view
from food.views import OrderListView
from food.views import OrderPendingListView
from food.views import MenuItemListView
from food.views import BillListView
from food.views import MenuItemDeleteView
from food.views import MenuItemUpdateView
from food.views import OrderDayView
from food.views import bill_detail_view
from food.views import MakeOrderUpdateView
from food.views import MakeOrderDeleteView
from food.views import MakeOrderCreateView

from food.viewsets import OrderAddViewSet
from food.viewsets import OrderVerboseViewSet
from food.viewsets import MenuItemViewSet
from food.viewsets import FoodCategoryViewSet
from food.viewsets import FuckV
from food.forms import CustomAuthForm

from django.contrib.auth import views as auth_views
#admin.autodiscover()
rt = DefaultRouter()
rt.register(r'order',OrderVerboseViewSet)
rt.register(r'orderadd',OrderAddViewSet)
rt.register(r'foodcategory',FoodCategoryViewSet)
rt.register(r'menu',MenuItemViewSet)
rt.register(r'orderadd',OrderAddViewSet),

urlpatterns = [

    url(r'api/makeorder',FuckV.as_view()),

    url(r'^$', index_view,name='home'),
    url(r'^login/$',auth_views.login,{'template_name':'registration/login.html',
                                      'authentication_form':CustomAuthForm,
                                      'redirect_field_name':'/menu/'}),
    url(r'^logout/$',auth_views.logout,{'template_name':'registration/logout.html'}),
#    url(r'^admin/', admin.site.urls),
    url(r'^api/',include(rt.urls)),
    url(r'^billlist/',BillListView.as_view()),

    url(r'^menu/$',MenuItemListView.as_view(),name='menu_list_view'),
    url(r'^menu/add/$',MenuItemCreateView.as_view(),name='menu_create_view'),
    url(r'^menu/delete/(?P<pk>\d+)$',MenuItemDeleteView.as_view(),name='menu_delete_view'),
    url(r'^menu/update/(?P<pk>\d+)/$',MenuItemUpdateView.as_view(),name='menu_update_view'),
    url(r'^menu/update-ajax/(?P<pk>\d+)/$',menu_item_update_mini_view,name='menu_update_ajax_view'),

    url(r'^foodcategory/$',FoodCategoryListView.as_view(),name='category_list_view'),
    url(r'^foodcategory/add/$',FoodCategoryCreateView.as_view(),name='category_create_view'),
    url(r'^foodcategory/update/(?P<pk>\d+)$',FoodCategoryUpdateView.as_view(),name='category_update_view'),
    url(r'^foodcategory/detail/(?P<pk>\d+)$',FoodCategoryDetailView.as_view(),name='category_detail_view'),
    url(r'^foodcategory/delete/(?P<pk>\d+)$',FoodCategoryDeleteView.as_view(),name='category_delete_view'),



    url(r'^makeorder/create$',MakeOrderCreateView.as_view()),
    url(r'^makeorder/delete/(?P<pk>\d+)$',MakeOrderDeleteView.as_view()),
    url(r'^makeorder/update/(?P<pk>\d+)$',MakeOrderUpdateView.as_view()),
    url(r'^bill/(?P<pk>\d+)$',bill_detail_view),
    url(r'^billpayment/$',bill_payment_view),
    url(r'^order/pending/',OrderPendingListView.as_view(),name="order_pending_view"),
    url(r'^order/$',OrderListView.as_view(),name="order_list_view"),
    url(r'^order/date/(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<day>\d+)/$',OrderDayView.as_view()),

    url(r'^accountcreate/$',AccountCreateView.as_view()),
    url(r'^accountlist/$',AccountListView.as_view()),
    url(r'^accountdelete/$',delete_account_view),

url(r'report/',include('datareport.urls'))
]

import datareport
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT )
#urlpatterns+=url(r'report/',include('datareport.urls'))
