import csv
from django.core.management.base import BaseCommand, CommandError
from MicrobiomeSnehalApp.models import ClassificationMethod
import sys

class Command(BaseCommand):
    args = '<adminFile>'              #arguments from command-line
    help = 'Loads flat file of authors into the database, to run use the command: python manage.py loadData <filename>'       #message displayed upon help command

    def handle(self, *args, **options):
        for filename in args:       #for each of the files
            try:                    #try to open the file
                classification_list = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
            except csv.Error, e:    #if it fails throw an error
                print e

            self.stdout.write("Loading Classification Data...")


            for classification in classification_list:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
                print >> sys.stdout, classification
                classification = ClassificationMethod.createClassification(classification['NAME'],classification['DESCRIPTION'],classification['CONTACT NAME'], classification['CONTACT EMAIL'])

            self.stdout.write("Loaded Classification Methods")
