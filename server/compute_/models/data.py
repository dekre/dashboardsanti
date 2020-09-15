from django.db import models
from .core import Item
from datetime import datetime
from apidata import utils as utl
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager


class AiModuleManager(PolymorphicManager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


# Create your models here.
class AiModuleCollection(Item):
    name = models.CharField(max_length=20, unique=True)
    lang = models.CharField(max_length=128)
    species = models.CharField(max_length=128)
    framework = models.CharField(max_length=128)
    author = models.CharField(max_length=128, default=None, blank=True, null=True)
    genre = models.CharField(max_length=128, default=None, blank=True, null=True)
    size = models.CharField(max_length=2, default=None, blank=True, null=True)
    license = models.CharField(max_length=128, default=None, blank=True, null=True)
    description = models.CharField(max_length=500, default=None, blank=True, null=True)
    active = models.BooleanField(default=True)

    objects = AiModuleManager()

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return True


class AiModuleVersionsManager(PolymorphicManager):
    def get_by_natural_key(self, aimodule, ailink, version):
        return self.get(aimodule=aimodule, ailink=ailink, version=version)


class AiModuleVersionCollection(Item):
    """Global VC for AI Modules
    Version Control for AI Modules within the Market Place / AI Zoo / ...     
    """

    aimodule = models.ForeignKey(
        AiModuleCollection,
        on_delete=models.CASCADE,
        related_name="aimoduleversions",
        related_query_name="aimoduleversion",
    )
    ailink = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
    version = models.IntegerField()
    objects = AiModuleVersionsManager()

    def natural_key(self):
        return (
            self.aimodule,
            self.ailink,
            self.version,
        )

    class Meta:
        unique_together = [["aimodule", "ailink", "version",]]

    def __str__(self):
        return "{0} - {1}".format(self.aimodule, self.ailink)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class AiModuleParameterManager(PolymorphicManager):
    def get_by_natural_key(self, aiversion, name):
        return self.get(aiversion=aiversion, name=name)


class AiModuleParameterCollection(Item):
    aiversion = models.ForeignKey(
        AiModuleVersionCollection,
        on_delete=models.CASCADE,
        related_name="aimoduleparameters",
        related_query_name="aimoduleparameter",
    )
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=500)
    description = models.CharField(max_length=500)    

    objects = AiModuleParameterManager()

    class Meta:
        unique_together = [["aiversion", "name"]]

    def natural_key(self):
        return (
            self.aiversion,
            self.name,
        )

    def __str__(self):
        return "{0}: {1}".format(self.aiversion, self.name)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class AiModuleLabelManager(PolymorphicManager):
    def get_by_natural_key(self, aiversion, name):
        return self.get(aiversion=aiversion, name=name)


class AiModuleLabelCollection(Item):
    aiversion = models.ForeignKey(
        AiModuleVersionCollection,
        on_delete=models.CASCADE,
        related_name="aimodulelabels",
        related_query_name="aimodulelabel",
    )
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    description = models.CharField(max_length=500)    

    objects = AiModuleLabelManager()

    class Meta:
        unique_together = [["aiversion", "name"]]

    def natural_key(self):
        return (
            self.aiversion,
            self.name,
        )

    def __str__(self):
        return "{0}: {1}".format(self.aiversion, self.name)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class ProjectManager(PolymorphicManager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class ProjectCollection(Item):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=500, default=None, blank=True, null=True)

    objects = ProjectManager()

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return "(ID {0} {1})".format(self.id, self.name)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return True


class ProjectAiModuleManager(PolymorphicManager):
    def get_by_natural_key(self, project, name):
        return self.get(project=project, name=name)


class ProjectAiModuleCollection(Item):
    project = models.ForeignKey(
        ProjectCollection,
        on_delete=models.CASCADE,
        related_name="projectaimodules",
        related_query_name="projectaimodule",
    )
    aibase = models.ForeignKey(
        AiModuleVersionCollection,
        on_delete=models.PROTECT,
        related_name="projectaimodules",
        related_query_name="projectaimodule",
    )
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500, default=None, blank=True, null=True)
    active = models.BooleanField(default=True)

    objects = ProjectAiModuleManager()

    def natural_key(self):
        return (
            self.project,
            self.name,
        )

    class Meta:
        unique_together = [["project", "name"]]

    def __str__(self):
        return "(ID {2}) {0} - {1}".format(self.project, self.name, self.id)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class ProjectAiModuleVersionManager(PolymorphicManager):
    def get_by_natural_key(self, aimodule, ailink, version):
        return self.get(aimodule=aimodule, ailink=ailink, version=version)


