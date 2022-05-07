function [R] = getR(x,m)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
total_effective = 1 - sum(sum(x));
R = m - sum(x,2)';
R = R ./ total_effective;
end

