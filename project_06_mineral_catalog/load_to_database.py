import os
import json
import django
import re
os.environ["DJANGO_SETTINGS_MODULE"] = 'Mineral_Catalog.settings'

django.setup()
from minerals.models import Mineral


if __name__ == '__main__': 

    def load_data_from_json():
        '''Loads mineral data from dictionary to database.''' 
        with open('minerals.json', encoding="utf8") as data_file:
            mineral_data = json.loads(data_file.read()) 
        return mineral_data
        
    def load_data_to_database(mineral_data):
        '''Loads mineral data from json file to a dictionary.''' 
        for obj in mineral_data:        
            key_list = ["name", "image filename", "image caption", "category", "formula", 
"strunz classification", "color", "crystal system", "unit cell", "crystal symmetry",
"cleavage", "mohs scale hardness", "luster", "streak", "diaphaneity",
"optical properties", "refractive index", "crystal habit", "specific gravity"]
            object_dict = {}
            for key_name in key_list:
                object_dict[key_name] = ""        
            for k, v in obj.items():
                if k == "name":
                    object_dict[k] = v                    
                    m = re.search(r'^[^(,-]*', v)                    
                    object_dict["simple name"] = m.group()
                if k == "image filename":    
                    object_dict[k] = v
                if k == "image caption":    
                    object_dict[k] = v
                if k == "category":    
                    object_dict[k] = v
                if k == "formula":    
                    object_dict[k] = v
                if k == "strunz classification":        
                    object_dict[k] = v
                if k == "color":        
                    object_dict[k] = v
                if k == "crystal system":        
                    object_dict[k] = v
                if k == "unit cell":        
                    object_dict[k] = v         
                if k == "crystal symmetry":        
                    object_dict[k] = v
                if k == "cleavage":        
                    object_dict[k] = v               
                if k == "mohs scale hardness":        
                    object_dict[k] = v
                if k == "luster":        
                    object_dict[k] = v
                if k == "streak":        
                    object_dict[k] = v
                if k == "diaphaneity":        
                    object_dict[k] = v
                if k == "optical properties":        
                    object_dict[k] = v
                if k == "refractive index":        
                    object_dict[k] = v
                if k == "crystal habit":        
                    object_dict[k] = v
                if k == "specific gravity":        
                    object_dict[k] = v          
            Mineral.objects.create(name=object_dict["name"],
simple_name=object_dict["simple name"],
image_filename=object_dict["image filename"],
image_caption=object_dict["image caption"],
category=object_dict["category"],
formula=object_dict["formula"],
strunz_classification=object_dict["strunz classification"], 
color=object_dict["color"],
crystal_system=object_dict["crystal system"],
unit_cell=object_dict["unit cell"],
crystal_symmetry=object_dict["crystal symmetry"], 
cleavage=object_dict["cleavage"],
mohs_scale_hardness=object_dict["mohs scale hardness"],
luster=object_dict["luster"],
streak=object_dict["streak"],
diaphaneity=object_dict["diaphaneity"],
optical_properties=object_dict["optical properties"],
refractive_index=object_dict["refractive index"],
specific_gravity=object_dict["specific gravity"]
)
        
    load_data_to_database(load_data_from_json())