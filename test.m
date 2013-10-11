x = [];
y = [];
for j=1:360
    x(j) = sind(j);
    y(j) = cosh(j*2*pi/360);
end
z = x+y*1i
plot(z)
