function [profit] = sample_profit(number_player,s,m) 
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

being_infil =  sum(s,1);
infil = sum(s,2);
effective_m = m - infil;
total_fake_m = m' + being_infil;
H_Denominator = repmat(total_fake_m,number_player,1);
H = s ./H_Denominator;
G_Denominator = m'./total_fake_m;
G = diag(G_Denominator);

profit = zeros(number_player,1);
unshared_profit = zeros(number_player,1);
probability = (effective_m)./(1-sum(sum(s)));
probability_upper = cumsum(probability);
probability_lower(2:number_player,1) = cumsum(probability(1:number_player-1,1));
probability_lower(1) = 0;
random = rand;
winning = (probability_lower < random).*(probability_upper > random);
unshared_profit = 1 * winning;
for i = 1:10
    profit = profit + G * unshared_profit;
    unshared_profit = H * unshared_profit;
end

end

