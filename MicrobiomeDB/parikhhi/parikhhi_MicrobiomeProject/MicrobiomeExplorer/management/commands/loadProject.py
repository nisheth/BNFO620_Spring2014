__author__ = 'Hardik'

import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeExplorer.models import Project
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of projects into the database, to run use the command: python manage.py loadProject <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
		for filename in args:       #for each of the files
			try:                    #try to open the file
				projectList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
			except csv.Error, e:    #if it fails throw an error
				print e

		self.stdout.write("Loading projects...")


		for eachproject in projectList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
			print >> sys.stderr, eachproject
			project = Project.createProject(eachproject['Name'],eachproject['Description'],eachproject['ContactName'],eachproject['ContactEmail'])
	
		self.stdout.write("Loaded all projects in file")
