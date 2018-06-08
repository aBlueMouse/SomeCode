clear; close all;

%%
folder = 'teddy';
scale = 8;
depthpath = strcat('D:\lanhao\FSRCNN\FSRCNN\paper\', folder, '\');
rgbpath = strcat('D:\lanhao\FSRCNN\FSRCNN\paper\', folder, '\');
savepath = strcat('D:\lanhao\FSRCNN\FSRCNN\paper\', folder, '\', num2str(scale), '\');


depth = imread(strcat(depthpath, 'depth.png'));
rgb = imread(strcat(rgbpath, 'rgb.png'));

rgb = rgb2ycbcr(rgb);
rgb = rgb(:, :, 1);

[hei,wid] = size(depth);
hei1 = ceil(hei/scale) * scale;
hei2 = hei1 - hei;
wid1 = ceil(wid/scale) * scale;
wid2 = wid1 - wid;

ds = padarray(depth, [hei2, wid2], 'symmetric', 'post');
ds = imresize(ds, 1/scale, 'bicubic');
ds = imresize(ds, scale, 'bicubic');
ds = ds(1 : hei, 1 : wid);

rgb1 = rgb(1 : (hei/2 + 5), 1 : (wid/2 + 5));
rgb2 = rgb(1 : (hei/2 + 5), (wid/2 - 4) : wid);
rgb3 = rgb((hei/2 - 4) : hei, 1 : (wid/2 + 5));
rgb4 = rgb((hei/2 - 4) : hei, (wid/2 - 4) : wid );

ds1 = ds(1 : (hei/2 + 5), 1 : (wid/2 + 5));
ds2 = ds(1 : (hei/2 + 5), (wid/2 - 4) : wid);
ds3 = ds((hei/2 - 4) : hei, 1 : (wid/2 + 5));
ds4 = ds((hei/2 - 4) : hei, (wid/2 - 4) : wid );

imwrite(depth, strcat(savepath, 'gt.png'));
imwrite(rgb, strcat(savepath, 'rgb_g.png'));
imwrite(ds, strcat(savepath, 'bds_', num2str(scale), '.png'));

imwrite(rgb1, strcat(savepath, 'rgb_g_1.png'));
imwrite(rgb2, strcat(savepath, 'rgb_g_2.png'));
imwrite(rgb3, strcat(savepath, 'rgb_g_3.png'));
imwrite(rgb4, strcat(savepath, 'rgb_g_4.png'));

imwrite(ds1, strcat(savepath, 'bds_', num2str(scale), '_1.png'));
imwrite(ds2, strcat(savepath, 'bds_', num2str(scale), '_2.png'));
imwrite(ds3, strcat(savepath, 'bds_', num2str(scale), '_3.png'));
imwrite(ds4, strcat(savepath, 'bds_', num2str(scale), '_4.png'));