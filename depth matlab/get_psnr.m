clear; close all;

path = 'F:\record\0505-2\shishi2\15\';
gt = imread(strcat(path, 'gt15.png'));
ds2 = imread(strcat(path, 'bds2_15.png'));
sr = imread(strcat(path, 'sr100000_2.png'));
% sr = medfilt2(sr);

wf = fopen(strcat(path, 'psnr_rmse.txt'),'w'); 

% lr_psnr = psnr(gt, ds2);
% hr_psnr = psnr(gt, sr);

lr_psnr = PSNR(gt, ds2);
hr_psnr = PSNR(gt, sr);

lr_rmse = rmse(gt, ds2);
hr_rmse = rmse(gt, sr);

fprintf(wf,'%s\n',horzcat('lr_psnr:', num2str(lr_psnr), '       hr_psnr:', num2str(hr_psnr)));
fprintf(wf,'%s\n',horzcat('lr_rmse:', num2str(lr_rmse), '       hr_rmse:', num2str(hr_rmse)));
fclose(wf);  