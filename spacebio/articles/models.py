from django.db import models

class SpaceExploration(models.Model):
    id = models.TextField(primary_key=True)
    source = models.TextField(null=True, default='')
    pmid = models.TextField(null=True, default='')
    doi = models.TextField(null=True, default='')
    title = models.TextField(null=True, default='')
    authorstring = models.TextField(null=True, default='')
    journaltitle = models.TextField(null=True, default='')
    pubyear = models.TextField(null=True, default='')
    journalissn = models.TextField(null=True, default='')
    pubtype = models.TextField(null=True, default='')
    isopenaccess = models.TextField(null=True, default='')
    inepmc = models.TextField(null=True, default='')
    inpmc = models.TextField(null=True, default='')
    haspdf = models.TextField(null=True, default='')
    hasbook = models.TextField(null=True, default='')
    hassuppl = models.TextField(null=True, default='')
    citedbycount = models.TextField(null=True, default='')
    hasreferences = models.TextField(null=True, default='')
    hastextminedterms = models.TextField(null=True, default='')
    hasdbcrossreferences = models.TextField(null=True, default='')
    haslabslinks = models.TextField(null=True, default='')
    hastmaccessionnumbers = models.TextField(null=True, default='')
    firstindexdate = models.TextField(null=True, default='')
    firstpublicationdate = models.TextField(null=True, default='')
    issue = models.TextField(null=True, default='')
    journalvolume = models.TextField(null=True, default='')
    pageinfo = models.TextField(null=True, default='')
    pmcid = models.TextField(null=True, default='')
    abstract = models.TextField(null=True, default='')
    affiliation = models.TextField(null=True, default='')

    class Meta:
        db_table = 'spaceexploration'

    def __str__(self):
        return self.title
