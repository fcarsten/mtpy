# -*- coding: utf-8 -*-
"""
Spin-off from 'occamtools'
(Created August 2011, re-written August 2013)

Tools for Occam2D

authors: JP/LK


Classes:
    - Data
    - Model
    - Setup
    - Run
    - Plot
    - Mask


Functions:
    - getdatetime
    - makestartfiles
    - writemeshfile
    - writemodelfile
    - writestartupfile
    - read_datafile
    - get_model_setup
    - blocks_elements_setup


"""
#==============================================================================
import numpy as np
import scipy as sp
from scipy.stats import mode
import sys
import os
import os.path as op
import subprocess
import shutil
import fnmatch
import datetime
from operator import itemgetter
import time
import matplotlib.colorbar as mcb
from matplotlib.colors import Normalize
from matplotlib.ticker import MultipleLocator
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

import mtpy.core.edi as MTedi
import mtpy.modeling.winglinktools as MTwl
import mtpy.utils.conversions as MTcv
import mtpy.utils.filehandling as MTfh
import mtpy.utils.configfile as MTcf

reload(MTcv)
reload(MTcf)
reload(MTedi)

#==============================================================================

occamdict = {'1':'resxy','2':'phasexy','3':'realtip','4':'imagtip','5':'resyx',
             '6':'phaseyx'}

#------------------------------------------------------------------------------

