from django.db import models


##________________________________________________________________________________________________________________##

class Project(models.Model):
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
    project = models.ForeignKey(Project)
    sample_name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return self.sample_name

    @classmethod
    def createSample(cls, project, sample_name):
        sample = Sample(project=project,
                        sample_name=sample_name)
        sample.save()
        return sample

# ##_________________________________________________________________________________________________________________##

class ClassificationMethod(models.Model):
    methodName = models.CharField(max_length=20, unique=True)
    methodDescription = models.CharField(max_length=50)
    ContactName = models.CharField(max_length=40)
    ContactEmail = models.CharField(max_length=40)

    def __unicode__(self):
        return self.methodName

    @classmethod
    def createClassification(cls, methodName, methodDescription, ContactName, ContactEmail):
        classification = ClassificationMethod(methodName=methodName,
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
class TaxaTable(models.Model):
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=50)

    def __unicode__(self):
        return self.level + "-" + self.name

    class Meta:
        unique_together = ('name', 'level')

    @classmethod
    def createTaxaID(cls, name, level):
        taxaID = TaxaTable(name=name, level=level)
        taxaID.save()
        return taxaID

#
# ##___________________________________________________________________________________________________________________##
#
class ReadsTable(models.Model):
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
# # ##_______________________________________________________________________________________________________________________##
#
class ProfileSummary(models.Model):
    sample = models.ForeignKey(Sample)
    classificationmethod = models.ForeignKey(ClassificationMethod)
    taxaID = models.ForeignKey(TaxaTable)
    numreads = models.IntegerField()
    perctotal = models.FloatField()
    avgscore = models.FloatField()

    def __unicode__(self):
        rep = self.sample.sample_name + " - " + self.taxaID.name
        return rep

    class Meta:
        unique_together = ('sample', 'classificationmethod', 'taxaID')

    @classmethod
    def createProfileSummary(cls, sample, classificationmethod, taxaID, numreads, perctotal, avgscore):
        profilesummary = ProfileSummary(sample=sample, classificationmethod=classificationmethod, taxaID=taxaID,
                                        numreads=numreads, perctotal=perctotal, avgscore=avgscore)
        profilesummary.save()
        return profilesummary

# ##______________________________________________________________________________________________________________________##

