clc;
clear all;

% det_list_dir = 'E:\ң��\����\Ŀ�������\SSD-fine-tuning\���Լ�¼\20170915\SSD_PLANE_300x300_score\detect_result\20170915\detect_list.txt';
% fid = fopen(det_list_dir,'r');
% info = textscan(fid, '%s');
% fclose(fid);
% fid = fopen('E:\ң��\����\Ŀ�������\SSD-fine-tuning\���Լ�¼\20170915\SSD_PLANE_300x300_score\detect_result\20170915\test.txt','w+');
% for i=1:length(info{1})
%     num_loc = regexp(info{1}(i),'/','start');%ids��¼��ǰ�����ͼ��ı��
%     img_long = info{1}(i);
%     img_id = img_long{1}(num_loc{1}(end)+1:end-4);
% %     input_info = [img_id '\n'];
%     fprintf(fid,'%s\r\n',img_id);
% end
% fclose(fid);

result_list_dir = 'E:\ң��\����\Ŀ�������\SSD-fine-tuning\���Լ�¼\20170915\SSD_PLANE_300x300_score\detect_result\20170915\vision_result.txt';
fid = fopen(result_list_dir,'r');
info = textscan(fid, '%s %f %f %f %f %f %f');
fclose(fid);
