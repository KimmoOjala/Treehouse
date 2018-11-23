import os
import django
import operator
os.environ["DJANGO_SETTINGS_MODULE"] = 'Mineral_Catalog.settings'

django.setup()
from minerals.models import Mineral


if __name__ == '__main__': 

        
    def load_data_to_dictionary():
        '''Loads data from database to a dictionary with counts (values) for 
        each attribute (keys).'''
        minerals = Mineral.objects.all()
        mineral_dict = {"category": 0, "formula": 0, 
"strunz_classification": 0, "color": 0, "crystal_system": 0, "unit_cell": 0,
"crystal_symmetry": 0, "cleavage": 0, "mohs_scale_hardness": 0, "luster": 0,
"streak": 0, "diaphaneity": 0, "optical_properties": 0,
"refractive_index": 0, "crystal_habit": 0, "specific_gravity": 0}
        for mineral in minerals:   
            if mineral.category is not "":
                mineral_dict["category"] += 1
            if mineral.formula is not "":
                mineral_dict["formula"] += 1
            if mineral.strunz_classification is not "":
                mineral_dict["strunz_classification"] =+ 1
            if mineral.color is not "":
                mineral_dict["color"] += 1
            if mineral.crystal_system is not "":
                mineral_dict["crystal_system"] += 1
            if mineral.unit_cell is not "":
                mineral_dict["unit_cell"] += 1
            if mineral.crystal_symmetry is not "":
                mineral_dict["crystal_symmetry"] += 1
            if mineral.cleavage is not "":
                mineral_dict["cleavage"] += 1
            if mineral.mohs_scale_hardness is not "":
                mineral_dict["mohs_scale_hardness"] += 1
            if mineral.luster is not "":
                mineral_dict["luster"] += 1
            if mineral.streak is not "":
                mineral_dict["streak"] += 1
            if mineral.diaphaneity is not "":
                mineral_dict["diaphaneity"] += 1
            if mineral.optical_properties is not "":
                mineral_dict["optical_properties"] += 1    
            if mineral.refractive_index is not "":
                mineral_dict["refractive_index"] += 1    
            if mineral.crystal_habit is not "":
                mineral_dict["crystal_habit"] += 1
            if mineral.specific_gravity is not "":
                mineral_dict["specific_gravity"] += 1
        return mineral_dict                  
     
    def dictionary_to_ordered_list(mineral_dict):
        '''Creates on ordered list out of passed in dictionary.'''
        sorted_attributes = sorted(mineral_dict.items(), key=operator.itemgetter(1), reverse=True)
        for num in range(0, 7):
            print(sorted_attributes[num])
                               
    dictionary_to_ordered_list(load_data_to_dictionary())     