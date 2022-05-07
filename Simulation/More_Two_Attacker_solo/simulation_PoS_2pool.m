player = 2;
z1 = 0.15;
z2 = 0.25;
total_pool = 0.3;
sample = 20;
initial = 100;
times = 10000;
player1 = zeros(sample,times);
player2 = zeros(sample,times);
playersolo = zeros(sample,times);
normalized_accu_reward_other_player = zeros(sample,times);
% for i = 1 : sz
power_temp = 0;
m_ini = [z1;z2].*initial;
s = zeros(player,player);
for smp = 1 : sample
   s = zeros(player,player);
   stake = m_ini;
   for i = 1 : times
    stake_ratio = stake./(initial+i-1);
    [s] = iteration_equilibria(player,stake_ratio',s);
    profit = sample_profit(player,s,stake_ratio);
    stake = stake + profit';
    player1(smp,i) = (stake(1))./(i+initial);
    player2(smp,i) = (stake(2))./(i+initial);
    playersolo(smp,i) = 1 - player1(smp,i) - player2(smp,i);
   end
end
save('15_25_60.mat',player1,player2,playersolo);