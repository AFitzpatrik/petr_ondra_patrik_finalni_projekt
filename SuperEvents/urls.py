"""
URL configuration for SuperEvents.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from accounts.views import SignUpView, UserLogoutView, RegistrationSuccessView, LogoutSuccessView, LoginSuccessView
from api.views import Events, AllEvents, FilteredEvents
from viewer.views import home, EventsListView, EventDetailView, CitiesListView, LocationsListView, search, \
    EventUpdateView, EventDeleteView, EventCreateView, ProfileDetailView, make_reservation, cancel_reservation, \
    TypeCreateView, LocationCreateView
from viewer.views import home, EventsListView, EventDetailView, CitiesListView, LocationsListView, EventCreateView, \
    search, CityCreateView, CountryCreateView, CountryListView, CountryUpdateView, CityUpdateView, TypeCreateView, \
    LocationCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', EventsListView.as_view(), name='home'),
    path('events/', EventsListView.as_view(), name='events'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/<int:event_id>/reserve/', make_reservation, name='make_reservation'),
    path('event/<int:event_id>/cancel/', cancel_reservation, name='cancel_reservation'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('type/create/', TypeCreateView.as_view(), name='type_create'),
    path('location/create/', LocationCreateView.as_view(), name='location_create'),
    path('type/create/', TypeCreateView.as_view(), name='type_create'),
    path('location/create/', LocationCreateView.as_view(), name='location_create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('cities/', CitiesListView.as_view(), name='cities'),
    path('city/create/', CityCreateView.as_view(), name='city_create'),
    path('city/<int:pk>/update/', CityUpdateView.as_view(), name='city_update'),
    path('countries/', CountryListView.as_view(), name='countries'),
    path('country/create/', CountryCreateView.as_view(), name='country_create'),
    path('country/<int:pk>/update/', CountryUpdateView.as_view(), name='country_update'),
    path('locations/', LocationsListView.as_view(), name='locations'),
    path('search/', search, name='search'),


    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/registration_success/', RegistrationSuccessView.as_view(), name='registration_success'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login_success/', LoginSuccessView.as_view(), name='login_success'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/logout_success/', LogoutSuccessView.as_view(), name='logout_success'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('accounts/', include('django.contrib.auth.urls')),


    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),



    path('api/events/', Events.as_view(), name='api_events'),
    path('api/all_events/', AllEvents.as_view(), name='all_events'),
    path('api/filtered_events/', FilteredEvents.as_view(), name='filtered_events'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
