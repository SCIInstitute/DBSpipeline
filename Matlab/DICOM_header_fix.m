%cd('Z:\TBI_Study\pDA301\Burned_Images')
orig_dicom_directory=uigetdir; %burned image written by Slicer
new_dicom_directory=uigetdir; %New directory to be created
goodHeader_directory=uigetdir; %original image with a working header
home = pwd;
orig_filenames=dir(orig_dicom_directory);
goodHeader_filenames=dir(goodHeader_directory);

for n=3:size(orig_filenames,1)
    cd(orig_dicom_directory);
    curFile=orig_filenames(n).name;
    newVol=dicomread(curFile);
    cd(goodHeader_directory);
    curHeader=goodHeader_filenames(n).name;
    goodHeader=dicominfo(curHeader);
    cd(new_dicom_directory);
    writeDCMname=sprintf('T1_contacts_burned_%d.dcm',n);
    %newVol = flip(newVol,1); % might be needed for flipping DICOMS
    %newVol = flip(newVol,2); % ^^
    dicomwrite(newVol,writeDCMname,goodHeader);
    %imagesc(newVol)
    %pause
end

cd(home)