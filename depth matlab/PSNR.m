function PSNR = PSNR(f1, f2)

f1 = double(f1);
f2 = double(f2);

e = f1 - f2;

[m, n] = size(f1);

b = (sum(sum(e.^2)))/(m*n);

PSNR = 10*log10((255.^2)/b);