function principalaxes(subject_dir)
% PRINCIPLEAXES Calcualtes the normal vector for each electrode.
% Needs fielddata input from SCIRun
% Chantel Charlebois
subject_dir =  convertCharsToStrings(subject_dir);
load(subject_dir+'\fielddata.mat')
A = scirunmatrix;
x = A(:,1);
y = A(:,2);
z = A(:,3);
elec = A(:,4);
eigval = [];
eigvec = [];
I=[];
n=[];
for i = 1:max(elec)
    B=A;
    Ixx = sum(y(elec==i).^2 + z(elec==i).^2);
    Iyy = sum(x(elec==i).^2 + z(elec==i).^2);
    Izz = sum(x(elec==i).^2 + y(elec==i).^2);
    Ixy = -sum(x(elec==i).*y(elec==i));
    Ixz = -sum(x(elec==i).*z(elec==i));
    Iyz = -sum(y(elec==i).*z(elec==i));
    I{i} = [Ixx Ixy Ixz; Ixy Iyy Iyz; Ixz Iyz Izz];
    [eigvec{i},eigval{i}] = eig(I{i});
    eigval1{i}=[eigval{i}(1,1) eigval{i}(2,2) eigval{i}(3,3)];
    n(i) = find(min(eigval1{i}));
    normalvec(i,:) = eigvec{i}(:,n(i));%.*eigval{i}(1,1); scale
    if normalvec(i,3)<0
        normalvec(i,:)=-normalvec(i,:);
    end
end
save([subject_dir+'\normalvec'],'normalvec');
end