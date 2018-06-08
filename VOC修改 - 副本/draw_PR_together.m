clc;
clear all;

load('E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\SSD\20171206\detect_result\0.8\eval_result.mat');
prec1 = prec;
rec1 = rec;

ap1=0;
p=[];
for t=0:0.001:1
    p=max(prec1(rec1>=t));%设置不同阈值，画PR曲线
    if isempty(p)
        p=0;
    end
    ap1=ap1+p/1001;
end

load('E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\SSD\20171024\detect_result\0.8\eval_result.mat');
prec2 = prec;
rec2 = rec;

ap2=0;
p=[];
for t=0:0.001:1
    p=max(prec2(rec2>=t));%设置不同阈值，画PR曲线
    if isempty(p)
        p=0;
    end
    ap2=ap2+p/1001;
end


% load('E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\20170921\1\detect_result\th0.8\eval_result.mat');
% prec3 = prec;
% rec3 = rec;
% 
% ap3=0;
% p=[];
% for t=0:0.1:1
%     p=max(prec3(rec3>=t));%设置不同阈值，画PR曲线
%     if isempty(p)
%         p=0;
%     end
%     ap3=ap3+p/11;
% end


plot(rec1,prec1,'-b','LineWidth',2);
hold on;
plot(rec2,prec2,'-r','LineWidth',2);
% hold on;
% plot(rec3,prec3,'-g','LineWidth',2);

xlabel 'recall'
ylabel 'precision'
title(sprintf('class: %s','Airplane   IOU=0.8'));
axis([0 1 0 1]);
grid off;
legend([sprintf('SSD-TS,AP=%s'),num2str(ap1)],[sprintf('SSD-VGG16,AP=%s'),num2str(ap2)],4);
% legend([sprintf('Th=0.5,AP=%s'),num2str(ap1)],[sprintf('Th=0.7,AP=%s'),num2str(ap2)],[sprintf('Th=0.8,AP=%s'),num2str(ap3)],4);

% hold on;
% 
% plot(rec2,prec2,'-');
% xlabel 'recall'
% ylabel 'precision'
% title(sprintf('class: %s','Airplane'));
% axis([0 1 0 1]);
% grid off;
% legend(['AP=',num2str(ap2)]);


