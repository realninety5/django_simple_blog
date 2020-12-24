from actions.utils import create_action
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from django.conf import settings
import redis

# Create a connection to redis db
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

# Create your views here.

# The image creation view
@login_required
def image_create(request):
    if request.method == 'POST':
        # Form is submitted
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            # Calls create_action which prevents multiple actions in a given time
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully!')
            return redirect(new_item.get_absolute_url())
    else:
        # Build new form by the data provided by the bookmark with GET
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images',
                                                                'form': form})
# View to display image and its details
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # Increment count of total number of views by 1
    total_views = r.incr(f'image:{image.id}:views')
    # Keeps track of the total number kf views an image has in a sorted set
    r.zincrby('image_ranking', 1, image.id)
    return render(request, 'images/image/detail.html',
                  {'section': 'images',
                   'image': image,
                   'total_views': total_views})
@login_required
def image_ranking(request):
    # Get the first ten most viewed images
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    # Based on their index value in the R3dis' sorted set
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'section': 'images',
                                                         'most_viewed': most_viewed})

# View to manipulate an image's like and dislike and returns a Json response
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                # Calls create_action to save the image
                create_action(request.user, 'likes', image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})

# List available images, 8 per request
@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer return the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If it is an ajax request and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range, return last page
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images',
                                                               'images': images})
    return render(request, 'images/image/list.html', {'section': 'images',
                                                      'images': images})
# List active users
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html',
                  {'section': 'people',
                   'users': user})
# Returns the user detail
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username,
                             is_active=True)
    return render(request, 'account/user/detail.html',
                  {'section': 'people',
                   'user': user})
