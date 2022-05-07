function [profit] = sample_profit(number_player,s,m) 
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
random = rand;
total_active_eff = 1 - sum(sum(s));
player_total_withhold = sum(s,2);
player_total_being_withhold = sum(s,1);
pool_active_eff = m - player_total_withhold;
pool_probability = pool_active_eff ./ total_active_eff;
pool_rand_upper = cumsum(pool_probability')';
pool_rand_lower = [0; pool_rand_upper(1:number_player-1)];
pool_win = (random>pool_rand_lower).*(random<pool_rand_upper);

profit(1) = 0;
profit(2) = 0;
if (pool_win(1) == 1)
    profit(1) = m(1)*(m(2) + s(1,2))/(m(1)*m(2)+m(1)*s(1,2)+m(2)*s(2,1));
    profit(2) = 1 - profit(1);
end
if (pool_win(2) == 1)
    profit(2) = m(2)*(m(1) + s(2,1))/(m(2)*m(1)+m(2)*s(2,1)+m(1)*s(1,2));
    profit(1) = 1 - profit(2);
end
end

