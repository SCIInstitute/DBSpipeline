%% vtk_9col_2_scirun_curvefield
% Read VTK file, must have 9 colum format for points, (e.g. Morel) and convert to
% SciRun format *.pts and *.edge
% SGJ

%% Reading File

clear all; 
clc;
home = pwd;
[filename,dirname] = uigetfile('*.vtk', 'MultiSelect', 'on');
cd(dirname);
for k = 1:length(filename)
fid = fopen(filename{k});
%fid = fopen(filename);
%% Extract Points. This extracts the co-ordinates of the points and stores
% them in a vector 'points'. This part of the code is copied from
% vtk_9col_2_scirun. 

C = textscan(fid,'%s %f %s',1,'HeaderLines',4);
pnt = C{1,2}; %how many points are in the file (p = str2num(char(C{1,2})))
rowes_scan = ceil((pnt/3));%how many rowes to read
d = textscan(fid,'%f  %f  %f %f  %f  %f  %f %f %f',rowes_scan);
all = [d{1} d{2} d{3} d{4} d{5} d{6} d{7} d{8} d{9}];
[m,n] = size(all);
rowes = (m * n)/3;
all2 = all';
all3 = reshape(all2,3,rowes);%make sure you have the correct size depending on file:
all4 = all3';
points = all4;
points=points(1:pnt,:);  %SJ added line to overcome NaN in the points vector 
clear C d all* rowes_scanv rowes m n;

%% Extract connection information for curves from vtk file 

tline=fgets(fid);
while(tline(1)~='L')
    tline=fgets(fid);
end
tline=sscanf(tline,'%s %d %d');
total_fibers=tline(6); % First 5 values are for string 'LINES'

ind_pts=zeros(total_fibers,1);
for i=1:total_fibers
    temp=fgets(fid);
    ind_pts(i)=sscanf(temp,'%d',1);
    %sscanf(temp,'%d',1)
end

if sum(ind_pts)==pnt
    disp('Reading Successful...Now Preparing Files');
else
    disp('Total no. of points contradictory');
end

fclose(fid);
%% Write .pts and .edge file 
name = filename{k};
%file_final = name(1:end-11); %Remove legacy/fibers.vtk
file_final = name(1:end-4); %Remove .vtk

fid = fopen([file_final,'.pts'],'wt');
fprintf(fid,'%12.8f %12.8f %12.8f\n',points');
fclose(fid);

fid = fopen([file_final,'.edge'],'wt');
counter=0; %% SCIRUN has zero based indexng
counter1=ind_pts(1);
for i=1:total_fibers
    temp=[(counter:(counter1-2)); (counter+1:(counter1-1))];
    fprintf(fid,'%d %d\n',temp);
    counter=sum(ind_pts(1:i));
    if(i<total_fibers)
        counter1=sum(ind_pts(1:i+1));
    end
end
fclose(fid);
end
cd(home)