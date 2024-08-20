from django.db import models

class LaunchStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = 'space_launch_status'
        

class Updates(models.Model):
    id = models.AutoField(primary_key=True)
    profile_image = models.URLField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    info_url = models.URLField(null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'space_updates'
        
class NetPrecision(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField()
    
    class Meta:
        db_table = 'space_net_precicion'


class ProgramType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'space_program_type'
        
class Program(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    agencies = models.ManyToManyField('Agency')
    image_url = models.URLField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    info_url = models.URLField(blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)
    mission_patches = models.ManyToManyField('MissionPatches', related_name='programs')
    type = models.ForeignKey(ProgramType, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'space_program'

class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    type = models.CharField(max_length=50)
    country_code = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    administrator = models.CharField(max_length=100, blank=True, null=True)
    founding_year = models.CharField(max_length=4, blank=True, null=True)
    launchers = models.CharField(max_length=255, blank=True, null=True)
    spacecraft = models.CharField(max_length=255, blank=True, null=True)
    parent = models.CharField(max_length=255, blank=True, null=True)
    launch_library_url = models.URLField(blank=True, null=True)
    total_launch_count = models.IntegerField(blank=True, null=True)
    successful_launches = models.IntegerField(blank=True, null=True)
    consecutive_successful_launches = models.IntegerField(blank=True, null=True)
    failed_launches = models.IntegerField(blank=True, null=True)
    pending_launches = models.IntegerField(blank=True, null=True)
    successful_landings = models.IntegerField(blank=True, null=True)
    failed_landings = models.IntegerField(blank=True, null=True)
    attempted_landings = models.IntegerField(blank=True, null=True)
    consecutive_successful_landings = models.IntegerField(blank=True, null=True)
    info_url = models.URLField(blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    nation_url = models.URLField(blank=True, null=True)
    launcher_list = models.ManyToManyField('LauncherConfig', related_name='launcher_agencies')
    spacecraft_list = models.ManyToManyField('SpacecraftConfig', related_name='spacecraft_agencies')
    
    
    class Meta:
        db_table = 'space_agency'

class SpacecraftType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'space_spacecraft_type'

class SpacecraftConfig(models.Model):    
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(SpacecraftType, on_delete=models.CASCADE, null=True, blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, blank=True)
    in_use = models.BooleanField()
    capability = models.CharField(max_length=100, blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    maiden_flight = models.DateTimeField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    diameter = models.FloatField(blank=True, null=True)
    human_rated = models.BooleanField()
    crew_capacity = models.IntegerField(blank=True, null=True)
    payload_capacity = models.IntegerField(blank=True, null=True)
    payload_return_capacity = models.IntegerField(blank=True, null=True)
    flight_life = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    nation_url = models.URLField(blank=True, null=True)
    wiki_link = models.URLField(blank=True, null=True)
    info_link = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'space_spacecraft_config'

class SpacecraftStatus(models.Model):
    id = models.IntegerField(primary_key=True)    
    name = models.CharField(max_length=100)
        
    class Meta:
        db_table = 'space_spacecraft_status'
    
class Spacecraft(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    is_placeholder = models.BooleanField()
    in_space = models.BooleanField()
    time_in_space = models.CharField(blank=True, null=True)
    time_docked = models.CharField(blank=True, null=True)
    flights_count = models.IntegerField(blank=True, null=True)
    mission_ends_count = models.IntegerField(blank=True, null=True)
    status = models.ForeignKey(SpacecraftStatus, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    spacecraft_config = models.ForeignKey(SpacecraftConfig, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'space_spacecraft'


class AstronautStatus(models.Model):
    id = models.IntegerField(primary_key=True)    
    name = models.CharField(max_length=100)
        
    class Meta:
        db_table = 'space_astronaut_status'

    
class AstronautType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)  

    class Meta:
        db_table = 'space_astronaut_type'
        
        

class AstronautRole(models.Model):
    id = models.IntegerField(primary_key=True)    
    role = models.CharField(max_length=100)
    priority = models.IntegerField()
    
    class Meta:
        db_table = 'space_astronaut_role'
        
        

class Astronaut(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.ForeignKey(AstronautStatus, on_delete=models.CASCADE)
    type = models.ForeignKey(AstronautType, on_delete=models.CASCADE)
    in_space = models.BooleanField()
    time_in_space = models.CharField(max_length=100, blank=True, null=True)
    eva_time = models.CharField(max_length=100, blank=True, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    profile_image_thumbnail = models.URLField(blank=True, null=True)
    wiki = models.URLField(blank=True, null=True)
    flights = models.ManyToManyField('Launch')
    landings = models.ManyToManyField('SpacecraftFlight')
    flights_count = models.IntegerField(blank=True, null=True)
    landings_count = models.IntegerField(blank=True, null=True)
    spacewalks_count = models.IntegerField(blank=True, null=True)
    last_flight = models.DateTimeField(blank=True, null=True)
    first_flight = models.DateTimeField(blank=True, null=True)
    spacewalks = models.ManyToManyField('Spacewalk')
    
    class Meta:
        db_table = 'space_astronaut'
    
    
    
class Spacewalk(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    crew = models.ManyToManyField('Crew')
    spacestation = models.ForeignKey('Spacestation', on_delete=models.CASCADE)
    expedition = models.ForeignKey('Expedition', on_delete=models.CASCADE, related_name='related_spacewalks')
    spacecraft_flight = models.ForeignKey('SpacecraftFlight', on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey('DockingEvent', on_delete=models.CASCADE, null=True, blank=True)
    program = models.ManyToManyField('Program')
    
    class Meta:
        db_table = 'space_spacewalk'
    
class Crew(models.Model):
    id = models.IntegerField(primary_key=True)
    role = models.ForeignKey(AstronautRole, on_delete=models.CASCADE)
    astronaut = models.ForeignKey(Astronaut, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'space_crew'
        
    
class SpacecraftFlight(models.Model):
    id = models.IntegerField(primary_key=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    mission_end = models.DateTimeField(blank=True, null=True) 
    launch_crew = models.ManyToManyField(Crew, related_name='launched_spacecraft_flights')
    onboard_crew = models.ManyToManyField(Crew, related_name='onboard_spacecraft_flights')
    landing_crew = models.ManyToManyField(Crew, related_name='landed_spacecraft_flights')
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE)
    launch = models.ForeignKey('Launch', on_delete=models.CASCADE)
    landing = models.ForeignKey('Landing', on_delete=models.CASCADE)
    docking_events = models.ManyToManyField('DockingEvent')
    
    class Meta:
        db_table = 'space_spacecraft_flight'
    
    
class DockingEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    launch_id = models.ForeignKey('Launch', on_delete=models.CASCADE)
    docking = models.DateTimeField(null=True, blank=True)
    departure = models.DateTimeField(null=True, blank=True)
    flight_vehicle = models.ForeignKey(SpacecraftFlight, on_delete=models.CASCADE)
    docking_location = models.ForeignKey('DockingLocation', on_delete=models.CASCADE)
    space_station = models.ForeignKey('Spacestation', on_delete=models.CASCADE)
        
    class Meta:
        db_table = 'space_docking_event'
        
        
    
class DockingLocation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    spacestation = models.ForeignKey('Spacestation', on_delete=models.CASCADE)
    docked = models.ManyToManyField(DockingEvent)

    class Meta:
        db_table = 'space_docking_location'
        
        

class SpacestationStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)    
    
    class Meta:
        db_table = 'space_spacestation_status'
        
    
class Spacestation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.ForeignKey(SpacestationStatus, on_delete=models.CASCADE)
    type = models.ForeignKey(AstronautType, on_delete=models.CASCADE)
    founded = models.DateField(blank=True, null=True)
    deorbited = models.DateField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    orbit = models.CharField(max_length=100, blank=True, null=True)
    onboard_crew = models.IntegerField(blank=True, null=True)
    docked_vehicles = models.IntegerField(blank=True, null=True)
    owners = models.ManyToManyField('Agency')
    active_expeditions = models.ManyToManyField('Expedition', related_name='station_expeditions')
    docking_location = models.ForeignKey('Spacestation', on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = 'space_spacestation'    


    
class Expedition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    spacestation = models.ForeignKey('Spacestation', on_delete=models.CASCADE, related_name='related_expeditions')
    crew = models.ManyToManyField('Crew')
    mission_patches = models.ManyToManyField('MissionPatches')
    spacewalks = models.ManyToManyField('Spacewalk', related_name='related_expeditions')
        
    class Meta:
        db_table = 'space_expedition'
        
            
    
class MissionPatches(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    priority = models.IntegerField()    
    image_url = models.URLField(blank=True, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, blank=True, null=True)
    launches = models.ManyToManyField('Launch')
    expeditions = models.ManyToManyField('Expedition')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table = 'space_mission_patches'

class Configuration(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    reusable = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    family = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
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
     
    class Meta:
        db_table = 'space_configuration'
    
class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    map_image = models.URLField(blank=True, null=True)
    timezone_name = models.CharField(max_length=50)
    total_launch_count = models.IntegerField(blank=True, null=True)
    total_landing_count = models.IntegerField(blank=True, null=True)
    pads = models.ManyToManyField('Pad', related_name='locations')    

    class Meta:
        db_table = 'space_location'
    
class LandingLocation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    successful_landings = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'space_landing_location'

class LandingType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'space_landing_type'


class Landing(models.Model):
    id = models.IntegerField(primary_key=True)
    attempt = models.BooleanField()
    success = models.BooleanField()
    description = models.TextField(blank=True, null=True)
    downrange_distance = models.FloatField(blank=True, null=True)
    location = models.ForeignKey(LandingLocation, on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(LandingType, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'space_landing'  
    
class LauncherConfig(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    reusable = models.BooleanField()
    description = models.TextField(blank=True, null=True)
    family = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, blank=True)
    program = models.ManyToManyField(Program)
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

    class Meta:
        db_table = 'space_launcher_config'

    
class Launcher(models.Model):
    id = models.IntegerField(primary_key=True)
    flight_proven = models.BooleanField()
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    is_placeholder = models.BooleanField()
    status = models.CharField(max_length=100, blank=True, null=True)
    details = models.CharField(max_length=255, blank=True, null=True)
    launcher_config = models.ForeignKey(LauncherConfig, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)   
    successful_landings = models.IntegerField(blank=True, null=True)
    attempted_landings = models.IntegerField(blank=True, null=True)
    flights = models.IntegerField(blank=True, null=True)
    last_launch_date = models.DateField(blank=True, null=True)
    first_launch_date = models.DateField(blank=True, null=True)
        
    class Meta:
        db_table = 'space_launcher'

class LauncherStage(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100)
    reused = models.BooleanField(blank=True, null=True)
    launcher_flight_number = models.IntegerField(blank=True, null=True)
    launcher = models.ForeignKey(Launcher, on_delete=models.CASCADE, null=True, blank=True)
    landing = models.ForeignKey(Landing, on_delete=models.CASCADE, null=True, blank=True)
    previous_flight_date = models.DateField(blank=True, null=True)
    turn_around_time_days = models.IntegerField(blank=True, null=True)
    previous_flight = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'space_launcher_stage'
        

class Rocket(models.Model):
    id = models.IntegerField(primary_key=True)
    configuration = models.ForeignKey(LauncherConfig, on_delete=models.CASCADE, null=True, blank=True)
    launcher_stage = models.ManyToManyField(LauncherStage,  default=1)
    spacecraft_stage = models.CharField(max_length=255, blank=True, null=True)

    class Meta: 
        db_table = 'space_rocket'
    
class Orbit(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)

    class Meta:
        db_table = 'space_orbit'
    
    
class Pad(models.Model):
    id = models.IntegerField(primary_key=True)
    agency_id  = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    info_url = models.URLField(blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)
    map_url = models.URLField(blank=True, null=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    map_image = models.URLField(blank=True, null=True)
    total_launch_count = models.IntegerField(blank=True, null=True)
    orbital_launch_attempt_count = models.IntegerField(blank=True, null=True)
    
    class Meta: 
        db_table = 'space_pad'
    

class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    class Meta:
        db_table = 'space_language'

class InfoURLType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta: 
        db_table = 'space_info_url_type'


class InfoURLs(models.Model):
    launch = models.ForeignKey('Launch', related_name='info_urls', on_delete=models.CASCADE, null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    feature_image = models.URLField(blank=True, null=True)
    url = models.URLField()
    type = models.ForeignKey(InfoURLType, on_delete=models.CASCADE, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'space_info_urls'
    
class VidURLType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta: 
        db_table = 'space_vid_url_type'
    
    
    
class VidURLs(models.Model):
    launch = models.ForeignKey('Launch', related_name='vid_urls', on_delete=models.CASCADE)
    priority = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    feature_image = models.URLField(blank=True, null=True)
    url = models.URLField()
    type = models.ForeignKey(VidURLType, on_delete=models.CASCADE, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'space_vid_urls'
        
    def get_embedded_url(self):
        if 'watch?v=' in self.url:
            return self.url.replace('watch?v=', 'embed/')
        elif 'youtube.com/live/' in self.url:
            return self.url.replace('youtube.com/live/', 'youtube.com/embed/')
        else:
            return self.url
    

class Mission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    launch_designator = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    orbit = models.ForeignKey(Orbit, on_delete=models.CASCADE, null=True, blank=True)
    agencies = models.ManyToManyField(Agency)
    info_urls = models.ManyToManyField(InfoURLs)
    vid_urls = models.ManyToManyField(VidURLs)   
    
    class Meta:
        db_table = 'space_mission'
        
        
class TimelineEventType(models.Model):
    id = models.IntegerField(primary_key=True)
    abbrev = models.CharField(max_length=50)    
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'space_timeline_event_type'
    
    
class Launch(models.Model):
    id = models.CharField(max_length=36, primary_key=True) # UUID. Ex: "id": "e3df2ecd-c239-472f-95e4-2b89b4f75800"
    slug = models.CharField(max_length=255)
    flightclub_url = models.URLField(null=True, blank=True)
    r_spacex_api_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    status = models.ForeignKey(LaunchStatus, on_delete=models.CASCADE, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    updates = models.ManyToManyField(Updates)
    net = models.DateTimeField(null=True, blank=True)
    net_precision = models.ForeignKey(NetPrecision, on_delete=models.CASCADE, null=True, blank=True)
    window_end = models.DateTimeField(null=True, blank=True)
    window_start = models.DateTimeField(null=True, blank=True)
    probability = models.IntegerField(null=True, blank=True)
    weather_concerns = models.CharField(max_length=255, null=True, blank=True)
    holdreason = models.CharField(max_length=255, null=True, blank=True)
    failreason = models.TextField(null=True, blank=True)
    hashtag = models.CharField(max_length=255, null=True, blank=True)
    launch_service_provider = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, blank=True)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE, null=True, blank=True)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, null=True, blank=True)
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE, null=True, blank=True)
    InfoURLs = models.ManyToManyField(InfoURLs, related_name='launches')
    VidURLs = models.ManyToManyField(VidURLs, related_name='launches')
    webcast_live = models.BooleanField(null=True, blank=True)
    timeline = models.ManyToManyField('TimelineEventType')
    image = models.URLField(null=True, blank=True)
    infographic = models.URLField(null=True, blank=True)
    program = models.ManyToManyField(Program)
    orbital_launch_attempt_count = models.IntegerField(null=True, blank=True)
    location_launch_attempt_count = models.IntegerField(null=True, blank=True)
    pad_launch_attempt_count = models.IntegerField(null=True, blank=True)
    agency_launch_attempt_count = models.IntegerField(null=True, blank=True)
    orbital_launch_attempt_count_year = models.IntegerField(null=True, blank=True)
    location_launch_attempt_count_year = models.IntegerField(null=True, blank=True)
    pad_launch_attempt_count_year = models.IntegerField(null=True, blank=True)
    agency_launch_attempt_count_year = models.IntegerField(null=True, blank=True)
    pad_turnaround = models.CharField(max_length=255, null=True, blank=True)
    mission_patches = models.ManyToManyField(MissionPatches)
        
    class Meta:
        db_table = 'space_launch'
    


class News(models.Model):
    title = models.TextField()
    url = models.TextField()
    image_url = models.TextField()
    news_site = models.TextField()
    summary = models.TextField()
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    featured = models.BooleanField()
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE, null=True, blank=True)
    # TODO: Add event field here. Needs to create agencies, launches, expeditios, spacestations and program models/tables first
    
    class Meta:
        db_table = 'space_news'

class ExecutionLog(models.Model):
    script_name = models.CharField(max_length=100)
    url = models.URLField(unique=True, default='No url provided')
    last_executed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.script_name} for {self.url} last executed at {self.last_executed}"