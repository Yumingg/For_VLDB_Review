function [strategy] = iteration_equilibria(num,m,strategy)
alpha = 0.001;
threshold = 0.00001;
delta = 0.00000001;
err = 1;
round = 0 ;
profit_vec = m;
while (err > threshold)
round = round +1;
new_strategy = strategy;
        for i = 1 : num
            for j = 1 : num 
                if i == j 
                    continue
                end
                temp_strate = new_strategy;
                temp_strate(i,j) = temp_strate(i,j) + delta;
                profit_new = calculage_iteration_ave_profit(num,temp_strate,m,i,threshold);
                profit_old = calculage_iteration_ave_profit(num,new_strategy,m,i,threshold);
                derivitive = ( profit_new - profit_old)./delta;
                new_xy = new_strategy(i,j)+alpha * derivitive;
                new_strategy(i,j) = min(max(0,new_xy),m(i));
                profit_vec(i) = profit_new;
            end
        end
err = max(max(abs(new_strategy - strategy)));
strategy = new_strategy;
round
end
end


