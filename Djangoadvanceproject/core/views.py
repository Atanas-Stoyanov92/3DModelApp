# accounts/views.py
from django.views.generic import TemplateView


class ContactUsView(TemplateView):
    template_name = 'footer.html'
