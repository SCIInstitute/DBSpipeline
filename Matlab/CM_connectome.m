clear
clc
home = pwd;
dirname = uigetdir(title='Connectome Folder');
cd(dirname)

subject = readmatrix('connectome_matrix.csv');
data = subject(2:end,2:end); %Remove unassigned
data = data(:,371:372); %extract ROI data
data = data(1:370,:); %remove ROI from outputs

mu = readmatrix('sift2_mu.txt');
data_weighted = mu.*data;
%data_norm = data_weighted./sum(data_weighted);
data_norm = data_weighted;
ROI_left = data_norm(:,1);
ROI_right = data_norm(:,2);

save('connectivity_left.mat','ROI_left')
save('connectivity_right.mat', 'ROI_right')
%%
percent = 100; %top x percentage of connections

top = percent/100;
[ROI_left_top, Index_left] = maxk(ROI_left, floor(length(ROI_left)*top)); %find top 20% highest connections
[ROI_right_top, Index_right] = maxk(ROI_right, floor(length(ROI_right)*top));

bins = 150;
figure()
subplot(1,2,1)
histogram(ROI_left_top,bins)
title('Left')
xlabel('Connectivity')
xlim([0,0.15])
ylim([0,20])
ylabel('Count')
subplot(1,2,2)
histogram(ROI_right_top,bins)
title('Right')
xlabel('Connectivity')
xlim([0,0.15])
ylim([0,20])
ylabel('Count')
sgtitle(['Top ',num2str(percent),'%'])
%%
labels = readcell('Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Bash\Freesurfer\hcpmmp1_subcortex.txt');
clear left_save
clear right_save
labels_left = string([]);
data_sort_left = zeros(1,length(Index_left));
for i = 1:length(Index_left)
    labels_left(i) = string(labels{Index_left(i),2});
    data_sort_left(i) = string(ROI_left(Index_left(i)));
end
left_save(1,:) = labels_left;
left_save(2,:) = Index_left;
left_save(3,:) = data_sort_left;
fid = fopen('labels_left.txt','wt');
fprintf(fid, '%-20s%-20s%s\n', left_save);
fclose(fid);

labels_right = string([]);
data_sort_right = zeros(1,length(Index_right));
for i = 1:length(Index_right)
    labels_right(i) = string(labels{Index_right(i),2});
    data_sort_right(i) = string(ROI_right(Index_right(i)));
end
right_save(1,:) = labels_right;
right_save(2,:) = Index_right;
right_save(3,:) = data_sort_right;
fid = fopen('labels_right.txt','wt');
fprintf(fid, '%-20s%-20s%s\n', right_save);
fclose(fid);
%%
cd(home)
%% Other Regions
%{
clear
clc
home = pwd;
dirname = uigetdir(title='Connectome Folder');
cd(dirname)

labels = readcell('Z:\Dropbox (UFL)\DataProcessing\Pipeline Code\Bash\Freesurfer\hcpmmp1_labels.txt');
subject = readmatrix('connectome_matrix.csv');
data = subject(2:end,2:end);
ACC_left = [57,58,59,60,61,62,63,65,69,88,164,165,179,180];
ACC_right = ACC_left + 180;
data_left = data(:,ACC_left);
data_right = data(:,ACC_right);

data_left_sum = sum(data_left,2);
data_right_sum = sum(data_right,2);

mu = readmatrix('../sift2_mu.txt');
data = [data_left_sum data_right_sum];
data_weighted = mu.*data;
data_norm = data_weighted./sum(data_weighted);
ROI_left = data_norm(1:360,1); %remove addons because not part of lookup
ROI_right = data_norm(1:360,2);
ROI_left(ACC_left) = nan;
ROI_right(ACC_right) = nan;

percent = 100; %top x percentage of connections

top = percent/100;
[ROI_left_top, Index_left] = maxk(ROI_left, floor(length(ROI_left)*top)); %find top 20% highest connections
[ROI_right_top, Index_right] = maxk(ROI_right, floor(length(ROI_right)*top));

ROI_left_top = ROI_left_top(~isnan(ROI_left_top));
Index_left = Index_left(~isnan(ROI_left_top));
ROI_right_top = ROI_right_top(~isnan(ROI_right_top));
Index_right = Index_right(~isnan(ROI_right_top));

clear left_save
clear right_save
labels_left = string([]);
data_sort_left = zeros(1,length(Index_left));
for i = 1:length(Index_left)
    labels_left(i) = string(labels{Index_left(i),2});
    data_sort_left(i) = string(ROI_left(Index_left(i)));
end
left_save(1,:) = labels_left;
left_save(2,:) = Index_left;
left_save(3,:) = data_sort_left;
fid = fopen('labels_left.txt','wt');
fprintf(fid, '%-10s%-5s%s\n', left_save);
fclose(fid);

labels_right = string([]);
data_sort_right = zeros(1,length(Index_right));
for i = 1:length(Index_right)
    labels_right(i) = string(labels{Index_right(i),2});
    data_sort_right(i) = string(ROI_right(Index_right(i)));
end
right_save(1,:) = labels_right;
right_save(2,:) = Index_right;
right_save(3,:) = data_sort_right;
fid = fopen('labels_right.txt','wt');
fprintf(fid, '%-10s%-5s%s\n', right_save);
fclose(fid);

cd(home)
%}