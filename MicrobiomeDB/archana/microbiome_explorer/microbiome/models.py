from django.db import models
import sys

class Project(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50, unique = True)
	description = models.CharField(max_length = 200)
	contact_name = models.CharField(max_length = 100)
	contact_email = models.EmailField()

	def __unicode__(self):
		return self.name

	@classmethod
	def createProject(cls, name, description, contact_name, contact_email):
		project = Project(name = name, description = description, contact_name = contact_name, contact_email = contact_email)
		project.save()
		return project


class Sample(models.Model):
	id = models.AutoField(primary_key = True)
	project = models.ForeignKey(Project)
	name = models.CharField(max_length = 50, unique = True)

	def __unicode__(self):
		return self.name
	
	@classmethod
	def createSample(cls, project, name):
		sample = Sample(project = project, name = name)
		sample.save()
		return sample


class SampleVariable(models.Model):
	id = models.AutoField(primary_key = True)
	sample = models.ForeignKey(Sample)
	variable = models.CharField(max_length = 100)
	value = models.CharField(max_length = 100)
	
	def __unicode__(self):
		return self.sample

	@classmethod
	def createSampleVariable(cls, sample, variable, value):
		samplevariable = SampleVariable(sample = sample, variable = variable, value = value)
		samplevariable.save()
		return samplevariable


class Read(models.Model):
	id = models.AutoField(primary_key = True)
	sample = models.ForeignKey(Sample)
	read_id = models.CharField(max_length = 50)
	length = models.IntegerField()
	quality_score = models.FloatField()
	seq = models.TextField(null=True)
	
	def __unicode__(self):
		return self.name

	@classmethod
	def createRead(cls, sample, read_id, length, qualityscore):
		read = Read(sample = sample, read_id = read_id, length = length, quality_score = quality_score)
		read.save()
		return read


class Method(models.Model):
	id = models.AutoField(primary_key = True)
	method_id = models.IntegerField(unique = True)
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200)
	contact_name = models.CharField(max_length = 100)
	contact_email = models.EmailField()
	
	def __unicode__(self):
		return self.key

	@classmethod
	def createMethod(cls, method_id, name, description, contact_name, contact_email):
		method = Method(method_id = method_id, name = name, description = description, contact_name = contact_name, contact_email = contact_email)
		method.save()
		return method


class Taxonomy(models.Model):
	id = models.AutoField(primary_key = True)
	taxa_id = models.CharField(max_length = 50, unique = True)
	name = models.CharField(max_length = 100)
	parent_taxa_id = models.CharField(max_length = 50)
	rank = models.CharField(max_length = 50)
	
	def __unicode__(self):
		return_str = self.name + " - " + self.taxa_id
		return return_str
	
	@classmethod
	def createTaxonomy(cls, taxa_id, name, parent_taxa_id, rank):
		taxa_ID = Taxonomy(taxa_id = taxa_id, name = name, parent_taxa_id = parent_taxa_id, rank = rank)
		taxa_ID.save()
		return taxa_ID


class ReadAssignment(models.Model):
	id = models.AutoField(primary_key = True)
	read = models.ForeignKey(Read)
	method = models.ForeignKey(Method)
	taxa_Id = models.ForeignKey(Taxonomy)
	score = models.FloatField()
	
	def __unicode__(self):
		return_str = self.read + " - " + self.taxa_Id
		return return_str

	class Meta:
		unique_together = ('read', 'method', 'taxa_Id')
		
	@classmethod
	def createReadAssignment(cls, read, method, taxa_Id, score):
		readassignment = ReadAssignment(read = read, method = method, taxa_Id = taxa_Id, score = score)
		readassignment.save()
		return readassignment


class ProfileSummary(models.Model):
	id = models.AutoField(primary_key = True)
	sample = models.ForeignKey(Sample)
	method = models.ForeignKey(Method)
	taxa_Id = models.ForeignKey(Taxonomy)
	num_of_reads = models.IntegerField()
	percentage = models.FloatField()
	avg_score = models.FloatField()

	def __unicode__(self):
		return_str = self.sample + " - " + self.taxaId
		return return_str
	
        class Meta:
		unique_together = ('sample', 'method', 'taxa_Id')

	@classmethod
	def createProfileSummary(cls, sample, method, taxa_Id, num_of_reads, percentage, avg_score):
		profile_summary = ProfileSummary(sample = sample, method = method, taxa_Id = taxa_Id, num_of_reads = num_of_reads, percentage = percentage, avg_score = avg_score)
		profile_summary.save()
		return profile_summary
	
