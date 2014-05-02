# Create your models here.
from django.db import models
import datetime


###########################
###    Project Table    ###
###########################
class Project(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=200)
	contactName = models.CharField(max_length=50)
	contactEmail = models.EmailField()
	#datetime = models.DateTimeField(auto_add_now=True)

	def __unicode__(self):
		return self.name

	@classmethod
	def createProject(cls, name, description, contactName, contactEmail):
		project = Project(name=name, description=description, contactName=contactName, contactEmail=contactEmail)
		project.save()
		return project



##########################
###    Sample Table    ###
##########################
class Sample(models.Model):
	id = models.AutoField(primary_key=True)
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.name
	
	@classmethod
	def createSample(cls, project, name):
		sample = Sample(project=project, name=name)
		sample.save()
		return sample



###################################
###    Sample Variables Table   ###
###################################
class SampleVariable(models.Model):
	id = models.AutoField(primary_key=True)
	sample = models.ForeignKey(Sample)
	variable = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	
	def __unicode__(self):
		rep = self.sample.name + " - " + self.variable
		return rep

	class Meta:
		unique_together = ('sample', 'variable')

	@classmethod
	def createSampleVariable(cls, sample, variable, value):
		samplevariable = SampleVariable(sample=sample, variable=variable, value=value)
		samplevariable.save()
		return samplevariable



#########################
###    Reads Table    ###
#########################
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



##########################################
###    Classification Methods Table    ###
##########################################
class ClassificationMethod(models.Model):
	id = models.AutoField(primary_key=True)
	# Added this column as our ReadAssignment and ProfileSummary files have methodID, instead of methodName
	method_id = models.IntegerField(unique=True)
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=100)
	contactname = models.CharField(max_length=50)
	contactemail = models.EmailField()
	
	def __unicode__(self):
		return self.name

	@classmethod
	def createClassificationMethod(cls, method_id, name, description, contactname, contactemail):
		classificationmethod = ClassificationMethod(method_id=method_id, name=name, description=description, contactname=contactname, contactemail=contactemail)
		classificationmethod.save()
		return classificationmethod



############################
###    Taxonomy Table    ###
############################
class TaxaID(models.Model):
	id = models.AutoField(primary_key=True)
	#taxa_id = models.CharField(max_length=50, unique=True)
	#parent_taxa_id = models.CharField(max_length=50)
	name = models.CharField(max_length=200)
	level = models.CharField(max_length=50)
	
	def __unicode__(self):
		rep = self.level + " - " + self.name
		return rep
	
	class Meta:
		unique_together = ('name', 'level')

	@classmethod
	def createTaxaID(cls, name, level):
		taxaID = TaxaID(name=name, level=level)
		taxaID.save()
		return taxaID



###################################
###    Read Assignment Table    ###
###################################
class ReadAssignment(models.Model):
	id = models.AutoField(primary_key=True)
	read = models.ForeignKey(Read)
	classificationmethod = models.ForeignKey(ClassificationMethod)
	taxaID = models.ForeignKey(TaxaID)
	score = models.FloatField()
	
	def __unicode__(self):
		rep = self.read.name + self.taxaID.level
		return rep

	class Meta:
		unique_together = ('read', 'classificationmethod', 'taxaID')

	@classmethod
	def createReadAssignment(cls, read, classificationmethod, taxaID, score):
		readassignment = ReadAssignment(read=read, classificationmethod=classificationmethod, taxaID=taxaID, score=score)
		readassignment.save()
		return readassignment



###################################
###    Profile Summary Table    ###
###################################
class ProfileSummary(models.Model):
	id = models.AutoField(primary_key=True)
	sample = models.ForeignKey(Sample)
	classificationmethod = models.ForeignKey(ClassificationMethod)
	taxaID = models.ForeignKey(TaxaID)
	numreads = models.IntegerField()
	perctotal = models.FloatField()
	avgscore = models.FloatField()

	def __unicode__(self):
		rep = self.sample.name + " - " + self.taxaID.name
		return rep

	class Meta:
		unique_together = ('sample', 'classificationmethod', 'taxaID')
	
	@classmethod
	def createProfileSummary(cls, sample, classificationmethod, taxaID, numreads, perctotal, avgscore):
		profilesummary = ProfileSummary(sample=sample, classificationmethod=classificationmethod, taxaID=taxaID, numreads=numreads, perctotal=perctotal, avgscore=avgscore)
		profilesummary.save()
		return profilesummary


