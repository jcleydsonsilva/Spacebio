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
    # mission patches aqui
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    updates = models.ManyToManyField('Updates')
    net_precision = models.ForeignKey('NetPrecicion', on_delete=models.CASCADE)
    launch_service_provider = models.ForeignKey('LaunchServiceProvider', on_delete=models.CASCADE)
    rocket = models.ForeignKey('Rocket', on_delete=models.CASCADE)
    mission = models.ForeignKey('Mission', on_delete=models.CASCADE)
    pad = models.ForeignKey('Pad', on_delete=models.CASCADE)
    program = models.ManyToManyField('Program')
    
    
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
    image_url = models.URLField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    info_url = models.URLField(blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)
    agencies = models.ManyToManyField('Agencies')
    # mission_patches = [] olhar no json
    # type olhar no json
    
class ProgramType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class Agencies(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ProgramType, on_delete=models.CASCADE)
    # ver com urgencia no json como modelar Agencies

    
class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    map_image = models.URLField(blank=True, null=True)
    timezone_name = models.CharField(max_length=50)
    total_launch_count = models.IntegerField(blank=True, null=True)
    total_landing_count = models.IntegerField(blank=True, null=True)
    pads = models.ManyToManyField('Pad')
    


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
    spacecraft_stage = models.CharField(max_length=255, blank=True, null=True)


class launcher(models.Model):
    id = models.IntegerField(primary_key=True)
    details = models.CharField(max_length=255)
    flight_proven = models.BooleanField()
    serial_number = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    successful_landings = models.IntegerField(blank=True, null=True)
    attempted_landings = models.IntegerField(blank=True, null=True)
    flights = models.IntegerField(blank=True, null=True)
    last_launch_date = models.DateField(blank=True, null=True)
    first_launch_date = models.DateField(blank=True, null=True)
    
    
class LandingLocation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    successful_landings = models.IntegerField(blank=True, null=True)

class LandingType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)


class Landing(models.Model):
    id = models.IntegerField(primary_key=True)
    attempt = models.BooleanField()
    success = models.BooleanField()
    description = models.TextField(blank=True, null=True)
    downrange_distance = models.FloatField(blank=True, null=True)
    location = models.ForeignKey(LandingLocation, on_delete=models.CASCADE)
    type = models.ForeignKey(LandingType, on_delete=models.CASCADE)
    

class LauncherStage(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100)
    reused = models.BooleanField(blank=True, null=True)
    launcher_flight_number = models.IntegerField(blank=True, null=True)
    previous_flight_date = models.DateField(blank=True, null=True)
    turn_around_time_days = models.IntegerField(blank=True, null=True)
    previous_flight = models.BooleanField(blank=True, null=True)
    launcher = models.ForeignKey(launcher, on_delete=models.CASCADE)
    landing = models.ForeignKey(Landing, on_delete=models.CASCADE)

class Rocket(models.Model):
    id = models.IntegerField(primary_key=True)
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    spacecraft_stage = models.CharField(max_length=255, blank=True, null=True)
    launcher_stage = models.ForeignKey(LauncherStage, on_delete=models.CASCADE, null=True)
    # spacecraft_stage = models.CharField(max_length=255, blank=True, null=True) olhar no json pois vai virar muitas tabelas
    
    
class Orbit(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    
    
class Mission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    launch_designator = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    orbit = models.ForeignKey(Orbit, on_delete=models.CASCADE)
    # ver com urgência no json como modelar Agencies

    
    
class Pad(models.Model):
    id = models.IntegerField(primary_key=True)
    agency_id  = models.ForeignKey(Agencies, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    info_url = models.URLField(blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)
    map_url = models.URLField(blank=True, null=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    map_image = models.URLField(blank=True, null=True)
    total_launch_count = models.IntegerField(blank=True, null=True)
    orbital_launch_attempt_count = models.IntegerField(blank=True, null=True)
    

class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

class InfoURLType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

class InfoURLs(models.Model):
    launch = models.ForeignKey('Launch', related_name='info_urls', on_delete=models.CASCADE)
    priority = models.IntegerField()
    source = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    feature_image = models.URLField(blank=True, null=True)
    url = models.URLField()
    type = models.ForeignKey(InfoURLType, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    
class VidURLType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    
class VidURLs(models.Model):
    launch = models.ForeignKey('Launch', related_name='vid_urls', on_delete=models.CASCADE)
    priority = models.IntegerField()
    source = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    feature_image = models.URLField(blank=True, null=True)
    url = models.URLField()
    type = models.ForeignKey(VidURLType, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    