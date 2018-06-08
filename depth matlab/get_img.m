clear; close all;

% name = 'temple_2';
% folder = strcat('D:\DATA\MPI sinetl\training\depth_viz\', name);
folder = ('D:\DATA\monkaa\rgb\family_x2\left');
savepath = 'D:\lanhao\FSRCNN\FSRCNN\rgb\';

filepaths = dir(fullfile(folder,'*.png'));

j = 797;
for i = 1 : length(filepaths)
    filename = filepaths(i).name;
    image = imread(fullfile(folder, filename));
    imwrite(image, strcat(savepath, 'rgb', num2str(j), '.png'));
    j = j+1;
end