from django.views.generic import FormView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .forms import ContactForm
from django.conf import settings

class ContactUsView(FormView):
    template_name = 'contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact us')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        full_message = f"Message from {name} ({email}):\n\n{message}"

        # Send email with the correct recipient
        send_mail(
            'Contact Us Form Submission',
            full_message,
            settings.EMAIL_HOST_USER,  # Your "from" email address (matches EMAIL_HOST_USER)
            [settings.EMAIL_HOST_USER],  # Your "to" email address (inbox receiving the messages)
            fail_silently=False,
        )

        return super().form_valid(form)
