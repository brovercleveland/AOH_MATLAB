function biasArray = biasSweep(freq,scope,i2c,id,pos)
    vdivs = [0.010,0.020,0.050,0.100,0.200,0.50];
    vindex = 1
    inArray = [];
    outArray = [];
    freqSetup(freq,'bias')
    lecroySetup(scope,999)
    if strcmp('middle',pos)==1
        addr = '61'
    elseif strcmp('left',pos)==1
        addr = '60'
    elseif strcmp('right',pos)==1
        addr = '62'
    end
    
    for i=0:127
        i
        calllib('aardvark','c_aa_i2c_write',i2c,hex2dec(addr), 0, 1, i);
        ampl = getAve(scope,10,'bias')
        inArray = [inArray i];
        outArray = [outArray ampl];
        if ampl > vdivs(vindex)*2.5
            vindex= vindex +1;
            fprintf(scope,sprintf('C1:VDIV %0.3f V',vdivs(vindex)));
        end 
    end
    biasArray = [inArray;outArray];
    csvwrite(sprintf('biasFiles/id%s_%s_bias.txt',id,pos),biasArray);
        
        
end    