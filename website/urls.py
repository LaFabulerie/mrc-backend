from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='website/index.html'), name='index'),
    path('mediateur', TemplateView.as_view(template_name='website/mediateur/index.html'), name='mediateur'),
    path('mediateur/maison', TemplateView.as_view(template_name='website/mediateur/maison.html'), name='maison'),
    path('mediateur/popup', TemplateView.as_view(template_name='website/mediateur/popup.html'), name='popup'),
    path('mediateur/profile', TemplateView.as_view(template_name='website/mediateur/profile.html'), name='profile'),
    path('mediateur/contenu', TemplateView.as_view(template_name='website/mediateur/contenu.html'), name='contenu'),
    path('auth/login', TemplateView.as_view(template_name='website/auth/login.html'), name='login'),
    path('auth/signup', TemplateView.as_view(template_name='website/auth/signup.html'), name='signup'),
    path('auth/signup-structure-lookup', TemplateView.as_view(template_name='website/auth/signup-structure-lookup.html'), name='signup-structure-lookup'),
    path('auth/signup-structure-choose', TemplateView.as_view(template_name='website/auth/signup-structure-choose.html'), name='signup-structure-choose'),
    path('auth/signup-structure-new', TemplateView.as_view(template_name='website/auth/signup-structure-new.html'), name='signup-structure-new'),
    path('projet', TemplateView.as_view(template_name='website/vitrine/index.html'), name='projet'),
]

