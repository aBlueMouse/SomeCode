clc;
clear all;

VOCopts.imgsetpath = ...%测试样本集的txt文件路径，txt文件保存所有参与测试的图片名称,无路径和后缀名
    'E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\SSD\20171206\detect_result\test.txt';
%     'E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\20170915\SSD_PLANE_300x300_score\detect_result\20170915\test.txt';
    
% VOCopts.testset = 'test';%选用测试还是验证集用于测试
VOCopts.annopath='E:\遥感\数据\目标检测程序\数据集\飞机数据集\韩军伟\plane_8darg\Annotations\';%标注文件的路径
% VOCopts.annopath='E:\遥感\数据\目标检测程序\数据集\飞机数据集\小目标\Annotations\';%标注文件的路径
% VOCopts.annopath=[VOCopts.datadir 'Annotations\'];%d.xml'];
VOCopts.detrespath=...%检测结果保存路径
    'E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\SSD\20171206\detect_result\vision_result.txt';
%     'E:\遥感\数据\目标检测程序\SSD-fine-tuning\调试记录\20170915\SSD_PLANE_300x300_score\detect_result\20170915\vision_result.txt';
      
VOCopts.minoverlap=0.8;%IOU的阈值，大于此阈值认为是检测正确
cls = 'Airplane';%检测的目标类别
draw = true;%是否画出PR曲线


% load test set
% [gtids_temp,~]=textread(VOCopts.imgsetpath,'%s%s');%gtids为测试集中图像的编号向量
[gtids,~]=textread(VOCopts.imgsetpath,'%s%s');%gtids为测试集中图像的编号向量
% for i=1:length(gtids_temp)
%     gtids{i} = gtids_temp(i);
% end
% load ground truth objects
tic;
npos=0;
gt(length(gtids))=struct('BB',[],'diff',[],'det',[]);
for i=1:length(gtids)%i为测试集中第几幅图像
%     gtids{i}
    % display progress，输出时间
    if toc>1
        fprintf('%s: pr: load: %d/%d\n',cls,i,length(gtids));
        drawnow;
        tic;
    end
%     a = [VOCopts.annopath num2str(gtids{i}) '.xml']
    % read annotation
    rec=PASreadrecord([VOCopts.annopath gtids{i} '.xml']);
    
    % extract objects of class
    clsinds=strmatch(cls,{rec.objects(:).class},'exact');%比较groundTruth与所需的类别是否一致，相同的objects(:).class索引记录在clsinds
    gt(i).BB=cat(1,rec.objects(clsinds).bbox)';%提取clsinds对应的gt目标的坐标，记录在BB
    gt(i).diff=[rec.objects(clsinds).difficult];
    gt(i).det=false(length(clsinds),1);%生成clsinds行1列的逻辑非矩阵（全为0），记录在det，用于判断某一个gt是否被检测到
    npos=npos+sum(~gt(i).diff);%记录整个测试集中非困难的目标总数（完整的目标？）
end
% % % % % % % % % % % % % % % % % % % % % % 

% load results
fid = fopen(VOCopts.detrespath,'r');
info = textscan(fid, '%s %s %f %f %f %f %f');
fclose(fid);
det_ids = info{1};
det_num = unique(det_ids);%det_num表示所有检测结果中一共包含这些图像
tp_all = [];%记录所有检测图像的true positive
fp_all = [];%记录所有检测图像的false positive
confidence_all = [];%记录所有检测图像的每个结果对应的置信度
for jpg_id=1:length(det_num)%一幅一幅将检测图像结果进行处理
    index = [];
    for k=1:length(det_ids)%挑选出所有检测结果中某一幅图像的结果
        if(det_ids{k}==det_num{jpg_id})
            index = [index k];
        end
    end
    class_id = info{2}(index);%记录这一图像对应的类别、置信度、坐标等等
    confidence = info{3}(index);
    b1 = info{4}(index);
    b2 = info{5}(index);
    b3 = info{6}(index);
    b4 = info{7}(index);

    % [ids, ~, confidence,b1,b2,b3,b4]=textread(VOCopts.detrespath,'%s %d %d %d %d %d','delimiter', ' ');%提取检测结果的第id幅图像的第cls类结果
    BB=[b1 b2 b3 b4]';%某一幅图像的所有检测结果记录在BB矩阵中，每一列为一个目标结果

    % sort detections by decreasing confidence
    [sc,si]=sort(-confidence);%将所有结果的置信度降序排列
