function projection_bin(subject_dir)
% PROJECTION projects the electrode centroids to the perimeter of the
% loaded surface
subject_dir =  convertCharsToStrings(subject_dir);
%load electrode coordinates
load(subject_dir+'\centroids.mat');
eleccoord_flip = scirunmatrix';
elecoord_flip_orig = eleccoord_flip;

%load normalvectors 
load(subject_dir+'\normalvec.mat');
normalvec_flip = normalvec;

%stl dilated surface
[surf_data] = stlread(subject_dir+'\smooth_gm_flip.stl'); %dilated surface from Slicer
vertices = surf_data.Points;
faces = surf_data.ConnectivityList;

% Visualize Mesh
X = vertices(:,1);
Y = vertices(:,2);
Z = vertices(:,3);
trisurf(faces,X,Y,Z)

dt = 1; %step size 
n = 1; % iteration counter
maxn = 25; %max iterations
% direct = 0;
%Projection
for i = 1:length(eleccoord_flip)
    n = 1;
    disp(i)
    in = intriangulation(vertices,faces,eleccoord_flip(i,:));
    if 1 == in
        while 1 == in && n < maxn
        eleccoord_flip(i,1) = eleccoord_flip(i,1) + dt*normalvec_flip(i,1); %move in direction opposite of normal
        eleccoord_flip(i,2) = eleccoord_flip(i,2) + dt*normalvec_flip(i,2);
        eleccoord_flip(i,3) = eleccoord_flip(i,3) + dt*normalvec_flip(i,3);
        in = intriangulation(vertices,faces,eleccoord_flip(i,:));
        n = n + 1;
%         direct = -1; %direction relative to normal vector
        end
        if maxn == n && 1 == in
            eleccoord_flip(i,1) = eleccoord_flip(i,1) + (n-1)*-dt*normalvec_flip(i,1); %return to original location
            eleccoord_flip(i,2) = eleccoord_flip(i,2) + (n-1)*-dt*normalvec_flip(i,2);
            eleccoord_flip(i,3) = eleccoord_flip(i,3) + (n-1)*-dt*normalvec_flip(i,3);
            n = 1;
            in = intriangulation(vertices,faces,eleccoord_flip(i,:));   
                    while 1 == in && n < maxn 
                        eleccoord_flip(i,1) = eleccoord_flip(i,1) + -dt*normalvec_flip(i,1);% move in same direction as normal
                        eleccoord_flip(i,2) = eleccoord_flip(i,2) + -dt*normalvec_flip(i,2);
                        eleccoord_flip(i,3) = eleccoord_flip(i,3) + -dt*normalvec_flip(i,3);
                        in = intriangulation(vertices,faces,eleccoord_flip(i,:));
                        n = n + 1;
%                         direct = 1; %direction relative to normal vector
                    end
        elseif maxn == n
           sprintf('Error for electrode %d , could not converge', i)
        end
    elseif 0 == in
        while  0 == in && n < maxn 
            eleccoord_flip(i,1) = eleccoord_flip(i,1) + -dt*normalvec_flip(i,1); %move in direction of normal
            eleccoord_flip(i,2) = eleccoord_flip(i,2) + -dt*normalvec_flip(i,2);
            eleccoord_flip(i,3) = eleccoord_flip(i,3) + -dt*normalvec_flip(i,3);
            in = intriangulation(vertices,faces,eleccoord_flip(i,:));
            n = n + 1;
        end
        if maxn == n
            eleccoord_flip(i,1) = eleccoord_flip(i,1) + (n-1)*dt*normalvec_flip(i,1); %return to original location
            eleccoord_flip(i,2) = eleccoord_flip(i,2) + (n-1)*dt*normalvec_flip(i,2);
            eleccoord_flip(i,3) = eleccoord_flip(i,3) + (n-1)*dt*normalvec_flip(i,3);
            n = 1;
            in = intriangulation(vertices,faces,eleccoord_flip(i,:));   
                    while 0 == in && n < maxn 
                        eleccoord_flip(i,1) = eleccoord_flip(i,1) + dt*normalvec_flip(i,1);% move in opposite direction as normal
                        eleccoord_flip(i,2) = eleccoord_flip(i,2) + dt*normalvec_flip(i,2);
                        eleccoord_flip(i,3) = eleccoord_flip(i,3) + dt*normalvec_flip(i,3);
                        in = intriangulation(vertices,faces,eleccoord_flip(i,:));
                        n = n + 1;
                    end
        elseif maxn == n
           sprintf('Error for electrode %d , could not converge', i)
           break
        end
    end
    disp(n)
    n=1;
    proj_eleccoord(i,:) = eleccoord_flip(i,:);
end

save(subject_dir+'\centroids_proj.txt','proj_eleccoord','-ascii');