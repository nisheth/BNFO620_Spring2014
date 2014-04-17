import csv
from django.core.management.base import BaseCommand, CommandError
from microbiome.models import SampleVariable, Sample
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of projects into the database, to run use the command: python manage.py loadProject <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
            for filename in args:       #for each of the files
                try:                    #try to open the file
                    sampleList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
		except csv.Error, e:    #if it fails throw an error
		    print e

	    self.stdout.write("Loading sample...")


	    for sample in sampleList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
                print >> sys.stderr, sample
                samp = Sample.objects.get(name = sample['Sample_id'])
		sample = SampleVariable.createSampleVariable(samp, sample['Variable'], sample['Value'])
	
	    self.stdout.write("Loaded all samples and its variables from file")
