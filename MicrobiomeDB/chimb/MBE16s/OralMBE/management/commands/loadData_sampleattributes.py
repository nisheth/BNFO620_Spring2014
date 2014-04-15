__author__ = 'Bryan'
import csv
from django.core.management.base import BaseCommand, CommandError
from OralMBE.models import SampleAttribute
from OralMBE.models import Sample
import sys

class Command(BaseCommand):
    args = '<sampleattributesFile>'              #arguments from command-line
    help = 'Loads flat file of attributes into database, to run use the command: python manage.py loadData_sampleattributes <filename>'       #message displayed upon help command

    def handle(self, *args, **options):
        for filename in args:       #for each of the files
            try:                    #try to open the file
                attributeList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
            except csv.Error, e:    #if it fails throw an error
                print e

            #print attributeList
            for attribute in attributeList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)



                samplename = attribute['sample ']
                samplename = samplename.strip()
                sampleobj = Sample.objects.get(name=samplename)
                newsample = SampleAttribute.createSampleAttribute(sampleobj,attribute['attribute '],attribute['value'])

            self.stdout.write("Loaded all attributes in file")
