from django.db import models

class GenderChoices(models.TextChoices):
    Unknown = '', 'Будь ласка виберіть стать:'
    Male = 'M', 'Чоловіча'
    Woman = 'W', 'Жіноча'