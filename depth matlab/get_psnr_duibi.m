clear; close all;

path = 'C:\Users\sxl\Desktop\VCIP_A4_latex_for\新建文件夹\My Results\shishi\teddy\8\';
gt = imread(strcat(path, 'gt.png'));
sr = imread(strcat(path, 'sr.png'));
sr = im2uint8(sr);

wf = fopen(strcat(path, 'rmse.txt'),'w'); 

hr_rmse = rmse(gt, sr);

fprintf(wf,'%s\n',horzcat('hr_rmse:', num2str(hr_rmse)));
fclose(wf);  