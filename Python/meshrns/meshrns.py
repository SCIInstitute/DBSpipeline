
import os
import subprocess
import matlab.engine


def grid_mesh(subject_dir, scirun_net_dir, sci_run_bin, rad, centroid):
    """Makes a mesh of the ECoG grids and strips. The rad input determines the radius of the first triangulation. If
    tetgen fails try radii between 9-11 to start."""
    # set environment variabless
    os.environ["SMOOTH_GM"] = os.path.join(subject_dir, 'smooth_gm.stl')
    os.environ["FLAT_ELEC"] = os.path.join(scirun_net_dir, 'strip_contact.fld')
    os.environ["RING_ELEC"] = os.path.join(scirun_net_dir, 'strip_ring.fld')
    # os.environ["CENTROIDS_PROJ"] = os.path.join(subject_dir, 'centroids.txt')
    os.environ["CENTROIDS_PROJ"] = os.path.join(subject_dir, centroid)

    # call scirun to place projected electrodes
    cmd = (sci_run_bin + " -E " + os.path.join(scirun_net_dir, 'place_electrodes.srn5'))
    print(cmd)
    subprocess.call(cmd, shell=True)

    # Triangulate ring electrode nodes
    eng = matlab.engine.start_matlab()
    eng.addpath(os.environ["ECOG_matlab_dir"])
    print("Triangulating ring electrode nodes")
    eng.triangulate_grid(os.path.join(subject_dir), 1, rad, nargout=0)
    eng.quit()

    # First step of meshing
    # Setup environment variables to run network w/ Interface w/ Python module
    os.environ["GM"] = os.path.join(subject_dir, 'gm.stl')
    os.environ["WM"] = os.path.join(subject_dir, 'wm.stl')
    os.environ["VENTRICLES"] = os.path.join(subject_dir, 'ventricles.stl')
    os.environ["DIL_CSF"] = os.path.join(subject_dir, 'dil_csf.stl')
    os.environ["FLAT_ELECS"] = os.path.join(subject_dir, 'flat_elec.fld')
    os.environ["RING_TRIANGULATION"] = os.path.join(subject_dir, 'ring_triangulation.vtk')


    # meshing the insulation
    os.environ["MOVE_MM"] = "0"
    cmd = (sci_run_bin + " -E " + os.path.join(scirun_net_dir, 'meshing_1.srn5'))
    print(cmd)
    subprocess.call(cmd, shell=True)

    os.environ["GRID_BOTTOM_LAYER"] = os.path.normpath(os.path.join(subject_dir, "grid_bottom_layer.fld"))

    
    # creating volume electrodes 
    cmd = (sci_run_bin + " -E " + os.path.join(scirun_net_dir, 'volume_electrodes.srn5'))
    print(cmd)
    subprocess.call(cmd, shell=True)

    # Triangulate
    # final grid
    print("Triangulating final grid nodes and")
    eng = matlab.engine.start_matlab()
    eng.addpath(os.environ["ECOG_matlab_dir"])
    eng.triangulate_grid(os.path.join(subject_dir), 2, rad, nargout=0)
    eng.quit()

    # Create environment variables for meshing 2
    os.environ["FINAL_GRID_TRIANGULATION"] = os.path.join(subject_dir, 'finalgrid_triangulation.vtk')
    os.environ["DOUBLE_ELECTRODE"] = os.path.join(subject_dir, 'double_electrode.mat')
    os.environ["MESHED_CONTACTS"] = os.path.join(subject_dir, 'meshed_electrode.vtk')

    # meshing 2
    cmd = (sci_run_bin + " -E " + os.path.join(scirun_net_dir, 'meshing_2.srn5'))
    print(cmd)
    subprocess.call(cmd, shell=True)


def head_mesh(subject_dir, scirun_net_dir, sci_run_bin):
    """Creates a volumetric head_mesh using the previous results from grid_mesh. Saves files to subject directory."""
    # First step of meshing
    # Setup environment variables to run network w/ Interface w/ Python module
    os.environ["GM"] = os.path.join(subject_dir, 'gm.stl')
    os.environ["WM"] = os.path.join(subject_dir, 'wm.stl')
    os.environ["VENTRICLES"] = os.path.join(subject_dir, 'ventricles.stl')
    os.environ["DIL_CSF"] = os.path.join(subject_dir, 'dil_csf.stl')
    os.environ["FLAT_ELECS"] = os.path.join(subject_dir, 'flat_elec.fld')
    os.environ["FINAL_GRID"] = os.path.join(subject_dir, 'FINAL_GRID.fld')

    cmd = (sci_run_bin + " -E " + os.path.join(scirun_net_dir, 'map_conductivities_1.srn5'))
    print(cmd)
    subprocess.call(cmd, shell=True)

    os.environ["VOL_MESH_INTEGERS"] = os.path.join(subject_dir, 'vol_mesh_integers.fld')
    os.environ["LINK_NODES"] = os.path.join(subject_dir, 'link_nodes.mat')

    cmd = (sci_run_bin + " -E " + os.path.join(scirun_net_dir, 'map_conductivities_2.srn5'))
    print(cmd)
    subprocess.call(cmd, shell=True)






