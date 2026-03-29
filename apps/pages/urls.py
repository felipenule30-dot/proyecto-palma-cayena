from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('nosotras/', views.about, name='about'),
    path('contacto/', views.contact, name='contact'),
    path('envios/', views.shipping, name='shipping'),
    path('cambios-y-devoluciones/', views.returns, name='returns'),
    path('terminos/', views.terms, name='terms'),
    path('privacidad/', views.privacy, name='privacy'),
    path('faq/', views.faq, name='faq'),
    path('journal/', views.journal_list, name='journal'),
    path('journal/<slug:slug>/', views.journal_post, name='journal_post'),
    path('newsletter/suscribirse/', views.newsletter_subscribe, name='newsletter'),
    path('<slug:slug>/', views.static_page, name='static_page'),
]
