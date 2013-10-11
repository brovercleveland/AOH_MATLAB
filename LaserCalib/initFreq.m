% frequency sweep program, brah, use to initialize the frequency generator.
% (Standford Model DG535)
% This assumes GPIB1, but I might change it later to a varible.  Output is
% for AB inverted.
% Call like freqObject = initFreq()

function freq = initFreq(amp)
    if nargin == 1
      initAmp = amp
    else
     initAmp = 0.10
    end
    freq = visa('ni','GPIB1::15::0::INSTR');
    fopen(freq)
    fprintf(freq,'CL')
    fprintf(freq,'TM 0')
    fprintf(freq,'TZ 4,0')
    fprintf(freq,'TZ 7,0')
    fprintf(freq,'DT 3,2,10E-9')
    fprintf(freq,'DT 6,5,10E-9')
    fprintf(freq,'OM 4,3')
    fprintf(freq,'OM 7,0')
    fprintf(freq,'OA 4,%s',num2str(initAmp))
    fprintf(freq,'OO 4,1.2')
    fprintf(freq,'DL 2,4,2')

end