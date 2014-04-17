import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeDBApp.models import Project, Sample
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of samples into the database, to run use the command: python manage.py loadSample <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
		for filename in args:       #for each of the files
			try:                    #try to open the file
				sampleList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
			except csv.Error, e:    #if it fails throw an error
				print e

		self.stdout.write("Loading samples...")


		for s in sampleList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)

			project = Project.objects.get(name= s['Project'])
			sample = Sample.createSample(project, s['SampleName'])

		self.stdout.write("Loaded all samples in file")