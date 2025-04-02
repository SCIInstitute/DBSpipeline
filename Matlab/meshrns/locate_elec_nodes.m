function locate_elec_nodes(subject_dir)
%LOCATE_ELEC_NODES finds the nodes corresponding to specific electrodes in
%the headmesh

subject_dir =  convertCharsToStrings(subject_dir);
%Determining which nodes are electrodes
%seeg lead mesh
elec_node = [];
load(strcat(subject_dir,'/lead_data.mat'));
elecs = scirunfield.node;
elec_node_val = scirunfield.field;
for i = 1:max(elec_node_val)
    elec_node{i}=elecs(:,find(elec_node_val==i));
end

%Head model mesh
load(strcat(subject_dir,'/head_mesh.mat'));
mesh_node = scirunfield.node;
mesh_val = scirunfield.field;
mesh_ind = find(mesh_val == 5); %mesh values that are electrode nodes

%Nodes for all electrodes
nodes = cell(1,max(elec_node_val));
for k = 1:max(elec_node_val)
    elec_node_new = elec_node{k};
    for i = 1:length(elec_node_new)
        for j = 1:length(mesh_node)
            if (mesh_node(1,j) == elec_node_new(1,i)) && (mesh_node(2,j) == elec_node_new(2,i)) && (mesh_node(3,j) == elec_node_new(3,i))
                nodes{k} = [nodes{k} j];
            end
        end
    end
end

links = NaN*ones(length(mesh_node),1);
for k =1:max(elec_node_val)
    for i=1:length(nodes{1,k})
        links(nodes{1,k}(i))=k;
    end
end

save(fullfile(subject_dir, "/linked_nodes.mat"), 'links');
end

