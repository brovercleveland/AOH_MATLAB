function freqSetup(freq,mode)
    if mode == 'gain'
        fprintf(freq,'TM 0')
    elseif mode == 'bias'
        fprintf(freq,'TM 1')
    else
        disp('freqSetup is being used incorrectly, even though it is an incredibly simple function. How do you fuck something up that is this trivial?  I feel bad, and you should too')
    end
end        