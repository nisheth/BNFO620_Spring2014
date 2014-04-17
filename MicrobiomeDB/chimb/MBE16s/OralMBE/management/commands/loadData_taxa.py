__author__ = 'Bryan'
import csv
from django.core.management.base import BaseCommand, CommandError
from OralMBE.models import Taxa
import sys

class Command(BaseCommand):
    args = '<sampleFile>'              #arguments from command-line
    help = 'Loads flat file of taxa and taxa data into database, ' \
           'to run use the command: python manage.py loadData_taxa <filename>'       #message displayed upon help command

    def handle(self, *args, **options):
        for filename in args:       #for each of the files
            try:                    #try to open the file
                taxanomiesList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
            except csv.Error, e:    #if it fails throw an error
                print e


            for taxan in taxanomiesList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
                #print taxan
                print 'loading taxa: ', taxan['name']
                #print >> sys.stdout, sample
                #print sample['project']
                #print sample['name']
                #projectname = sample['project']
                #projectname = projectname.strip()
                #newproject = Project.objects.get(name=projectname)

                newtaxa = Taxa.createTaxa(taxa_id=taxan['taxa_id'],
                                          name=taxan['name'],
                                          level=taxan['level'],
                                          parent_taxa_id=taxan['parent_taxa_id'])

            self.stdout.write("Loaded all taxas from file")
