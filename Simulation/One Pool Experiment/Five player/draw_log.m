clear
load('color2');


pink = [0.93,0.79,0.79];
purpel = [0.90,0.84,0.94];
gray = [0.87,0.87,0.8777];
n = 100000;

%%%%%% Plot PoW Simulation
x = [1:100000];
load('5player_pow');
player1 = squeeze(normalized_accu_reward(1,:,:));
maximum = min(maxk(player1,5,1));
minimum = max(mink(player1,5,1));
average = mean(player1);
figure
patch([x fliplr(x)],[maximum fliplr(average)],[0.62,0.53,0.04],'LineStyle','none');
patch([x fliplr(x)],[minimum fliplr(average)],[0.62,0.53,0.04],'LineStyle','none');
hold on 
h = plot(x,average,'-','linewidth',2,'Color',orange);


PoW_max = maximum;
PoW_min = minimum;
PoW_ave = averge;

%%%%%%% Plot PoS Simulation

x = [1:100000];
load('5player_pos');
player1 = squeeze(normalized_accu_reward(1,:,:));
maximum = min(maxk(player1,5,1))';
minimum = max(mink(player1,5,1))';
average = mean(player1);

patch([x fliplr(x)],[maximum' fliplr(average)],[0.01,0.55,1.00],'LineStyle','none');
patch([x fliplr(x)],[minimum' fliplr(average)],[0.01,0.55,1.00],'LineStyle','none');
hold on 
h = plot(x,average,'-','linewidth',2,'Color',[0.00,0.45,0.74]);



% patch([px fliplr(px)],[purpo_uper' fliplr(purpo_lower')],gray,'LineStyle','none');
% patch([x fliplr(x)],[minimum' fliplr(averge')],anotherblue,'LineStyle','none');

%%%%%%% Plot pos System Experiment
% xbox = [100,200,500,1000,2000,5000];
% load('data/nxt_2gamesolo1');
% neg = max(mink(player1_real,5));
% pos = min(maxk(player1_real,5));
% middle = mean(player1_real);
% errorb= errorbar(xbox(1:6),middle(1,1:6),middle(1:6)-neg(1,1:6),pos(1:6)-middle(1,1:6),'*','LineStyle','none','LineWidth',2,'MarkerSize',17,'CapSize',24 ...,'Color' , deep_green);

%%%%%%% Plot pow System Experiment
% xbox = [100,200,500,1000,2000,5000];
% load('data/eth_3');
% neg = min(player1_real_pow);
% pos = max(player1_real_pow);
% middle = mean(player1_real_pow);
% 
% errorb= errorbar(xbox(1:6),middle(1,1:6),middle(1:6)-neg(1,1:6),pos(1:6)-middle(1,1:6),'*','LineStyle','none','LineWidth',2,'MarkerSize',17,'CapSize',24 ...
%     ,'Color' , [0.65,0.26,0.09]);


%%%%%%% Adjust Plot 
alpha(0.3)   
xlim([100,n]);
ylim([0,0.5]); 
title('Game with Five Players','Interpreter','latex');
xlabel('Number of Blocks','Interpreter','latex','FontSize',25);% x???
ylabel({'Norm. Reward'},'Interpreter','latex','FontSize',25);
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(gca, 'Fontname', 'Times New Roman','FontSize',25);
set(gcf,'unit','centimeters','position',[0 20 20 13]);
set(gca, 'XScale', 'log')
box on