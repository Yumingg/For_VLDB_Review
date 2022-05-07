function [x,averge] = two_gamer_sim(w,a,times,n)
    ini = 1./w;
    stakea = a * ini*ones(times,1);
    stakeb = (1-a) * ini*ones(times,1);
    maximum = zeros(times,1);
    minimum = zeros(times,1);
    averge = zeros(times,1);
    averge_inj = zeros(times,1);
    injt = 0;

    for i = 1 : n
        proba = stakea ./ (ini+i-1);
        probb = stakeb ./ (ini+i-1);
        x = proba;
        y = probb;
        cond1 = (x <= y./5);
        cond2 = (y <= x./5);
        xw = (sqrt(x.*y) .*(2*sqrt(x)-sqrt(y)))./(sqrt(x)+sqrt(y));
        yw = (sqrt(x.*y) .*(2*sqrt(y)-sqrt(x)))./(sqrt(x)+sqrt(y));
        xw = xw - xw.*cond1 - xw.*cond2;
        yw = yw - yw.*cond1 - yw.*cond2;
        yw = yw + cond1 .* y./2;
        xw = xw + cond2 .* x./2;
        yr = y - yw;
        xr = x - xw;


        poolawin = (xr)./(xr+yr);
        poolbwin = 1 - poolawin;
        rnd = rand(times,1);
        logi = rnd < poolawin;
        logd = ~logi;
        stakea = stakea + logi .* ((x.*(y+xw))./(x.*y+x.*xw+y.*yw)) + logd.* ((x.*xw)./(x.*y+x.*xw+y.*yw));
        stakeb = stakeb + logi .* ((y.*yw)./(x.*y+x.*xw+y.*yw)) + logd.* ((y.*(x+yw))./(x.*y+x.*xw+y.*yw));
        newproa = (stakea)./(ini+i);
        newprob = (stakeb)./(ini+i);
        maximum(i,1) = max(newproa);
        minimum(i,1) = min(newproa);
        averge(i,1) = mean(newproa);
        averge_inj(i,1) = mean(injt);
    end

    x = [10:100000];

    maximum = maximum(1:1:n);
    minimum = minimum(1:1:n);
    averge = averge(1:1:n);
end