clear; close all;

%% settings
folder = 'D:\lanhao\FSRCNN\FSRCNN\rgb-aug';
labelsavepath = 'D:\lanhao\FSRCNN\FSRCNN\rgb-data\';
size_data = 128;
size_label = 128;
stride = 100;

%% initialization
% data = zeros(size_data, size_data, 1, 1);
% label = zeros(size_label, size_label, 1, 1);
filepaths = dir(fullfile(folder,'*.png'));

%% get gray 
for i = 1 : length(filepaths)
    filename = filepaths(i).name;
    [add, im_name, type] = fileparts(filepaths(i).name);
    image = imread(fullfile(folder, filename)); 
    image = rgb2ycbcr(image);
    image = image(:, :, 1);

    [hei,wid] = size(image);
    
    count = 1;
    
    for j = 1 : stride : hei-127
        for k = 1 : stride : wid-127
            im_label = image(j : j+127, k : k+127);
            imwrite(im_label, strcat(labelsavepath, 'rgb_', im_name, '_', num2str(count), '.png'));
            count = count + 1;
        end
    end   
end