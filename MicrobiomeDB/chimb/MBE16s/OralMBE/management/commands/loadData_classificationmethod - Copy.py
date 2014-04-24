__author__ = 'Bryan'
import csv
from django.core.management.base import BaseCommand, CommandError
from OralMBE.models import ClassificationMethod
import sys

class Command(BaseCommand):
    args = '<sampleFile>'              #arguments from command-line
    help = 'Loads flat file of classification methods into database, ' \
           'to run use the command: python manage.py loadData_classificationmethod <filename>'       #message displayed upon help command

    def handle(self, *args, **options):
        for filename in args:       #for each of the files
            try:                    #try to open the file
                cmethList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
            except csv.Error, e:    #if it fails throw an error
                print e


            for cmeth in cmethList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
                #print cmeth
                #projectname = sample['project']
                #projectname = projectname.strip()
                #newproject = Project.objects.get(name=projectname)
                newclassificationmethod = ClassificationMethod.createClassificationMethod(key=cmeth['key'],
                                                                                          description=cmeth['description'],
                                                                                          contactname=cmeth['contactname'],
                                                                                          contactemail=cmeth['contactemail'])

            self.stdout.write("Loaded all classification methods in file")
