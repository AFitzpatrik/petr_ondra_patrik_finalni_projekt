from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from accounts.views import SignUpView, UserLogoutView, RegistrationSuccessView, LogoutSuccessView, LoginSuccessView
from accounts.forms import CustomPasswordResetForm
from api.views import EventsAPI, AllEventsAPI, FilteredEventsAPI
from viewer.views import EventUpdateView, EventDeleteView, ProfileDetailView, make_reservation, cancel_reservation, \
    CountryDetailView, CountryDeleteView, CityDeleteView
from viewer.views import EventsListView, EventDetailView, CitiesListView, LocationsListView, EventCreateView, \
    search, CityCreateView, CountryCreateView, CountryListView, CountryUpdateView, CityUpdateView, TypeCreateView, \
    LocationCreateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Events
    path('', EventsListView.as_view(), name='home'),
    path('events/', EventsListView.as_view(), name='events'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/<int:event_id>/reserve/', make_reservation, name='make_reservation'),
    path('event/<int:event_id>/cancel/', cancel_reservation, name='cancel_reservation'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('type/create/', TypeCreateView.as_view(), name='type_create'),
    path('location/create/', LocationCreateView.as_view(), name='location_create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),

    # Cities
    path('cities/', CitiesListView.as_view(), name='cities'),
    path('city/create/', CityCreateView.as_view(), name='city_create'),
    path('city/update/<int:pk>/', CityUpdateView.as_view(), name='city_update'),
    path('city/delete/<int:pk>/', CityDeleteView.as_view(), name='city_delete'),

    # Countries
    path('countries/', CountryListView.as_view(), name='countries'),
    path('country/<int:pk>/', CountryDetailView.as_view(), name='country_detail'),
    path('country/create/', CountryCreateView.as_view(), name='country_create'),
    path('country/update/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),  # URL pro smazání státu

    # Locations
    path('locations/', LocationsListView.as_view(), name='locations'),

    # Search
    path('search/', search, name='search'),

    # Accounts
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/registration_success/', RegistrationSuccessView.as_view(), name='registration_success'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login_success/', LoginSuccessView.as_view(), name='login_success'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/logout_success/', LogoutSuccessView.as_view(), name='logout_success'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='password_change_form.html'),
         name='password_change'),
    path('accounts/password_reset/',
         PasswordResetView.as_view(template_name='password_reset_form.html', form_class=CustomPasswordResetForm),
         name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/', include('django.contrib.auth.urls')),

    # User Profile
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),

    # API Endpoints
    path('api/events/', EventsAPI.as_view(), name='api_events'),
    path('api/all_events/', AllEventsAPI.as_view(), name='all_events'),
    path('api/filtered_events/', FilteredEventsAPI.as_view(), name='filtered_events'),


]

# Serve static and media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
