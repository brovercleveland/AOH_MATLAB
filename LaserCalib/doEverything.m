function allClear = doEverything(freq,scope,i2c,id,pos)
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('60'), 0, 1, hex2dec('20'));
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('61'), 0, 1, hex2dec('20'));
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('62'), 0, 1, hex2dec('20'));
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('63'), 0, 1, 00);
    leftGArray = [hex2dec('00'),hex2dec('01'),hex2dec('02'),hex2dec('03')]
    middleGArray = [hex2dec('00'),hex2dec('04'),hex2dec('08'),hex2dec('0C')]
    rightGArray = [hex2dec('00'),hex2dec('10'),hex2dec('20'),hex2dec('30')]
    if strcmp(pos,'right') == 1
        gainArray = rightGArray
    elseif strcmp(pos,'middle') == 1
        gainArray = middleGArray
    elseif strcmp(pos,'left') == 1
        gainArray = leftGArray
    end
    
    %for i = 1:4
    %  calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('63'), 0, 1, gainArray(i));
    %  aveAmp  = ampSweep(freq,scope,10,id,pos,i-1)
    %end
    
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('63'), 0, 1, 00);
    bs = biasSweep(freq,scope,i2c,id,pos)
    allClear = 'all done, bro';
end