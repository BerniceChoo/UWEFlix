from django.db import models

import uuid

class Club(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    club_name = models.CharField(max_length=200)

    club_address_number = models.CharField(max_length=5)
    club_address_street = models.CharField(max_length=100)
    club_address_city = models.CharField(max_length=100)
    club_address_postcode = models.CharField(max_length=8)

    club_tphone = models.IntegerField()
    club_phone = models.IntegerField()
    club_email = models.CharField(max_length=50)

    rep_first_name = models.CharField(max_length=25)
    rep_last_name = models.CharField(max_length=30)
    rep_dob = models.CharField(max_length=10)

    image = models.ImageField(blank=True, upload_to='images')
    
    def __str__(self):
        return self.club_name

    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        
        return url