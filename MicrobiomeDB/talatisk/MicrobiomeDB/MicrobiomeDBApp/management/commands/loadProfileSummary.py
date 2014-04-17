import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeDBApp.models import ProfileSummary
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of projects into the database, to run use the command: python manage.py loadProject <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
		for filename in args:       #for each of the files
			try:                    #try to open the file
				profile_summary = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
			except csv.Error, e:    #if it fails throw an error
				print e

		self.stdout.write("Loading Profile Summary...")


		for profile in profile_summary:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
			profile = ProfileSummary.createProfileSummary(profile['Sample'],profile['Method'],profile['taxaName'],profile['NumRead'],profile['PercTotal'],profile['Qscore'])

		self.stdout.write("Loaded all Profile Summary in file")