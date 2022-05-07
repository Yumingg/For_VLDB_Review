load('color');
pink = [0.93,0.79,0.79];
purpel = [0.90,0.84,0.94];
gray = [0.79,0.78,0.80];
%%%%%% Plot PoW Simulation

zp = 0.7;
zv = 0.3;
n = 5000;
times = 1000;
ini = 100;
stakea = zp * ini*ones(times,1);
stakeb = zv * ini*ones(times,1);
maximum = zeros(times,1);
minimum = zeros(times,1);
averge = zeros(times,1);
averge_inj = zeros(times,1);
injt = 0;

for i = 1 : n
    proba = stakea ./ (ini+i-1);
    probb = stakeb ./ (ini+i-1);
    
    x = zp;
    y = zv;
    
    xw = x./2;
    yw = 0;
    
    yr = y - yw;
    xr = x - xw;
    
    poolawin = (xr)./(xr+yr);
    poolbwin = 1 - poolawin;
    rnd = rand(times,1);
    logi = rnd < poolawin;
    logd = ~logi;
    stakea = stakea + logi .* xr ./ ( xr + yw)  + logd.* xw ./(xw+yr);
    stakeb = stakeb + logi .* yw ./ (xr + yw) + logd.* yr ./(xw+yr);
    newproa = (stakea)./(ini+i);
    newprob = (stakeb)./(ini+i);
    
    norm_accum = (stakeb - zv * ini*ones(times,1))./(i);
    maximum(i,1) = min(maxk(norm_accum,50));
    minimum(i,1) = max(mink(norm_accum,50));
    averge(i,1) = mean(norm_accum);
    averge_inj(i,1) = mean(injt);
end

x = [1:5000];
maximum = maximum(1:1:n);
minimum = minimum(1:1:n);
averge = averge(1:1:n);
figure
patch([x fliplr(x)],[maximum' fliplr(averge')],'g','LineStyle','none');
patch([x fliplr(x)],[minimum' fliplr(averge')],'g','LineStyle','none');
hold on 
h = plot(x,PoW_ave,'-','linewidth',2,'Color',black);
%%%%%% Plot PoS Simulation



zp = 0.7;
zv = 0.3;
data = syssim37;
n = 5000;
times = 10000;
ini = 100;
stakea = zp * ini*ones(times,1);
stakeb = zv * ini*ones(times,1);
maximum = zeros(times,1);
minimum = zeros(times,1);
averge = zeros(times,1);
averge_inj = zeros(times,1);
injt = 0;

for i = 1 : n
    proba = stakea ./ (ini+i-1);
    probb = stakeb ./ (ini+i-1);
    
    x = proba;
    y = probb;
    
    xw = x./2;
    yw = 0;
    
    yr = y - yw;
    xr = x - xw;
    
    poolawin = (xr)./(xr+yr);
    poolbwin = 1 - poolawin;
    rnd = rand(times,1);
    logi = rnd < poolawin;
    logd = ~logi;
    stakea = stakea + logi .* xr ./ ( xr + yw)  + logd.* xw ./(xw+yr);
    stakeb = stakeb + logi .* yw ./ (xr + yw) + logd.* yr ./(xw+yr);
    newproa = (stakea)./(ini+i);
    newprob = (stakeb)./(ini+i);
    
    norm_accum = (stakeb - zv * ini*ones(times,1))./(i);
    maximum(i,1) = min(maxk(norm_accum,50));
    minimum(i,1) = max(mink(norm_accum,50));
    averge(i,1) = mean(norm_accum);
    averge_inj(i,1) = mean(injt);
end

x = [1:5000];
maximum = maximum(1:1:n);
minimum = minimum(1:1:n);
averge = averge(1:1:n);
hold on
patch([x fliplr(x)],[maximum' fliplr(averge')],[0.01,0.55,1.00],'LineStyle','none');
patch([x fliplr(x)],[minimum' fliplr(averge')],[0.01,0.55,1.00],'LineStyle','none');
hold on 
h = plot(x,PoS_ave,'-','linewidth',2,'Color',orange);



  

%%%%%% Plot System Experiment
% 
% xbox = [500:500:5000];
% ori = xbox + 100*zv;
% data_origin = repmat(ori,95,1);
% real_stake =  data.*data_origin - 100*zv;
% total_accumulated_data = repmat([500:500:5000],95,1);
% uniform_accumulated_data = real_stake./total_accumulated_data;
% data = uniform_accumulated_data;
% 
% neg = max(mink(data,5));
% pos = min(maxk(data,5));
% middle = mean(data);
% 
% errorb= errorbar(xbox(1:9),middle(1,1:9),middle(1:9)-neg(1,1:9),pos(1:9)-middle(1,1:9),'*','LineStyle','none','LineWidth',2,'MarkerSize',17,'CapSize',24 ...
%     ,'Color' , deep_green);
% 
% neg = min(eth_real);
% pos = max(eth_real);
% middle = mean(eth_real);
% 
% errorb= errorbar(xbox(1:9),middle(1,1:9),middle(1:9)-neg(1,1:9),pos(1:9)-middle(1,1:9),'*','LineStyle','none','LineWidth',2,'MarkerSize',17,'CapSize',24 ...
%     ,'Color' , [0.24,0.65,0.98]);
% alpha(0.3)   
% 


%%%%%%% Adjust Plot 
alpha(0.3) 
xlim([10,n]);
ylim([0,0.5]); 
title('One Attacker One Victim','Interpreter','latex');
xlabel('Number of Blocks','Interpreter','latex','FontSize',25);% x???
ylabel({'Norm. Reward'},'Interpreter','latex','FontSize',25);
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(gca, 'Fontname', 'Times New Roman','FontSize',25);
set(gcf,'unit','centimeters','position',[0 20 20 13]);
box on