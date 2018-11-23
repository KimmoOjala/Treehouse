from django.db import models

# Create your models here.

class Mineral(models.Model):
    name = models.TextField(blank=True)
    simple_name = models.TextField(blank=True)
    image_filename = models.TextField(blank=True)
    image_caption = models.TextField(blank=True)
    category = models.TextField(blank=True)
    formula = models.TextField(blank=True)
    strunz_classification = models.TextField(blank=True)
    color = models.TextField(blank=True)
    crystal_system = models.TextField(blank=True)
    unit_cell = models.TextField(blank=True) 
    crystal_symmetry = models.TextField(blank=True) 
    cleavage = models.TextField(blank=True)
    mohs_scale_hardness = models.TextField(blank=True) 
    luster = models.TextField(blank=True)
    streak = models.TextField(blank=True)
    diaphaneity = models.TextField(blank=True)
    optical_properties = models.TextField(blank=True) 
    refractive_index = models.TextField(blank=True) 
    crystal_habit = models.TextField(blank=True)
    specific_gravity = models.TextField(blank=True)
    
 