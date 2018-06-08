clear; close all;

path = 'G:\0831\teddy\';
gt = imread(strcat(path, 'gt.png'));
% ds2 = imread(strcat(path, 'bds_8.png'));
sr1 = imread(strcat(path, 'sr150000_x2_1.png'));
sr2 = imread(strcat(path, 'sr150000_x2_2.png'));
sr3 = imread(strcat(path, 'sr150000_x2_3.png'));
sr4 = imread(strcat(path, 'sr150000_x2_4.png'));
% sr = medfilt2(sr);

[hei,wid] = size(gt);
[h, w] = size(sr1);
sr = zeros(hei, wid);
sr(1 : (hei/2), 1 : (wid/2)) = sr1(1 : (hei/2), 1 : (wid/2));
sr(1 : (hei/2), (wid/2 + 1) : wid) = sr2(1 : (hei/2), 6 : w);
sr((hei/2 + 1) : hei, 1 : (wid/2)) = sr3(6 : h, 1 : (wid/2));
sr((hei/2 + 1) : hei, (wid/2 + 1) : wid) = sr4(6 : h, 6 : w);
sr = uint8(sr);

% wf = fopen(strcat(path, 'psnr_rmse.txt'),'w'); 
% 
% % lr_psnr = psnr(gt, ds2);
% % hr_psnr = psnr(gt, sr);
% 
% lr_psnr = PSNR(gt, ds2);
% hr_psnr = PSNR(gt, sr);
% 
% lr_rmse = rmse(gt, ds2);
% hr_rmse = rmse(gt, sr);
% 
% fprintf(wf,'%s\n',horzcat('lr_psnr:', num2str(lr_psnr), '       hr_psnr:', num2str(hr_psnr)));
% fprintf(wf,'%s\n',horzcat('lr_rmse:', num2str(lr_rmse), '       hr_rmse:', num2str(hr_rmse)));
% fclose(wf);
% 
% imwrite(sr, strcat(path, 'sr.png'));

hr_rmse = rmse(gt, sr);
hr_psnr = PSNR(gt, sr);
imwrite(sr, strcat(path, 'sr150000.png'));