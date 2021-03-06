player = 2;
z1 = 0.3;
z2 = 0.5;
sample = 100;
initial = 100;
times = 100000;
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
   stake_ratio = m_ini./(initial); %pOW
   [s] = iteration_equilibria(2,stake_ratio',s);
   for i = 1 : times
    profit = sample_profit(player,s,stake_ratio);
    stake = stake + profit';
    player1(smp,i) = (stake(1)-m_ini(1))./(i);
    player2(smp,i) = (stake(2)-m_ini(2))./(i);
    playersolo(smp,i) = 1 - player1(smp,i) - player2(smp,i);
   end
end
save('30_50_20_log_pow.mat',player1,player2,playersolo);