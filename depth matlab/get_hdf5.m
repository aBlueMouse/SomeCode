clear;close all;
%% settings
savepath = 'D:\lanhao\FSRCNN\FSRCNN\hdf5\lh_train';
size_input = 256;
size_label = 256;
scale = 2;
% stride = 41;

%% initialization
data = zeros(size_input, size_input, 1, 1);
label = zeros(size_label, size_label, 1, 1);
% padding = abs(size_input - size_label)/2;

%% generate data
file = importdata('label.txt');
[num, ~] = size(file.textdata);

filenum = 1;

for j = 1 : 16384 : num
    count = 0;
    for i = j : j+16383
        filepaths = file.textdata(i, :);
        filepaths = strcat(filepaths{1}, filepaths{2}, filepaths{3});

        im_label = imread(filepaths);
%     image = rgb2ycbcr(image);
        im_label = im2double(im_label);

        [hei,wid] = size(im_label);
        im_input = imresize(imresize(im_label,1/scale,'bicubic'),[hei,wid],'bicubic');

        count=count+1;
        data(:, :, 1, count) = im_input;
        label(:, :, 1, count) = im_label;
    end

    order = randperm(count);
    data = data(:, :, 1, order);
    label = label(:, :, 1, order);

%% writing to HDF5
    for batch = 1 : 2048 : 16384
        data1 = data(:, :, 1, batch : batch + 2047);
        label1 = label(:, :, 1, batch : batch + 2047);

        chunksz = 64;
        created_flag = false;
        totalct = 0;

        for batchno = 1:floor(2048/chunksz)
            last_read=(batchno-1)*chunksz;
            batchdata = data1(:,:,1,last_read+1:last_read+chunksz);
            batchlabs = label1(:,:,1,last_read+1:last_read+chunksz);

            startloc = struct('dat',[1,1,1,totalct+1], 'lab', [1,1,1,totalct+1]);
            save = strcat(savepath, '_', num2str(file), '.h5');
            curr_dat_sz = store2hdf5(save, batchdata, batchlabs, ~created_flag, startloc, chunksz);
            filenum = filenum + 1;
            created_flag = true;
            totalct = curr_dat_sz(end);
        end
    end
end
% h5disp(savepath);
