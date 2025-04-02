function centroids_vectors(subject_dir)
    % Load Data + Create Variables
    subject_dir =  convertCharsToStrings(subject_dir);
    file = 'Elec_Strip_Conn_Mask_Ordered.mat';
    elec = load(fullfile(subject_dir, file));
    data = elec.scirunnrrd.data;
    axis = elec.scirunnrrd.axis;
    disp(['Calculating centroids'])
    
    % Process Images
    connc = bwconncomp(data,6);
    reorder = zeros(1,connc.NumObjects);
    for i = 1:connc.NumObjects
        reorder(i) = data(connc.PixelIdxList{i}(1)); 
    end
    cont_prop = regionprops3(connc,'Centroid','EigenValues','EigenVectors');

    % Find Centroids
    cont_cent = regionprops3(connc,'Centroid');
    cont_cent = cont_cent.Centroid;
    cont_cent = [cont_cent(:,2)*axis(1).spacing + axis(1).min - axis(1).spacing, ...
                 cont_cent(:,1)*axis(2).spacing + axis(2).min - axis(2).spacing, ...
                 cont_cent(:,3)*axis(3).spacing + axis(3).min - axis(3).spacing];
             
    % Reorder centroids
    old_cont_cent = cont_cent;
    for i = 1:connc.NumObjects
        cont_cent(reorder(i),:) = old_cont_cent(i,:);
    end
    cont_cent(:,1) = cont_cent(:,1)*-1;
    cont_cent(:,2) = cont_cent(:,2)*-1; 
    
    save([subject_dir+'/centroids.mat'],'cont_cent');
    save([subject_dir+'/centroids.txt'],'cont_cent','-ascii');
end

