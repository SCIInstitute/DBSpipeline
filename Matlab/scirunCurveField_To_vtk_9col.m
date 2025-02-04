function scirunCurveField_To_vtk_9col()

% clear all;
% close;
% clc;
home = pwd;
[filename,dirname] = uigetfile('*.pts');
cd(dirname);
name = filename(1:end-4);

m = dlmread(sprintf('%s.edge',name));          % Edge file
linePoints = dlmread(sprintf('%s.pts',name));  % Points file

display('Fiber Bundle Read');

%% Separate into individual fibers
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
cd(home)
end