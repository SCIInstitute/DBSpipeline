function triangulate_grid(subject_dir,s,rad)
% TRIANGULATE_GRID takes a point cloud and a radius and triangulates all of
% the points.
% The first input is the subject_dir, and the second is the first or second
% triangualtion, third is the radius for the first triangulation, try rad=10)
% Chantel Charlebois

% First triangulation with the 4 mm ring
subject_dir =  convertCharsToStrings(subject_dir);
cd(subject_dir)
if s == 1
    load(subject_dir+'/ring_elec.mat')
    [V,S] = alphavol(scirunfield.node',rad,1);
    exportTriangulation2VTK('ring_triangulation', scirunfield.node', S.bnd);
    
    
elseif s == 2
    %  Second triangulation with the two grid sheets to be connected
    load(subject_dir+'/grid_nodes.mat')
    [V,S] = alphavol(scirunfield.node',2,1);
    exportTriangulation2VTK('finalgrid_triangulation', scirunfield.node', S.bnd);
    
    load(subject_dir+'/double_electrode.mat')
    [V,S] = alphavol(scirunfield.node',2,1);
    exportTriangulation2VTK('meshed_electrode', scirunfield.node', S.bnd);
end