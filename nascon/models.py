from django.db import models
from django.contrib.auth.models import AbstractUser

class Accommodation(models.Model):
    accommodation_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=50)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)


class User(AbstractUser):
    # overriding email field to be unique
    email = models.EmailField(unique=True)
    role_choices = {
        'participant' : 'Participant',
        'organizer' : 'Organizer',
        'judge' : 'Judge',
        'society' : 'Society',
        'sponsor' : 'Sponsor',
    }
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    role = models.CharField(max_length=20, choices=role_choices)
    accommodation_id = models.ForeignKey(Accommodation, models.DO_NOTHING, blank=True, null=True)


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('business', 'Business'),
        ('gaming', 'Gaming'),
        ('general', 'General'),
    ]

    event_id = models.AutoField(primary_key=True)
    organizer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizers')
    judge_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='judges')
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    max_participants = models.IntegerField()
    registration_fees = models.DecimalField(max_digits=10, decimal_places=2)
    registration_last_date = models.DateField()
    date_time = models.DateTimeField()


class Venue(models.Model):
    venue_id = models.AutoField(primary_key=True)
    venue_name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    location = models.CharField(max_length=255)


class EventRound(models.Model):
    pk = models.CompositePrimaryKey('round_id', 'event_id')
    round_id = models.IntegerField()
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    round_type = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('round_id', 'event_id'))


class ParticipantEvent(models.Model):
    pk = models.CompositePrimaryKey('participant_id', 'event_id')
    participant_id = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('participant_id', 'event_id'),)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateField()


class Society(models.Model):
    society_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    society_name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)


class SponsorshipPackage(models.Model):
    package_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    benefits = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)


class Sponsor(models.Model):
    pk = models.CompositePrimaryKey('sponsor_id', 'event_id')
    sponsor_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    package = models.ForeignKey(SponsorshipPackage, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('sponsor_id', 'event_id'),)

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(unique=True, max_length=255)
    max_size = models.IntegerField()
    score = models.IntegerField(blank=True, null=True)
    paymentid = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)

