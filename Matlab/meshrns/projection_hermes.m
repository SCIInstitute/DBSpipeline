function projection_hermes(subject_dir,ids)
% PROJECTION_HERMES projects the electrode to the smooth gm surface using
% the Hermes et al. 2010 method (local norm vector) for grids and nearest
% node for strips
    subject_dir =  convertCharsToStrings(subject_dir);
    cfg = [];
    cfg.method = 'headshape';
    cfg.warp = 'hermes2010';
    [surf_data] = stlread(strcat(subject_dir,'/smooth_gm.stl')); %dilated surface from Slicer
    cfg.headshape = surf_data;%structure containing a single triangulated boundary 
    surf.pos = surf_data.Points;

    elec = [];
    all_elecs = load(strcat(subject_dir,'/centroids.mat'));
    all_elecs = all_elecs.cont_cent;
    all_elecs = all_elecs;
    elec.elecpos = all_elecs;
    grids = cell(1,length(ids));
    for i=1:length(ids)
        ids{i} = cell2mat(ids{i});
        if length(ids{i})<10
            grids{i} = 'strip';
        else 
            grids{i} = 'grid';
        end
    end
    grids
    for g = 1:numel(grids)
        clear elec
        %cfg.channel = grids{g};
        cfg.warp = 'hermes2010';
        elec.elecpos = all_elecs(ids{g},:);
        for i = 1:length(elec.elecpos)
            elec.label{i} = strcat(grids{g},num2str(i));
        end
        %cfg.keepchannel = 'yes';
        cfg.elec        = elec;
        cfg.feedback    = 'yes';
        elec_realign = warp_hermes2010(cfg,elec,surf);
        elec_grid{g} = elec_realign;
        disp('Finished')
    end

    elecfinal = [];
    for g = 1:numel(grids)
        elecfinal = [elecfinal; elec_grid{g}];
    end
    save(subject_dir+'/centroids_proj_hermes.txt','elecfinal','-ascii');
end