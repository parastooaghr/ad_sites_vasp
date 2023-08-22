import os
import shutil
#import pandas as pd

Subhmoy_materials_str = 'Co3Ni  CoPt3  CuPt   Fe3Co   FeCo  FeNi3  FePt3  NiPt VPt   VPt3  Zn11Co2  Zn13Co  Zn22Ni3 Zn3Cu  Zn8Cu5  ZnCu  ZnPt Co3Pt  Cu3Pt  CuPt7  Fe9Co7  FeNi  FePt   Ni3Pt  NiPt3  V3Pt VPt2  VPt8  Zn11Ni2  Zn13Fe  Zn35Cu17  Zn3Pt  Zn9Fe4  ZnNi  ZnPt3'
Subhmoy_materials = Subhmoy_materials_str.split()

origin = '/home/parastoo/Desktop/ML_N2_H2/Subhmoy_MITACS_2023/'
destination = '/home/parastoo/Desktop/ML_N2_H2/0_adsite_calcs/Subhmoy/'
desired_files = ['INCAR','KPOINTS','POSCAR','POTCAR','submitVASP.sh','OUTCAR','CONTCAR']


for material in Subhmoy_materials:
    #Creating required directories in each material folder
    os.mkdir(destination + material)
    os.mkdir(destination + material + '/0_bulk')
    os.mkdir(destination + material + '/1_surf')
    #os.mkdir(destination + material + '/dos_step')
    
    for file_name in desired_files: 
        shutil.copy(origin + material + '/0_bulk/' + file_name, origin + material + '/0_bulk/')
        shutil.copy(origin + material + '/1_surf/' + file_name, origin + material + '/1_surf/')

    
