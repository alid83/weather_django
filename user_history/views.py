from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from account_module.models import User, UserActivity
from khayyam import JalaliDate
from django.http import JsonResponse

global_date = {
    'start': None,
    'end': None,
}

def UserHistory(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    user = User.objects.filter(id=request.user.id).first()
    activities_list = UserActivity.objects.filter(name__iexact=user)
    paginator = Paginator(activities_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_history/user_history.html', {'user': user, 'page_obj': page_obj})

def ajax_user_history(request):
    start = request.POST.get('start')
    end = request.POST.get('end')
    page_number = request.POST.get('page', 1)

    start_date = JalaliDate(*map(int, start.split('/'))).todate()
    end_date = JalaliDate(*map(int, end.split('/'))).todate()

    user = User.objects.get(id=request.user.id)
    user_activity_list = UserActivity.objects.filter(
        name__iexact=user,
        date_search__range=[start_date, end_date]
    )

    paginator = Paginator(user_activity_list, 5)
    page_obj = paginator.get_page(page_number)

    activities = [
        {
            'name': activity.name,
            'cities': activity.cities,
            'persian_date_search': activity.persian_date_search
        } for activity in page_obj
    ]

    return JsonResponse({
        'activities': activities,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    })
