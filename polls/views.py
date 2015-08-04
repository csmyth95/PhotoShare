from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from mysite.forms import CategoryForm, PageForm
from polls.models import UserProfile, Category, Image
from mysite.forms import UserForm, UserProfileForm


def encode_url(str):
    return str.replace(' ', '_')


def decode_url(str):
    return str.replace('_', ' ')


def track_url(request, image_id):
    context = RequestContext(request)

    if request.method == 'GET':
        # i = get_object_or_404(Image, id=image_id)
        img = Image.objects.get(pk=image_id)
        img.views += 1
        img.save()
        caturl = encode_url(img.category.name)

    return render_to_response("polls/display.html", {'image': img, 'caturl': caturl}, context)


@login_required
def profile(request, profile_id):
    context = RequestContext(request)
    cat_list = get_user_albums(request)
    context_dict = {'cat_list': cat_list}
    image_list = Image.objects.filter(user=User.objects.get(pk=profile_id))
    context_dict['image_list'] = image_list
    u = User.objects.get(pk=profile_id)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    # context_dict['current'] = current
    # context_dict['friends'] = currentfriends




    return render_to_response('polls/profile.html', context_dict, context)


# def addriend(request)


def albumlist(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'albums': cat_list}
    images = Image.objects.all().order_by('-views')
    context_dict['images'] = images
    return render_to_response('polls/albums.html', context_dict, context)

@login_required()
def upload(request):
    context = RequestContext(request)
    cat_list = Category.objects.all().order_by('name')

    for cat in cat_list:
        cat.url = encode_url(cat.name)

    context_dict = {'albums': cat_list}

    return render_to_response('polls/upload.html', context_dict, context)


def category(request, category_name_url):
    # Request our context
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URL's don't handle spaces well, so we encode them as underscores.
    category_name = decode_url(category_name_url)

    # Build up the dictionary we will use as out template context dictionary.
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list

    try:
        cat = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = cat
        cat.views += 1
        cat.save()
        pages = Image.objects.filter(category=cat).order_by('-views')
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render_to_response('polls/category.html', context_dict, context)


def get_category_list():
    cat_list = Category.objects.all().order_by('-views')

    for cat in cat_list:
        cat.url = encode_url(cat.name)

    return cat_list


def get_user_albums(request):
    cat_list = Category.objects.filter(user=request.user).order_by('-views')

    for cat in cat_list:
        cat.url = encode_url(cat.name)

    return cat_list


def index(request):
    context = RequestContext(request)

    top_category_list = Category.objects.order_by('-views')[:5]

    for category in top_category_list:
        category.url = encode_url(category.name)

    context_dict = {'categories': top_category_list}

    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list

    page_list = Image.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')

        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    # Render and return the rendered response back to the user.
    return render_to_response('polls/index.html', context_dict, context)


@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, request.user)

        if form.is_valid():

            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            newimg = Image(title=request.POST.get('title'), image=request.FILES['image'], user=request.user,
                           category=Category.objects.get(name=category_name))

            newimg.save()
            url = "/goto/" + str(newimg.id)
            return HttpResponseRedirect(url)

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict['category_name_url'] = category_name_url
    context_dict['category_name'] = category_name
    context_dict['form'] = form

    return render_to_response('polls/add_page.html',
                              context_dict,
                              context)


@login_required
def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.user)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            newcat = Category(name=request.POST.get('name'), views=request.POST.get('views'), likes=request.POST.get('likes'), user=request.user)
            newcat.save()

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    context_dict['form'] = form
    return render_to_response('polls/add_category.html', context_dict, context)


def about(request):
    # Request the context.
    context = RequestContext(request)
    context_dict = {}
    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.

    count = request.session.get('visits', 0)

    context_dict['visit_count'] = count

    # Return and render the response, ensuring the count is passed to the template engine.
    return render_to_response('polls/about.html', context_dict, context)


# register.html
def register(request):
    context = RequestContext(request)

    # boolean to tell template whether the registration was successful
    registered = False

    if request.method == 'POST':
        # attempt to grab raw info
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if 2 forms valid
        if user_form.is_valid() and profile_form.is_valid():
            # save user form to database
            user = user_form.save()

            # hash user with set password method
            user.set_password(user.password)
            user.save()

            # sort out UserProfile instance
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did user provide profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # save user profile
            profile.save()

            # update register boolean
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

            # Not a HTTP POST, render form using 2 ModelForm instances
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render_to_response(
        'polls/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        # gather username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # if user object, details are correct
        if user:
            # is account active?
            if user.is_active:
                # send user to homepage
                login(request, user)

                url = '/profile/' + str(user.id)
                return HttpResponseRedirect(url)
            else:
                # inactive account used
                return HttpResponse("Your Photoshare account is disabled.")

        else:
            # bad login details provided
            print("Invalid login details: {0}, {1}").format(username, password)
            return HttpResponse("Invalid login details supplied.")
    # else request is not a POST
    else:
        # no context variables to pass to template system
        return render_to_response('polls/login.html', context)


# Only allow logged in users to logout - add the @login_required decorator!
@login_required
def user_logout(request):
    # As we can assume the user is logged in, we can just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

