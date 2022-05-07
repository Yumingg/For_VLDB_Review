function [profit] = get_profit(R,x,m,r)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
total_fake_stake = m + sum(x);
profit = x*r+R';
profit = profit ./ total_fake_stake';
end

