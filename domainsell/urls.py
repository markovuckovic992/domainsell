"""domainsell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import mails.views
import maintenance.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #  login
    url(r'^home_login/', maintenance.views.Login),
    url(r'^logout/', maintenance.views.homeLogout),
    #  mails
    url(r'^offer/', mails.views.receive_mails),
    url(r'^process_offer/', mails.views.process_offer),
    url(r'^process_offer_redirect/', mails.views.process_offer_redirect),
    url(r'^contact/', mails.views.contact),
    url(r'^farewell/', mails.views.farewell),
    url(r'^thank-you/', mails.views.thank),
    url(r'^unsubscribe/', mails.views.unsubscribe),
    # add offer
    url(r'^add_offer/', mails.views.addoffer),
    # maintenance
    url(r'^maintenance/', maintenance.views.monitoring),
    url(r'^revert_state/', maintenance.views.revert_state),
    url(r'^zakazani_delete_for_old_datas__/', maintenance.views.delete_old_data),
    url(r'^check_status/', maintenance.views.check_status),
    url(r'^start_post_release/', maintenance.views.start_post_release),
    url(r'^start_post_sale/', maintenance.views.start_post_sale),
    url(r'^del_hash/', maintenance.views.del_hash),
    url(r'^change_amount/', maintenance.views.change_amount),
    url(r'^check_for_offers/', maintenance.views.check_for_offers),
    # control_panel
    url(r'^control_panel/', maintenance.views.control_panel),
    url(r'^save_settings/', maintenance.views.save_settings),
    # sales
    url(r'^sales/', mails.views.sales_page),
    # search
    url(r'^search/', maintenance.views.search),
    url(r'^search_results/', maintenance.views.search_results),
    # .NET
    url(r'^hello/', mails.views.hello),
]
