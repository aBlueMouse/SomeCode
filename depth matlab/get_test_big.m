clear; close all;

%%
depthpath = 'C:\Users\sxl\Desktop\Sampler\test19\';
rgbpath = 'C:\Users\sxl\Desktop\Sampler\test19\';
savepath = 'F:\record\0423\test_8\19\';
scale = 8;

depth = imread(strcat(depthpath, 'depth.png'));
rgb = imread(strcat(rgbpath, 'rgb.png'));

rgb = rgb2ycbcr(rgb);
rgb = rgb(:, :, 1);

depth = imresize(depth, 1/2);
rgb = imresize(rgb, 1/2);

% depth = depth(136 : 391, 542 : 797);
% rgb = rgb(136 : 391, 542 : 797);


[hei,wid] = size(depth);
hei1 = ceil(hei/scale) * scale;
hei2 = hei1 - hei;
wid1 = ceil(wid/scale) * scale;
wid2 = wid1 - wid;

ds = padarray(depth, [hei2, wid2], 'symmetric', 'post');
ds = imresize(ds, 1/scale, 'bicubic');
ds = imresize(ds, scale, 'bicubic');
ds = ds(1 : hei, 1 : wid);
% ds = imresize(depth, 1/scale, 'bicubic');
% ds = imresize(ds, scale, 'bicubic');

imwrite(depth, strcat(savepath, 'gt19.png'));
imwrite(rgb, strcat(savepath, 'rgb19.png'));
imwrite(ds, strcat(savepath, 'bds', num2str(scale), '_19.png'));