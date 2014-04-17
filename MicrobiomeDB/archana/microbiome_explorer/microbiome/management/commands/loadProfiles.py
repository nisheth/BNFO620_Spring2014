import csv
from django.core.management.base import BaseCommand, CommandError
from microbiome.models import Taxonomy, Method, Sample, ProfileSummary
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of projects into the database, to run use the command: python manage.py loadProject <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
            for filename in args:       #for each of the files
                try:                    #try to open the file
                    profileList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
		except csv.Error, e:    #if it fails throw an error
		    print e

	    self.stdout.write("Loading profiles...")


	    for profile in profileList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
                print >> sys.stderr, profile

                sample = Sample.objects.get(name = profile['SampleID'])
                method = Method.objects.get(name = profile['Method-id'])
                taxa = Taxonomy.objects.get(name = profile['Taxa-name'])
		prof = ProfileSummary.createProfileSummary(sample, method, taxa, profile['#_of_reads'], profile['%_of_total'], profile['Avg_Score'])
	
	    self.stdout.write("Loaded all profiles from file")
