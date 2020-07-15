# Views is responsible for handling which template/html gets displayed

from django.views.generic import TemplateView

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'
    
class HomePage(TemplateView):
    template_name = 'index.html'
