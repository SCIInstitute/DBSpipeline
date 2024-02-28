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
pts_dist=[];
for i = 2:lineCount
    fiber = linePoints(lineEnd(i-1)+1:lineEnd(i),:);
    n = fiber(1,:);
    pts = [pts;n];
    for j = 1:length(fiber)-1
        a = fiber(j,:);      
        b = fiber(j+1,:);
        e = pdist([a;b]);
        pts_dist = [pts_dist e];
    end
end
histogram(pts_dist)
end