clear; close; %clc;

rng default;
[X,XN] = wnoise('bumps',12,sqrt(6)); %returns values x of the test signal fun evaluated at 2n linearly spaced points from 0 to 1
denoised_signal = wdenoise(XN,4,'Wavelet','sym4','DenoisingMethod','BlockJS');
denoised_signal_db1 = wdenoise(XN,4,'Wavelet','db1','DenoisingMethod','BlockJS');


fig3=figure('Renderer', 'painters', 'Position', [100 100 1000 400], 'color','w');
ax1 = subplot(211)
plot(XN,'r')
hold on;
plot(denoised_signal,'b', 'linewidth',2)
legend('Noisy Data', 'Denoised Signal (sym4)')
hold off;
xlim([0, 4000])
axis tight;
ax2 = subplot(212)
plot(XN,'r')
hold on;
plot(denoised_signal_db1,'g', 'linewidth',2)
legend('Noisy Data', 'Denoised Signal (db1)')
hold off;
xlim([0, 4000])
axis tight;
linkaxes([ax1 ax2],'x')
print(fig3,['noisy_test_signal','.jpg'],'-djpeg')

snrsym = -20*log10(norm(abs(denoised_signal-XN))/norm(XN))
snrdb1 = -20*log10(norm(abs(denoised_signal_db1-XN))/norm(XN))