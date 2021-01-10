from django.db import models
from django.utils import timezone
import string, random

class Student(models.Model):

    LEVEL = (
        ('100', '100 L'),
        ('200', '200 L'),
        ('300', '300 L'),
        ('400', '400 L'),
        ('500', '500 L'),
        ('600', '600 L'),
    )
    matric = models.CharField(max_length=10)
    email = models.EmailField()
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=3, choices=LEVEL)
    phone = models.CharField(max_length=11)
    total_gb = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    ref = models.CharField(max_length=300, )
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.matric

    def save(self, *args, **kwargs):
        def rand():
            rand = "".join(random.choices(string.ascii_lowercase, k=20))
            return rand
        
        if self.total_gb < 11 :
            amount = self.total_gb * 264
            self.amount = amount
        elif self.total_gb > 10 and self.total_gb < 21 :
            amount = self.total_gb * 250
            self.amount = amount
        elif self.total_gb > 20 and self.total_gb < 31 :
            amount = self.total_gb * 230
            self.amount = amount
        else:
            amount = self.total_gb * 200
            self.amount = amount
        if self.ref == '':
            self.ref = f'{self.phone}{self.total_gb}{rand()}'
        self.created = timezone.now()
        super().save(*args, **kwargs)
