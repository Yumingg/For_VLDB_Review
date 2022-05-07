function [strategy] = iteration_equilibria(num,m,strategy)
derivitive = zeros(num,num);
new_strategy = zeros(num,num);
s0 = strategy; 
alpha = 0.0003;
threshold = 0.000001;
delta = 0.0000001;
err = 1;
round = 0 ;
strategy = [0.005,0.003;0.001,0.002];
while (err > threshold)
round = round +1;
        for i = 1 : num
            for j = 1 : num 
                if i == j 
                    continue
                end
                temp_strate = strategy;
                temp_strate(i,j) = temp_strate(i,j) + delta;
                profit_new = calculage_iteration_ave_profit(num,temp_strate,m,i,threshold);
                profit_old = calculage_iteration_ave_profit(num,strategy,m,i,threshold);
                derivitive = ( profit_new - profit_old)./delta;
                new_xy = strategy(i,j)+alpha * derivitive;
                new_strategy(i,j) = min(max(0,new_xy),m(i));
            end
        end
err = max(max(abs(new_strategy - strategy)));
strategy = new_strategy;
end
s1 = strategy;
 
%%%
% strategy = [0.005,0.003;0.001,0.002];
% round = 0
% err = 1;
% while (err > threshold)
% round = round +1;
%         for i = 1 : num
%             for j = 1 : num 
%                 if i == j 
%                     continue
%                 end
%                 temp_strate = strategy;
%                 temp_strate(i,j) = temp_strate(i,j) + delta;
%                 profit_new = calculate_ROI(num,temp_strate,m,i);
%                 profit_old = calculate_ROI(num,strategy,m,i);
%                 derivitive = ( profit_new - profit_old)./delta;
%                 new_xy = strategy(i,j)+alpha * derivitive;
%                 new_strategy(i,j) = min(max(0,new_xy),m(i));
%             end
%         end
% err = max(max(abs(new_strategy - strategy)));
% strategy = new_strategy;
% end

end



