clc;
clear all;

VOCopts.imgsetpath = ...%������������txt�ļ�·����txt�ļ��������в�����Ե�ͼƬ����,��·���ͺ�׺��
    'E:\ң��\����\Ŀ�������\SSD-fine-tuning\���Լ�¼\SSD\20171206\detect_result\test.txt';
%     'E:\ң��\����\Ŀ�������\SSD-fine-tuning\���Լ�¼\20170915\SSD_PLANE_300x300_score\detect_result\20170915\test.txt';
    
% VOCopts.testset = 'test';%ѡ�ò��Ի�����֤�����ڲ���
VOCopts.annopath='E:\ң��\����\Ŀ�������\���ݼ�\�ɻ����ݼ�\����ΰ\plane_8darg\Annotations\';%��ע�ļ���·��
% VOCopts.annopath='E:\ң��\����\Ŀ�������\���ݼ�\�ɻ����ݼ�\СĿ��\Annotations\';%��ע�ļ���·��
% VOCopts.annopath=[VOCopts.datadir 'Annotations\'];%d.xml'];
VOCopts.detrespath=...%���������·��
    'E:\ң��\����\Ŀ�������\SSD-fine-tuning\���Լ�¼\SSD\20171206\detect_result\vision_result.txt';
%     'E:\ң��\����\Ŀ�������\SSD-fine-tuning\���Լ�¼\20170915\SSD_PLANE_300x300_score\detect_result\20170915\vision_result.txt';
      
VOCopts.minoverlap=0.8;%IOU����ֵ�����ڴ���ֵ��Ϊ�Ǽ����ȷ
cls = 'Airplane';%����Ŀ�����
draw = true;%�Ƿ񻭳�PR����


% load test set
% [gtids_temp,~]=textread(VOCopts.imgsetpath,'%s%s');%gtidsΪ���Լ���ͼ��ı������
[gtids,~]=textread(VOCopts.imgsetpath,'%s%s');%gtidsΪ���Լ���ͼ��ı������
% for i=1:length(gtids_temp)
%     gtids{i} = gtids_temp(i);
% end
% load ground truth objects
tic;
npos=0;
gt(length(gtids))=struct('BB',[],'diff',[],'det',[]);
for i=1:length(gtids)%iΪ���Լ��еڼ���ͼ��
%     gtids{i}
    % display progress�����ʱ��
    if toc>1
        fprintf('%s: pr: load: %d/%d\n',cls,i,length(gtids));
        drawnow;
        tic;
    end
%     a = [VOCopts.annopath num2str(gtids{i}) '.xml']
    % read annotation
    rec=PASreadrecord([VOCopts.annopath gtids{i} '.xml']);
    
    % extract objects of class
    clsinds=strmatch(cls,{rec.objects(:).class},'exact');%�Ƚ�groundTruth�����������Ƿ�һ�£���ͬ��objects(:).class������¼��clsinds
    gt(i).BB=cat(1,rec.objects(clsinds).bbox)';%��ȡclsinds��Ӧ��gtĿ������꣬��¼��BB
    gt(i).diff=[rec.objects(clsinds).difficult];
    gt(i).det=false(length(clsinds),1);%����clsinds��1�е��߼��Ǿ���ȫΪ0������¼��det�������ж�ĳһ��gt�Ƿ񱻼�⵽
    npos=npos+sum(~gt(i).diff);%��¼�������Լ��з����ѵ�Ŀ��������������Ŀ�ꣿ��
end
% % % % % % % % % % % % % % % % % % % % % % 

% load results
fid = fopen(VOCopts.detrespath,'r');
info = textscan(fid, '%s %s %f %f %f %f %f');
fclose(fid);
det_ids = info{1};
det_num = unique(det_ids);%det_num��ʾ���м������һ��������Щͼ��
tp_all = [];%��¼���м��ͼ���true positive
fp_all = [];%��¼���м��ͼ���false positive
confidence_all = [];%��¼���м��ͼ���ÿ�������Ӧ�����Ŷ�
for jpg_id=1:length(det_num)%һ��һ�������ͼ�������д���
    index = [];
    for k=1:length(det_ids)%��ѡ�����м������ĳһ��ͼ��Ľ��
        if(det_ids{k}==det_num{jpg_id})
            index = [index k];
        end
    end
    class_id = info{2}(index);%��¼��һͼ���Ӧ��������Ŷȡ�����ȵ�
    confidence = info{3}(index);
    b1 = info{4}(index);
    b2 = info{5}(index);
    b3 = info{6}(index);
    b4 = info{7}(index);

    % [ids, ~, confidence,b1,b2,b3,b4]=textread(VOCopts.detrespath,'%s %d %d %d %d %d','delimiter', ' ');%��ȡ������ĵ�id��ͼ��ĵ�cls����
    BB=[b1 b2 b3 b4]';%ĳһ��ͼ������м������¼��BB�����У�ÿһ��Ϊһ��Ŀ����

    % sort detections by decreasing confidence
    [sc,si]=sort(-confidence);%�����н�������ŶȽ�������
