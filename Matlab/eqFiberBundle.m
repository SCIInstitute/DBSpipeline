clear all; 
clc;
home = pwd;
[filename,dirname] = uigetfile('*.edge', 'MultiSelect', 'on');
cd(dirname);
filename = string(filename);

for k = 1:length(filename)
m = dlmread(filename{k});
linePoints = dlmread([filename{k}(1:end-5) '.pts']);
display('Fiber Bundle Read');

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
lineCount - 1
display('Fiber Lines Separated');

% figure;
% plot(lineVoltages(lineEnd(1):lineEnd(2),1));
d = 0.5;
pts = [];
edges = [];
tlinecount = 0;
edgecount = 0;
index = [];
count = 1;
for i = 2:lineCount
    fiber = linePoints(lineEnd(i-1)+1:lineEnd(i),:);
    n = fiber(1,:);
    pts = [pts;n];
    for j = 1:length(fiber)-1
        a = n;      
        b = fiber(j+1,:);
        e = pdist([a;b]);
        while (e > d)
            a = n;
            v = (b-a)/norm(b-a);
            n = a + d*v;
            e = pdist([n;b]);
            pts = [pts;n];
            edges = [edges; edgecount edgecount+1];
            edgecount = edgecount + 1;
        end
    end
    edgecount = edgecount + 1;
    %disp(i)
end
%histogram(edgeLengths,100);
clear m;
m = edges;
% Check edges
lineCount = 1;
tlineEnd(1) = -1;
for i = 2:length(m);
    if m(i,1) ~= m(i-1,2)
        lineCount = lineCount + 1;
        tlineEnd(lineCount) = i-3+lineCount;
    end
end
lineCount
fid = fopen([filename{k}(1:end-5) '_resamp.pts'],'wt');
fprintf(fid,'%12.8f %12.8f %12.8f\n',pts');
fclose(fid);

fid = fopen([filename{k}(1:end-5) '_resamp.edge'],'wt');
fprintf(fid,'%d %d\n',edges');
display('Fibers saved');
fclose(fid);
end
mkdir Resample_0.5mm
movefile *resamp* Resample_0.5mm
cd("Resample_0.5mm")
resamp = dir("*resamp*");
for ii = 1:length(resamp)
    newname = erase(resamp(ii).name,'_resamp');
    movefile(resamp(ii).name,newname)
end
cd(home)

