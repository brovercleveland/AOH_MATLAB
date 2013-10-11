% simple function to initialize the LeCroy Waverunner LT354M and set the C1
% to trigger, C2 to laser input, and TC to a trace of C2.  Currently
% channels are hardcoded, but we can change that later if we want.  This
% code should set everything up perfectly even if someone messed with the
% scope when you were getting coffee.

%Call like this: scopeObject = initLecroy()
%Remember to do fclose(scopeObject) when you're finished

function scope = initLecroy(gain)
    if nargin == 1
        gainSet = gain;
    else
        gainSet = 3;
    end
    scope = visa('ni','GPIB0::5::0::INSTR');
    fopen(scope)
    fprintf(scope, '*RST');
    fprintf(scope,'CHDR OFF');
    fprintf(scope,'TC:TRA ON');
    fprintf(scope,'C1:TRA ON');
    fprintf(scope,'C2:TRA OFF');
    fprintf(scope,'C4:TRA ON');
    fprintf(scope,'TRIG_MODE AUTO');
    fprintf(scope,'TRSE EDGE,SR,C4');
    fprintf(scope,'C4:TRIG_COUPLING DC');
    fprintf(scope,'C4:TRSL NEG');
    fprintf(scope,'C1:CPL D50');
    fprintf(scope,'C4:CPL D50');
    fprintf(scope,'C4:VDIV 2.0 V');
    fprintf(scope,'C4:OFST 0.0 V');
    fprintf(scope,'C4:TRLV 2.0 V');
    lecroySetup(scope, gainSet)
    fprintf(scope,'TC:VPOS 0.0');
    fprintf(scope,'TDIV 10 NS');
    fprintf(scope,'TRDL 40');

end

