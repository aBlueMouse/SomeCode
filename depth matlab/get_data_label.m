clear; close all;

%% settings
folder = 'D:\lanhao\FSRCNN\FSRCNN\depth-aug';
labelsavepath = 'D:\lanhao\FSRCNN\FSRCNN\depth-label\';
datasavepath = 'D:\lanhao\FSRCNN\FSRCNN\depth-data2\';
size_data = 128;
size_label = 128;
scale = 2;
stride = 100;

%% initialization
% data = zeros(size_data, size_data, 1, 1);
% label = zeros(size_label, size_label, 1, 1);
filepaths = dir(fullfile(folder,'*.png'));

% %% get label 
% for i = 1 : length(filepaths)
%     filename = filepaths(i).name;
%     [add, im_name, type] = fileparts(filepaths(i).name);
%     image = imread(fullfile(folder, filename));    
% %     image = imresize(image, 1/2, 'nearest');
% 
%     [hei,wid] = size(image);
%     
%     count = 1;
%     
%     for j = 1 : stride : hei-127
%         for k = 1 : stride : wid-127
%             im_label = image(j : j+127, k : k+127);
%             imwrite(im_label, strcat(labelsavepath, 'label_', im_name, '_', num2str(count), '.png'));
%             count = count + 1;
%         end
%     end   
% end

%% get data
for i = 1 : length(filepaths)
    filename = filepaths(i).name;
    [add, im_name, type] = fileparts(filepaths(i).name);
    image = imread(fullfile(folder, filename));
%     image = imresize(image, 1/2, 'nearest');
    [hei,wid] = size(image);
    hei1 = ceil(hei/scale) * scale;
    hei2 = hei1 - hei;
    wid1 = ceil(wid/scale) * scale;
    wid2 = wid1 - wid;

    image = padarray(image, [hei2, wid2], 'symmetric', 'post');
    image = imresize(image, 1/scale, 'bicubic');
    image = imresize(image, scale, 'bicubic');
    image = image(1 : hei, 1 : wid);
    
    count = 1;
    
    for j = 1 : stride : hei-127
        for k = 1 : stride : wid-127
            im_data = image(j : j+127, k : k+127);
            imwrite(im_data, strcat(datasavepath, 'data_', num2str(scale), '_', im_name, '_',  num2str(count), '.png'));
            count = count + 1;
        end
    end    
end