class ProjectAiModuleVersionCollection(Item):
    """Local VC for AI Modules on project level
    Version Control for AI Modules within the Market Place / AI Zoo / ...     
    """

    aimodule = models.ForeignKey(ProjectAiModuleCollection, on_delete=models.CASCADE)
    ailink = models.CharField(max_length=128)
    version = models.IntegerField()
    status = models.CharField(max_length=128)
    autopredict = models.IntegerField(default=None, blank=True, null=True)
    mincompletions = models.IntegerField(default=None, blank=True, null=True)    

    objects = ProjectAiModuleVersionManager()

    def natural_key(self):
        return (
            self.aimodule,
            self.ailink,
            self.version,
        )

    class Meta:
        unique_together = [["aimodule", "ailink", "version",]]

    def __str__(self):
        return "{0}: {1} (v{2})".format(self.aimodule, self.ailink, self.version)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class ProjectAiModuleParameterManager(PolymorphicManager):
    def get_by_natural_key(self, aiversion, name):
        return self.get(aiversion=aiversion, name=name)


class ProjectAiModuleParameterCollection(Item):
    aiversion = models.ForeignKey(
        ProjectAiModuleVersionCollection,
        on_delete=models.CASCADE,
        related_name="projectaimoduleparameters",
        related_query_name="projectaimoduleparameter",
    )
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    objects = ProjectAiModuleParameterManager()

    class Meta:
        unique_together = [["aiversion", "name",]]

    def natural_key(self):
        return (
            self.aiversion,
            self.name,
        )

    def __str__(self):
        return "{0}: {1}".format(aimodule, name)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class ProjectAiModuleLabelManager(PolymorphicManager):
    def get_by_natural_key(self, aiversion, name):
        return self.get(aiversion=aiversion, name=name)


class ProjectAiModuleLabelCollection(Item):
    aiversion = models.ForeignKey(
        ProjectAiModuleVersionCollection,
        on_delete=models.CASCADE,
        related_name="projectaimodulelabels",
        related_query_name="projectaimodulelabel",
    )
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    objects = ProjectAiModuleLabelManager()

    def natural_key(self):
        return (
            self.aiversion,
            self.name,
        )

    class Meta:
        unique_together = [["aiversion", "name",]]

    def __str__(self):
        return "{0}: {1}".format(self.aiversion, self.name)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class ProjectAiModuleExecutionManager(PolymorphicManager):
    def get_by_natural_key(self, aiversion, iteration):
        return self.get(aiversion=aiversion, iteration=iteration)


class ProjectAiModuleExecutionCollection(Item):
    aiversion = models.ForeignKey(
        ProjectAiModuleVersionCollection,
        on_delete=models.CASCADE,
        related_name="projectaimoduleexecutions",
        related_query_name="projectaimoduleexecution",
    )
    iteration = models.IntegerField()
    accuracy = models.FloatField()    

    objects = ProjectAiModuleExecutionManager()

    class Meta:
        unique_together = [["aiversion", "iteration",]]

    def natural_key(self):
        return (
            self.aiversion,
            self.iteration,
        )

    def __str__(self):
        return "{0} - {1}".format(self.aimodule, self.iteration)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class ProjectDocumentManager(PolymorphicManager):
    def get_by_natural_key(self, project, name):
        return self.get(project=project, file=file)


class ProjectDocumentCollection(Item):
    project = models.ForeignKey(
        ProjectCollection,
        on_delete=models.CASCADE,
        related_name="projectfiles",
        related_query_name="projectfile",
    )
    name = models.CharField(max_length=255) 
    datapool = models.CharField(max_length=24)  # idle / train / test / inference    

    objects = ProjectDocumentManager()

    class Meta:
        unique_together = [["project", "name",]]

    def natural_key(self):
        return (
            self.project,
            self.name,
        )

    def __str__(self):
        return "(Id {2}) {0} - {1}".format(self.project, self.name, self.id)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False

class ProjectFileManager(PolymorphicManager):
    def get_by_natural_key(self, project, file):
        return self.get(project=project, file=file)


class ProjectFileCollection(Item):
    document = models.ForeignKey(
        ProjectDocumentCollection,
        on_delete=models.CASCADE,
        related_name="projectfiles",
        related_query_name="projectfile",
    )
    file = models.FileField(upload_to=utl._upload_nlp_file_to)    
    status = models.CharField(
        max_length=200
    )  # idle / completed / ready / image conversion / text extraction
    steps = models.CharField(
        max_length=200, default=None, blank=True, null=True
    )  # None / high resolution / ocr / linguistical analsis / ...

    objects = ProjectFileManager()

    class Meta:
        unique_together = [["document", "file",]]

    def natural_key(self):
        return (
            self.document,
            self.file,
        )

    def __str__(self):
        return "{0} - {1}".format(self.document, self.file.name)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class ProjectFileCompletionManager(PolymorphicManager):
    def get_by_natural_key(self, aiversion, file):
        return self.get(aiversion=aiversion, file=file)


