__author__ = 'Hardik'

import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeExplorer.models import Project, Sample, SampleVariable, Read, ClassificationMethod
import sys

class Command(BaseCommand):
	args = '<adminFile>'              #arguments from command-line
	help = 'Loads flat file of classification methods into the database, to run use the command: python manage.py loadClassificationMethod <filename>'       #message displayed upon help command

	def handle(self, *args, **options):
		for filename in args:       #for each of the files
			try:                    #try to open the file
				classificationmethodList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
			except csv.Error, e:    #if it fails throw an error
				print e

		self.stdout.write("Loading classification methods ...")


		for eachCMs in classificationmethodList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
			print eachCMs
			classificationmethod = ClassificationMethod.createClassificationMethod(eachCMs['MethodID'], eachCMs['Name'], eachCMs['Description'], eachCMs['ContactName'], eachCMs['ContactEmail'])

		self.stdout.write("Loaded all classification methods in file")


