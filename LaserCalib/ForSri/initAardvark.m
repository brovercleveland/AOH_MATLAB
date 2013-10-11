function i2c = initAardvark()
    loadlibrary('aardvark.so','aardvark.h')
    i2c = calllib('aardvark','c_aa_open',0);
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('60'), 0, 1, 20);
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('61'), 0, 1, 20);
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('62'), 0, 1, 20);
    calllib('aardvark','c_aa_i2c_write',i2c,hex2dec('63'), 0, 1, 00);
end