test = [41.0547 42.0878 43.0534 43.3275 43.6844 43.7819 43.8803 43.7782 43.9873 43.8544];
shishi = [41.9350 43.2146 43.4434 43.5510 43.8665 43.8945 43.9578 43.9219 44.1721 44.0449];
x = [10000 20000 30000 40000 50000 60000 70000 80000 90000 100000];

set(gcf,'Position',[200 200 620 340]);
figure(1)
plot(x, test,'-s', 'LineWidth',2.5);
axis([10000 100000 41 44.5]);
hold on;
xlabel(['Number of iterations'],'Fontsize',15,'Interpreter','latex');
% xlabel(['迭代次数'],'Fontsize',15,'Interpreter','latex');
ylabel(['PSNR(dB)'],'Fontsize',15,'Interpreter','latex');
plot(x, shishi,'-^', 'LineWidth',2.5);
grid on;
gca = legend('Using $I_h$','Using $E_h$', 'Location', 'southeast');
% gca = legend('使用 $I_h$','使用 $E_h$', 'Location', 'southeast');
set(gca,'Fontsize',18,'Interpreter','latex');
% set( gca, 'Position', [200, 200, 300, 200]);
print(1,'-dpng','D:\lanhao\专利\蓝浩\quxian.png');