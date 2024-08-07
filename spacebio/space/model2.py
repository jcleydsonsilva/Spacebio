from django.db import models


class Launch(models.Model):
    id = models.IntegerField(primary_key=True)
    launch_id = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    flightclub_url = models.URLField()
    r_spacex_api_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_updated = models.DateTimeField()
    net = models.DateTimeField()
    window_end = models.DateTimeField()
    window_start = models.DateTimeField()
    probability = models.IntegerField()
    weather_concerns = models.CharField(max_length=255)
    holdreason = models.CharField(max_length=255)
    failreason = models.CharField(max_length=255)
    hashtag = models.CharField(max_length=255)
    webcast_live = models.BooleanField()
    image = models.URLField(null=True, blank=True)
    infographic = models.URLField(null=True, blank=True)
    orbital_launch_attempt_count = models.IntegerField(null=True, blank=True)
    location_launch_attempt_count = models.IntegerField(null=True, blank=True)
    pad_launch_attempt_count = models.IntegerField(null=True, blank=True)
    agency_launch_attempt_count = models.IntegerField(null=True, blank=True)
    orbital_launch_attempt_count_year = models.IntegerField(null=True, blank=True)
    location_launch_attempt_count_year = models.IntegerField(null=True, blank=True)
    pad_launch_attempt_count_year = models.IntegerField(null=True, blank=True)
    agency_launch_attempt_count_year = models.IntegerField(null=True, blank=True)
    pad_turnaround = models.CharField(max_length=255, null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    updates = models.ManyToManyField('Updates')
    net_precision = models.ForeignKey('NetPrecicion', on_delete=models.CASCADE)
    launch_service_provider = models.ForeignKey('LaunchServiceProvider', on_delete=models.CASCADE)
    rocket = models.ForeignKey('Rocket', on_delete=models.CASCADE)
    mission = models.ForeignKey('Mission', on_delete=models.CASCADE)
    pad = models.ForeignKey('Pad', on_delete=models.CASCADE)
    
    
    class Meta:
        db_table = 'space_launch'

class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = 'space_status'
        

class Updates(models.Model):
    id = models.IntegerField(primary_key=True)
    profile_image = models.URLField(blank=True)
    comment = models.TextField(blank=True)
    info_url = models.URLField(blank=True)
    created_by = models.CharField(max_length=255)
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'space_updates'
        
class NetPrecicion(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField()
    
    class Meta:
        db_table = 'space_net_precicion'
        
class LaunchServiceProvider(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    featured = models.BooleanField()
    type = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    administrator = models.CharField(max_length=255)
    founding_year = models.CharField(max_length=4)
    launchers = models.CharField(max_length=255)
    spacecraft = models.CharField(max_length=255)
    launch_library_url = models.URLField(blank=True)
    total_launch_count = models.IntegerField(null=True)
    consecutive_successful_launches = models.IntegerField(null=True)
    successful_launches = models.IntegerField(null=True)
    failed_launches = models.IntegerField(null=True)
    pending_launches = models.IntegerField(null=True)
    consecutive_successful_landings = models.IntegerField(null=True)
    successful_landings = models.IntegerField(null=True)
    failed_landings = models.IntegerField(null=True)
    attempted_landings = models.IntegerField(null=True)
    info_url = models.URLField(blank=True)
    wiki_url = models.URLField(blank=True)
    logo_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    nation_url = models.URLField(blank=True)
    
    class Meta:
        db_table = 'space_launch_service_providers'
        
class Manufacturer(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    type = models.CharField(max_length=50)
    country_code = models.CharField(max_length=10)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    administrator = models.CharField(max_length=255, blank=True, null=True)
    founding_year = models.CharField(max_length=4, blank=True, null=True)
    launchers = models.CharField(max_length=255, blank=True, null=True)
    spacecraft = models.CharField(max_length=255, blank=True, null=True)
    launch_library_url = models.URLField(blank=True, null=True)
    total_launch_count = models.IntegerField(blank=True, null=True)
    consecutive_successful_launches = models.IntegerField(blank=True, null=True)
    successful_launches = models.IntegerField(blank=True, null=True)
    failed_launches = models.IntegerField(blank=True, null=True)
    pending_launches = models.IntegerField(blank=True, null=True)
    consecutive_successful_landings = models.IntegerField(blank=True, null=True)
    successful_landings = models.IntegerField(blank=True, null=True)
    failed_landings = models.IntegerField(blank=True, null=True)
    attempted_landings = models.IntegerField(blank=True, null=True)
    info_url = models.URLField(blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    nation_url = models.URLField(blank=True, null=True)
        
class Program(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
class Agencies(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
        
class Configuration(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    reusable = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    family = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True)
    variant = models.CharField(max_length=50, blank=True, null=True)
    alias = models.CharField(max_length=50, blank=True, null=True)
    min_stage = models.IntegerField(blank=True, null=True)
    max_stage = models.IntegerField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    diameter = models.FloatField(blank=True, null=True)
    maiden_flight = models.DateField(blank=True, null=True)
    launch_cost = models.CharField(max_length=50, blank=True, null=True)
    launch_mass = models.IntegerField(blank=True, null=True)
    leo_capacity = models.IntegerField(blank=True, null=True)
    gto_capacity = models.IntegerField(blank=True, null=True)
    to_thrust = models.IntegerField(blank=True, null=True)
    apogee = models.IntegerField(blank=True, null=True)
    vehicle_range = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    info_url = models.URLField(blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)
    total_launch_count = models.IntegerField(blank=True, null=True)
    consecutive_successful_launches = models.IntegerField(blank=True, null=True)
    successful_launches = models.IntegerField(blank=True, null=True)
    failed_launches = models.IntegerField(blank=True, null=True)
    pending_launches = models.IntegerField(blank=True, null=True)
    attempted_landings = models.IntegerField(blank=True, null=True)
    successful_landings = models.IntegerField(blank=True, null=True)
    failed_landings = models.IntegerField(blank=True, null=True)
    consecutive_successful_landings = models.IntegerField(blank=True, null=True)


class Rocket(models.Model):
    id = models.IntegerField(primary_key=True)
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    spacecraft_stage = models.CharField(max_length=255, blank=True, null=True)