x = [1:100000];
[simx sim19] = two_gamer_sim(0.01,0.1,1000,100000)
[sim19_plot]=printoneline(x,sim19,0.1,weakblue,'<');
hold on 
[simx sim37] = two_gamer_sim(0.01,0.3,1000,100000)
[sim37_plot]=printoneline(x,sim37,0.1,[0.93,0.69,0.13],'^');
hold on 
[simx sim55] = two_gamer_sim(0.01,0.5,1000,100000)
[sim55_plot]=printoneline(x,sim55,0.1,deep_green,'s');
hold on 
[simx sim73] = two_gamer_sim(0.01,0.7,1000,100000)
[sim73_plot]=printoneline(x,sim73,0.1,deep_blue,'o');
hold on 
[simx sim91] = two_gamer_sim(0.01,0.9,1000,100000)
[sim91_plot]=printoneline(x,sim91,0.1,weakred,'d');
hold on 

set(gca, 'XScale', 'log')
xlim([100,100000]);
ylim([0,1]); 
xticks([10 100 1000 10000 100000])
xlabel('Number of Blocks','Interpreter','latex','FontSize',25);% x???
ylabel({'$$Z_A$$'},'Interpreter','latex','FontSize',25);
hlegend = legend([sim19_plot sim37_plot sim55_plot sim73_plot sim91_plot],'a=0.1','a=0.3','a=0.5','a=0.7','a=0.9')
hlegend.NumColumns = 2;


legend boxoff
set(gca,'FontSize',22);
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(gca, 'Fontname', 'Times New Roman','FontSize',25);
set(gcf,'unit','centimeters','position',[0 20 20 13]);

