from django.shortcuts import redirect


def homepage_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return redirect('/dashboard/current-well-readings/')
