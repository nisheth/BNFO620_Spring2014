# Create your models here.
from django.db import models
import sys


class Project(models.Model):
	id = models.AutoField(primary_key=True)
	projectID = models.CharField(max_length=10)
	projectDescription = models.CharField(max_length=100)

	def __unicode__(self):
		return self.projectID

	@classmethod
	def createProject(cls, projectID, projectDescription):
		project = Project(projectID=projectID, projectDescription=projectDescription)
		project.save()
		return project


class Sample(models.Model):
	id = models.AutoField(primary_key=True)
	project = models.ForeignKey(Project)
	sampleID = models.CharField(max_length=50)

	def __unicode__(self):
		return self.sampleID
	
	@classmethod
	def createSample(cls, project, sampleID):
		sample = Sample(project=project, sampleID=sampleID)
		sample.save()
		return sample


class SampleVariables(models.Model):
	id = models.AutoField(primary_key=True)
	sample = models.ForeignKey(Sample)
	date = models.CharField(max_length=10)
	barcode = models.CharField(max_length=6)
	
	def __unicode__(self):
		return self.sample

	@classmethod
	def createSampleVariables(cls, sample, date, barcode):
		samplevariables = SampleVariables(sample=sample, date=date, barcode=barcode)
		samplevariables.save()
		return samplevariables


class Read(models.Model):
	id = models.AutoField(primary_key=True)
	sample = models.ForeignKey(Sample)
	readID = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.readID

	@classmethod
	def createRead(cls, sample, readID):
		read = Read(sample=sample, readID=readID)
		read.save()
		return read


class ClassificationMethod(models.Model):
	id = models.AutoField(primary_key=True)
	methodID = models.IntegerField()
	methodDescription = models.CharField(max_length=100)
	methodcontactname = models.CharField(max_length=50)
	methodcontactemail = models.EmailFiled()
	
	def __unicode__(self):
		return self.methodID

	@classmethod
	def createClassificationMethod(cls, methodID, methodDescription, methodcontactname, methodcontactemail)
		classificationmethod = ClassificationMethod(methodID=methodID, methodDescription=methodDescription, methodcontactname=methodcontactname, methodcontactemail=methodcontactemail)
		classificationmethod.save()
		return classificationmethod


class TaxaCode(models.Model):
	id = models.AutoField(primary_key=True)
	level = models.CharField(max_length=20)
	code = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.level
	
	@classmethod
	def createTaxaCode(cls, level, code):
		taxacode = TaxaCode(level=level, code=code)
		taxacode.save()
		return taxacode


class ReadAssignment(models.Model):
	id = models.AutoField(primary_key=True)
	read = models.ForeignKey(Read)
	classificationmethod = models.ForeignKey(ClassificationMethod)
	taxa = models.ManytoManyField(TaxaCode)
	taxaname = models.CharField(max_length=50)
	taxascore = models.FloatField()
	
	def __unicode__(self):
		return_str = self.read + " - " + self.taxa
		return return_str

	@classmethod
	def createReadAssignment(cls, read, classificationmethod, taxa, taxaname, taxascore):
		readassignment = ReadAssignment(read=read, classificationmethod=classificationmethod, taxa=taxa, taxaname=taxaname, taxascore=taxascore)
		readassignment.save()
		return readassignment


class ProfileSummary(models.Model):
	id = models.AutoField(primary_key=True)
	sample = models.ForeignKey(Sample)
	classificationmethod = models.ForeignKey(ClassificationMethod)
	taxa = models.ManytoManyField(TaxaCode)
	taxaname = models.CharField(max_length=50)
	numreads = models.IntegerField()
	perctotal = models.FloatField()
	avgscore = models.FloatField()

	def __unicode__(self):
		return_str = self.sample + " - " + self.taxa
		return return_str

	@classmethod
	def createProfileSummary(cls, sample, classificationmethod, taxa, taxaname, numreads, perctotal, avgscore):
		profilesummary = ProfileSummary(sample=sample, classificationmethod=classificationmethod, taxa=taxa, taxaname=taxaname, numreads=numreads, perctotal=perctotal, avgscore=avgscore)
		profilesummary.save()
		return profilesummary
	





