from django.db import models

# Create your models here.
class UserBase(models.Model):
	user_id = models.CharField(primary_key = True, max_length = 8)
	first_name = models.CharField(max_length = 20)
	other_names = models.CharField(max_length = 50)
	gender = models.CharField(max_length = 6)
	email_address = models.CharField(max_length = 50)
	tel_number = models.CharField(max_length = 15)
	date_created = models.DateTimeField(auto_now_add = True)