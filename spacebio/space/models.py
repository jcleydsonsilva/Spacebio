from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(default='')

    class Meta:
        db_table = 'space_status'

class NetPrecision(models.Model):
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(default='')

    class Meta:
        db_table = 'space_netprecision'

class LaunchServiceProvider(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    url = models.URLField()
    description = models.TextField(default='')
    
    class Meta:
        db_table = 'space_launchserviceprovider'

class RocketConfiguration(models.Model):
    name = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    variant = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(default='')

    class Meta:
        db_table = 'space_rocketconfiguration'

class Rocket(models.Model):
    configuration = models.ForeignKey(RocketConfiguration, on_delete=models.CASCADE)
    description = models.TextField(default='')
    
    class Meta:
        db_table = 'space_rocket'

class Orbit(models.Model):
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(default='')

    class Meta:
        db_table = 'space_orbit'

class Agency(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    country_code = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    administrator = models.CharField(max_length=255, null=True, blank=True)
    founding_year = models.CharField(max_length=4, null=True, blank=True)
    info_url = models.URLField(blank=True, default='')
    wiki_url = models.URLField(blank=True, default='')
    logo_url = models.URLField(null=True, blank=True, default='')
    image_url = models.URLField(null=True, blank=True, default='')
    
    def save(self, *args, **kwargs):
        if self.description is None:
            self.description = ''
        if self.info_url is None:
            self.info_url = ''
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'space_agency'

class Mission(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    type = models.CharField(max_length=50)
    orbit = models.ForeignKey(Orbit, on_delete=models.CASCADE)
    agencies = models.ManyToManyField(Agency)

    class Meta:
        db_table = 'space_mission'

class Location(models.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    map_image = models.URLField()
    timezone_name = models.CharField(max_length=50)
    total_launch_count = models.IntegerField()
    total_landing_count = models.IntegerField()
    description = models.TextField(default='')

    class Meta:
        db_table = 'space_location'

class Pad(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    map_url = models.URLField()
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    total_launch_count = models.IntegerField()
    description = models.TextField(default='')

    class Meta:
        db_table = 'space_pad'

class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    image_url = models.URLField(blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(null=True, blank=True)
    info_url = models.URLField(blank=True, default='')
    wiki_url = models.URLField(blank=True)
    agencies = models.ManyToManyField(Agency)
    type = models.CharField(max_length=50)
    description = models.TextField(default='')

    class Meta:
        db_table = 'space_program'

class Launch(models.Model):
    launch_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    last_updated = models.DateTimeField()
    net = models.DateTimeField()
    window_end = models.DateTimeField()
    window_start = models.DateTimeField()
    net_precision = models.ForeignKey(NetPrecision, on_delete=models.CASCADE)
    launch_service_provider = models.ForeignKey(LaunchServiceProvider, on_delete=models.CASCADE)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    webcast_live = models.BooleanField(default=False)
    image = models.URLField(null=True, blank=True)
    infographic = models.URLField(null=True, blank=True)
    programs = models.ManyToManyField(Program)

    class Meta:
        db_table = 'space_launch'

class News(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField()
    news_site = models.CharField(max_length=100)
    summary = models.TextField()
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    featured = models.BooleanField()
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE, null=True, blank=True)
    # TODO: Add event field here. Needs to create agencies, launches, expeditios, spacestations and program models/tables first
    
    class Meta:
        db_table = 'space_news'