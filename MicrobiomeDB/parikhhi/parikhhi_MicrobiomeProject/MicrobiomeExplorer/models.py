# Create your models here.
from django.db import models
import sys


class Project(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	contactname = models.CharField(max_length=50)
	contactemail = models.EmailField()

	def __unicode__(self):
		return self.name

	@classmethod
	def createProject(cls, name, description, contactname, contactemail):
		project = Project(name=name, description=description, contactname=contactname, contactemail=contactemail)
		project.save()
		return project


class Sample(models.Model):
	id = models.AutoField(primary_key=True)
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name
	
	@classmethod
	def createSample(cls, project, name):
		sample = Sample(project=project, name=name)
		sample.save()
		return sample


class SampleVariables(models.Model):
	id = models.AutoField(primary_key=True)
	sample = models.ForeignKey(Sample)
	attribute = models.CharField(max_length=50)
	value = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.sample

	@classmethod
	def createSampleVariables(cls, sample, attribute, value):
		samplevariables = SampleVariables(sample=sample, attribute=attribute, value=value)
		samplevariables.save()
		return samplevariables


class Read(models.Model):
	id = models.AutoField(primary_key=True)
	sample = models.ForeignKey(Sample)
	name = models.CharField(max_length=50)
	length = models.IntegerField()
	qualityscore = models.FloatField()
	seq = models.TextField(null=True)
	
	def __unicode__(self):
		return self.name

	@classmethod
	# Seq can be null. Not included in following create function. Add separately
	def createRead(cls, sample, name, length, qualityscore):
		read = Read(sample=sample, name=name, length=length, qualityscore=qualityscore)
		read.save()
		return read


class ClassificationMethod(models.Model):
	id = models.AutoField(primary_key=True)
	key = models.IntegerField()
	description = models.CharField(max_length=100)
	contactname = models.CharField(max_length=50)
	contactemail = models.EmailFiled()
	
	def __unicode__(self):
		return self.methodID

	@classmethod
	def createClassificationMethod(cls, key, description, contactname, contactemail)
		classificationmethod = ClassificationMethod(key=key, description=description, contactname=contactname, contactemail=contactemail)
		classificationmethod.save()
		return classificationmethod


class TaxaID(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	level = models.CharField(max_length=50)
	taxa_id = models.CharField(max_length=50, unique=True)
	parent_taxa_id = models.CharField(max_length=50, unique=True)
	
	def __unicode__(self):
		return_str = self.name + " - " + self.taxa_id
		return return_str
	
	@classmethod
	def createTaxaID(cls, name, level, taxa_id, parent_taxa_id):
		taxaID = TaxaID(name=name, level=level, taxa_id=taxa_id, parent_taxa_id=parent_taxa_id)
		taxaID.save()
		return taxaID


class ReadAssignment(models.Model):
	id = models.AutoField(primary_key=True)
	read = models.ForeignKey(Read)
	classificationmethod = models.ForeignKey(ClassificationMethod)
	taxaID = models.ManytoManyField(TaxaID)
	score = models.FloatField()
	
	def __unicode__(self):
		return_str = self.read + " - " + self.taxaID
		return return_str

	@classmethod
	def createReadAssignment(cls, read, classificationmethod, taxaID, score):
		readassignment = ReadAssignment(read=read, classificationmethod=classificationmethod, taxaID=taxaID, score=score)
		readassignment.save()
		return readassignment


class ProfileSummary(models.Model):
	id = models.AutoField(primary_key=True)
	sample = models.ForeignKey(Sample)
	classificationmethod = models.ForeignKey(ClassificationMethod)
	taxaID = models.ManytoManyField(TaxaID)
	numreads = models.IntegerField()
	perctotal = models.FloatField()
	avgscore = models.FloatField()

	def __unicode__(self):
		return_str = self.sample + " - " + self.taxaID
		return return_str

	@classmethod
	def createProfileSummary(cls, sample, classificationmethod, taxaID, numreads, perctotal, avgscore):
		profilesummary = ProfileSummary(sample=sample, classificationmethod=classificationmethod, taxaID=taxaID, numreads=numreads, perctotal=perctotal, avgscore=avgscore)
		profilesummary.save()
		return profilesummary
	





