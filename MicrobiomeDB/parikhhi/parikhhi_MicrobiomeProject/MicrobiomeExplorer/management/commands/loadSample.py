__author__ = 'Hardik'

import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeExplorer.models import Project, Sample
import sys

class Command(BaseCommand):
	args = '<ProjectName SampleFile>'              #arguments from command-line
	help = 'Loads flat file of samples into the database, to run use the command: python manage.py loadSample <ProjectName SampleFile>'       #message displayed upon help command


	def handle(self, *args, **options):
	
		try:
			sampleList = csv.DictReader(open(args[1], "rb"),delimiter="\t")
		except csv.Error, e:
			print e

		self.stdout.write("Loading samples...")
		
		project = Project.objects.get(name=args[0])
		print project
	
		for eachsample in sampleList:
			print eachsample
			sample = Sample.createSample(project, eachsample['SampleName'])

		self.stdout.write("Loaded all samples in file")


