% Communicates with LeCroy LT354 oscilloscope to gather signal information
% from BSC. Amplitude gathered every 1 seconds, saved and plotted against
% time. 


%Change Directory to one where you want to store the data as a default (in
%case someone turns off the computer before you have a chance to save it
%manually)

%cd 'F:\MATLAB701\work\BSC_Commissioning Histograms\Magnet_Tests';

clear all;

index=1;

%Ask user how many signal he/she wants to record.
grabs=input('Number of signals to record?    ');

%Set up some variables. The Oscilloscope understands 'char' types.
%ch1='1';
ch2='2';
%ch3='3';
trig='1';
%grabs=1000; 

secs=2;

try

    
    % THIS CREATES A GPIB OBJECT. 'NI' IS FOR NATIONAL INSTRUMENTS, 0 AND 5
    % ARE FOR BOARD INDEX AND PRIMARY ADDRESS (SET IN THE DEVICE YOU WANT
    % TO CONTROL).
    
%g = gpib('ni',0,5,'InputBufferSize',10000);
g = visa('ni','GPIB0::5::0::INSTR');

%Open the communication to the device.
fopen(g);
%Change the default Time Out to 3 seconds (Stop the program if no answer after 3 seconds)
g.Timeout=3;


%Set the triggering mode of the oscilloscope.
fprintf(g,'TRIG_MODE NORM');

%The command CHDR OFF instructs the oscilloscope to omit any command 
%headers when responding to a query, simplifying the decoding of the
%response.
fprintf(g,'CHDR OFF');

for i=1:grabs;
    
    %These arrays hold several measurements which are then averaged and
    %plotted. Each time a new loop begins, we zero these arrays ready for
    %new data.
    dataCh1(:,1)=0;
    dataCh2(:,1)=0;
    dataCh3(:,1)=0;
    index = 1;    
    elapsed_time=0;
    
    
    tic; %set stopwatch. toc is used to stop the stopwatch. Tells us when 
    %acquisition finished.
    
while elapsed_time<secs  %take as many measurements as you can in a given amount of time (eg, secs=10)
    elapsed_time=toc;    %Check if we elapsed time is > secs
    
    %The C%s:INR? command asks if the trig ch (Ch 4 in this case) has any
    %new data.
        fprintf(g,sprintf('C%s:INR?',trig));
        
    %The oscilloscope will send a reply. We need to tell matlab to read in 
    %that reply (Scan the communication port known as 'g')
        new = str2num(fscanf(g));
        
%bit 1 of the register = 1 if new data is in the buffer. Hence, the
%register value will be odd. rem(new,2) checks if new is odd or even by looking
%at the remainder of new/2
if (rem(new,2))
        
        %Ask the oscilloscope to send the Amplitude measurement for Ch1.
        %fprintf(g,sprintf('C%s:PAVA? AMPL',ch1));
        %Read in the reply
        %x = fscanf(g);
        
        %The data from the scope is comma separated. We want to find and
        %remove the commas (,).
        %[commas]=find(x==',')
    
 
        %Extract the (string) numbers between the 1st and 2nd comma, convert
        %to a (double) number (str2num), x1000 to get millivolts. Store the
        %result in the dataCh1 array, location (index,1).
        %dataCh1(index,1)=str2num(x(commas(1):commas(2)))*1000;    


        %Same as above.
        fprintf(g,sprintf('C%s:PAVA? AMPL',ch2));
        x = fscanf(g);
        [commas]=find(x==',');
    
        dataCh2(index,1)=str2num(x(commas(1):commas(2)))*1000;    

        
        %fprintf(g,sprintf('C%s:PAVA? AMPL',ch3));
        %x = fscanf(g);
        %[commas]=find(x==',');
    
        %dataCh3(index,1)=str2num(x(commas(1):commas(2)))*1000;    

              
        index=index+1;
       
end %if
    
    %Clk=clock;
    %Time(i,1)=[num2str(Clk(4)) ':' num2str(Clk(5))]
end %while

    %We now have an unknown number of measurements of 3 channel amplitudes
    %(however many there were in 'secs' seconds.
    %Take the mean of each dataCh array and store it in a new matrix called
    %AvgAmp.
    AvgAmp(i,1)=mean(dataCh1(:,1)); %Ch1 data
    AvgAmp(i,2)=mean(dataCh2(:,1)); %Ch2 data
    AvgAmp(i,3)=mean(dataCh3(:,1)); %Ch3 data
    %AvgAmp(:,:)
end %for

%Plot stuff.
%Create a vector, x = 1 2 3 ..... grabs-1, grabs.
x=1:grabs;

%Plot the data for the 3 channels on the same graph.
plot(x,AvgAmp(:,1),x,AvgAmp(:,2),x,AvgAmp(:,3));

%Calculate the best range for the Y axis (Maximum value of AvgAmp + 10%)
maxValue=max(max(AvgAmp))*1.10;

%Set the graph axes (x min, x max, y min, y max)
axis([1 grabs 0 maxValue])
%Close the communication
fclose(g);

%Create a Windows type 'Save As' box. Allows you to graphically chose a
%path & filename where you will save the data.
[file,path] = uiputfile('*.txt','Save file name');

%Change directory to this new path. 
cd (path);
%Save the AvgAmp matrix as a txt file 
save (file,'AvgAmp','-ascii');

%cd 'F:\MATLAB701\work\';


%If something goes wrong, close the communication before crashing out.
catch
    fclose(g);
    
disp('error during acquisition')
end

fclose(g);

