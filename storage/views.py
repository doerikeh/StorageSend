from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FileFieldForm

class StorageView(FormView):
    form_class = FileFieldForm
    template_name = 'home.html'  # Replace with your template.
    success_url = '/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                f.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
def home(request):
    return render(request, "home.html", {})