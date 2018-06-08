clc;
clear all;

% det_list_dir = 'E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\20170915\SSD_PLANE_300x300_score\detect_result\20170915\detect_list.txt';
% fid = fopen(det_list_dir,'r');
% info = textscan(fid, '%s');
% fclose(fid);
% fid = fopen('E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\20170915\SSD_PLANE_300x300_score\detect_result\20170915\test.txt','w+');
% for i=1:length(info{1})
%     num_loc = regexp(info{1}(i),'/','start');%ids记录当前处理的图像的编号
%     img_long = info{1}(i);
%     img_id = img_long{1}(num_loc{1}(end)+1:end-4);
% %     input_info = [img_id '\n'];
%     fprintf(fid,'%s\r\n',img_id);
% end
% fclose(fid);

result_list_dir = 'E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\20170915\SSD_PLANE_300x300_score\detect_result\20170915\vision_result.txt';
fid = fopen(result_list_dir,'r');
info = textscan(fid, '%s %f %f %f %f %f %f');
fclose(fid);
