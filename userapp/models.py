from django.db import models
from datetime import datetime
from mainapp.models import UserModel

# Create your models here.


class InteractionModel(models.Model):
    interac_id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(UserModel,on_delete=models.CASCADE, related_name='from_user',null=True)
    to_user = models.ForeignKey(UserModel,on_delete=models.CASCADE, related_name='to_user',null=True)
    message = models.CharField(max_length=500, blank=False,null=True)
    interac_type = models.CharField(max_length=50, blank=False,null=True)
    datetime_sent = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interactions_details'


class FeedbackModel(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    reviewer = models.ForeignKey(UserModel,on_delete=models.CASCADE, related_name='reviewer',null=True)
    
    review = models.CharField(max_length=500, blank=False,null=True)
    rating = models.IntegerField(blank=False,null=True)
    sentiment = models.CharField(max_length=50, blank=False,null=True)
    datetime_reviewed = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_feedbacks'
        