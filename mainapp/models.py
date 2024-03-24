from django.db import models
from datetime import datetime
# Create your models here.
class ImgModel(models.Model):
    image=models.FileField(verbose_name='img',upload_to='temp_img/', blank=False)


    class Meta:
        db_table='temp_img'


class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField( max_length=100, blank=False,null=False)
    user_email = models.EmailField( max_length=100, blank=False,null=False)
    user_contact = models.BigIntegerField(  blank=False,null=False)
    user_password = models.CharField( max_length=50, blank=False,null=False)
    user_license = models.CharField( max_length=50, blank=False,null=False)
    user_photo = models.FileField( upload_to='media/', blank=False,null=False)
    user_status = models.CharField(default='pending', max_length=50, blank=False,null=False)
    user_email_status = models.CharField( max_length=50, blank=True,null=True)
    user_sms_status = models.CharField( max_length=50, blank=True,null=True)
    user_call_status = models.CharField( max_length=50, blank=True,null=True)
    user_privacy_status = models.CharField( max_length=50, blank=False,null=False)
    datetime_created = models.DateTimeField(default=datetime.now)


    class Meta:
        db_table='user_details'