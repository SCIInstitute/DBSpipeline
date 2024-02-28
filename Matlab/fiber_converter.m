% Fiber Converter
% Works in conjuntion with the two .m files 
% DSIStudio_2_curveField and scirunCurveField_To_vtk_9col
% Both have been converted to funcitons.
% Drop all of the .mat (fiber bundles) files exported from DSI Studio into 
% the same folder and just run this one (fiber_converter). 
% The output will be a .edge, a .pts, and a .vtk file for each .mat file in
% the folder, each packaged into its own folder.
%%
home = pwd;
folder = uigetdir();
cd(folder)
files = dir('*.mat');
%%
for i=1:length(files)
    %fprintf(files(i).name)
    DSIStudio_2_curveField(files(i).name)
    scirunCurveField_To_vtk_9col(files(i).name)
    
    name = files(i).name(1:end-4);
    mkdir(sprintf(name)) % make new directory for fiber files
    movefile(sprintf([name,'.edge']),sprintf(name))
    movefile(sprintf([name,'.pts']),sprintf(name))
    %movefile(sprintf([name,'_ASCII.vtk']),sprintf(name))
    movefile(sprintf([name,'.mat']),sprintf(name))
end
cd(home)

%% Functions
% DSIStudio_2_curveField
function DSIStudio_2_curveField(fibers)
% close all;
% clear;
% clc;

file = load(strcat(pwd,['\',fibers]));
tracts = file.tracts;
len = file.length;
% Adjust for voxel sizes from DSI Studio
tracts(1,:) = tracts(1,:)*2;
tracts(2,:) = tracts(2,:)*2;
tracts(3,:) = tracts(3,:)*2;
%adjusting for voxel size
edges = len;
%clear length;
fid = fopen([fibers(1:end-4),'.pts'],'wt');
fprintf(fid,'%12.8f %12.8f %12.8f\n',tracts);
fclose(fid);

fid = fopen([fibers(1:end-4),'.edge'],'wt');
counter=0; %% SCIRUN has zero based indexng
counter1=edges(1);
total_fibers = length(edges);
for i=1:total_fibers
    temp=[(counter:(counter1-2)); (counter+1:(counter1-1))];
    fprintf(fid,'%d %d\n',temp);
    counter=sum(edges(1:i));
    if(i<total_fibers)
        counter1=sum(edges(1:i+1));
    end
end
fclose(fid);
end

% scirunCurveField_To_vtk_9col
function scirunCurveField_To_vtk_9col(fibers)

% clear all;
% close;
% clc;

name = fibers(1:end-4);

m = dlmread(sprintf('%s.edge',name));          % Edge file
linePoints = dlmread(sprintf('%s.pts',name));  % Points file

display('Fiber Bundle Read');

% Separate into individual fibers
lineCount = 1;
lineEnd(1) = 0;
for i = 2:length(m);
    if m(i,1) ~= m(i-1,2)
        lineCount = lineCount + 1;
        lineEnd(lineCount) = i-2+lineCount;
    end
end
lineCount = lineCount + 1;
lineEnd(lineCount) = length(linePoints);
lineCount
display('Fiber Lines Separated');

fid = fopen(sprintf('%s_ASCII.vtk',name),'wt');
fprintf(fid,'# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\n');
fprintf(fid,sprintf('POINTS %d float\n',length(linePoints)));
fprintf(fid,'%12.8f %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f\n',linePoints');
fprintf(fid,'\n');
fprintf(fid,sprintf('LINES %d %d\n',lineCount-1,length(linePoints)+lineCount-1));

for i = 2:lineCount
    num_pts = lineEnd(i)-lineEnd(i-1);
    fprintf(fid,'%d ', num_pts);
    fprintf(fid,'%d ', [lineEnd(i-1):lineEnd(i)-1]);
    fprintf(fid,'\n');
end
fclose(fid);
end