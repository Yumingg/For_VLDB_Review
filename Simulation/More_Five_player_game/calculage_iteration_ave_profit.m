function [ave_profit] = calculage_iteration_ave_profit(number_player,s,m,player,threshold)
%s[i,j]??i?j??s[i,j]
%   Detailed explanation goes here
%
round = 0;
err = 1;
profit = zeros(number_player,1);
sz = player;
new_profit = zeros(number_player,1);
itr = 0;
while (err > threshold)
    itr = itr + 1;
       R = getR(s,m);
       for i = 1 : number_player
           profit_new = get_profit(R,s,m,new_profit);
           player_profit_new = profit_new(i);
           new_profit(i) = player_profit_new;
       end
       err = max(abs(new_profit-profit));
       profit = new_profit;
end
ave_profit = profit(player);
end

