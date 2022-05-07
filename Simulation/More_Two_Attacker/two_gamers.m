function [x,averge] = two_gamers(w,a,times,n)
    zp = 1-a;
    zv = a;
    ini = 1./w;
    stakea = zp * ini*ones(times,1);
    stakeb = zv * ini*ones(times,1);
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

        xw = x./2;
        yw = 0;

        yr = y - yw;
        xr = x - xw;

        poolawin = (xr)./(xr+yr);
        poolbwin = 1 - poolawin;
        rnd = rand(times,1);
        logi = rnd < poolawin;
        logd = ~logi;
        stakea = stakea + logi .* xr ./ ( xr + yw)  + logd.* xw ./(xw+yr);
        stakeb = stakeb + logi .* yw ./ (xr + yw) + logd.* yr ./(xw+yr);
        newproa = (stakea)./(ini+i);
        newprob = (stakeb)./(ini+i);
        maximum(i,1) = max(newprob);
        minimum(i,1) = min(newprob);
        averge(i,1) = mean(newprob);
        averge_inj(i,1) = mean(injt);
    end

    x = [1:n];
    maximum = maximum(1:1:n);
    minimum = minimum(1:1:n);
    averge = averge(1:1:n);
end