class ProjectFileCompletionCollection(Item):
    file = models.ForeignKey(
        ProjectFileCollection,
        on_delete=models.CASCADE,
        related_name="projectfilecompletions",
        related_query_name="projectfilecompletion",
    )
    aiversion = models.ForeignKey(
        ProjectAiModuleVersionCollection,
        on_delete=models.CASCADE,
        related_name="projectfilecompletions",
        related_query_name="projectfilecompletion",
    )
    ls_completions_key = models.CharField(max_length=200)
    completion = models.TextField()

    objects = ProjectFileCompletionManager()

    class Meta:
        unique_together = [["file", "aiversion"]]

    def natural_key(self):
        return (
            self.file,
            self.aiversion,
        )

    def __str__(self):
        return "{0}: {1}".format(self.aiversion, self.file)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class ProjectFilePredictionManager(PolymorphicManager):
    def get_by_natural_key(self, aiversion, file):
        return self.get(aiversion=aiversion, file=file)


class ProjectFilePredictionCollection(Item):
    file = models.ForeignKey(
        ProjectFileCollection,
        on_delete=models.CASCADE,
        related_name="projectfilepredictions",
        related_query_name="projectfileprediction",
    )
    aiversion = models.ForeignKey(
        ProjectAiModuleVersionCollection,
        on_delete=models.CASCADE,
        related_name="projectfilepredictions",
        related_query_name="projectfileprediction",
    )
    prediction = models.TextField()

    objects = ProjectFilePredictionManager()

    def natural_key(self):
        return (
            self.file,
            self.aiversion,
        )

    class Meta:
        unique_together = [["file", "aiversion"]]

    def __str__(self):
        return "{0}: {1}".format(self.aiversion, self.file)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class TmpProjectPdfFileManager(PolymorphicManager):
    def get_by_natural_key(self, project, file):
        return self.get(project=project, file=file)


class TmpProjectPdfFileCollection(Item):
    project = models.ForeignKey(
        ProjectCollection,
        on_delete=models.CASCADE,
        related_name="tmpprojectpdffiles",
        related_query_name="tmpprojectpdffile",
    )
    file = models.FileField(
        upload_to=utl._upload_nlp_file_to_tmp, default=None, blank=True, null=True
    )  # SET Field as nullable since we add files through celery
    status = models.CharField(
        max_length=200
    )  # idle / completed / ready / image conversion / text extraction

    objects = TmpProjectPdfFileManager()

    def natural_key(self):
        return (
            self.project,
            self.file,
        )

    class Meta:
        unique_together = [["project", "file"]]

    def __str__(self):
        return "{0}: {1}".format(self.project, self.file)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class TmpProjectImageFileManager(PolymorphicManager):
    def get_by_natural_key(self, project, tmppdf, file):
        return self.get(project=project, tmppdf=tmppdf, file=file)


class TmpProjectImageFileCollection(Item):
    project = models.ForeignKey(
        ProjectCollection,
        on_delete=models.CASCADE,
        related_name="tmpprojectimagefiles",
        related_query_name="tmpprojectimagefile",
    )
    tmppdf = models.ForeignKey(
        TmpProjectPdfFileCollection,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name="tmpprojectimagefiles",
        related_query_name="tmpprojectimagefile",
    )
    file = models.FileField(
        upload_to=utl._upload_nlp_file_to_tmp, default=None, blank=True, null=True
    )  # SET Field as nullable since we add files through celery
    status = models.CharField(
        max_length=200
    )  # idle / completed / ready / image conversion / text extraction

    objects = TmpProjectImageFileManager()

    class Meta:
        unique_together = [["project", "file",]]

    def natural_key(self):
        return (self.project, self.file)

    def __str__(self):
        return "{0} - {1}".format(self.project, self.file)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False


class TmpProjectTextFileMAnager(PolymorphicManager):
    def get_by_natural_key(self, project, tmppdf, file):
        return self.get(project=project, tmppdf=tmppdf, file=file)


class TmpProjectTextFileCollection(Item):
    project = models.ForeignKey(
        ProjectCollection,
        on_delete=models.CASCADE,
        related_name="tmpprojecttextfiles",
        related_query_name="tmpprojecttextfile",
    )
    tmpimg = models.ForeignKey(
        TmpProjectImageFileCollection,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name="tmpprojecttextfiles",
        related_query_name="tmpprojecttextfile",
    )
    tmppdf = models.ForeignKey(
        TmpProjectPdfFileCollection,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name="tmpprojecttextfiles",
        related_query_name="tmpprojecttextfile",
    )
    file = models.FileField(
        upload_to=utl._upload_nlp_file_to_tmp, default=None, blank=True, null=True
    )  # SET Field as nullable since we add files through celery
    status = models.CharField(
        max_length=200
    )  # idle / completed / ready / image conversion / text extraction    

    objects = TmpProjectTextFileMAnager()

    class Meta:
        unique_together = [["project", "file",]]

    def natural_key(self):
        return (self.project, self.file)

    def __str__(self):
        return "{0} - {1}".format(self.project, self.file)

    @property
    def is_ultimate(self) -> bool:
        """
        Set if the inherting model should be either ultimate (on top of the CollectionHierarchy)
        or not. Ultimate models don't bother to check for a parent collection when they are
        created.
        """
        return False

