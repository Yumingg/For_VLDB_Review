function [pltsim pltsys] = printoneline(xbox,real,x,ave,w,color,maker)
pltsim = plot(x,ave,'linewidth',3,'Color',color); hold on
hold on

pltsys = plot(xbox,real,maker,...
    'LineWidth',2,...
    'MarkerFaceColor',color,...
    'MarkerSize',15,...
    'MarkerEdgeColor','k');
set(gca, 'Fontname', 'Times New Roman','FontSize',20);

hold on
%legend('Sim. Area','Sim. Average','Fair Area')
%legend boxoff  

xticks([1000 2000 3000 4000 5000])
%xticklabels('$5\times10^2$','$1\times10^3$','$5\times10^3$','$1\times10^4$','$5\times10^4$','$1\times10^5$')
set(groot,'defaultAxesTickLabelInterpreter','latex');  
%ylabel('Unfair Probability','FontSize',20);
lines = findobj(gcf, 'type', 'line', 'Tag', 'Median');
set(lines, 'Color', 'r','linewidth',2)
end

