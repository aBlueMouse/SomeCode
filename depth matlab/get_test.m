clear; close all;

%% settings
depthpath = 'F:\record\0328\Sampler\Monkaa\disparity\';
rgbpath = 'F:\record\0328\Sampler\Monkaa\RGB_cleanpass\left\';
savepath = 'F:\record\0328\test\';
scale = 2;

depth = imread(strcat(depthpath, 'monkaa_48_depth.png'));
rgb = imread(strcat(rgbpath, '0048.png'));

rgb = rgb2ycbcr(rgb);
rgb = rgb(:, :, 1);

% depth = imresize(depth, [256, 256]);
% rgb = imresize(rgb, [256, 256]);

ds = imresize(depth, 1/scale, 'bicubic');
ds = imresize(ds, scale, 'bicubic');

imwrite(depth, strcat(savepath, 'gt10.png'));
imwrite(rgb, strcat(savepath, 'rgb10.png'));
imwrite(ds, strcat(savepath, 'bds2_10.png'));