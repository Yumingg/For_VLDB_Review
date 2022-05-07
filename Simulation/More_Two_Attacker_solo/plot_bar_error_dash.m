clear
clc
%% Import simulation data
load('color.mat')
load('40_40_20.mat')
player1 = player1(:,[1 100 1000 10000]);
player2 = player2(:,[1 100 1000 10000]);
players = playersolo(:,[1 100 1000 10000]);


%% Plot simulation result
y = [mean(players);mean(player1);mean(player2)]';
b = bar(y,'BarWidth',1,'FaceColor','flat','EdgeColor','k','LineWidth',1);
b(1).FaceColor = yellow;
b(2).FaceColor = weakblue;
b(3).FaceColor = deep_green;
ylim([0,1]);



hold on

[ngroups,nbars] = size([mean(players);mean(player1);mean(player2)]');
groupwidth = min(1, nbars/(nbars + 1.5));


% Adding numbers on top of bars 
% use a meaningful variable for a handle array...
hAx=gca;            % get a variable for the current axes handle
 % label the ticks
hT=[];              % placeholder for text object handles
for i=1:length(b)  % iterate over number of bar objects
  hT=[hT text(b(i).XData+b(i).XOffset,b(i).YData,[num2str((b(i).YData).','%.2f')], ...
                          'VerticalAlignment','bottom','horizontalalign','center','Fontname', 'Times New Roman','FontSize',14)];
end

[~,legend_h,~,~] = legendflex(b,{'Private Staker','Player A','Player B'},'anchor', [1 1], 'buffer', [10 -5],'Fontname', 'Times New Roman','FontSize',25,'box','off');

hatchfill2(b(1),'single','HatchAngle',0);
hatchfill2(b(2),'cross','HatchAngle',45);
hatchfill2(b(3),'single','HatchAngle',45);
% Legend = legend(b,{'Private Staker','Player A','Player B'},'Fontname', 'Times New Roman','FontSize',25);
% Legend = {'Private Staker','Player A','Player B'};

hatchfill2(legend_h(length(b)+1),'single','HatchAngle',0,'HatchDensity',15);
hatchfill2(legend_h(length(b)+2),'cross','HatchAngle',45,'HatchDensity',15);
hatchfill2(legend_h(length(b)+3),'single','HatchAngle',45,'HatchDensity',15);

% legend boxoff

set(gca,'xticklabel', {'Initial','$10^2$','$10^3$','$10^4$'});
% ylim([0,1]);
xlabel('Number of Blocks','Interpreter','latex','FontSize',25);
ylabel({'Norm. Stake'},'Interpreter','latex','FontSize',25);
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(gca, 'Fontname', 'Times New Roman','FontSize',25);
set(gcf,'unit','centimeters','position',[5 3 20 13]);
