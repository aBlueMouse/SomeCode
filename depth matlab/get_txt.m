clc;  
clear;  
%%生成顺序的txt文件 

filename = '3.txt';
delete(filename);
folder = 'G:\0819\3\';  
wf = fopen(filename, 'w');  
  
filepaths = dir(fullfile(folder,'*.jpg'));  
  
for i = 1 : length(filepaths) 
    fprintf(wf,'%s\n',horzcat(filepaths(i).name, ' ', num2str(3)));    
end       
fclose(wf);  
