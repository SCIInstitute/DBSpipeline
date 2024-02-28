filenames = dir("Image*");
AquisitionHeader = cell(1,length(filenames));
for i = 1:lenght(filenames)
    header = dicominfo(filenames(i));
    AquisitionHeader{i} = header.SequenceName;
end