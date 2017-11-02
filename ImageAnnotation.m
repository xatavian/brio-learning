%% Read image data and write to file

% Recipe for labeling images

% 1. Open 'Training Image Labeler' from APPS. You might need to install image
% processing and computer vision package for MATLAB, if you made a custom
% installation. 
% 2. In the APP, add the images that needs to be precessed.
% 3. Add ROI Label, eg name it ball 
% 4. center the box around the ball - it should now be labeled 'ball'
% 5. When done with the images, press 'Export ROIs' as a table and name of
% your choice, eg just table.. 
% 6. Run the script - file is saved on the root locale drive, unless
% specified otherwise by user.

table = table; %name of table
N = size(table,1);

fileID = fopen('tableofballpos2.txt','w');
for i = 1 : N
   
    x = round(table.ball(i,1) + table.ball(i,3)/2);
    y = round(table.ball(i,2) + table.ball(i,4)/2);
    
    [filepath,name,ext] = fileparts(table.imageFilename{i});
    fprintf(fileID, name);
    fprintf(fileID,ext);
    fprintf(fileID, ' %2d %2d\n',x,y);
    
end

fclose(fileID);