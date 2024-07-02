from django.shortcuts import render

from .forms import SampleForm

# Create your views here.

def index_view(request):
    form = SampleForm()

    if request.method == "POST":
        form = SampleForm(request.POST)

    context = {
        "form": form
    }
    return render(request, "core/index.html", context)