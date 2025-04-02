% Distance of projection

c_orig = load('Z:\pipeline\ecog\subjects\20f8a3\centroids.mat');
c_orig = c_orig.scirunmatrix;

c_proj = load('Z:\pipeline\ecog\subjects\20f8a3\proj_centroids_2.pts')';

dis = [];
for i = 1:length(c_orig)
    dis(i) = sqrt((c_orig(1,i)-c_proj(1,i)).^2 + (c_orig(2,i)-c_proj(2,i)).^2 + (c_orig(3,i)-c_proj(3,i)).^2);
end