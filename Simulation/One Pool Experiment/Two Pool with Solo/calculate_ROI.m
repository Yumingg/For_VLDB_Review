function [ave_profit] = calculate_ROI(number_player,s,m,player)
z = m;
ss2 = sum(s,2);
sn = z + (-1).* ss2'  ;
ss1 = sum(s,1);
sd = (z + ss1).* (1 - sum(s(:)));
mm = sn./sd;
on1 = eye([number_player,number_player]);
G = s ./(z + ss1)';
r = mm';
profit = inv(on1 - G)*mm'
ave_profit = profit(player);
end