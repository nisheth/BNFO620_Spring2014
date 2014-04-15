__author__ = 'Bryan'
import csv
from django.core.management.base import BaseCommand, CommandError
from OralMBE.models import Project
from OralMBE.models import Sample
import sys

class Command(BaseCommand):
    args = '<sampleFile>'              #arguments from command-line
    help = 'Loads flat file of samples into database, to run use the command: python manage.py loadData_sample <filename>'       #message displayed upon help command

    def handle(self, *args, **options):
        for filename in args:       #for each of the files
            try:                    #try to open the file
                sampleList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
            except csv.Error, e:    #if it fails throw an error
                print e


            for sample in sampleList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
                #print >> sys.stdout, sample
                print sample['project']
                print sample['name']
                projectname = sample['project']
                projectname = projectname.strip()
                newproject = Project.objects.get(name=projectname)
                newsample = Sample.createSample(newproject,sample['name'])

            self.stdout.write("Loaded all samples in file")
