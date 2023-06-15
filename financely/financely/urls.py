"""
URL configuration for financely project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from my_auth.views import login_view, logout_view, home_view
from finance.views import (dashboard_view, accounts_view, 
                           add_account_view, edit_account_view, 
                           account_records_view, add_record_view, edit_record_view,
                           add_record_type_view)


urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('', home_view),
    path('login/', login_view),
    path('logout/', logout_view),

    # finance
    path('dashboard/', dashboard_view),
    path('accounts/', accounts_view),
    path('accounts/add_account', add_account_view),
    path('accounts/<int:acc_id>/', edit_account_view),
    path('accounts/<int:acc_id>/records', account_records_view),
    path('accounts/<int:acc_id>/records/add_record', add_record_view),
    path('accounts/<int:acc_id>/records/<int:record_id>', edit_record_view),
    path('accounts/record_types/add_record_type', add_record_type_view),
]
