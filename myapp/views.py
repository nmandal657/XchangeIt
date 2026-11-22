from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.
from .models import User, UserProfile, Item, TradeProposal
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
    if not current_user_email:
        return redirect('login')

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


def propose_swap(request, item_id):
    user_email = request.session.get('user')
    if not user_email:
        return redirect('login')

    sender = get_object_or_404(User, email=user_email)
    clicked_item = get_object_or_404(Item, id=item_id)
    receiver = clicked_item.user

    if receiver == sender:
        return redirect('home')

    receiver_items = Item.objects.filter(user=receiver, is_product_available=True)
    my_items = Item.objects.filter(user=sender, is_product_available=True)
    error = None

    if request.method == 'POST':
        selected_target_ids = request.POST.getlist('target_items')
        selected_offered_ids = request.POST.getlist('offered_items')
        message = request.POST.get('message', '')

        if not selected_target_ids or not selected_offered_ids:
            error = "Please select at least one item you want AND at least one item to offer."
        else:
            proposal = TradeProposal.objects.create(
                sender=sender,
                receiver=receiver,
                message=message
            )
            proposal.target_items.set(Item.objects.filter(id__in=selected_target_ids, user=receiver))
            proposal.offered_items.set(Item.objects.filter(id__in=selected_offered_ids, user=sender))
            return redirect('my_trades')

    context = {
        'clicked_item': clicked_item,
        'receiver': receiver,
        'receiver_items': receiver_items,
        'my_items': my_items,
        'error': error,
    }
    return render(request, 'propose_swap.html', context)


def my_trades(request):
    user_email = request.session.get('user')
    if not user_email:
        return redirect('login')

    user = get_object_or_404(User, email=user_email)
    received_offers = TradeProposal.objects.filter(receiver=user)
    sent_offers = TradeProposal.objects.filter(sender=user)

    context = {
        'received_offers': received_offers,
        'sent_offers': sent_offers,
    }
    return render(request, 'my_trades.html', context)


def respond_swap(request, proposal_id, action):
    proposal = get_object_or_404(TradeProposal, id=proposal_id)

    if action == 'accept':
        proposal.status = 'AC'
        proposal.save()

        proposal.target_item.is_product_available = False
        proposal.target_item.save()

        for item in proposal.offered_items.all():
            item.is_product_available = False
            item.save()

    elif action == 'reject':
        proposal.status = 'RE'
        proposal.save()

    return redirect('my_trades')


def complete_swap(request, proposal_id):
    proposal = get_object_or_404(TradeProposal, id=proposal_id)

    if proposal.status == 'AC':
        proposal.status = 'CO'
        proposal.save()

        sender_profile = UserProfile.objects.filter(user=proposal.sender).first()
        receiver_profile = UserProfile.objects.filter(user=proposal.receiver).first()

        if sender_profile:
            sender_profile.successful_trades_count += 1
            sender_profile.save()

        if receiver_profile:
            receiver_profile.successful_trades_count += 1
            receiver_profile.save()

    return redirect('my_trades')