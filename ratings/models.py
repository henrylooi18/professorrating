from django.db import models

class Professor(models.Model):
    code = models.CharField(max_length=10, unique=True, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"  # display professor name and code in admin site

class Module(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"  # display module name and code in admin site

class ModuleInstance(models.Model):
    professor = models.ManyToManyField(Professor)  # one module can be taught by multiple professors at the same time, many to many
    module = models.ForeignKey(Module, on_delete=models.CASCADE) 
    year = models.IntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.module} ({self.year}/{self.semester})"  # display module and year/semester in admin site

class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.professor} rated {self.module_instance.module} ({self.module_instance.year}/{self.module_instance.semester}) with {self.rating}"
    