class Setup():
    """
    Dealing with the setup  for an Occam2D run. Generate 'startup', 'inmodel', 
    'mesh' files. Calling Data() for generating a suitable input data file.

    Setting up those files within one (pre-determined) folder, so Occam can be 
    run there straight away.

    """


    def __init__(self, configfile = None, **input_parameters):



        self.parameters_startup = {}
        self.parameters_inmodel = {}
        self.parameters_data = {}
        self.parameters_mesh = {}


        self.parameters_startup['description'] = 'generic MTpy setup'

        self.parameters_startup['iter_format'] = 'OCCAM_ITER'
        self.parameters_startup['datetime_string'] = datetime.datetime.now().strftime(
                                                             '%Y/%m/%d %H:%M:%S')

        self.parameters_startup['no_iteration'] = 0
        self.parameters_startup['roughness_start'] = 1.0E+07
        self.parameters_startup['reached_misfit'] = 0        
        self.parameters_startup['roughness_type'] = 1
        self.parameters_startup['debug_level'] = 1
        self.parameters_startup['mu_start'] = 5.0
        self.parameters_startup['max_no_iterations'] = 30
        self.parameters_startup['target_rms'] = 1.5
        self.parameters_startup['rms_start'] = 1000

        self.parameters_inmodel['no_sideblockelements'] = 7
        self.parameters_inmodel['no_bottomlayerelements'] = 4
        self.parameters_inmodel['max_blockwidth'] = 500
        self.parameters_inmodel['firstlayer_thickness'] = 250
        self.parameters_inmodel['no_layersperdecade'] = 10
        self.parameters_inmodel['no_layers'] = 50

        self.parameters_inmodel['model_name'] = 'Modelfile generated with MTpy'
        self.parameters_inmodel['block_merge_threshold'] = 0.75

        self.parameters_data['phase_errorfloor'] = 10
        self.parameters_data['res_errorfloor'] = 10
        self.parameters_data['mode'] = 'both'
        
        self.parameters_data['minimum_frequency'] = None
        self.parameters_data['maximum_frequency'] = None
        self.parameters_data['max_no_frequencies'] = None


        self.parameters_mesh['mesh_title'] = 'Mesh file generated with MTpy'

 
        self.mesh = None
        self.meshlocations_x = None
        self.meshlocations_z = None
        self.meshblockwidths_x = None
        self.meshblockdepths_z = None

        self.lo_modelblockstrings = []
        self.lo_columnnumbers = []

        self.inmodel = None
 
        self.data = None
        self.no_parameters = None

        self.stationnames = []
        self.stationlocations = []

        self.halfspace_resistivity = 100.

        self.edifiles = []

        self.datafile = 'occaminputdata.dat'
        self.meshfile = 'mesh'
        self.inmodelfile = 'inmodel'
        self.startupfile = 'startup'
        self.staticsfile = None
        self.prejudicefile = None

        self.edi_directory = None
        #working directory
        self.wd = '.'

        update_dict = {}

        if configfile is not None:
            if op.isfile(configfile):
                if 1:
                    config_dict = MTcf.read_configfile(configfile)
                    temp_dict = {}
                    for key in config_dict:
                        temp_dict = config_dict[key]
                        update_dict.update(temp_dict)
                # except:
                #     print 'Warning - could not read config file {0}'.format(op.abspath(configfile))
                #     pass

        #correcting dictionary for upper case keys
        input_parameters_nocase = {}
        for key in input_parameters.keys():
            input_parameters_nocase[key.lower()] = input_parameters[key]

        update_dict.update(input_parameters_nocase)

        for dictionary in [self.parameters_startup, self.parameters_inmodel, 
                                    self.parameters_mesh, self.parameters_data]:
            for key in dictionary.keys():
                if key in update_dict:
                    if len(update_dict[key]) > 0 :
                        try:
                            value = float(update_dict[key])
                            dictionary[key] = value
                        except:
                            dictionary[key] = update_dict[key]

        for key in update_dict:
            try:
                value = getattr(self,key)
                if len(update_dict[key]) > 0:
                    try:
                        value = float(update_dict[key])
                        setattr(self,key,value)
                    except:
                        setattr(self,key,update_dict[key])
            except:
                continue 



    def read_configfile(self, configfile):

        cf = op.abspath(configfile)
        if not op.isfile(cf):
            print 'Warning - config file not found {0}'.format(cf)
            return

        config_dictionary = MTcf.read_configfile(cf)

        no_p = self.update_parameters(config_dictionary)
        no_a = self.update_attributes(config_dictionary)
        print '{0} parameters and attributes updated'.format(no_a + no_p)


    def update_parameters(self, **parameters_dictionary):

        input_parameters_nocase = {}
        for key in parameters_dictionary.keys():
            input_parameters_nocase[key.lower()] = parameters_dictionary[key]

        if self.validate_parameters(input_parameters_nocase) is False:
            print 'Error - parameters invalid \n'
            return

        counter = 0
        for dictionary in [self.parameters_startup, self.parameters_inmodel, 
                                    self.parameters_mesh, self.parameters_data]:
            for key in dictionary.keys():
                if key in input_parameters_nocase:
                    dictionary[key] = input_parameters_nocase[key]
                    counter += 1

        return counter



    def validate_parameters(self, **parameters_dictionary):
        
        valid = True

        return valid


    def update_attributes(self, **attributes_dictionary):
        input_attributes_nocase = {}
        for key in attributes_dictionary.keys():
            input_attributes_nocase[key.lower()] = attributes_dictionary[key]

        if self.validate_attributes(input_attributes_nocase) is False:
            print 'Error - attributes invalid \n'
            return
        counter = 0
        for attr in dir(self):
            if attr in input_attributes_nocase:
                self.setattr(attr,input_attributes_nocase[attr])
                counter += 1

        return counter 


    def validate_attributes(self, **attributes_dictionary):
        
        valid = True

        return valid


    def add_edifiles_directory(self, directory = None):

        if directory is None:
            print 'Error - provide directory name'
            return

        if op.isdir(directory) is False:
            print 'Warning - not a valid directory - cannot browse for EDI files: {0}'.format(directory)
            return

        edilist_raw = fnmatch.filter(os.listdir(directory),'*.[Ee][Dd][Ii]')
        edilist_full = [op.abspath(op.join(edi_dir,i)) for i in edilist_raw]
        
        counter = 0
        for edi in edilist_full:
            try:
                e = MTedi.Edi()
                e.readfile(edi)
                self.edifiles.append(edi)
                counter += 1
            except:
                continue
        
        print 'Added {0} Edi files'.format(counter)


    def add_edifiles(self, edilist):
        
        if not np.iterable(edilist):
            print 'Error - provide valid file list'
            return

        counter = 0
        for edi in edilist:
            try:
                fn = op.abspath(op.join(os.curdir,edi))
                e = MTedi.Edi()
                e.readfile(fn)
                self.edifiles.append(fn)
                counter += 1                
            except:
                continue

        print 'Added {0} Edi files'.format(counter)


    def remove_edifiles(self, edilist):
        if not np.iterable(edilist):
            print 'Error - provide valid file list'
            return

        counter = 0
        for edi in edilist:
            try:
                fn = op.abspath(op.join(os.curdir,edi))
                if fn in self.edifiles:
                    self.edifiles.remove(fn)
                counter += 1                
            except:
                continue

        print 'Removed {0} Edi files'.format(counter)


    def read_edifiles(self, edi_dir = None):
        
        if self.edi_directory is None:
            self.edi_directory = '.'

        if (edi_dir is not None):
            if (op.isdir(edi_dir)):
                self.edi_directory = edi_dir
            else:
                print 'Warning - given directory not found: {0} \n\t-'\
                    ' using current directory instead:{1}'.format(edi_dir,os.curdir)


        edilist_raw = fnmatch.filter(os.listdir(self.edi_directory),'*.[Ee][Dd][Ii]')
        edilist_full = [op.abspath(op.join(self.edi_directory,i)) for i in edilist_raw]
        edilist = []
        for edi in edilist_full:
            if op.isfile(edi):
                edilist.append(edi)
            else: 
                continue

            # try:
            #     e = MTedi.Edi()
            #     e.readfile(edi)
            #     edilist.append(edi)
            # except:
            #     continue

        self.edifiles = edilist
       

    def write_datafile(self):

        data_object = Data(edilist = self.edifiles, wd = self.wd, **self.parameters_data)
        self.sitelocations = data_object.stationlocations
        data_object.writefile()

        self.datafile = data_object.filename
        

    def setup_mesh_and_model(self):
        """
        Build the mesh and inmodel blocks from given data and parameters.

        Attributes required: 

        - self.no_layers
        - self.sitelocations
        - self.parameters_inmodel


        """
        #given as offset on the profile line
        lo_sites = self.sitelocations
        n_sites  = len(lo_sites)

        #maximum width of MODEL block - implicitely defines finiteness of the mesh
        maxblockwidth = float(self.parameters_inmodel['max_blockwidth'])

        #define vertical setup
        #number of layers per depth meters decade
        layers_per_decade     = float(self.parameters_inmodel['no_layersperdecade'])
        #depth of first layer
        first_layer_thickness = float(self.parameters_inmodel['firstlayer_thickness'])
        #so "layers_per_decade" layers between "first_layer_thickness" and 10* "first_layer_thickness"
        #then the same number between 10* "first_layer_thickness" and 100* "first_layer_thickness"

        #altogether stop at number of maximum layers:
        n_layers = int(float(self.parameters_inmodel['no_layers']))

        #number of padding mesh layers at the bottom 
        n_bottompadding = int(float(self.parameters_inmodel['no_bottomlayerelements']))

        #number of padding mesh columns to the sides
        n_sidepadding    = int(float(self.parameters_inmodel['no_sideblockelements']))

        #1. check, if inter-station spacing is smaller than the allowed max block size
        #if not, add dummy station locations

        lo_allsites = []
        lo_distances = []
        no_dummys = 0

        for idx_site,location in enumerate(lo_sites):
            lo_allsites.append(location)
            if idx_site == len(lo_sites)-1:
                break
            distance = np.abs(lo_sites[idx_site+1] - location)
            if distance >= maxblockwidth:
                dummys = int(distance/maxblockwidth) 
                smallblockwidth = distance/float(dummys+1)
                no_dummys += dummys
                for d in range(dummys):
                    lo_allsites.append(location + (d+1)* smallblockwidth)
                
                    lo_distances.append(smallblockwidth)
            
            else:
                lo_distances.append(distance)

        print 'added {0} dummy stations'.format(no_dummys)
        totalstations = no_dummys+len(lo_sites)
        totalmeshblocknumber = 2*n_sidepadding+4+2*(totalstations)
        totalmodelblocknumber = 4+totalstations
        print '{0} stations in total => \n\t{1} meshblocks and {2} modelblocks expected in top layer'.format(
                                    totalstations,totalmeshblocknumber, totalmodelblocknumber)

        #2. determine padding column widths:
        paddingwidth = 0.5 * np.max(lo_distances)
        meshnodelocations = []
        #add left half of block under first station 
        leftedge = lo_allsites[0] - lo_distances[0]/2.
        meshnodelocations.insert(0,leftedge)

        #add extra block column on the left of first station
        #consists of two mesh cells
        leftedge -= paddingwidth
        meshnodelocations.insert(0,leftedge)
        leftedge -= paddingwidth
        meshnodelocations.insert(0,leftedge)

            
        #3. split the inner station gaps into 2 mesh blocks each 
        for idx,station in enumerate(lo_allsites):
            meshnodelocations.append(station)
            if idx == len(lo_allsites)-1:
                break
            #include point in the middle between here and next station
            meshnodelocations.append(station+(lo_allsites[idx+1]-station)/2.)

        #add right half of block under last station 
        rightedge = lo_allsites[-1] + lo_distances[-1]/2.
        meshnodelocations.append(rightedge)

        #add extra block column on the right of last station
        #consists of two mesh cells
        rightedge += paddingwidth
        meshnodelocations.append(rightedge)
        rightedge += paddingwidth
        meshnodelocations.append(rightedge)


        #add 2 side padding blocks with expon. increasing width of N mesh cells
        padding_absolute = 0 
        for p in range(n_sidepadding):
            current_padding = 3**(p+1)*paddingwidth
            if current_padding > 1000000:
                current_padding = 1000000

            padding_absolute+=current_padding
            
            rightedge += current_padding
            meshnodelocations.append(rightedge)

            leftedge -= current_padding
            meshnodelocations.insert(0,leftedge) 
        

        #4.determine the overall width of mesh blocks
        lo_meshblockwidths = []
        for loc in range(len(meshnodelocations)-1):            
            lo_meshblockwidths.append( meshnodelocations[loc+1] - meshnodelocations[loc] )

        #5. build top layer modelblocks by merging paddings and then 2 blocks each:
        lo_columns_to_merge = []
        lo_modelblockwidths = [] 
        current_meshblock_index = 0

        lo_columns_to_merge.append(n_sidepadding)
        lo_modelblockwidths.append(padding_absolute)
        current_meshblock_index += n_sidepadding

        #merge the extra column at the left:
        lo_columns_to_merge.append(2)
        lo_modelblockwidths.append( lo_meshblockwidths[current_meshblock_index] 
                                + lo_meshblockwidths[current_meshblock_index+1] )
        current_meshblock_index += 2

        for idx,location in enumerate(lo_allsites):
            #each sit is on top of a block, consisting of 2 mesh cells each
            lo_columns_to_merge.append(2)
            lo_modelblockwidths.append(lo_meshblockwidths[current_meshblock_index] 
                                + lo_meshblockwidths[current_meshblock_index+1] )
            current_meshblock_index += 2
        
        #merge right extra column
        lo_columns_to_merge.append(2)
        lo_modelblockwidths.append( lo_meshblockwidths[current_meshblock_index] 
                                + lo_meshblockwidths[current_meshblock_index+1] )
        current_meshblock_index += 2

        #merge the side padding columns on the right
        lo_columns_to_merge.append(n_sidepadding)
        lo_modelblockwidths.append(np.sum(padding_absolute))
        current_meshblock_index += n_sidepadding


        #6.right side of left most model block - effectively the edge of the padding
        #given with resspect to location of the first station
        #idx of station 1 is n_sidepadding + 2(extra column) + 1 (half the block under the station)
        binding_offset =  meshnodelocations[n_sidepadding+3] - meshnodelocations[n_sidepadding]

        #should be identical!
        no_horizontal_nodes = current_meshblock_index + 1
        nodey = len(lo_meshblockwidths) + 1 #vertical nodes

        ncol0 = len(lo_columns_to_merge) # number of blocks in the first layer

        #7. now turn to depths - set up the z axis for the mesh:

        no_decades = int(n_layers/layers_per_decade)+1
        no_depthpoints_max = layers_per_decade * no_decades
        depthscale = 10**np.linspace(0,no_decades,no_depthpoints_max + 1) 
        
        lo_model_depths = list((depthscale[:n_layers-1] * first_layer_thickness))
        
        
        lo_mesh_depths = []
        lo_rows_to_merge = []

        for idx, depth in enumerate(lo_model_depths):
            lo_mesh_depths.append(depth)
            lo_rows_to_merge.append(2)
            if idx == len(lo_model_depths) - 1 :
                break
            lo_mesh_depths.append(lo_model_depths[idx+1] - depth)

        lo_mesh_thicknesses = []
        for idx,depth in enumerate(lo_mesh_depths):
            if idx == 0:
                thickness = depth
            else:
                thickness = depth - lo_mesh_depths[idx-1]
            lo_mesh_thicknesses.append(thickness)

        max_thickness = np.max(lo_mesh_thicknesses)
        maxdepth = lo_mesh_depths[-1]

        for i in range(n_bottompadding):
            lo_mesh_thicknesses.append(max_thickness)
            lo_mesh_depths.append(maxdepth+max_thickness)
            maxdepth += max_thickness
        
        lo_model_depths.append(lo_model_depths[-1]+n_bottompadding*max_thickness)
        
        #just to be safe!
        self.parameters_inmodel['no_layers'] = len(lo_model_depths)

        lo_model_thicknesses = []
        for idx,depth in enumerate(lo_model_depths):
            if idx == 0:
                thickness = depth
            else:
                thickness = depth - lo_model_depths[idx-1] 
            lo_model_thicknesses.append(thickness)


        lo_rows_to_merge.append(n_bottompadding)
        no_vertical_nodes = len(lo_mesh_depths) +1
        


        
        self.parameters_inmodel['bindingoffset']      = binding_offset
        self.parameters_inmodel['max_number_columns'] = ncol0
        self.parameters_inmodel['lo_merged_lines']    = lo_rows_to_merge
        self.parameters_inmodel['lo_merged_columns']  = lo_columns_to_merge  
        self.meshblockwidths_x                        = lo_meshblockwidths
        self.meshblockdepths_z                        = lo_mesh_thicknesses
         
        self.meshlocations_z                          = lo_mesh_depths
        self.meshlocations_x                          = meshnodelocations
        self.parameters_mesh['no_nodes_hor']          = no_horizontal_nodes
        self.parameters_mesh['no_nodes_vert']         = no_vertical_nodes

        #mesh DONE
        #-----------------------------------------------------
        #defining the actual blocks:

        trigger    = self.parameters_inmodel['block_merge_threshold']

        modelblockstrings = []
        lo_column_numbers = []
        num_params = 0
        

        ncol = ncol0
        #loop over all model layers
        for layer_idx in range(len(lo_model_depths)):
            block_idx = 1
        
            #sweep columns
            while block_idx+1 < ncol-1 :

                if lo_model_depths[layer_idx] < (trigger*(lo_modelblockwidths[block_idx]+
                                                            lo_modelblockwidths[block_idx+1])):
                    block_idx += 1
                    continue

                else:
                    #concatenate/merge blocks

                    lo_modelblockwidths[block_idx] += lo_modelblockwidths[block_idx+1]
                    lo_columns_to_merge[block_idx]   += lo_columns_to_merge[block_idx+1]
                    lo_modelblockwidths.pop(block_idx+1)
                    lo_columns_to_merge.pop(block_idx+1)

                    ncol -=1

            lo_column_numbers.append(ncol)

            tempstring = ""
            for j in range(ncol):
                tempstring += "%i "%(lo_columns_to_merge[j])
            tempstring += "\n"
            modelblockstrings.append(tempstring)

            num_params += ncol

        print 'number of model blocks: {0}'.format(num_params)
        self.no_parameters = num_params
        self.parameters_inmodel['lo_modelblockstrings'] = modelblockstrings
        self.parameters_inmodel['lo_column_numbers']    = lo_column_numbers
        self.parameters_inmodel['lo_merged_columns']    = lo_columns_to_merge




    def write_meshfile(self):

        """
        Create the mesh file

        Attributes required:

        - self.meshlocations_x
        - self.meshlocations_z
        - self.meshnodes_x
        - self.meshnodes_z
        - self.meshfile
        - self.wd

        """
        mesh_positions_vert = self.meshlocations_z
        mesh_positions_hor  = self.meshlocations_x
        n_nodes_hor         = self.parameters_mesh['no_nodes_hor'] 
        n_nodes_vert        = self.parameters_mesh['no_nodes_vert']
        

        mesh_outstring =''

        temptext = '{0}\n'.format(self.parameters_mesh['mesh_title'])
        mesh_outstring += temptext

        temptext = "{0} {1} {2} {0} {0} {3}\n".format(0,n_nodes_hor,n_nodes_vert,2)
        mesh_outstring += temptext

        temptext = ""
        counter = 0 
        for i in range(n_nodes_hor-1):
            temptext += "%.1f "%(mesh_positions_hor[i])
            counter +=1 
            if counter == 10:
                temptext += '\n'
                counter = 0
        temptext +="\n"
        mesh_outstring += temptext

        temptext = ""
        counter = 0 
        for i in range(n_nodes_vert-1):
            temptext += "%.1f "%(mesh_positions_vert[i])
            counter +=1 
            if counter == 10:
                temptext += '\n'
                counter = 0
        temptext +="\n"
        mesh_outstring += temptext

        mesh_outstring +="%i\n"%(0)
        
        for j in range(4*(n_nodes_vert-1)):
            tempstring=''
            tempstring += (n_nodes_hor-1)*"?"
            tempstring += '\n'
            mesh_outstring += tempstring


        fn = op.join(self.wd,self.meshfile)       
        F_mesh = open(fn,'w')
        F_mesh.write(mesh_outstring)
        F_mesh.close()


    def write_inmodelfile(self):
        """
        Generate inmodel file.

        Require attributes:
        - self.parameters_inmodel['lo_modelblockstrings']
        - self.parameters_inmodel['lo_columnnumbers']
        - self.parameters_inmodel['lo_merged_columns']
        - self.parameters_inmodel['bindingoffset']
        - self.no_layers
        """

        modelblockstrings = self.parameters_inmodel['lo_modelblockstrings']
        lo_merged_columns = self.parameters_inmodel['lo_merged_columns']
        lo_merged_lines   = self.parameters_inmodel['lo_merged_lines']
        lo_column_numbers = self.parameters_inmodel['lo_column_numbers']
        boffset           = self.parameters_inmodel['bindingoffset']
        n_layers          = self.parameters_inmodel['no_layers']

        model_outstring =''

        temptext = "Format:           {0}\n".format("OCCAM2MTMOD_1.0")
        model_outstring += temptext
        temptext = "Model Name:       {0}\n".format(self.parameters_inmodel['model_name'])
        model_outstring += temptext
        temptext = "Description:      {0}\n".format("Random Text")
        model_outstring += temptext
        temptext = "Mesh File:        {0}\n".format(op.abspath(self.meshfile))
        model_outstring += temptext
        temptext = "Mesh Type:        {0}\n".format("PW2D")
        model_outstring += temptext
        if self.staticsfile is not None:
            temptext = "Statics File:     {0}\n".format(self.staticsfile)
        else:
            temptext = "Statics File:     none\n"
        model_outstring += temptext
        if self.prejudicefile is not None:
            temptext = "Prejudice File:   {0}\n".format(self.prejudicefile)
        else:
            temptext = "Prejudice File:   none\n"
        model_outstring += temptext
        temptext = "Binding Offset:   {0:.1f}\n".format(boffset)
        model_outstring += temptext
        temptext = "Num Layers:       {0}\n".format(n_layers)
        model_outstring += temptext

        for k in range(n_layers):
            n_meshlayers  = lo_merged_lines[k]
            n_meshcolumns = lo_column_numbers[k]
            temptext="{0} {1}\n".format(n_meshlayers, n_meshcolumns)
            model_outstring += temptext

            temptext = modelblockstrings[k]
            model_outstring += temptext
            #model_outstring += "\n"
            

        temptext = "Number Exceptions:{0}\n".format(0)
        model_outstring += temptext
        

        fn = op.join(self.wd,self.inmodelfile)        
        F_model = open(fn,'w')
        F_model.write(model_outstring)
        F_model.close()



    def write_startupfile(self):
        """
        Generate startup file

        Require attributes:

        -


        """

        startup_outstring =''

        temptext = "Format:           {0}\n".format(self.parameters_startup['iter_format'])
        startup_outstring += temptext

        temptext = "Description:      {0}\n".format(self.parameters_startup['description'])
        startup_outstring += temptext

        temptext = "Model File:       {0}\n".format(self.inmodelfile)
        startup_outstring += temptext

        temptext = "Data File:        {0}\n".format(self.datafile)
        startup_outstring += temptext

        temptext = "Date/Time:        {0}\n".format(self.parameters_startup['datetime_string'])
        startup_outstring += temptext

        temptext = "Max Iter:         {0}\n".format(int(float(self.parameters_startup['max_no_iterations'])))
        startup_outstring += temptext

        temptext = "Target Misfit:    {0:.1f}\n".format(float(self.parameters_startup['target_rms']))
        startup_outstring += temptext

        temptext = "Roughness Type:   {0}\n".format(self.parameters_startup['roughness_type'])
        startup_outstring += temptext
    
        temptext = "Debug Level:      {0}\n".format(self.parameters_startup['debug_level'])
        startup_outstring += temptext

        temptext = "Iteration:        {0}\n".format(int(self.parameters_startup['no_iteration']))
        startup_outstring += temptext
    
        temptext = "Lagrange Value:   {0}\n".format(self.parameters_startup['mu_start'])
        startup_outstring += temptext
        
        temptext = "Roughness Value   {0}\n".format(self.parameters_startup['roughness_start'])
        startup_outstring += temptext
        
        temptext = "Misfit Value:     {0}\n".format(float(self.parameters_startup['rms_start']))
        startup_outstring += temptext
        
        temptext = "Misfit Reached:   {0}\n".format(self.parameters_startup['reached_misfit'])
        startup_outstring += temptext
        
        temptext = "Param Count:      {0}\n".format(self.no_parameters)
        startup_outstring += temptext
        
        temptext = ""
        counter = 0 
        for l in range(self.no_parameters):
            temptext += "{0:.1g}  ".format(np.log10(float(self.halfspace_resistivity)))
            counter += 1
            if counter == 20:
                temptext += '\n'
                counter = 0
        temptext += "\n"
        startup_outstring += temptext
     

        fn =  op.join(self.wd,self.startupfile)
        F_startup = open(fn,'w')
        F_startup.write(startup_outstring)
        F_startup.close()



    def generate_inputfiles(self, edi_dir):

        if not op.isdir(self.wd):
            os.makedirs(self.wd)

        self.read_edifiles(edi_dir)
        self.write_datafile()
        self.setup_mesh_and_model()
        self.write_meshfile()
        self.write_inmodelfile()
        self.write_startupfile()

        print '\nInput files in working directory {0}: \n'.format(op.abspath(self.wd))
        print '{0}'.format(op.basename(self.datafile))
        print '{0}'.format(op.basename(self.meshfile))
        print '{0}'.format(op.basename(self.inmodelfile))
        print '{0}'.format((self.startupfile))

        print '\n\t\t DONE !\n\n'

