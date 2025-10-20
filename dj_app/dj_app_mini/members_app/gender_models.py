from django.db import models

class GenderChoices(models.TextChoices):
    Male = 'M', 'Чоловіча'
    Woman = 'W', 'Жіноча'