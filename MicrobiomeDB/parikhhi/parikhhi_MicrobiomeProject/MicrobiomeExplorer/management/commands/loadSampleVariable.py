__author__ = 'Hardik'

import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeExplorer.models import Project, Sample, SampleVariable
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of sample variables into the database, to run use the command: python manage.py loadSampleVariable <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
		for filename in args:       #for each of the files
			try:                    #try to open the file
				samplevarList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
			except csv.Error, e:    #if it fails throw an error
				print e

		self.stdout.write("Loading sample variabless...")


		for eachsamplevar in samplevarList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
			print >> sys.stderr, eachsamplevar	
			sample = Sample.objects.get(name=eachsamplevar['Sample Name'])
			print sample
			samplevariable = SampleVariable.createSampleVariable(sample, eachsamplevar['Sample Variable'], eachsamplevar['Variable Value'])

		self.stdout.write("Loaded all sample variables in file")