%         ids=ids(si);%idsΪ��ǰ��id��ͼ������е�ͼ�����֣�һ����si��ֻ��Ӧ1��
    BB=BB(:,si);
    
    num_loc = regexp(det_num{jpg_id},'/','start');%ids��¼��ǰ�����ͼ��ı��
    ids = det_num{jpg_id}(num_loc(end)+1:end-4);
    
        % assign detections to ground truth objects
    nd=length(confidence);
    tp=zeros(nd,1);%��¼������м�⵽Ŀ��Ľ��true positive
    fp=zeros(nd,1);%��¼�������δ��⵽Ŀ��Ľ��false positive
    tic;
    for d=1:nd%d����ĳһ�������
        % display progress
        if toc>1
            fprintf('%s: pr: compute: %d/%d\n',cls,d,nd);
            drawnow;
            tic;
        end

        % find ground truth image
        gt_index = [];
        for i=1:length(gtids)   %��ȡgtids���뵱ǰ���ͼ��ids{d}��Ӧ��gt�������������ͼ��һ��Ŀ��Ҳû�м�⵽����ᱨ��
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
        bb=BB(:,d);%��¼��d�������������
        ovmax=-inf;%�ص�������Ϊ������
        for j=1:size(gt(gt_index).BB,2)%������groundTruth��һ�Ƚ�
            bbgt=gt(gt_index).BB(:,j);%gt�е�һ��gtĿ��
            bi=[max(bb(1),bbgt(1)) ; max(bb(2),bbgt(2)) ; min(bb(3),bbgt(3)) ; min(bb(4),bbgt(4))];%biΪ�ص����������
            iw=bi(3)-bi(1)+1;%�ص�������
            ih=bi(4)-bi(2)+1;%�ص�����߶�
            if iw>0 && ih>0                
                % compute overlap as area of intersection / area of union
                ua=(bb(3)-bb(1)+1)*(bb(4)-bb(2)+1)+...
                   (bbgt(3)-bbgt(1)+1)*(bbgt(4)-bbgt(2)+1)-...
                   iw*ih;%�����������
                ov=iw*ih/ua;%�����ȼ���
                if ov>ovmax%��¼���Ľ��������
                    ovmax=ov;
                    jmax=j;
                end
            end
        end
        % assign detection as true positive/don't care/false positive
        if ovmax>=VOCopts.minoverlap%�������ص�������ڵ�����ֵ������Ϊ�������ȷ���
            if ~gt(gt_index).diff(jmax)
                if ~gt(gt_index).det(jmax)%������gt֮ǰû������������Ϊ�������ȷ���
                    tp(d)=1;            % true positive
                    gt(gt_index).det(jmax)=true;%��gt.det����Ϊtrue���������gt�Ѿ������
                else
                    fp(d)=1;            % false positive (multiple detection)
                end
            end
        else%�������ص����С����ֵ������Ϊ�����������
            fp(d)=1;                    % false positive
        end
    end
    tp_all = [tp_all;tp];%��¼���в������ݵ���������Ŀ
    fp_all = [fp_all;fp];%��¼���в������ݵļ�������Ŀ
    confidence_all = [confidence_all;confidence];%��¼���м��ͼ���ÿ�������Ӧ�����Ŷ�
end

[~,resort_ind]=sort(-confidence_all);
tp_all_resort = tp_all(resort_ind);
fp_all_resort = fp_all(resort_ind);


% compute precision/recall
fp_all_resort_draw = cumsum(fp_all_resort);%����false positive����
tp_all_resort_draw = cumsum(tp_all_resort);%����true positive����
rec = tp_all_resort_draw/npos;%�����ȫ��
prec = tp_all_resort_draw./(fp_all_resort_draw+tp_all_resort_draw);%�����׼��

% compute average precision
save eval_result rec prec;
ap=0;
for t=0:0.001:1
    p=max(prec(rec>=t));%���ò�ͬ��ֵ����PR����
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
