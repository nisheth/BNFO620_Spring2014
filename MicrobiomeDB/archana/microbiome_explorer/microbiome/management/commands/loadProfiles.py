
import csv
from django.core.management.base import BaseCommand, CommandError
from microbiome.models import Sample, Taxonomy, Method, ProfileSummary
import sys


class Command(BaseCommand):
    args = '<ProfileSummaryFile>'              #arguments from command-line
    help = 'Loads Profile Summaries into the database, to run use the command: python manage.py loadProfileSummary <filename>'       #message displayed upon help command

    def handle(self, *args, **options):
        for filename in args:       #for each of the files
            try:                    #try to open the file
                profilesummaryList = csv.DictReader(open(filename, "rb"), delimiter='\t')      #open the file
            except csv.Error, e:    #if it fails throw an error
                print e

        self.stdout.write("Loading profile summaries...")

        for eachPS in profilesummaryList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
         #print >> sys.stderr, eachPS
         sample = Sample.objects.get(name=eachPS['Sample ID'])
         classificationmethod = Method.objects.get(method_id=eachPS['Method ID'])
         taxaID = Taxonomy.objects.get(name=eachPS['Taxa-Name'].strip(), level=eachPS['Taxa-Level'].strip())
         profilesummary = ProfileSummary.createProfileSummary(sample, classificationmethod, taxaID, eachPS['# of Reads'],
                                                         eachPS['% of Total'], eachPS['Avg-Score'])


