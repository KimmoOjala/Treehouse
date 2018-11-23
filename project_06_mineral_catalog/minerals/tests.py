from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Mineral


class MineralModelTests(TestCase):
    def test_mineral_creation(self):
        mineral = Mineral.objects.create(
name = "test mineral",
simple_name = "",
image_filename = "",
image_caption = "",
category = "",
formula = "",
strunz_classification = "",
color = "",
crystal_system = "",
unit_cell = "",
crystal_symmetry = "", 
cleavage = "",
mohs_scale_hardness = "", 
luster = "",
streak = "",
diaphaneity = "",
optical_properties = "", 
refractive_index = "", 
crystal_habit = "",
specific_gravity = ""
        )
        self.assertEqual(mineral.name, "test mineral")
        

class MineralViewsTests(TestCase):
    def setUp(self):
        self.mineral1 = Mineral.objects.create(
name = "test mineral",
simple_name = "",
image_filename = "",
image_caption = "",
category = "",
formula = "",
strunz_classification = "",
color = "",
crystal_system = "",
unit_cell = "",
crystal_symmetry = "", 
cleavage = "",
mohs_scale_hardness = "", 
luster = "",
streak = "",
diaphaneity = "",
optical_properties = "", 
refractive_index = "", 
crystal_habit = "",
specific_gravity = ""
        )
        self.mineral2 = Mineral.objects.create(
name = "another test mineral",
simple_name = "",
image_filename = "",
image_caption = "",
category = "",
formula = "",
strunz_classification = "",
color = "",
crystal_system = "",
unit_cell = "",
crystal_symmetry = "", 
cleavage = "",
mohs_scale_hardness = "", 
luster = "",
streak = "",
diaphaneity = "",
optical_properties = "", 
refractive_index = "", 
crystal_habit = "",
specific_gravity = ""
        )
        
    def test_mineral_list_view(self):
        resp = self.client.get(reverse('minerals:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral1, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'minerals/mineral_list.html')
      
    def test_mineral_detail_view(self):
        resp = self.client.get(reverse('minerals:detail',
                                       kwargs={'pk': self.mineral1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.mineral1, resp.context['mineral'])
        self.assertTemplateUsed(resp, 'minerals/mineral_detail.html')
   
    def test_index_view(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Tervetuloa ihastumaan mineraaleihin!")
        self.assertTemplateUsed(resp, 'index.html')
