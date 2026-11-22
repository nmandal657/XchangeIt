from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, blank=False, null=True)
    phone_number = models.CharField(max_length=15,blank=False, null=False)

    def __str__(self):
            return self.name

class UserProfile(models.Model):
    profile_picture = models.ImageField(upload_to='user/profile_pics/', blank=True)
    dob = models.DateField(null=True)
    house_no = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=False)
    state = models.CharField(max_length=100, blank=False, null=False)
    postal_code = models.CharField(max_length=10, blank=False, null=False)
    successful_trades_count = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.user.name


class Item(models.Model):
    image = models.ImageField(upload_to='item/item_img/', blank=True)
    name = models.CharField(max_length=50)
    desc = models.TextField()
    category = models.CharField(
        max_length = 2,
        choices=[
            ('EL', 'Electronics Items'),
            ('HK', 'Home & Kitchen Items'),
            ('FA', 'Fashion & Clothing Items'),
            ('BM', 'Books & Media Items'),
            ('VE', 'Vehicles & Parts'),
            ('SO', 'Sports & Outdoors Items'),
            ('TS', 'Tech & Design Services'),
            ('ED', 'Lessons & Tutoring'),
            ('HS', 'Home & Pet Services'),
            ('SK', 'Skills & Services')
            ],
            blank=True)
    wishlist = models.TextField()
    is_product_available = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name



class TradeProposal(models.Model):
    STATUS_CHOICES = [
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('RE', 'Rejected'),
        ('CO', 'Completed'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_proposals')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_proposals')
    
    target_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='target_proposals')
    
    offered_items = models.ManyToManyField(Item, related_name='offered_in_proposals')
    
    message = models.TextField(blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PE')

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name} for {self.target_item.name}"