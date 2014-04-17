from django.db import models


##________________________________________________________________________________________________________________##

class Project(models.Model):
    project_id = models.IntegerField(primary_key=True, db_column="project ID")
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=300)
    contactName = models.CharField(max_length=30)
    contactEmail = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

    @classmethod
    def createProject(cls, name, description, contactName, contactEmail):
        project = Project(name=name,
                          description=description,
                          contactName=contactName,
                          contactEmail=contactEmail)
        project.save()
        return project

##_________________________________________________________________________________________________________________##

class Sample(models.Model):
    sample_id = models.IntegerField(primary_key=True, db_column="sample ID")
    project = models.ForeignKey(Project, null=True, db_column="project ID")
    sample_name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
            return self.sample_name

    @classmethod
    def createSample(cls, project, sample_name):
        sample = Sample(project =project,
                        sample_name=sample_name)
        sample.save()
        return sample

# ##_________________________________________________________________________________________________________________##

class ClassificationMethod(models.Model):
    methodID = models.IntegerField(primary_key=True, db_column="method ID")
    methodName = models.CharField(max_length=20, unique=True)
    methodDescription = models.CharField(max_length=50)
    ContactName = models.CharField(max_length=40)
    ContactEmail = models.CharField(max_length=40)

    def __unicode__(self):
        return self.methodID

    @classmethod
    def createClassification(cls, methodID, methodName, methodDescription, ContactName, ContactEmail):
        classification = ClassificationMethod(methodID=methodID,
                                              methodName=methodName,
                                              methodDescription=methodDescription,
                                              ContactName=ContactName,
                                              ContactEmail=ContactEmail)
        classification.save()
        return classification
#
# ##_____________________________________________________________________________________________________________________##
#
#
class SampleVariable(models.Model):
    sampleID = models.IntegerField(primary_key=True, db_column="id")
    sample = models.ForeignKey(Sample)
    attribute = models.CharField(max_length=70)
    value = models.CharField(max_length=70)

    def __unicode__(self):
       line = self.sample.sample_name + "-" + self.value
       return line

    #class Meta:
        #unique_together = ('sample_name', 'attribute')

    @classmethod
    def createSamAttribute(cls, sample, attribute, value):
        sample_attribute = SampleVariable(sample=sample,
                                          attribute=attribute,
                                          value=value)
        sample_attribute.save()
        return sample_attribute
#
# #
# # ##_________________________________________________________________________________________________________________##
#
class TaxaIDTable:
    taxaID = models.IntegerField(primary_key=True, db_column="taxa ID")
    taxa_name = models.CharField(max_length=50)
    taxa_level = models.CharField(max_length=50)
    name = models.CharField(max_length=60)
    parent_taxaID = models.CharField(max_length=50)

    def __unicode__(self):
        line = self.name + "-" + self.taxaID
        return line

    @classmethod
    def createTaxaTable(cls, taxa_name, parent_taxaID, name, taxa_level):
        taxa_info = TaxaIDTable(taxa_name=taxa_name,
                                name=name,
                                taxa_level=taxa_level,
                                parent_taxaID=parent_taxaID)
        taxa_info.save()
        return taxa_info
#
# ##___________________________________________________________________________________________________________________##
#
class ReadsTable(models.Model):
    read_id = models.IntegerField(primary_key=True, db_column="read ID")
    ReadName = models.CharField(max_length=60)
    sample = models.ForeignKey(Sample)
    length = models.IntegerField()
    quality_score = models.FloatField()
    sequence = models.TextField(null=True)

    def __unicode__(self):
        return self.ReadName

    @classmethod
    def createReadsTable(cls, sample, ReadName, length, quality_score):
        reads = ReadsTable(sample=sample, ReadName=ReadName, length=length, quality_score=quality_score,
                           )
        reads.save()
        return reads
#
# ##_________________________________________________________________________________________________________________________##
#

# class ReadAssignment:
#     id = models.IntegerField(primary_key=True, db_column="ID")
#     name = models.ForeignKey(ReadsTable)
#     classificationID = models.ForeignKey(ClassificationMethod)
#     taxa_ID = models.ForeignKey(TaxaIDTable)
#     score = models.FloatField()
#
#     def __unicode__(self):
#        line = self.name + self.taxa_ID.level
#        return line
#
#     class Meta:
#         unique_together = ('read_name', 'classificationID', 'taxaID')
#
#     @classmethod
#     def createReadAssignment(cls, name, classificationID, taxa_ID, score):
#         rainfo = ReadAssignment(name=name, classificationID=classificationID, taxa_ID=taxa_ID, score=score)
#         rainfo.save()
#         return rainfo
# # ##_______________________________________________________________________________________________________________________##
#
# class ProfileSummary:
#     sample_ID = models.IntegerField(primary_key=True, db_column="Sample_ID")
#     sample = models.ForeignKey(Sample)
#     classification_id = models.ForeignKey(ClassificationMethod)
#     taxaID = models.ForeignKey(TaxaIDTable)
#     numReads = models.IntegerField()
#     percentage = models.FloatField()
#     average_score = models.FloatField()
#
#     #class Meta:
#         #unique_together = ('sample_ID', 'classification_id', 'taxaID')
#
#     @classmethod
#     def createProfileSummary(cls, sample, classification_id, taxaID, numReads, percentage, average_score):
#         profile_summary = ProfileSummary(sample=sample, classification_id=classification_id, taxaID=taxaID, numReads=numReads, percentage=percentage, average_score=average_score)
#         profile_summary.save()
#         return profile_summary

# ##______________________________________________________________________________________________________________________##

