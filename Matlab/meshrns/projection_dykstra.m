function projection_dykstra(subject_dir)
% PROJECTION_DYKSTRA projects the electrode to the smooth gm surface using
% the Dykstra et al. 2010 method using energy minimization algorithm to
% minimize projected distance of each electrode and keep interelectrode
% distance
    addpath('C:\Users\Chantel\fieldtrip-20190714')
    subject_dir =  convertCharsToStrings(subject_dir);
    [surf_data] = stlread(strcat(subject_dir,'\smooth_gm_flip.stl')); %dilated surface from Slicer
    surf.vert = surf_data.Points;
    surf.tri = surf_data.ConnectivityList;
    elec = [];
    all_elecs = load(strcat(subject_dir,'\centroids.mat'));
    all_elecs = all_elecs.cont_cent;
    all_elecs = all_elecs;
    %Check if any values are zero
    if any(all_elecs,'all')
        [row,col] = find(all_elecs == 0);
        for i = 1:length(row)
            t(row(i),col(i)) = 0.00000000001;
        end
    end
    [coord_snapped,pairs]=snap2dural_energy(all_elecs,surf);
    save(subject_dir+'\centroids_proj_dykstra.txt','coord_snapped','-ascii');
end