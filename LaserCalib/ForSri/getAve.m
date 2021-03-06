% use the init function, the call like this: getAve(scopeObject)

function aveAmp = getAve(scopeArg, sweepsArg, gbToggle, channelArg, traceArg)
    if nargin == 1
        scope = scopeArg;
        sweeps = 500;
        toggle = 'gain';
        channel = '1';
        trace = 'C';
    elseif nargin == 2
        scope = scopeArg;
        sweeps = sweepsArg;
        toggle = 'gain';
        channel = '1';
        trace = 'C';
    elseif nargin == 3
        scope = scopeArg;
        sweeps = sweepsArg;
        toggle = gbToggle;
        channel = '1';
        trace = 'C';
    elseif nargin == 4
        scope = scopeArg;
        sweeps = sweepsArg;
        toggle = gbToggle;
        channel = channelArg;
        trace = 'C';
    elseif nargin == 5
       scope = scopeArg;
       sweeps = sweepsArg;
       toggle = gbToggle;
       channel = channelArg;
       trace = traceArg;
    elseif nargin > 5
        error('too many args')
    else
        error('you need to input a scope object')
    end
    
    fprintf(scope,'CLSW');
    fprintf(scope,sprintf('TC:DEF EQN,"ERES(C1)",MAXPTS,5000,SWEEPS,%s,BITS,1.0',num2str(sweeps)));
    sweepCount = 0;
    while (sweepCount < sweeps)
        fprintf(scope,'PAST? VPAR, SWEEPS');
        sweepstring = fscanf(scope);
        [commas]=find(sweepstring==',');
        sweepCount = str2num(sweepstring(commas(2):commas(3)));
    end
    sweepCount;
    if strcmp(toggle,'gain') == 1
        fprintf(scope,sprintf('T%s:PAVA? AMPL',trace));
    elseif strcmp(toggle,'bias') == 1
        fprintf(scope,sprintf('T%s:PAVA? MEAN',trace));
    end
    ampl = fscanf(scope);
    [commas]=find(ampl==',');
    aveAmp = str2num(ampl(commas(1):commas(2)));
        
    
    %fprintf(scope,sprintf('T%s:PAVA? AMPL',trace))
    
end

    
    