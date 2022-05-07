clear;
clc

%load('equal_player_10_8.mat')
 load('player_10.mat')
% load('equal_player_2.mat')
load('color.mat')
x = [1 100 1000 9000];
data = player_stake;
%data = player_10;
player_num = 11;
stake = zeros(player_num,4);
for i = 1 : 4
    for player = 1 : player_num
        stake(player,i) = mean(data(player,:,x(i)));
    end
    
end
% 5 Players
% colorpal = [grass_green;gray;pink;deep_green;weakblue;yellow;];  % 5
% hatchangel = [90;35;35;45;45;0];
% hatchlinestyle = {'-';':';'-.';'-';'-';'-'};
% hatchstyle= {'cross';'single';'cross';'single';'cross';'single'};
% 
% % 2 Players
% colorpal = [deep_green;weakblue;yellow;];  % 5
% hatchangel = [45;45;0];
% hatchlinestyle = {'-';'-';'-'};
% hatchstyle= {'single';'cross';'single'};
% 10 Players
colorpal = [weakred;weakgreen;orange;weakblue;purpel;grass_green;gray;pink;deep_green;weakblue;yellow;];  % 5
hatchangel = [90;0;0;15;10;55;35;35;45;45;0];
hatchlinestyle = {'-.';':';'-';'--';'-.';'-';':';'-.';'-';'-';'-'};
hatchstyle= {'single';'cross';'single';'single';'cross';'cross';'single';'cross';'single';'cross';'single'};

%%
set(gcf,'unit','centimeters','position',[5 2 30 20]);
xx = [1:1:4];
b = bar(xx,stake','stacked','BarWidth',0.6,'FaceColor','flat','EdgeColor','k','LineWidth',1);
barnum = size(stake,1);
% set texture
% hatchstyle = {'single';'cross';'single';'cross';'single';'cross';...
%             'single';'cross';'single';'cross';'single'};
% hatchlinestyle = {'-';'--';'-.';':';'-';'--';'-.';':';'-';'--';'-.'};
% specklestyle = {'+', 'o', '*', 'x', 'square', 'diamond', 'v', '^', '>', '<', 'pentagram', 'hexagram'};
%  you can use some SpeckleMarkerStyle as follows:
%  SpeckleMarkerStyle: '+', 'o', '*', '.', 'x', 'square', 'diamond', 'v', '^', '>', '<', 'pentagram', 'hexagram'
% hatchangel = [90;0;15;10;35;35;55;55;75;75;0];  

for ii = 1:barnum
    b(ii).FaceColor = colorpal(ii,:);
    %b(ii).FaceColor = cell2mat(colorpal2(1,:));
%    hatchfill2(b(ii),'speckle','SpeckleMarkerStyle',char(specklestyle(ii)),'HatchAngle',hatchangel(ii),'SpeckleDensity',1000,'HatchColor','k','SpeckleWidth',1.5);
    hatchfill2(b(ii),'HatchStyle',char(hatchstyle(ii)),'HatchLineStyle',char(hatchlinestyle(ii)),'HatchAngle',hatchangel(ii),'HatchLineWidth',1.2);
end

ylim([0,1]);
xlim([0,5]);

hold on


hBar = b;% Return ?bar? Handle
Ysum = hBar(1).YData.*0;
for k1 = 1:length(b)
    ctr(k1,:) = bsxfun(@plus, hBar(1).XData, hBar(k1).XOffset');    % Note: ?XOffset? Is An Undocumented Feature, This Selects The ?bar? Centres
    ydt(k1,:) = hBar(k1).YData;
    Ysum = Ysum + ydt(k1,:);
    text(ctr(k1,:)-0.1, Ysum - ydt(k1,:).*0.85, sprintfc('%.2f', ydt(k1,:)), 'HorizontalAlignment','center', 'VerticalAlignment','bottom','Fontname', 'Times New Roman','FontSize',10,'BackgroundColor',b(k1).FaceColor)
end

%%%%%%%%%%%%%%%%%%
% set legend label
% leglabel = {'Player A';'Player B';'Player ...';'Player D';...
%             'Player E';'The Other Players';'Player G';'Player H';'Player I';'Player J';'Private Staker'};
% 
% [~,legend_h,~,~] = legendflex(b,leglabel,'Fontname', 'Times New Roman','FontSize',25,'box','off','anchor',{'ne','ne'});
% 
% legend textures have to be coincident with the bar
% for jj = 1:barnum
%     hatchfill2(legend_h(length(b)+jj),'HatchStyle',char(hatchstyle(jj)),'HatchAngle',hatchangel(jj),'HatchDensity',30);
% end


% set(legend_h,'position',[0.1 0.1 0.2 0.8]);
% legend('Private Staker','Player A','Player B','Fontname', 'Times New Roman','FontSize',25)
% legend boxoff

set(gca,'xticklabel', {'Initial','$10^2$','$10^3$','$10^4$','$10^5$'});
% ylim([0,1]);
xlabel('Number of Blocks','Interpreter','latex','FontSize',25);
ylabel({'Norm. Stake'},'Interpreter','latex','FontSize',25);
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(gca, 'Fontname', 'Times New Roman','FontSize',25);
set(gcf,'unit','centimeters','position',[5 3 20 13]);
