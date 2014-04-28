__author__ = 'Bryan'
import csv
from django.core.management.base import BaseCommand, CommandError
from OralMBE.models import Taxa
from OralMBE.models import Sample
from OralMBE.models import ClassificationMethod
from OralMBE.models import ProfileSummary
import sys

class Command(BaseCommand):
    args = '<profileFile>'              #arguments from command-line
    help = 'Loads flat file of profile summary data into database, ' \
           'to run use the command: python manage.py loadData_profilesummary <filename>'       #message displayed upon help command

    def handle(self, *args, **options):
        for filename in args:       #for each of the files
            try:                    #try to open the file
                profileList = csv.DictReader(open(filename,"rb"),delimiter='\t')      #open the file
            except csv.Error, e:    #if it fails throw an error
                print e


            for profile in profileList:     #for each row in the file (row is a dict using the header row as the keys and the values in the following rows as the values)
                print profile
                sample = Sample.objects.get(name=profile['Sample ID'])
                method = ClassificationMethod.objects.get(key=profile['Method ID'])
                taxa = Taxa.objects.get(name=profile['Taxa-Name'], level=profile['Taxa-Level'])

                newprosum = ProfileSummary.createProfileSummary(
                                              sample=sample,
                                              classificationmethod=method,
                                              taxa=taxa,
                                              numreads=profile['# of Reads'],
                                              perctotal=profile['% of Total'],
                                              avgscore=profile['Avg-Score']
                                          )

            self.stdout.write("Loaded all taxas from file")
