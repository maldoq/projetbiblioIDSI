from django.utils import timezone
from django.shortcuts import render

# Create your views here.
def signin(request):
    return render(request, 'login.html')

def dash(request):
    recent_activities = []
    # Placeholder si aucune activité récente n'est trouvée
    activities_placeholder = [
        {"message": "Aucune activité récente", "date": ""}
    ]
    context = {
        "recent_activities": recent_activities,
        "activities_placeholder": activities_placeholder
    }
    return render(request, 'dashboard.html', context)

def books_list(request):
    return render(request, 'books_list.html')

def loans_list(request):
    return render(request, 'loans_list.html')

def users_list(request):
    return render(request, 'users_list.html')

def categories_list(request):
    return render(request, 'categories_list.html')

def history(request):
    return render(request, 'history.html')

def profile(request):
    return render(request, 'profile.html')

def logout(request):
    return render(request, 'login.html')

def history(request):
    return render(request, 'history.html')

def loans_form(request):
    context = {
        'today': timezone.now().date()
    }
    return render(request, 'loans_form.html', context)

def returns_form(request):
    return render(request, 'returns_form.html')

def books_form(request):
    return render(request, 'books_form.html')

def users_form(request):
    return render(request, 'users_form.html')

def categories_form(request):
    return render(request, 'categories_form.html')

def history_export(request):
    pass

def change_password(request):
    pass
