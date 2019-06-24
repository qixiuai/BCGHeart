
%%
raw_bcg = csvread("raw_bcg.txt");
%b = csvread("../data/bandpass_b_500.csv");
%a = csvread("../data/bandpass_a_500.csv");
[b,a] = sos2tf(SOS,G);
bcg = filter(b,a,raw_bcg);

plot(raw_bcg)
hold on;
plot(bcg);
dlmwrite("bcg_bandpass_1_15_b.csv", b, 'delimiter', ',', 'precision', 1000);
dlmwrite("bcg_bandpass_1_15_a.csv", a, 'delimiter', ',', 'precision', 1000);