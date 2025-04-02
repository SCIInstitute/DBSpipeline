function calc_voltages(subject_dir)
% get subject_dir
subject_dir =  convertCharsToStrings(subject_dir);

%load link matrix
load(subject_dir+'\link_matrix.mat');
links = scirunmatrix;

% Determine electrode voltage
load(subject_dir+'\voltage_sol.mat')
field = scirunfield.field;

vol = [];
for i = 1:max(links)
    ind = find(links==i);
    vol(i) = field(ind(1));
end

save(subject_dir+'\voltage_sol.txt','vol','-ascii');
end