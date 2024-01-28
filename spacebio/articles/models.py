from django.db import models

class SpaceExploration(models.Model):
    id = models.TextField(primary_key=True)
    source = models.TextField(null=True)
    pmid = models.TextField(null=True)
    doi = models.TextField(null=True)
    title = models.TextField(null=True)
    authorstring = models.TextField(null=True)
    journaltitle = models.TextField(null=True)
    pubyear = models.TextField(null=True)
    journalissn = models.TextField(null=True)
    pubtype = models.TextField(null=True)
    isopenaccess = models.TextField(null=True)
    inepmc = models.TextField(null=True)
    inpmc = models.TextField(null=True)
    haspdf = models.TextField(null=True)
    hasbook = models.TextField(null=True)
    hassuppl = models.TextField(null=True)
    citedbycount = models.TextField(null=True)
    hasreferences = models.TextField(null=True)
    hastextminedterms = models.TextField(null=True)
    hasdbcrossreferences = models.TextField(null=True)
    haslabslinks = models.TextField(null=True)
    hastmaccessionnumbers = models.TextField(null=True)
    firstindexdate = models.TextField(null=True)
    firstpublicationdate = models.TextField(null=True)
    issue = models.TextField(null=True)
    journalvolume = models.TextField(null=True)
    pageinfo = models.TextField(null=True)
    pmcid = models.TextField(null=True)
    abstract = models.TextField(null=True)
    affiliation = models.TextField(null=True)

    class Meta:
        db_table = 'spaceexploration'

    def __str__(self):
        return self.name