%         ids=ids(si);%ids为当前第id幅图检测结果中的图像名字，一个（si）只对应1幅
    BB=BB(:,si);
    
    num_loc = regexp(det_num{jpg_id},'/','start');%ids记录当前处理的图像的编号
    ids = det_num{jpg_id}(num_loc(end)+1:end-4);
    
        % assign detections to ground truth objects
    nd=length(confidence);
    tp=zeros(nd,1);%记录检测结果中检测到目标的结果true positive
    fp=zeros(nd,1);%记录检测结果中未检测到目标的结果false positive
    tic;
    for d=1:nd%d代表某一个检测结果
        % display progress
        if toc>1
            fprintf('%s: pr: compute: %d/%d\n',cls,d,nd);
            drawnow;
            tic;
        end

        % find ground truth image
        gt_index = [];
        for i=1:length(gtids)   %提取gtids中与当前检测图像ids{d}对应的gt索引，如果检测的图像一个目标也没有检测到这里会报错
            if(gtids{i}==ids)
                gt_index = [gt_index i];
            end
        end
        if isempty(gt_index)
            error('unrecognized image "%s"',ids);
        elseif length(gt_index)>1
            error('multiple image "%s"',ids);
        end

        % assign detection to ground truth object if any
        bb=BB(:,d);%记录第d个检测结果的坐标
        ovmax=-inf;%重叠区域设为负无穷
        for j=1:size(gt(gt_index).BB,2)%对所有groundTruth逐一比较
            bbgt=gt(gt_index).BB(:,j);%gt中第一个gt目标
            bi=[max(bb(1),bbgt(1)) ; max(bb(2),bbgt(2)) ; min(bb(3),bbgt(3)) ; min(bb(4),bbgt(4))];%bi为重叠区域的坐标
            iw=bi(3)-bi(1)+1;%重叠区域宽度
            ih=bi(4)-bi(2)+1;%重叠区域高度
            if iw>0 && ih>0                
                % compute overlap as area of intersection / area of union
                ua=(bb(3)-bb(1)+1)*(bb(4)-bb(2)+1)+...
                   (bbgt(3)-bbgt(1)+1)*(bbgt(4)-bbgt(2)+1)-...
                   iw*ih;%并集面积计算
                ov=iw*ih/ua;%交并比计算
                if ov>ovmax%纪录最大的交并比面积
                    ovmax=ov;
                    jmax=j;
                end
            end
        end
        % assign detection as true positive/don't care/false positive
        if ovmax>=VOCopts.minoverlap%如果最大重叠面积大于等于阈值，则认为检测结果正确检测
            if ~gt(gt_index).diff(jmax)
                if ~gt(gt_index).det(jmax)%如果这个gt之前没被检测过，则认为检测结果正确检测
                    tp(d)=1;            % true positive
                    gt(gt_index).det(jmax)=true;%将gt.det设置为true，表明这个gt已经被检测
                else
                    fp(d)=1;            % false positive (multiple detection)
                end
            end
        else%如果最大重叠面积小于阈值，则认为检测结果错误检测
            fp(d)=1;                    % false positive
        end
    end
    tp_all = [tp_all;tp];%记录所有测试数据的真阳性数目
    fp_all = [fp_all;fp];%记录所有测试数据的假阳性数目
    confidence_all = [confidence_all;confidence];%记录所有检测图像的每个结果对应的置信度
end

[~,resort_ind]=sort(-confidence_all);
tp_all_resort = tp_all(resort_ind);
fp_all_resort = fp_all(resort_ind);


% compute precision/recall
fp_all_resort_draw = cumsum(fp_all_resort);%计算false positive总数
tp_all_resort_draw = cumsum(tp_all_resort);%计算true positive总数
rec = tp_all_resort_draw/npos;%计算查全率
prec = tp_all_resort_draw./(fp_all_resort_draw+tp_all_resort_draw);%计算查准率

% compute average precision
save eval_result rec prec;
ap=0;
for t=0:0.001:1
    p=max(prec(rec>=t));%设置不同阈值，画PR曲线
    if isempty(p)
        p=0;
    end
    ap=ap+p/1001;
end
figure
if draw
    % plot precision/recall
    plot(rec,prec,'-b','LineWidth',2);
    grid;
    xlabel 'recall'
    ylabel 'precision'
    title(sprintf('class: %s, AP = %.3f',cls,ap));
    axis([0 1 0 1]);
    grid off;
end
