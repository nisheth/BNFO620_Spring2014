from django.db import models


##________________________________________________________________________________________________________________##

class Project(models.Model):
    project_id = models.IntegerField(primary_key=True, db_column="project ID")
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=300)
    contactName = models.CharField(max_length=30)
    contactEmail = models.CharField(max_length=40)

    def user(self):
        return self.project_id.name

    @classmethod
    def createProject(cls, name, description, contactName, contactEmail):
        project = Project(name=name, description=description, contactName=contactName, contactEmail=contactEmail)
        project.save()
        return project

##_________________________________________________________________________________________________________________##

class Sample(models.Model):
    sample_id = models.IntegerField(primary_key=True, db_column="sample ID")
    project_ID = models.ForeignKey(Project, null=True, db_column="project ID")
    project_name = models.CharField()
    sample_name = models.CharField(max_length=60, unique=True)

    def projectName(self):
        try:
            return self.project_ID.name
        except ValueError:
            return self.project_name

    def __unicode__(self):
        return int(self.sample_id)

    @classmethod
    def createSample(cls, project_name, sample_name):
        sample = Sample(project_name=project_name, sample_name=sample_name)
        sample.save()
        return sample

##_________________________________________________________________________________________________________________##

class SampleVariable(models.Model):
    sample_id = models.ForeignKey(Sample)
    attribute = models.CharField(max_length=60)
    value = models.CharField(max_length=60)

    class Meta:
        unique_together = ('sample_name', 'attribute')

    @classmethod
    def createSamAttribute(cls, sample_id, sample_name, attribute, value):
        sample_attribute = SampleVariable(sample_id=sample_id, sample_name=sample_name, attribute=attribute,
                                          value=value)
        sample_attribute.save()
        return sample_attribute


##_________________________________________________________________________________________________________________##

class ReadsTable(models.Model):
    ReadName = models.CharField(max_length=40)
    sample_ID = models.ForeignKey(Sample)
    length = models.IntegerField
    quality_score = models.IntegerField
    sequence = models.TextField(null=True)

    def __unicode__(self):
        return self.ReadName

    @classmethod
    def createReadsTable(cls, ReadName, sample_ID, length, quality_score, sequence):
        reads = ReadsTable(ReadName=ReadName, sample_ID=sample_ID, length=length, quality_score=quality_score,
                           sequence=sequence)
        reads.save()
        return reads

##__________________________________________________________________________________________________________________##

class ClassificationMethod(models.Model):
    methodID = models.IntegerField(primary_key=True, db_column="method ID")
    methodName = models.CharField(max_length=20, unique=True)
    methodDescription = models.CharField(max_length=50)
    ContactName = models.CharField(max_length=40)
    ContactEmail = models.CharField(max_length=40)

    def __unicode__(self):
        return int(self.methodID)


    @classmethod
    def createClassification(cls, methodID, methodName, methodDescription, ContactName, ContactEmail):
        classification = ClassificationMethod(methodID=methodID, methodName=methodName,
                                              methodDescription=methodDescription, ContactName=ContactName,
                                              ContactEmail=ContactEmail)
        classification.save()
        return classification

##_____________________________________________________________________________________________________________________##


class TaxaIDTable:
    taxaID = models.IntegerField(primary_key=True, db_column="taxa ID")
    taxa_name = models.CharField(max_length=50)
    taxa_level = models.CharField(max_length=50)
    parent_taxaID = models.CharField(max_length=50)

    def __unicode__(self):
        return int(self.taxaID)

    @classmethod
    def createTaxaTable(cls, taxaID, taxa_name, taxa_level, parent_taxaID):
        taxa_info = TaxaIDTable(taxaID=taxaID, taxa_name=taxa_name, taxa_level=taxa_level, parent_taxaID=parent_taxaID)
        taxa_info.save()
        return taxa_info

##_____________________________________________________________________________________________________________________##


class ReadAssignment:
    sample_ID = models.ForeignKey(Sample)
    read_name = models.ForeignKey(ReadsTable)
    classificationID = models.ForeignKey(ClassificationMethod)
    taxaID = models.ForeignKey(TaxaIDTable)
    score = models.FloatField()

    class Meta:
        unique_together = ('read_name', 'classificationID', 'taxaID')

    @classmethod
    def createReadAssignment(cls, sampleID, read_name, classificationID, taxaID, score):
        read_assignment = ReadAssignment(sampleID=sampleID, read_name=read_name, classificationID=classificationID, taxaID=taxaID, score=score)
        read_assignment.save()
        return read_assignment


##_______________________________________________________________________________________________________________________##

class ProfileSummary:
    sample_ID = models.ForeignKey(Sample)
    classification_id = models.ForeignKey(ClassificationMethod)
    taxaID = models.ForeignKey(TaxaIDTable)
    numReads = models.IntegerField()
    percentage = models.FloatField()
    average_score = models.FloatField()

    class Meta:
        unique_together = ('sample_ID', 'classification_id', 'taxaID')

    @classmethod
    def createProfileSummary(cls, sample_ID, classification_id, taxaID, numReads, percentage, average_score):
        profile_summary = ProfileSummary(sample_ID=sample_ID, classification_id=classification_id, taxaID=taxaID, numReads=numReads, percentage=percentage, average_score=average_score)
        profile_summary.save()
        return profile_summary

##______________________________________________________________________________________________________________________##

