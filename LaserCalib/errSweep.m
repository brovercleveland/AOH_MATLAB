% amplitude sweep, go through the entire amplitude range, get the averages,
% put them into an array.  Congrats, time to get crunk.

function errArray = errSweep(freq,scope,sweeps,id,pos,gain)
    amp = 0.10 %start with 0.10 V
    inArray = [];
    outArray = [];
    
    lecroySetup(scope, gain);    
    while (amp<2.5)
        fprintf(freq,'OA 4,%s',num2str(amp))
        tmpArray = [];
        inArray = [inArray amp];
        for i=1:sweeps
            aveAmp = getAve(scope, 1);
            %fprintf(scope,sprintf('C1:TRLV %0.4f V',max(minTrig,aveAmp/2.0)));
            tmpArray = [tmpArray aveAmp];
        end
        stndDev = std(tmpArray)
        outArray = [outArray stndDev];
        amp = amp + 0.05;
        if (amp > 0.69) && (amp < 0.71) && (gain == 1 || gain == 0)
            disp('change window')
            lecroySetup(scope, 11);
        end
        if (amp > 1.49) && (amp < 1.51) && (gain == 2)
            disp('change window')
            lecroySetup(scope, 31);
        end
        if (amp > 0.99) && (amp < 1.01) && (gain == 3)
            disp('change window')
            lecroySetup(scope, 31);
        end
            
    end
    errArray = [inArray/2;outArray];
    csvwrite(sprintf('errFiles/err_id%i_%s_gain%i.txt',id,pos,gain),errArray);
    beep
    pause(0.3)
    beep
    pause(0.3)
    beep
    pause(0.3)
    beep
end
    
    