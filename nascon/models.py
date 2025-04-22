# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Accommodation(models.Model):
    accommodationid = models.IntegerField(db_column='AccommodationID', primary_key=True)  # Field name made lowercase.
    room_number = models.CharField(db_column='Room_Number', max_length=50)  # Field name made lowercase.
    checkin_date = models.DateField(db_column='CheckIN_Date')  # Field name made lowercase.
    checkout_date = models.DateField(db_column='CheckOut_Date')  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Accommodation'

class Event(models.Model):
    eventid = models.IntegerField(db_column='EventID', primary_key=True)  # Field name made lowercase.
    organizerid = models.ForeignKey('User', models.DO_NOTHING, db_column='OrganizerID')  # Field name made lowercase.
    judgeid = models.ForeignKey('User', models.DO_NOTHING, db_column='JudgeID', related_name='event_judgeid_set', blank=True, null=True)  # Field name made lowercase.
    event_name = models.CharField(db_column='Event_Name', max_length=255)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255, blank=True, null=True)  # Field name made lowercase.
    max_participants = models.IntegerField(db_column='Max_Participants')  # Field name made lowercase.
    registration_fees = models.DecimalField(db_column='Registration_Fees', max_digits=10, decimal_places=2)  # Field name made lowercase.
    registration_last_date = models.DateField(db_column='Registration_last_Date')  # Field name made lowercase.
    date_time = models.DateTimeField(db_column='Date_Time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Event'


class Eventround(models.Model):
    pk = models.CompositePrimaryKey('roundid', 'eventid')
    roundid = models.IntegerField(db_column='RoundID')  # Field name made lowercase.
    eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='EventID')  # Field name made lowercase.
    round_type = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    venueid = models.ForeignKey('Venue', models.DO_NOTHING, db_column='VenueID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventRound'
        unique_together = (('roundid', 'eventid'),)


class Participantevent(models.Model):
    pk = models.CompositePrimaryKey('participantid', 'eventid')
    participantid = models.ForeignKey('User', models.DO_NOTHING, db_column='ParticipantID')  # Field name made lowercase.
    eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='EventID')  # Field name made lowercase.
    team = models.ForeignKey('Team', models.DO_NOTHING, db_column='Team_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ParticipantEvent'
        unique_together = (('participantid', 'eventid'),)


class Payment(models.Model):
    paymentid = models.IntegerField(db_column='PaymentID', primary_key=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    payment_due_date = models.DateField(db_column='Payment_Due_Date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Payment'


class Society(models.Model):
    societyid = models.IntegerField(db_column='SocietyID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    societyname = models.CharField(db_column='SocietyName', unique=True, max_length=255)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Society'


class Sponsor(models.Model):
    pk = models.CompositePrimaryKey('sponsorid', 'eventid')
    sponsorid = models.ForeignKey('User', models.DO_NOTHING, db_column='SponsorID')  # Field name made lowercase.
    eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='EventID')  # Field name made lowercase.
    package = models.ForeignKey('Sponsorshippackage', models.DO_NOTHING, db_column='Package_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sponsor'
        unique_together = (('sponsorid', 'eventid'),)


class Sponsorshippackage(models.Model):
    packageid = models.IntegerField(db_column='PackageID', primary_key=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255)  # Field name made lowercase.
    benefits = models.TextField(db_column='Benefits', blank=True, null=True)  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SponsorshipPackage'


class Team(models.Model):
    teamid = models.IntegerField(db_column='TeamID', primary_key=True)  # Field name made lowercase.
    team_name = models.CharField(db_column='Team_Name', unique=True, max_length=255)  # Field name made lowercase.
    max_size = models.IntegerField(db_column='Max_Size')  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    paymentid = models.ForeignKey(Payment, models.DO_NOTHING, db_column='PaymentID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Team'


class User(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', unique=True, max_length=255)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=255)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=11)  # Field name made lowercase.
    accommodationid = models.ForeignKey(Accommodation, models.DO_NOTHING, db_column='AccommodationID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'


class Venue(models.Model):
    venueid = models.IntegerField(db_column='VenueID', primary_key=True)  # Field name made lowercase.
    venue_name = models.CharField(db_column='Venue_Name', max_length=255)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity')  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Venue'

