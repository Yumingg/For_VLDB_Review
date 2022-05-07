
x = [1:100000];
[simx sim10] = two_gamer_sim(0.1,0.3,1000,100000)
[sim10_plot ]=printoneline(x,sim10,0.1,[0.93,0.69,0.13],'^');
hold on 
[simx sim100] = two_gamer_sim(0.01,0.3,1000,100000)
[sim100_plot ]=printoneline(x,sim100,0.1,deep_green,'s');
hold on 
[simx sim1000] = two_gamer_sim(0.001,0.3,1000,100000)
[sim1000_plot ]=printoneline(x,sim1000,0.1,deep_blue,'o');
hold on 
[simx sim10000] = two_gamer_sim(0.0001,0.3,1000,100000)
[sim10000_plot ]=printoneline(x,sim10000,0.1,weakred,'d');
hold on 


set(gca, 'XScale', 'log')
xlim([100,100000]);
ylim([0,1]); 
xticks([10 100 1000 10000 100000])
xlabel('Number of Blocks','FontSize',20);% x???
ylabel({'$$Z_A$$'},'Interpreter','latex','FontSize',20);
hlegend = legend([sim10_plot sim100_plot sim1000_plot sim10000_plot ],'w=0.1','w=0.01','w=0.001','w=0.0001')
hlegend.NumColumns = 2;


legend boxoff
set(gca,'FontSize',22);
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(gca, 'Fontname', 'Times New Roman','FontSize',25);
set(gcf,'unit','centimeters','position',[0 20 20 13]);
