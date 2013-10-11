function lecroySetup(scope, gain)
    if gain == 0
      fprintf(scope,'C1:VDIV 0.02 V');
      fprintf(scope,'C1:OFST -0.0610 V');
      %fprintf(scope,'C1:TRLV 1.2 mV');
    elseif gain == 3
      fprintf(scope,'C1:VDIV 0.05 V');
      fprintf(scope,'C1:OFST -0.1600 V');
      %fprintf(scope,'C1:TRLV 10 mV');
    elseif gain == 2
      fprintf(scope,'C1:VDIV 0.05 V');
      fprintf(scope,'C1:OFST -0.1600 V');
      %fprintf(scope,'C1:TRLV 4 mV');
    elseif gain == 1
      fprintf(scope,'C1:VDIV 0.02 V');
      fprintf(scope,'C1:OFST -0.0560 V');
      %fprintf(scope,'C1:TRLV 4.4 mV');
    elseif gain == 11
      fprintf(scope,'C1:VDIV 0.05 V');
      fprintf(scope,'C1:OFST -0.1300 V');
    elseif gain == 31
      fprintf(scope,'C1:VDIV 0.1 V');
      fprintf(scope,'C1:OFST -0.300 V');
    elseif gain == 999
      fprintf(scope,'C1:VDIV 0.010 V');
      fprintf(scope,'C1:OFST 0 V');
    end
end