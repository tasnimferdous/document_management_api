from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
# User.document_set.all()


class Document(models.Model):
    option = [
        ("pdf", "PDF"),
        ("txt", "TXT"),
        ("docx", "DOCX"),
        ("doc", "DOC"),
        ("xml", "XML"),
        ("json", "JSON"),
    ]
    owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="owner")
    shared_users = models.ManyToManyField(User, blank=True, related_name="shared_users")
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    file_format = models.CharField(max_length=4, choices=option, default="pdf")
    file = models.FileField(max_length=5242880, upload_to="docs", validators=[FileExtensionValidator( ['pdf', 'txt', 'docx', 'doc', 'xml', 'json'] ) ])
    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title + ' by ' + self.owner.username
