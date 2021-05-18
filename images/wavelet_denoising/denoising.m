clear; close; clc;
wdir='./';

fileloc0=[wdir,'II-PFO-BHZ'];
fileloc_ext = '.mat';
fileloc = [fileloc0 fileloc_ext];

if exist(fileloc,'file')
    disp(['File exists ', fileloc]);
    load(fileloc);
    
    all_stats = fieldnames(stats);
    all_data = fieldnames(data);
    
    for id=1
        %% read data and header information
        stats_0 = stats.(all_stats{id});
        data_0 = data.(all_data{id});
        
        sampling_rate = stats_0.('sampling_rate');
        delta = stats_0.('delta');
        starttime = stats_0.('starttime');
        endtime = stats_0.('endtime');
        t1 = datetime(starttime,'InputFormat',"yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
        t2 = datetime(endtime,'InputFormat',"yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
        datetime_array = t1:seconds(delta):t2;
        
        %% Plot waveforms
        fig = figure('Renderer', 'painters', 'Position', [100 100 1000 400], 'color','w');
        plot(t1:seconds(delta):t2, data_0, 'k-')
        title([stats_0.('network'),'-', stats_0.('station'), '-', stats_0.('channel')])
        axis tight;
        print(fig,[fileloc0, '_ts', num2str(id),'.jpg'],'-djpeg')
        data_double = double(data_0);
        
        %% Using sym4
        [XDEN,DENOISEDCFS] = wdenoise(data_double,9,'Wavelet','sym4','DenoisingMethod','BlockJS');
        close;
        
        fig2=figure('Renderer', 'painters', 'Position', [100 100 1000 400], 'color','w');
        plot(t1:seconds(delta):t2,data_double,'r')
        hold on;
        plot(t1:seconds(delta):t2,XDEN, 'b')
        legend('Original Signal','Denoised Signal')
        axis tight;
        hold off;
        axis tight;
        print(fig2,['denoise_signal_sym49','.jpg'],'-djpeg')
        
        snrsym = -20*log10(norm(abs(data_double-XDEN))/norm(data_double))
        
        %% Using db1
        [XDEN_db1,DENOISEDCFS2] = wdenoise(data_double,5,'Wavelet','db1','DenoisingMethod','BlockJS');
        close;
        
        fig3=figure('Renderer', 'painters', 'Position', [100 100 1000 400], 'color','w');
        plot(t1:seconds(delta):t2,data_double,'r')
        hold on;
        plot(t1:seconds(delta):t2,XDEN_db1, 'b')
        legend('Original Signal','Denoised Signal')
        axis tight;
        hold off;
        axis tight;
        print(fig3,['denoise_signal_db1','.jpg'],'-djpeg')
        
        snrdb1 = -20*log10(norm(abs(data_double-XDEN_db1))/norm(data_double))
        
        %% Plot reconstructions based on the level-4 approximation
        [sigden,coefs] = cmddenoise(data_double,'sym4',4);
        [C,L] = wavedec(data_double,4,'sym4');


        close all;
        fig5= figure('Renderer', 'painters', 'Position', [100 100 1000 400], 'color','w');
        app = wrcoef('a',C,L,'sym4',4); %Coefficients to reconstruct, specified as 'a' or 'd', for approximation or detail coefficients, respectively.
        subplot(5,1,1);
        plot(data_double, 'r-')
        title('Approximation Coefficients');
        hold on;
        plot(app, 'b'); 
        legend('Original Signal','Reconstructed Signal')
        for nn = 1:4
            det = wrcoef('d',C,L,'sym4',nn);
            subplot(5,1,nn+1)
            plot(det); title(['Noisy Wavelet Coefficients - Level '...
                  num2str(nn)]);
        end
        print(fig5,['wavelet_reconstruction','.jpg'],'-djpeg')

    end
end