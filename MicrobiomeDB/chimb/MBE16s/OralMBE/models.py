# Create your models here.
from django.db import models
import sys


class Project(models.Model):
	name = models.CharField(max_length=50, unique=True)
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
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.name

	@classmethod
	def createSample(cls, project, name):
		sample = Sample(project=project, name=name)
		sample.save()
		return sample


class SampleAttribute(models.Model):
	sample = models.ForeignKey(Sample)
	attribute = models.CharField(max_length=50)
	value = models.CharField(max_length=50)

	def __unicode__(self):
		return self.sample

	@classmethod
	def createSampleAttribute(cls, sample, attribute, value):
		sampleattribute = SampleAttribute(sample=sample, attribute=attribute, value=value)
		sampleattribute.save()
		return sampleattribute


class Read(models.Model):
    name = models.CharField(max_length=50)
    sample = models.ForeignKey(Sample)
    length = models.IntegerField()
    qualityscore = models.FloatField()
    seq = models.TextField(null=True)

    def __unicode__(self):
        return self.name


    @classmethod
    def createRead(cls, name, sample, length, qualityscore):
        read = Read(name=name, sample=sample, length=length, qualityscore=qualityscore)
        read.save()
        return read
	# Seq can be null. Not included in following create function. Add separately



class ClassificationMethod(models.Model):
	key = models.IntegerField(primary_key=True)
	description = models.CharField(max_length=100)
	contactname = models.CharField(max_length=50)
	contactemail = models.EmailField()

	def __unicode__(self):
		return self.key

	@classmethod
	def createClassificationMethod(cls, key, description, contactname, contactemail):
		classificationmethod = ClassificationMethod(key=key, description=description, contactname=contactname, contactemail=contactemail)
		classificationmethod.save()
		return classificationmethod


class Taxa(models.Model):
	name = models.CharField(max_length=50)
	level = models.CharField(max_length=50)

	def __unicode__(self):
		return_str = self.name + " - " + self.level
		return return_str

	@classmethod
	def createTaxa(cls, name, level):
		taxaID = Taxa(name=name, level=level)
		taxaID.save()
		return taxaID


class ReadAssignment(models.Model):
	read = models.ForeignKey(Read)
	classificationmethod = models.ForeignKey(ClassificationMethod)
	taxaID = models.ManyToManyField(Taxa)
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
	sample = models.ForeignKey(Sample)
	classificationmethod = models.ForeignKey(ClassificationMethod)
	taxa = models.ForeignKey(Taxa)
	numreads = models.IntegerField()
	perctotal = models.FloatField()
	avgscore = models.FloatField()

	def __unicode__(self):
		return_str = self.sample.name + " - " + self.taxa.name
		return return_str

	@classmethod
	def createProfileSummary(cls, sample, classificationmethod, taxa, numreads, perctotal, avgscore):
		profilesummary = ProfileSummary(sample=sample, classificationmethod=classificationmethod, taxa=taxa, numreads=numreads, perctotal=perctotal, avgscore=avgscore)
		profilesummary.save()
		return profilesummary