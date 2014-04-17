import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeDBApp.models import ReadAssignment
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of projects into the database, to run use the command: python manage.py loadProject <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
		for filename in args:       #for each of the files
			try:                    #try to open the file
				read_assignment = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
			except csv.Error, e:    #if it fails throw an error
				print e

		self.stdout.write("Loading Read Assignment...")


		for read in read_assignment:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
			read = ReadAssignment.createReadAssignment(read['ReadID'],read['Method-id'],read['Taxa-Name'],read['Score'])

		self.stdout.write("Loaded all Read Assignment in file")