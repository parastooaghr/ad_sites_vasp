# Workflow for Adsorption Site Generation and Job Submisison

Subhmoy_materials_str = 'Co3Ni  CoPt3  CuPt   Fe3Co   FeCo  FeNi3  FePt3  NiPt VPt   VPt3  Zn11Co2  Zn13Co  Zn22Ni3 Zn3Cu  Zn8Cu5  ZnCu  ZnPt Co3Pt  Cu3Pt  CuPt7  Fe9Co7  FeNi  FePt   Ni3Pt  NiPt3  V3Pt VPt2  VPt8  Zn11Ni2  Zn13Fe  Zn35Cu17  Zn3Pt  Zn9Fe4  ZnNi  ZnPt3'
Subhmoy_materials = Subhmoy_materials_str.split()
#del Subhmoy_material
#Subhmoy_materials

from pymatgen.core import Structure
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.core import Molecule
import os
import shutil

for material in Subhmoy_materials:
    material_folder = "/Users/parastooagharezaei/Downloads/test_adsite_workflow/Subhmoy/" + material + "/" # Main Folder for Material

    surf_folder = "/Users/parastooagharezaei/Downloads/test_adsite_workflow/Subhmoy/" + material + "/1_surf/" # Folder for Surface Calculations

    ads_folder_N2 = material_folder + "2_surf_ads_N2/" # Folder for N2 Adsorption 
    os.mkdir(ads_folder_N2) # Makes Directory (Throws Error if folder exists) 

    incar_path = surf_folder + 'INCAR' # Path to common INCAR file
    kpoints_path = surf_folder + 'KPOINTS' # Path to common KPOINTS
    potcar_path = '/Users/parastooagharezaei/Downloads/test_adsite_workflow/vasp_potpaw_PBE.54/' # Path to POTCAR Directory 
    submit_path = surf_folder + '/submitVASP.sh' # Path to Submit Script

    #Loading Slab Structure
    relaxed_surf = surf_folder + "CONTCAR"
    slab_struct = Structure.from_file(relaxed_surf)

    #Generating Adsorption Atructures
    asf = AdsorbateSiteFinder(slab_struct)
    mol_coords = [[0.499600147706,0.496579673269,0.377182266483], [0.535918199551,0.408898238259,0.378464237641]]
    adsorbate = Molecule(["N","N"],mol_coords) 
    ads_structs = asf.generate_adsorption_structures(adsorbate, repeat=None, find_args={"distance":1.00})

    count = 0
    for i in ads_structs:

        count += 1

        os.mkdir(ads_folder_N2 + f'ad_site_{count}') 
        i.to(fmt = 'POSCAR',filename = ads_folder_N2 + f'ad_site_{count}/POSCAR')
        shutil.copyfile(incar_path , ads_folder_N2+ f'ad_site_{count}/INCAR')
        shutil.copyfile(kpoints_path , ads_folder_N2+ f'ad_site_{count}/KPOINTS')
        #shutil.copyfile(submit_path , ads_folder_N2+ f'ad_site_{count}/submitVASP.sh')

        os.chdir(ads_folder_N2 + f'ad_site_{count}')

        # Generating POTCAR
        os.system("touch POTCAR")

        with open("POSCAR", "r") as POSCAR:
            species = POSCAR.readlines()[5].split()
    
        for atom in species:
            potcar_file = potcar_path + atom + "/POTCAR"
            command = "cat " + potcar_file + " >> ./POTCAR"
            os.system(command)
    
        # Submit Script Modification
        with open("POSCAR", "r") as POSCAR:
            atom_count = POSCAR.readlines()[6].split()
        num_atoms = 0
        for num in atom_count:
            num_atoms += int(num)
    
        num_nodes = round(num_atoms/32) # Number of Cores = Number of Atoms (32 = Number of Cores per Node)
    
        source_submit = open(submit_path,'r')
        dest_submit = open(ads_folder_N2 + f'ad_site_{count}/submitVASP.sh','w')

        all_lines = source_submit.readlines()
        for line in all_lines:
            if '#SBATCH --nodes' in line:
                line = re.sub('#SBATCH --nodes.*',f'#SBATCH --nodes={num_nodes}',line)
            if '#SBATCH --job-name' in line:
                line = re.sub('#SBATCH --job-name.*',f'#SBATCH --job-name={material}_site{count}',line)
            dest_submit.write(line)
        dest_submit.close()
        source_submit.close()
