clc
clear
player = 5;
total_pool = 0.3;
sample = 100;
initial = 100;
times = 100000;
normalized_accu_reward = zeros(player+1,sample,times);

power_temp = 0;
%%%%%%%%%%%%%%%% Uniform 
% m_ini = ones(player,1)*30;
% m_ini(1:player,1) = (ones(player,1)).*80./(player);
% m_total_ini(1:player,1) =  m_ini;
% m_total_ini(player+1,1) =  20;
%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%% Arithmetically 
% m_ini(1:player,1) = [27;21;16;11;5];
% m_total_ini(1:player,1) =  m_ini;
% m_total_ini(player+1,1) =  20;
%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%% Arithmetically 
% m_ini(1:player,1) = [41;21;10;5;2.5];
% m_total_ini(1:player,1) =  m_ini;
% m_total_ini(player+1,1) =  20;
%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%% Simulation 
m_ini(1:player,1) = [30,12.5,12.5,12.5,12.5];
m_total_ini(1:player,1) =  m_ini;
m_total_ini(player+1,1) =  20;
%%%%%%%%%%%%%%%%%%

for smp = 1 : sample
   s = zeros(player,player);
   stake = m_ini;
   stake_total = m_total_ini;
   t = 0; 
   for i = 1 : times
    stake_ratio = stake./(initial+i-1);
    [s] = iteration_equilibria(player,stake_ratio',s);
    profit = sample_profit(player,s,stake_ratio);
    stake = stake + profit;
    stake_total(1:player,1)=stake;
    stake_total(player+1,1)=initial+i-sum(stake);
    normalized_accu_reward(:,smp,i) = (stake_total-m_total_ini)./(i);
   end
end
player_stake = normalized_accu_reward;
save('5player_pos_default.mat',player_stake);
