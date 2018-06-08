clear; close all;
%% settings
folder = 'D:\CODE\FSRCNN\FSRCNN\Test\depth2';
folder2 = 'D:\CODE\FSRCNN\FSRCNN\Test\delta2';
savepath = 'test.h5';
size_input = 14;
size_label = 19;
scale = 2;
stride = size_input;

%% initialization
data = zeros(size_input, size_input, 1, 1);
label = zeros(size_label, size_label, 1, 1);
padding = abs(size_input - size_label)/2;
count = 0;

%% generate data
filepaths = dir(fullfile(folder,'*.png'));

for i = 1 : length(filepaths)
    
%     image = imread(fullfile(folder, filepaths(i).name));
%     %image = rgb2ycbcr(image);
%     %image = im2double(image(:, :, 1));
%     image = im2double(image(:, :));
%     
%     im_label = modcrop(image, scale);
%     im_input = imresize(im_label, 1/scale, 'bicubic');
%     [hei,wid] = size(im_input);
    
     image = imread(fullfile(folder, filepaths(i).name));
    %image = rgb2ycbcr(image);
    %image = im2double(image(:, :, 1));
    image = im2double(image(:, :));
    %image2 = imread(fullfile(folder2, filepaths(i).name));
    load(fullfile(folder2, filepaths(i).name(1:end-4)));
    image2 = delta;
    %image2 = im2double(image2(:,:));
    im_label = modcrop(image, scale);
    im_input = imresize(im_label, 1/scale, 'bilinear');
    im_label = modcrop(image2, scale);
    [hei,wid] = size(im_input);

    for x = 1 : stride : hei - size_input + 1
        for y = 1 : stride : wid - size_input + 1

            locx = scale * (x + floor((size_input - 1)/2)) - floor((size_label + scale)/2 - 1);
            locy = scale * (y + floor((size_input - 1)/2)) - floor((size_label + scale)/2 - 1);
            
            subim_input = im_input(x : size_input + x - 1, y : size_input + y - 1);
            subim_label = im_label(locx : size_label + locx - 1, locy : size_label + locy - 1);
            
            count = count + 1;
            data(:, :, 1, count) = subim_input;
            label(:, :, 1, count) = subim_label;
        end
    end
end
order = randperm(count);
data = data(:, :, 1, order);
label = label(:, :, 1, order); 

%% writing to HDF5
chunksz = 2;
created_flag = false;
totalct = 0;

for batchno = 1:floor(count/chunksz)
    last_read = (batchno-1)*chunksz;
    batchdata = data(:,:,1,last_read+1:last_read+chunksz); 
    batchlabs = label(:,:,1,last_read+1:last_read+chunksz);

    startloc = struct('dat',[1,1,1,totalct+1], 'lab', [1,1,1,totalct+1]);
    curr_dat_sz = store2hdf5(savepath, batchdata, batchlabs, ~created_flag, startloc, chunksz); 
    created_flag = true;
    totalct = curr_dat_sz(end);
end
h5disp(savepath);