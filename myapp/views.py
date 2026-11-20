from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.
from .models import User, UserProfile, Item
import datetime
from django.contrib import messages



def signup(request):
    if request.method == 'POST':
        form_name = request.POST.get('name')
        form_email = request.POST.get('email')
        form_phone_number = request.POST.get('phone_number')
        form_password = request.POST.get('password')

        users = User.objects.filter(email = form_email).exists()
        if users:
            return HttpResponse('email already exist')

        User.objects.create(
            name = form_name,
            email = form_email,
            phone_number = form_phone_number,
            password = form_password
        )
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        form_email = request.POST.get('email')
        form_password = request.POST.get('password')

        user = User.objects.filter(email=form_email).first()

        if not user:
            # messages.warning(request,'User with this email does not exist')
            return redirect('login')

        if not user.password == form_password:
            messages.error(request,'Password is incorrect')
            return redirect('login')
            
        request.session['user'] = user.email
        # messages.success(request, f'Welcome back, {user.name}!')
        return redirect('profile')

    return render(request, 'login.html')


def profile(request):
    if not request.session.get('user'):
        return redirect('login')
    
    
    curruser = User.objects.filter(email = request.session['user']).first()
    user_profile = UserProfile.objects.filter(user=curruser).first()


    if request.method == 'POST':

        if not user_profile:
            dob = request.POST.get('dob')
            house_no = request.POST.get('house_no')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            
            new_profile = UserProfile.objects.create(
                dob = dob,
                house_no = house_no,
                city = city,
                state = state,
                postal_code = postal_code,
                user=curruser,
            )

            if request.FILES.get('profile_picture'):
                profile_picture = request.FILES.get('profile_picture')
                new_profile.profile_picture = profile_picture

            new_profile.save()
            curruser.save()
            messages.success(request, 'new profile created')
            return redirect('profile')

        
        user_profile.dob = request.POST.get('dob')
        user_profile.house_no = request.POST.get('house_no')
        user_profile.city = request.POST.get('city')
        user_profile.state = request.POST.get('state')
        user_profile.postal_code = request.POST.get('postal_code')

        if request.FILES.get('profile_picture'):
            user_profile.profile_picture = request.FILES.get('profile_picture')

        curruser.save()
        user_profile.save()
       
        messages.success(request, 'profile updated')
        return redirect('profile')
    return render(request, 'profile.html', {'user': curruser, 'profile':user_profile})


def add_item(request):

    if 'user' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        curruser = User.objects.filter(email = request.session['user']).first()

        if not curruser:
            return redirect('login')

        item_image = request.FILES.get('image')
        item_name = request.POST.get('name')
        item_desc = request.POST.get('desc')
        item_category = request.POST.get('category')
        item_wishlist = request.POST.get('wishlist')

        Item.objects.create(
            user = curruser,
            image = item_image,
            name = item_name,
            desc = item_desc,
            category = item_category,
            wishlist = item_wishlist
        )
        messages.success(request, 'Item listed successfully!')
        return redirect('profile')
    return render(request, 'add_item.html')

def view_profile(request, user_id):

    owner = get_object_or_404(User, id=user_id)
    
    profile = UserProfile.objects.filter(user=owner).first()
    
    owner_items = Item.objects.filter(user=owner, is_product_available=True)
    
    context = {
        'owner': owner,
        'profile': profile,
        'owner_items': owner_items,
    }
    return render(request, 'view_profile.html', context)



def logout(request):
    request.session.flush()
    return redirect('login')

def home(request):
    current_user_email = request.session.get('user')
    # if not current_user_email:
    #     return redirect('login')

    current_user = User.objects.filter(email = current_user_email).first()
    
    items_category = request.GET.get('items_category', 'All Items')

    all_items = Item.objects.filter(is_product_available= True)
    electronics_items = Item.objects.filter(category = 'EL')
    home_kitchen_items = Item.objects.filter(category = 'HK')
    fashion_clothing_items = Item.objects.filter(category = 'FA')
    books_media_items = Item.objects.filter(category = 'BM')
    vehicles_parts_item = Item.objects.filter(category = 'VE')
    sports_outdoors_items = Item.objects.filter(category = 'SO')
    tech_design_service_items = Item.objects.filter(category = 'TS')
    lession_tutoring_items = Item.objects.filter(category = 'ED')
    home_pet_service_items = Item.objects.filter(category = 'HS')
    skill_service_items = Item.objects.filter(category = 'SK')

    context = {
        "current_user" : current_user,
        "items_category": items_category,
        "all_items" : all_items,
        "electronics_items" : electronics_items,
        "home_kitchen_items" : home_kitchen_items,
        "fashion_clothing_items" : fashion_clothing_items,
        "books_media_items" : books_media_items,
        "vehicles_parts_item" : vehicles_parts_item,
        "sports_outdoors_items" : sports_outdoors_items,
        "tech_design_service_items" : tech_design_service_items,
        "lession_tutoring_items" : lession_tutoring_items,
        "home_pet_service_items" : home_pet_service_items,
        "skill_service_items" : skill_service_items,
    }
    
    return render(request, 'home.html', context)