#------------------------------------------------------------------------------


class Data():
    """
    Handling input data.

    Generation of suitable Occam data file(s) from Edi files/directories.
    Reading and writing data files.
    Allow merging of data files.
    """
    def __init__(self, edilist = None, wd = None, **data_parameters):

        self.wd = os.curdir
        self.filename = 'OccamDataFile.dat'
        self.edilist = []

        if edilist is not None:
            if np.iterable(edilist):
                self.edilist = edilist
        
        if wd is not None:
            if op.isdir(wd):
                self.wd = wd


        self.azimuth = 0.
        self.profile = None
        self.frequencies = None
        self.stations = []
        self.stationlocations = []
        self.rotation_angle = 0.
        self.data = []
        self.mode = 'both'
        self.profile_offset = 0.
        self.format = 'OCCAM2MTDATA_1.0'
        self.title = 'MTpy Occam-Datafile'


        for key in data_parameters:
            setattr(self,key,data_parameters[key])

        self.generate_profile()
        self.build_data()

        #self.group_frequencies()
        #self._write_datafile(op.join(self.wd,self.filename))#
        

    def readfile(self,fn):
        if not op.isfile(fn):
            print 'Error - not a valid file: {0}'.fn

        self.filename = op.basename(fn)
        self.wd = op.split(fn)[0]

        F_in = file(fn,'r')
        datafile_raw = F_in.read()
        F_in.close()

        #string is reduced each step, i.e. cut off the sections, 
        #which are read in already
        reduced_string = self._read_format(datafile_raw)
        reduced_string = self._read_title(datafile_raw)
        reduced_string = self._read_sites(datafile_raw)
        reduced_string = self._read_offsets(datafile_raw)
        reduced_string = self._read_frequencies(datafile_raw)
        
        self._read_data(reduced_string)

    def _find_string(key,datastring):
        
        index = datastring.lower().find('key')
        return index

    def _read_format(self,datastring):
        idx = _find_string('format',datastring)
        reduced_string = datastring[idx:]
        data_list = datastring.split('\n')
        line = data_list[0]
        line = line.strip().split(':')
        self.format = line[1].strip().lower()

        return reduced_string 

    def _read_title(self,datastring):
        idx = _find_string('title',datastring)
        reduced_string = datastring[idx:]
        data_list = datastring.split('\n')
        line = data_list[0]
        line = line.strip().split(':')
        self.title = line[1].strip().lower()

        return reduced_string 
        

    def _read_sites(self,datastring):

        idx = _find_string('sites',datastring)
        reduced_string = datastring[idx:]
        data_list = datastring.split('\n')
        line = data_list[0]
        line = line.strip().split(':')
        no_sites = int(float(line[1].strip().lower()))
        lo_stations = []
        for idx in range(no_sites):
            sta = data_list[idx+1].strip()
            lo_stations.append(sta)

        self.stations = lo_stations

        return reduced_string 
        

    def _read_offsets(self,datastring):
        idx = _find_string('offsets',datastring)
        reduced_string = datastring[idx:]
        data_list = datastring.split('\n')
        line = data_list[0]
        line = line.strip().split(':')
        no_sites = len(self.stations)
        lo_offsets = []
        for idx in range(no_sites):
            offset = float(data_list[idx+1].strip())
            lo_offsets.append(offset)

        self.stationlocations = lo_offsets

        return reduced_string 
        

    def _read_frequencies(self,datastring):
        idx = _find_string('frequencies',datastring)
        reduced_string = datastring[idx:]
        data_list = datastring.split('\n')
        line = data_list[0]
        line = line.strip().split(':')
        no_freqs = int(float(line[1]))

        lo_freqs = []
        for idx in range(no_freqs):
            freq = float(data_list[idx+1].strip())
            lo_freqs.append(freq)

        self.frequencies = lo_freqs

        return reduced_string 

    def _read_data(self,datastring):
        idx = _find_string('data',datastring)
        reduced_string = datastring[idx:]
        data_list = datastring.split('\n')
        line = data_list[0]
        line = line.strip().split(':')
        no_data = int(float(line[1]))

        lo_data = []
        idx = 0
        row_idx = 2
        while idx < no_data:
            row = data_list[row_idx].strip().split()
            if row[0][0] == '#':
                row_idx += 1
                continue
            rowlist = [float(i) for i in row]
            lo_data.append(rowlist)
            row_idx += 1
            idx += 1



    def rotate(angle):
        """
        Rotate input data for geoelectric strike.


        Best done on the edi files before being read input_parameters
        TODO

        """
        pass


    def build_data(self):
        
        lo_modes = []
        modes = self.mode.lower().strip()
        if modes == 'both':
            lo_modes = [1,2,5,6]
        elif modes == 'te':
            lo_modes = [1,2]
        elif modes == 'tm':
            lo_modes = [5,6]


        lo_all_freqs = []
        for lo_f in self.station_frequencies:
            lo_all_freqs.extend(list(lo_f))
        lo_all_freqs = sorted(list(set(lo_all_freqs)),reverse=True)
        self.frequencies = np.array(lo_all_freqs)

        self.data = []

        for idx_s, station in enumerate(self.stations):
            station_number = idx_s + 1
            Z = self.Z[idx_s]
            rho_phi = Z.res_phase 
            for idx_f,freq in enumerate(self.station_frequencies[idx_s]):
                frequency_number = np.abs(self.frequencies-freq).argmin() + 1
                for mode in lo_modes:
                    if mode == 1 :
                        raw_value = rho_phi[0][idx_f][0,1]
                        value = np.log10(raw_value)
                        absolute_error = rho_phi[2][idx_f][0,1]
                        relative_error = absolute_error/raw_value
                        if self.res_errorfloor is not None:
                            if self.res_errorfloor/100. > relative_error:
                                relative_error = self.res_errorfloor/100.
                        error = relative_error/np.log(10.)
                    elif mode == 2 :
                        value = rho_phi[1][idx_f][0,1]
                        absolute_error = rho_phi[2][idx_f][0,1]
                        relative_error = absolute_error/value
                        if self.phase_errorfloor is not None:
                            if self.phase_errorfloor/100. > relative_error:
                                relative_error = self.phase_errorfloor/100.
                        error = relative_error*100.*0.285
                    elif mode == 5 :
                        raw_value = rho_phi[0][idx_f][1,0]
                        value = np.log10(raw_value)
                        absolute_error = rho_phi[2][idx_f][1,0]
                        relative_error = absolute_error/raw_value
                        if self.res_errorfloor is not None:
                            if self.res_errorfloor/100. > relative_error:
                                relative_error = self.res_errorfloor/100.
                        error = relative_error/np.log(10.)
                    elif mode == 6 :
                        value = (rho_phi[1][idx_f][1,0])%90
                        absolute_error = rho_phi[2][idx_f][1,0]
                        relative_error = absolute_error/value
                        if self.phase_errorfloor is not None:
                            if self.phase_errorfloor/100. > relative_error:
                                relative_error = self.phase_errorfloor/100.
                        error = relative_error*100.*0.285
                    self.data.append([station_number, frequency_number,mode,value,error])


    def generate_profile(self):
        """
            Generate linear profile by regression of station locations.

            Stations are projected orthogonally onto the profile. Calculate 
            orientation of profile (azimuth) and position of stations on the 
            profile.

            Orientation of the profile is ALWAYS West->East.
            (In unlikely/synthetic case of azimuth=0, it's North->South)


            (self.stationlocations, self.azimuth, self.stations)

        """

        self.station_coords = []
        self.stations = []
        self.station_frequencies = []
        
        self.Z = []

        lo_easts = []
        lo_norths = []
        utmzones = []

        for edifile in self.edilist:
            edi = MTedi.Edi()
            edi.readfile(edifile)
            self.station_coords.append([edi.lat,edi.lon,edi.elev])
            self.stations.append(edi.station)
            self.station_frequencies.append(np.around(edi.freq,5))
            self.Z.append(edi.Z)
            utm = MTcv.LLtoUTM(23,edi.lat,edi.lon)
            lo_easts.append(utm[1])
            lo_norths.append(utm[2])
            utmzones.append(int(utm[0][:-1]))

        main_utmzone = mode(utmzones)[0][0]

        for idx, zone in enumerate(utmzones):
            if zone == main_utmzone:
                continue
            utm = MTcv.LLtoUTM(23,edi.lat,edi.lon,main_utmzone)

            lo_easts[idx] = utm[1]
            lo_norths[idx] = utm[2]
        

        profile_line = sp.polyfit(lo_easts, lo_norths, 1) 
        self.azimuth = np.arctan(profile_line[0])*180/np.pi
        lo_easts = np.array(lo_easts)
        lo_norths = np.array(lo_norths)

        projected_stations = []
        lo_offsets = []
        profile_vector = np.array([1,profile_line[0]])
        profile_vector /= np.linalg.norm(profile_vector)

        for idx,sta in enumerate(self.stations):
            station_vector = np.array([lo_easts[idx],lo_norths[idx]-profile_line[1]])
            position = np.dot(profile_vector,station_vector) * profile_vector 
            lo_offsets.append(np.linalg.norm(np.array(position[0]-min(lo_easts),position[1]-min(lo_norths))))
            projected_stations.append([position[0],position[1]+profile_line[1]])

        #Sort from West to East:
        profile_idxs = np.argsort(lo_offsets)
        if self.azimuth == 0:
            #Exception: sort from North to South
            profile_idxs = np.argsort(lo_norths)


        #sorting along the profile
        projected_stations = [projected_stations[i] for i in profile_idxs]
        projected_stations =  np.array(projected_stations)
        lo_offsets = np.array([lo_offsets[i] for i in profile_idxs])
        lo_offsets -= min(lo_offsets)

        self.station_coords = [self.station_coords[i] for i in profile_idxs]
        self.stations = [self.stations[i] for i in profile_idxs]
        self.station_frequencies = [self.station_frequencies[i] for i in profile_idxs]
        self.Z = [self.Z[i] for i in profile_idxs]
        lo_easts = np.array([lo_easts[i] for i in profile_idxs])
        lo_norths = np.array([lo_norths[i] for i in profile_idxs])
              

        self.profile = profile_line
        self.stationlocations = lo_offsets
        self.easts = lo_easts
        self.norths = lo_norths
        #print self.stationlocations


        if 0:
            lo_all_easts = list(lo_easts)
            lo_all_easts.extend(list(projected_stations[:,0]))
            print sorted(lo_all_easts)
            lo_all_norths = list(lo_norths)
            lo_all_norths.extend(list(projected_stations[:,1]))
            x_extent = max(lo_all_easts) - min(lo_all_easts)
            y_extent = max(lo_all_norths) - min(lo_all_norths)
            plt.close('all')
            lfig = plt.figure(4, dpi=200, figsize=(2,2))
            plt.clf()
            ploty = sp.polyval(profile_line, sorted(lo_all_easts))
            lax = lfig.add_subplot(1, 1, 1,aspect='equal')
            lax.plot(sorted(lo_all_easts), ploty, '-k', lw=1)
            lax.scatter(lo_easts,lo_norths,color='b',marker='+')
            lax.scatter(projected_stations[:,0], projected_stations[:,1],color='r',marker='x')
            lax.set_title('Original/Projected Stations')
            lax.set_ylim(np.min([lo_norths.min(),projected_stations[:,1].min()])-0.2*y_extent, 
                                            np.max([lo_norths.max(),projected_stations[:,1].max()])+0.2*y_extent)
            lax.set_xlim(np.min([lo_easts.min(),projected_stations[:,0].min()])-0.2*x_extent, 
                                            np.max([lo_easts.max(),projected_stations[:,0].max()])+0.2*x_extent)
            lax.set_xlabel('Easting (m)', 
                           fontdict={'size':4, 'weight':'bold'})
            lax.set_ylabel('Northing (m)',
                           fontdict={'size':4, 'weight':'bold'})
            plt.show()


    # def group_frequencies(self):
    #     """
    #     collect frequencies of different stations, if they just vary by a 
    #     tolerance - set to 5% 
    #     """
    #     pass

    def writefile(self, filename = None):
        if filename is not None:
            try:
                fn = op.abspath(op.join(self.wd,filename))
                self.filename = op.abspath(op.split(fn)[1])
                self.wd = op.abspath(op.split(fn)[0])
            except:
                self.filename = 'OccamDataFile.dat' 

        outstring = ''

        outstring += 'FORMAT:'+11*' '+self.format+'\n'
        outstring += 'TITLE:'+12*' '+'{0} - profile azimuth {1:.1f} degrees\n'.format(self.title,self.azimuth)
        outstring += 'SITES:'+12*' '+'{0}\n'.format(len(self.stations))
        for s in self.stations:
            outstring += '    {0}\n'.format(s)
        outstring += 'OFFSETS (M):\n'
        for l in self.stationlocations:
            outstring += '    {0}\n'.format(l + self.profile_offset)
        outstring += 'FREQUENCIES:      {0}\n'.format(len(self.frequencies))
        for f in self.frequencies:
            outstring += '    {0}\n'.format(f)
        outstring += 'DATA BLOCKS:      {0}\n'.format(len(self.data))

        outstring += 'SITE    FREQ    TYPE    DATUM    ERROR\n'
        for d in self.data:
            outstring += '{0}    {1}    {2}    {3}    {4}\n'.format(*d)

        outfn = op.abspath(op.join(self.wd,self.filename))
        
        F = open(outfn,'w')
        F.write(outstring)
        F.close()



class Model():
    """
    Handling of Occam output files.

    Reading, writing, renaming,... of 'ITER' and 'RESP' files. 
    """


class Plot():
    """
    Graphical representations of in- and output data.

    Provide gui for masking points.
    Represent output models.
    """

class Run():
    """
    Run Occam2D by system call.

    Future plan: implement Occam in Python and call it from here directly.
    """


class Mask(Data):
    """
    Allow masking of points from data file (effectively commenting them out, 
    so the process is reversable). Inheriting from Data class.
    """



