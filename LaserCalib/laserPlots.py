#!/usr/bin/env python
import sys
import os
sys.argv.append('-b')
from ROOT import *
import numpy as np

# Made by Brian Pollack, 2013
# comments, mainly for Alan
# this line, sys.argv.append('-b'), is for running pyroot in batch mode (much faster, no X11 bullshit)



# load up my tdrStyle script to pretty the plots
gROOT.ProcessLine('.L ./tdrstyle.C')
setTDRStyle()

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

  def disable(self):
    self.HEADER = ''
    self.OKBLUE = ''
    self.OKGREEN = ''
    self.WARNING = ''
    self.FAIL = ''
    self.ENDC = ''

# laser class, holds all the fit info for that laser
class Laser():
  def __init__(self):
    self.scale = [-999,-999,-999,-999]
    self.denom = [-999,-999,-999,-999]
    self.exp = [-999,-999,-999,-999]
    self.const = [-999,-999,-999,-999]
    self.MSE = [-999,-999,-999,-999]
    self.INL = [-999,-999,-999,-999]
    self.DNL = [-999,-999,-999,-999]
    self.isGood = [False, False, False, False]
    self.isGoodLaser = False
    self.fits = [None, None, None, None]
  def findGoodLaser(self):
    if len(self.isGood) == sum(self.isGood):
      self.isGoodLaser = True
  def showGoodLaser(self):
    if self.isGoodLaser:
      print '  Good Laser'
    else:
      print '  Bad Laser'
      for i,val in enumerate(self.isGood):
        if not val: print '   Bad G'+str(i), 'MSE:',self.MSE[i]


# chip class, made up of 3 laser classes
class AOH():
  def __init__(self,name):
    self.GetID = name
    self.left = Laser()
    self.right = Laser()
    self.middle = Laser()
    self.allGood = False
  def findGoodChip(self):
    if self.left.isGoodLaser and self.right.isGoodLaser and self.middle.isGoodLaser:
      self.allGood = True
  def showGoodChip(self):
    if self.allGood:
      print self.GetID, bcolors.OKGREEN+'Good Chip'+bcolors.ENDC
    else:
      print self.GetID, bcolors.FAIL+'Bad Chip'+bcolors.ENDC
      if not self.left.isGoodLaser: print ' left:'; self.left.showGoodLaser()
      if not self.right.isGoodLaser: print ' right:'; self.right.showGoodLaser()
      if not self.middle.isGoodLaser: print ' middle:'; self.middle.showGoodLaser()

def randColor():
  import random as r
  colorList = [kPink,kViolet,kAzure,kTeal,kSpring,kOrange]
  return r.choice(colorList)+r.randint(-9,10)


# this is the main program
def makeLaserPlots():
  fileDict = {}
  graphDict = {}
  graphLinDict = {}
  yDict = {}
  AOHDict = {}
  ColorDict = {}
  #killList = ['.DS_Store', 'id5719']
  killList = ['.DS_Store']

# getting a list of files and removing any potential trash files
  fileList = os.listdir('calibFiles')
  radList = filter(lambda fileName: 'Z' in fileName,fileList)
  for killName in killList:
    fileList = filter(lambda fileName: killName not in fileName,fileList)

# initializing all the canvases we'll be using
  canvasTest = TCanvas('canvasTest','canvas',800,600)
  canvasTest.SetGrid()
  canvasTest.SetTopMargin(0.15)
  canvasG0 = TCanvas('canvasG0','canvas',800,600)
  canvasG0.SetGrid()
  canvasG0.SetTopMargin(0.15)
  canvasG1 = TCanvas('canvasG1','canvas',800,600)
  canvasG1.SetGrid()
  canvasG1.SetTopMargin(0.15)
  canvasG2 = TCanvas('canvasG2','canvas',800,600)
  canvasG2.SetGrid()
  canvasG2.SetTopMargin(0.15)
  canvasG3 = TCanvas('canvasG3','canvas',800,600)
  canvasG3.SetGrid()
  canvasG3.SetTopMargin(0.15)
  canvasRadComp = TCanvas('canvasRadComp','canvas',800,600)
  canvasRadComp.SetGrid()
  canvasRadComp.SetTopMargin(0.15)
  inputVoltArray = np.array(0)
  inputMipsArray = np.array(0)
  totalValG0 = [0]*49
  totalValG1 = [0]*49
  totalValG2 = [0]*49
  totalValG3 = [0]*49
  xErrs = np.array(0)
  #yErrs = np.array(0)
  yErrsG0 = np.array([0.0015234,0.0012198,0.0014253,0.0015814,0.0013965,0.0015825,0.0017171,0.0016138,0.0015875,0.0016141,0.001937,0.0025451,0.0017374,0.0019534,0.0021013,0.0019247,0.0018322,0.0016881,0.00154,0.0016557,0.0014584,0.0017732,0.0016657,0.0018691,0.0019423,0.00207,0.0018613,0.0019093,0.0017944,0.0028717,0.0019837,0.0017433,0.0023114,0.0030702,0.0020948,0.0056139,0.0025578,0.0023453,0.0024287,0.0035781,0.0033225,0.0068507,0.0055389,0.0040865,0.0031069,0.00462,0.007967,0.0041798,0.0079184])
  yErrsG1 = np.array([0.0067551,0.001329,0.001655,0.0018079,0.0016378,0.0019095,0.0020174,0.0026211,0.0030312,0.002992,0.0037941,0.004227,0.0019691,0.0019546,0.0019715,0.0022712,0.0020802,0.0019721,0.0019921,0.0041809,0.0027167,0.0043538,0.0046688,0.0041582,0.007539,0.007972,0.0075716,0.0023595,0.0030601,0.0055791,0.0033382,0.0067638,0.0038902,0.012231,0.0071276,0.0053126,0.012127,0.0079908,0.0069243,0.013584,0.014678,0.0098783,0.013326,0.015207,0.011359,0.0044449,0.012702,0.014919,0.016607])
  yErrsG2 = np.array([0.028544,0.0014604,0.001637,0.0015784,0.0017666,0.0021249,0.0020942,0.0017479,0.0019804,0.0021319,0.0020897,0.0020528,0.0019583,0.0024137,0.0036974,0.0081866,0.0071192,0.0050039,0.0080945,0.0096813,0.0098297,0.0035122,0.0093695,0.011477,0.0083179,0.015272,0.0050756,0.0056642,0.0027397,0.0037137,0.0027631,0.0028689,0.0029646,0.0031505,0.0038087,0.0046202,0.0030367,0.0031369,0.0034462,0.010943,0.0062866,0.004748,0.0046259,0.0056675,0.011869,0.0039645,0.013603,0.0093789,0.0096993])
  yErrsG3 = np.array([0.032383,0.001787,0.0019372,0.0023065,0.002361,0.0020714,0.0023775,0.0022554,0.0020204,0.0021065,0.0028728,0.005337,0.0073262,0.008318,0.0095575,0.0078936,0.0092119,0.0093799,0.0028809,0.0020908,0.0026885,0.0025833,0.0028073,0.0034809,0.0032058,0.0075917,0.0082623,0.003795,0.01352,0.0093752,0.0040672,0.0069043,0.0064869,0.011474,0.0094061,0.0093898,0.012992,0.014121,0.019611,0.014116,0.0092422,0.010617,0.011474,0.011291,0.01185,0.013771,0.020298,0.021439,0.024484])

  I2C_input = range(0,24)+range(24,128,4)
  I2C_input = np.array([float(i) for i in I2C_input])
  I2C_id10756 = np.array([1.56,1.58,1.59,1.63, 1.66,1.68,1.74,1.77, 1.82,1.89,1.96,2.07, 2.22,2.45,3.04,8.12, 16.85,26.07,35.31,45.17, 54.13,63.99,73.06,81.37, 90.51,128.40,167.27,203.8,
    244.3,281.0,319.8,355.0, 390.1,430.3,470.3,505.1, 539.7,574.9,613.9,652.6, 685.6,718.6,754.9,785.9, 817.6,849.9,885.0,916.5, 947.1,980.6])
  I2C_mZFarA = np.array([1.52,1.54,1.55,1.55, 1.56,1.58,1.59,1.60, 1.62,1.63,1.65,1.67, 1.69,1.72,1.75,1.79, 1.82,1.86,1.91,1.98, 2.05,2.16,2.34,2.69, 3.88,33.45,66.22,98.11, 130.32,162.73,189.8,224.5,
    252.9,282.0,313.8,344.1, 370.2,401.5,432.6,462.4, 488.7,516.7,545.6,576.0, 605.4,633.9,663.2,689.1, 715.2,742.3])

  canvasI2C = TCanvas('canvasI2C','canvas',800,600)
  canvasI2C.SetGrid()

# getting all the relevent info out of the files
# each file holds two lines, first is X-axis, second is Y-axis
  for i,calibFile in enumerate(fileList):
    fileDict[calibFile] = open('calibFiles/'+calibFile,'r')

# for now we are assuming that all X-axes are the same
    if i == 0:
      xLine  = fileDict[calibFile].readline()
      xLineStr = xLine.strip('\n').split(',')
      xLineFloat = [float(i)*2*0.742 for i in xLineStr]
      xLineMips = [i/0.160 for i in xLineFloat]
      inputVoltArray = np.array(xLineFloat)
      inputMipsArray = np.array(xLineMips)
      xErrs = np.array([0]*len(xLineFloat))
      fileDict[calibFile].seek(0)

# pulling the Y-axis info
    yLine = fileDict[calibFile].readline()
    yLine = fileDict[calibFile].readline()
    yLineStr = yLine.strip('\n').split(',')
    yLineFloat = [float(i) for i in yLineStr]

#cleaning a few of the datapoints that fucked up during datataking
#at some point i could go back and rerun these samples if i really wanted to be perfect
    prev = 0.0001
    for i,val in enumerate(yLineFloat[0:-1]):
      if val < 0.95*prev:
        print calibFile
        yLineFloat[i] = (yLineFloat[i-1]+yLineFloat[i+1])/2
      prev = yLineFloat[i]
    if yLineFloat[-1] < 0.95*yLineFloat[-2]:
        print calibFile
        yLineFloat[-1] = yLineFloat[-2]

    yLineFloatAmp = [i/1.1 for i in yLineFloat]
    yLineErrs = [i*0.01 for i in yLineFloatAmp]
    #yErrs = np.array(yLineErrs)
    outPutVoltArray = np.array(yLineFloat)
    outPutAmpArray = np.array(yLineFloatAmp)
    if 'Z' not in calibFile:
      if 'gain0' in calibFile:
        yErrs = yErrsG0
        totalValG0 = [a+b for a,b in zip(totalValG0,outPutAmpArray)]
      elif 'gain1' in calibFile:
        yErrs = yErrsG1
        totalValG1 = [a+b for a,b in zip(totalValG1,outPutAmpArray)]
      elif 'gain2' in calibFile:
        yErrs = yErrsG2
        totalValG2 = [a+b for a,b in zip(totalValG2,outPutAmpArray)]
      elif 'gain3' in calibFile:
        yErrs = yErrsG3
        totalValG3 = [a+b for a,b in zip(totalValG3,outPutAmpArray)]
    yErrs = yErrs/1.1

    graphDict[calibFile.rstrip('.txt')] = TGraphErrors(len(yLineFloat),inputVoltArray,outPutAmpArray,xErrs,yErrs)
    graphLinDict[calibFile.rstrip('.txt')] = TGraph(2,np.array([inputVoltArray[0],inputVoltArray[18]]),
        np.array([outPutAmpArray[0],outPutAmpArray[18]]))
    yDict[calibFile.rstrip('.txt')] = yLineFloatAmp
    fileDict[calibFile].close()
#raw_input('press enter to continue')

# since we are using TGraphs, we need to build axes (they don't just get drawn like for a TH1)
# there are a lot of ways to do this, but we'll do it using canvas.DrawFrame()
  canvasG0.cd()
  frameG0 = canvasG0.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.20)
  frameG0.SetTitle('Gain 0')
  frameG0.SetXTitle('Input Voltage (V)')
  frameG0.SetYTitle('Output Power (mW)')
  frameG0.GetYaxis().CenterTitle()
# adding a second X-axis on top for all these plots
  voltAxisG0 = TGaxis(0.0,0.2,1.25*1.1*2*0.742,0.2,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisG0.SetName('voltAxisG0')
  voltAxisG0.SetTitle('Mips')
  voltAxisG0.Draw()
  canvasG1.cd()
  frameG1 = canvasG1.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.30)
  frameG1.SetTitle('Gain 1')
  frameG1.SetXTitle('Input Voltage (V)')
  frameG1.SetYTitle('Output Power (mW)')
  frameG1.GetYaxis().CenterTitle()
  voltAxisG1 = TGaxis(0.0,0.3,1.25*1.1*2*0.742,0.3,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisG1.SetName('voltAxisG1')
  voltAxisG1.SetTitle('Mips')
  voltAxisG1.Draw()
  canvasG2.cd()
  frameG2 = canvasG2.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.35)
  frameG2.SetTitle('Gain 2')
  frameG2.SetXTitle('Input Voltage (V)')
  frameG2.SetYTitle('Output Power (mW)')
  frameG2.GetYaxis().CenterTitle()
  voltAxisG2 = TGaxis(0.0,0.35,1.25*1.1*2*0.742,0.35,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisG2.SetName('voltAxisG2')
  voltAxisG2.SetTitle('Mips')
  voltAxisG2.Draw()
  canvasG3.cd()
  frameG3 = canvasG3.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.45)
  frameG3.SetTitle('Gain 3')
  frameG3.SetXTitle('Input Voltage (V)')
  frameG3.SetYTitle('Output Power (mW)')
  frameG3.GetYaxis().CenterTitle()
  voltAxisG3 = TGaxis(0.0,0.45,1.25*1.1*2*0.742,0.45,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisG3.SetName('voltAxisG3')
  voltAxisG3.SetTitle('Mips')
  voltAxisG3.Draw()

  canvasRadComp.cd()
  frameRadComp = canvasRadComp.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.3)
  frameRadComp.SetTitle('-Z Far (B), before and after Termination Resistor')
  frameRadComp.SetXTitle('Input Voltage (V)')
  frameRadComp.SetYTitle('Output Power (mW)')
  frameRadComp.GetYaxis().CenterTitle()
  voltAxisRadComp = TGaxis(0.0,0.3,1.25*1.1*2*0.742,0.3,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisRadComp.SetName('voltAxisRadComp')
  voltAxisRadComp.SetTitle('Mips')
  voltAxisRadComp.Draw()

  totalValG0 = [a/((len(fileList)-len(radList))/4) for a in totalValG0]
  totalValG1 = [a/((len(fileList)-len(radList))/4) for a in totalValG1]
  totalValG2 = [a/((len(fileList)-len(radList))/4) for a in totalValG2]
  totalValG3 = [a/((len(fileList)-len(radList))/4) for a in totalValG3]

  totalValListTmp = [totalValG0,totalValG1,totalValG2,totalValG3]
  totalValList = []

  for i in range(0,4):
    totalValList.append(TGraph(len(totalValG0),inputVoltArray,np.array(totalValListTmp[i])))


# time to make fits, plot plots, and get paid
  for i,name in enumerate(graphDict.keys()):
    chipName = name.split('_')[0]
    if chipName not in ColorDict:
      ColorDict[chipName] = randColor()
    canvasTest.cd()
    frameTest = canvasTest.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.55)
    frameTest.SetTitle(name)
    frameTest.SetXTitle('Input Voltage (V)')
    frameTest.SetYTitle('Output Power (mW)')
    frameTest.GetYaxis().CenterTitle()
    voltAxisTest = TGaxis(0.0,0.55,1.25*1.1*2*0.742,0.55,inputMipsArray[0],inputMipsArray[-1],510,'-')
    voltAxisTest.SetName('voltAxisTest')
    voltAxisTest.SetTitle('Mips')
    voltAxisTest.Draw()
    testFit = TF1("testFit_"+name,"([0]/([1]+exp(-[2]*x))+[3])", inputVoltArray[0], inputVoltArray[-1])
    linFit = TF1('pol1_'+name,'pol1',inputVoltArray[0], inputVoltArray[11])
    linFitExt = TF1('pol1Ext_'+name,'pol1',inputVoltArray[11], inputVoltArray[-1])
    testFit.SetParNames('Scale','Denom','Exp','Constant')
    linFit.SetParNames('Intercept','Slope')
    if 'gain0' in name:
      testFit.SetParameters(0.1,0.46,2.8,-0.07)
    elif 'gain1' in name:
      testFit.SetParameters(0.18,0.5,2.6,-0.12)
    elif 'gain2' in name:
      testFit.SetParameters(0.24,0.51,2.7,-0.16)
    elif 'gain3' in name:
      testFit.SetParameters(0.46,0.7,2.4,-0.27)


    #fit the fit, get the params for later, and plot the plot
    gStyle.SetOptFit(1)
    testFit.SetLineWidth(2)
    linFit.SetLineColor(kBlue)
    linFit.SetLineWidth(2)
    graphLinDict[name].Fit(linFit,'0')
    linFitExt.SetParameters(linFit.GetParameter(0),linFit.GetParameter(1))
    linFitExt.SetLineColor(kBlue)
    linFitExt.SetLineWidth(2)
    linFitExt.SetLineStyle(2)
    graphDict[name].Fit(testFit,'M0')
    graphDict[name].Draw()
    testFit.Draw('sames')
    linFit.Draw('same')
    linFitExt.Draw('same')
    params = np.zeros(4,dtype = float)
    testFit.GetParameters(params)
    gPad.Update()
    ps = graphDict[name].GetListOfFunctions().FindObject("stats")
    ps.SetX1NDC(0.25)
    ps.SetX2NDC(0.65)
    ps.SetY1NDC(0.60)
    ps.SetY2NDC(0.85)
    canvasTest.Modified()
    canvasTest.Update()
    canvasTest.SaveAs('fitChecks/fitCheck_'+name+'.pdf')

    inl = 0
    dnl = 0
    for j,x in enumerate(inputVoltArray[0:19]):
      tmpInl = abs(testFit.Eval(x)-linFitExt.Eval(x))
      inl = max(inl, tmpInl)
      tmpDnl = abs(linFit.GetParameter(1)-abs(testFit.Eval(inputVoltArray[j])-testFit.Eval(inputVoltArray[j+1]))/0.025)
      dnl = max(dnl,tmpDnl)


    if chipName not in AOHDict:
      AOHDict[chipName] = AOH(chipName)

# unpack the params into our chip class and param lists for further calculation
    MSEList = []
    if 'gain0' in name:
      for j,aveVal in enumerate(totalValG0):
        fitVal = params[0]/(params[1]+exp(-params[2]*inputVoltArray[j]))+params[3]
        MSEList.append(pow(fitVal-aveVal,2))
      if 'left' in name:
        AOHDict[chipName].left.scale[0],AOHDict[chipName].left.denom[0],AOHDict[chipName].left.exp[0],AOHDict[chipName].left.const[0] = params
        AOHDict[chipName].left.MSE[0] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].left.fits[0] = testFit
        AOHDict[chipName].left.DNL[0] = dnl
        AOHDict[chipName].left.INL[0] = inl
      elif 'middle' in name:
        AOHDict[chipName].middle.scale[0],AOHDict[chipName].middle.denom[0],AOHDict[chipName].middle.exp[0],AOHDict[chipName].middle.const[0] = params
        AOHDict[chipName].middle.MSE[0] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].middle.fits[0] = testFit
        AOHDict[chipName].middle.DNL[0] = dnl
        AOHDict[chipName].middle.INL[0] = inl
      elif 'right' in name:
        AOHDict[chipName].right.scale[0],AOHDict[chipName].right.denom[0],AOHDict[chipName].right.exp[0],AOHDict[chipName].right.const[0] = params
        AOHDict[chipName].right.MSE[0] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].right.fits[0] = testFit
        AOHDict[chipName].right.DNL[0] = dnl
        AOHDict[chipName].right.INL[0] = inl


      canvasG0.cd()
    elif 'gain1' in name:
      for j,aveVal in enumerate(totalValG1):
        fitVal = params[0]/(params[1]+exp(-params[2]*inputVoltArray[j]))+params[3]
        MSEList.append(pow(fitVal-aveVal,2))
      if 'left' in name:
        AOHDict[chipName].left.scale[1],AOHDict[chipName].left.denom[1],AOHDict[chipName].left.exp[1],AOHDict[chipName].left.const[1] = params
        AOHDict[chipName].left.MSE[1] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].left.fits[1] = testFit
        AOHDict[chipName].left.DNL[1] = dnl
        AOHDict[chipName].left.INL[1] = inl
      elif 'middle' in name:
        AOHDict[chipName].middle.scale[1],AOHDict[chipName].middle.denom[1],AOHDict[chipName].middle.exp[1],AOHDict[chipName].middle.const[1] = params
        AOHDict[chipName].middle.MSE[1] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].middle.fits[1] = testFit
        AOHDict[chipName].middle.DNL[1] = dnl
        AOHDict[chipName].middle.INL[1] = inl
      elif 'right' in name:
        AOHDict[chipName].right.scale[1],AOHDict[chipName].right.denom[1],AOHDict[chipName].right.exp[1],AOHDict[chipName].right.const[1] = params
        AOHDict[chipName].right.MSE[1] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].right.fits[1] = testFit
        AOHDict[chipName].right.DNL[1] = dnl
        AOHDict[chipName].right.INL[1] = inl

      canvasG1.cd()
    elif 'gain2' in name:
      for j,aveVal in enumerate(totalValG2):
        fitVal = params[0]/(params[1]+exp(-params[2]*inputVoltArray[j]))+params[3]
        MSEList.append(pow(fitVal-aveVal,2))
      if 'left' in name:
        AOHDict[chipName].left.scale[2],AOHDict[chipName].left.denom[2],AOHDict[chipName].left.exp[2],AOHDict[chipName].left.const[2] = params
        AOHDict[chipName].left.MSE[2] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].left.fits[2] = testFit
        AOHDict[chipName].left.DNL[2] = dnl
        AOHDict[chipName].left.INL[2] = inl
      elif 'middle' in name:
        AOHDict[chipName].middle.scale[2],AOHDict[chipName].middle.denom[2],AOHDict[chipName].middle.exp[2],AOHDict[chipName].middle.const[2] = params
        AOHDict[chipName].middle.MSE[2] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].middle.fits[2] = testFit
        AOHDict[chipName].middle.DNL[2] = dnl
        AOHDict[chipName].middle.INL[2] = inl
      elif 'right' in name:
        AOHDict[chipName].right.scale[2],AOHDict[chipName].right.denom[2],AOHDict[chipName].right.exp[2],AOHDict[chipName].right.const[2] = params
        AOHDict[chipName].right.MSE[2] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].right.fits[2] = testFit
        AOHDict[chipName].right.DNL[2] = dnl
        AOHDict[chipName].right.INL[2] = inl

      canvasG2.cd()
    elif 'gain3' in name:
      for j,aveVal in enumerate(totalValG3):
        fitVal = params[0]/(params[1]+exp(-params[2]*inputVoltArray[j]))+params[3]
        MSEList.append(pow(fitVal-aveVal,2))
      if 'left' in name:
        AOHDict[chipName].left.scale[3],AOHDict[chipName].left.denom[3],AOHDict[chipName].left.exp[3],AOHDict[chipName].left.const[3] = params
        AOHDict[chipName].left.MSE[3] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].left.fits[3] = testFit
        AOHDict[chipName].left.DNL[3] = dnl
        AOHDict[chipName].left.INL[3] = inl
      elif 'middle' in name:
        AOHDict[chipName].middle.scale[3],AOHDict[chipName].middle.denom[3],AOHDict[chipName].middle.exp[3],AOHDict[chipName].middle.const[3] = params
        AOHDict[chipName].middle.MSE[3] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].middle.fits[3] = testFit
        AOHDict[chipName].middle.DNL[3] = dnl
        AOHDict[chipName].middle.INL[3] = inl
      elif 'right' in name:
        AOHDict[chipName].right.scale[3],AOHDict[chipName].right.denom[3],AOHDict[chipName].right.exp[3],AOHDict[chipName].right.const[3] = params
        AOHDict[chipName].right.MSE[3] = sum(MSEList)/len(MSEList)
        AOHDict[chipName].right.fits[3] = testFit
        AOHDict[chipName].right.DNL[3] = dnl
        AOHDict[chipName].right.INL[3] = inl

      canvasG3.cd()
    if 'Z' in name:
      AOHDict[chipName].right = AOHDict[chipName].middle
      AOHDict[chipName].left= AOHDict[chipName].middle



    graphDict[name].SetLineWidth(2)
    graphDict[name].SetLineColor(ColorDict[chipName])

    if 'id3633' not in name and 'Z' not in name:
      gStyle.SetOptFit(0)
      ps.Delete()
      graphDict[name].Draw('cX')
      if 'mZFarB' in name:
        canvasRadComp.cd()
        if 'TermRes' in name:
          graphDict[name].SetLineColor(kBlue)
        else:
          graphDict[name].SetLineColor(kRed)
        graphDict[name].Draw('cX')

    #  print graphDict[name].GetXaxis().GetXmin(), graphDict[name].GetXaxis().GetXmax()

  canvasG0.SaveAs('laserPlots_gain0.pdf')
  canvasG1.SaveAs('laserPlots_gain1.pdf')
  canvasG2.SaveAs('laserPlots_gain2.pdf')
  canvasG3.SaveAs('laserPlots_gain3.pdf')
  canvasRadComp.SaveAs('laserPlots_radComp.pdf')

  canvasG0.Clear()
  canvasG1.Clear()
  canvasG2.Clear()
  canvasG3.Clear()
  canvasRadComp.Clear()

  canvasG0.cd()
  frameG0 = canvasG0.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.20)
  frameG0.SetTitle('Gain 0')
  frameG0.SetXTitle('Input Voltage (V)')
  frameG0.SetYTitle('Output Power (mW)')
  frameG0.GetYaxis().CenterTitle()
# adding a second X-axis on top for all these plots
  voltAxisG0 = TGaxis(0.0,0.2,1.25*1.1*2*0.742,0.2,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisG0.SetName('voltAxisG0')
  voltAxisG0.SetTitle('Mips')
  voltAxisG0.Draw()
  canvasG1.cd()
  frameG1 = canvasG1.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.30)
  frameG1.SetTitle('Gain 1')
  frameG1.SetXTitle('Input Voltage (V)')
  frameG1.SetYTitle('Output Power (mW)')
  frameG1.GetYaxis().CenterTitle()
  voltAxisG1 = TGaxis(0.0,0.3,1.25*1.1*2*0.742,0.3,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisG1.SetName('voltAxisG1')
  voltAxisG1.SetTitle('Mips')
  voltAxisG1.Draw()
  canvasG2.cd()
  frameG2 = canvasG2.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.35)
  frameG2.SetTitle('Gain 2')
  frameG2.SetXTitle('Input Voltage (V)')
  frameG2.SetYTitle('Output Power (mW)')
  frameG2.GetYaxis().CenterTitle()
  voltAxisG2 = TGaxis(0.0,0.35,1.25*1.1*2*0.742,0.35,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisG2.SetName('voltAxisG2')
  voltAxisG2.SetTitle('Mips')
  voltAxisG2.Draw()
  canvasG3.cd()
  frameG3 = canvasG3.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.45)
  frameG3.SetTitle('Gain 3')
  frameG3.SetXTitle('Input Voltage (V)')
  frameG3.SetYTitle('Output Power (mW)')
  frameG3.GetYaxis().CenterTitle()
  voltAxisG3 = TGaxis(0.0,0.45,1.25*1.1*2*0.742,0.45,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisG3.SetName('voltAxisG3')
  voltAxisG3.SetTitle('Mips')
  voltAxisG3.Draw()
  canvasRadComp.cd()
  frameRadComp = canvasRadComp.DrawFrame(0,0,inputVoltArray[-1]*1.1,0.3)
  frameRadComp.SetTitle('-Z Far (B), before and after Termination Resistor')
  frameRadComp.SetXTitle('Input Voltage (V)')
  frameRadComp.SetYTitle('Output Power (mW)')
  frameRadComp.GetYaxis().CenterTitle()
  voltAxisRadComp = TGaxis(0.0,0.3,1.25*1.1*2*0.742,0.3,inputMipsArray[0],inputMipsArray[-1],510,'-')
  voltAxisRadComp.SetName('voltAxisRadComp')
  voltAxisRadComp.SetTitle('Mips')
  voltAxisRadComp.Draw()
  RadComp_legend = TLegend(0.2,0.65,0.4,0.8)
  RadComp_legend.SetBorderSize(0)
  RadComp_legend.SetTextSize(0.03)
  RadComp_legend.SetFillColor(1)
  RadComp_legend.SetFillStyle(0)
  canvasList = [canvasG0,canvasG1,canvasG2,canvasG3]

  MSECutOff = [
      6.6224879029e-05  + 2.9*8.84009016152e-05,
      0.000141756941771 + 2.9*0.000176893427967,
      0.000253889326891 + 2.9*0.000321099195681,
      0.000400161077294 + 2.9*0.000498443539451
      ]
  DNLCutOff = [
      0.014110972915    + 3.1*0.00371130025172,
      0.0213070232981   + 3.1*0.00651117157389,
      0.0271880517718   + 3.1*0.00831053336525,
      0.0451337720056   + 3.1*0.0157917665743
      ]
  INLCutOff = [
      0.00138369898718  + 3.1*0.000672089545231,
      0.00196402560259  + 3.1*0.000915086363153,
      0.00281839521376  + 3.1*0.00127943230252,
      0.00329824181506  + 3.1*0.00139026812399
      ]

  MSEAveList = [[],[],[],[]]
  INLAveList = [[],[],[],[]]
  DNLAveList = [[],[],[],[]]

  scaleHistList = []
  denomHistList = []
  expHistList = []
  constHistList = []
  DNLHistList = []
  INLHistList = []

  for i in range (0,4):
    scaleHistList.append(TH1F('scaleHist_G'+str(i),'scaleHist_G'+str(i),20,0,0.5))
    denomHistList.append(TH1F('denomHist_G'+str(i),'denomHist_G'+str(i),20,0.2,0.8))
    expHistList.append(TH1F('expHist_G'+str(i),'expHist_G'+str(i),20,1.8,5.4))
    constHistList.append(TH1F('constHist_G'+str(i),'constHist_G'+str(i),20,-0.3,0))
    DNLHistList.append(TH1F('DNLHist_G'+str(i),'DNLHist_G'+str(i),20,0,0.15))
    INLHistList.append(TH1F('INLHist_G'+str(i),'INLHist_G'+str(i),20,0,0.01))

  doMSE = True
  doNL =False
  for j,chip in enumerate(AOHDict.keys()):
    #print AOHDict[chip].GetID
    #print AOHDict[chip].left.MSE
    #print AOHDict[chip].middle.MSE
    #print AOHDict[chip].right.MSE
    #print

    for i in range(0,4):
      if doMSE:
        if (AOHDict[chip].left.MSE[i] < MSECutOff[i]):
          AOHDict[chip].left.isGood[i] = True
        if (AOHDict[chip].right.MSE[i] < MSECutOff[i]):
          AOHDict[chip].right.isGood[i] = True
        if (AOHDict[chip].middle.MSE[i] < MSECutOff[i]):
          AOHDict[chip].middle.isGood[i] = True
      if doNL:
        if (AOHDict[chip].left.DNL[i] < DNLCutOff[i] and AOHDict[chip].left.INL[i] < INLCutOff[i]):
          AOHDict[chip].left.isGood[i] = True
        if (AOHDict[chip].right.DNL[i] < DNLCutOff[i] and AOHDict[chip].right.INL[i] < INLCutOff[i]):
          AOHDict[chip].right.isGood[i] = True
        if (AOHDict[chip].middle.DNL[i] < DNLCutOff[i] and AOHDict[chip].middle.INL[i] < INLCutOff[i]):
          AOHDict[chip].middle.isGood[i] = True
      MSEAveList[i].append(AOHDict[chip].left.MSE[i])
      MSEAveList[i].append(AOHDict[chip].right.MSE[i])
      MSEAveList[i].append(AOHDict[chip].middle.MSE[i])
      DNLAveList[i].append(AOHDict[chip].left.DNL[i])
      DNLAveList[i].append(AOHDict[chip].right.DNL[i])
      DNLAveList[i].append(AOHDict[chip].middle.DNL[i])
      INLAveList[i].append(AOHDict[chip].left.INL[i])
      INLAveList[i].append(AOHDict[chip].right.INL[i])
      INLAveList[i].append(AOHDict[chip].middle.INL[i])

      scaleHistList[i].Fill(AOHDict[chip].left.scale[i])
      scaleHistList[i].Fill(AOHDict[chip].middle.scale[i])
      scaleHistList[i].Fill(AOHDict[chip].right.scale[i])

      denomHistList[i].Fill(AOHDict[chip].left.denom[i])
      denomHistList[i].Fill(AOHDict[chip].middle.denom[i])
      denomHistList[i].Fill(AOHDict[chip].right.denom[i])

      expHistList[i].Fill(AOHDict[chip].left.exp[i])
      expHistList[i].Fill(AOHDict[chip].middle.exp[i])
      expHistList[i].Fill(AOHDict[chip].right.exp[i])

      constHistList[i].Fill(AOHDict[chip].left.const[i])
      constHistList[i].Fill(AOHDict[chip].middle.const[i])
      constHistList[i].Fill(AOHDict[chip].right.const[i])

      DNLHistList[i].Fill(AOHDict[chip].left.DNL[i])
      DNLHistList[i].Fill(AOHDict[chip].middle.DNL[i])
      DNLHistList[i].Fill(AOHDict[chip].right.DNL[i])

      INLHistList[i].Fill(AOHDict[chip].left.INL[i])
      INLHistList[i].Fill(AOHDict[chip].middle.INL[i])
      INLHistList[i].Fill(AOHDict[chip].right.INL[i])


    AOHDict[chip].left.findGoodLaser()
    AOHDict[chip].right.findGoodLaser()
    AOHDict[chip].middle.findGoodLaser()
    AOHDict[chip].findGoodChip()
    AOHDict[chip].showGoodChip()

    for i in range(0,4):
      canvasList[i].cd()
      if AOHDict[chip].allGood:
        AOHDict[chip].left.fits[i].SetLineColor(kBlue)
        AOHDict[chip].right.fits[i].SetLineColor(kBlue)
        AOHDict[chip].middle.fits[i].SetLineColor(kBlue)
      else:
        AOHDict[chip].left.fits[i].SetLineColor(kRed)
        AOHDict[chip].right.fits[i].SetLineColor(kRed)
        AOHDict[chip].middle.fits[i].SetLineColor(kRed)
      if 'Z' in chip:
        AOHDict[chip].left.fits[i].SetLineColor(kBlack)
        AOHDict[chip].right.fits[i].SetLineColor(kBlack)
        AOHDict[chip].middle.fits[i].SetLineColor(kBlack)

      if ('Z' not in chip):
        AOHDict[chip].left.fits[i].Draw('same')
        AOHDict[chip].right.fits[i].Draw('same')
        AOHDict[chip].middle.fits[i].Draw('same')

      if j == len(AOHDict.keys())-1:
        totalValList[i].SetMarkerColor(kGreen)
        totalValList[i].SetMarkerSize(1)
        totalValList[i].Draw('sameP')


  canvasG0.cd()
  AOHDict['idmZFarBTermRes'].left.fits[0].Draw('same')
  canvasG0.SaveAs('laserPlotsFits_gain0.pdf')
  canvasG1.cd()
  AOHDict['idmZFarBTermRes'].left.fits[1].Draw('same')
  canvasG1.SaveAs('laserPlotsFits_gain1.pdf')
  canvasG2.cd()
  AOHDict['idmZFarBTermRes'].left.fits[2].Draw('same')
  canvasG2.SaveAs('laserPlotsFits_gain2.pdf')
  canvasG3.cd()
  AOHDict['idmZFarBTermRes'].left.fits[3].Draw('same')
  canvasG3.SaveAs('laserPlotsFits_gain3.pdf')

  canvasRadComp.cd()
  for chip in AOHDict:
    if 'mZFarB' in chip:
      for i in range(0,4):
        AOHDict[chip].middle.fits[i].SetLineStyle(i+1)
        if 'TermRes' in chip:
          if i is 0: RadComp_legend.AddEntry(AOHDict[chip].middle.fits[i],'-Z Far, with resistor','l')
          AOHDict[chip].middle.fits[i].SetLineColor(kBlue)
        else:
          AOHDict[chip].middle.fits[i].SetLineColor(kRed)
          if i is 0: RadComp_legend.AddEntry(AOHDict[chip].middle.fits[i],'-Z Far, without resistor','l')
        AOHDict[chip].middle.fits[i].Draw('same')
  RadComp_legend.Draw()
  canvasRadComp.SaveAs('laserPlotsFits_radComp.pdf')



  canvasG0.Clear()
  gStyle.SetOptStat(111111)
  for i in range(0,4):
    canvasG0.cd()
    scaleHistList[i].Draw()
    canvasG0.SaveAs('paramPlots/scaleParam_gain'+str(i)+'.pdf')
    canvasG0.Clear()
    denomHistList[i].Draw()
    canvasG0.SaveAs('paramPlots/denomParam_gain'+str(i)+'.pdf')
    canvasG0.Clear()
    expHistList[i].Draw()
    canvasG0.SaveAs('paramPlots/expParam_gain'+str(i)+'.pdf')
    canvasG0.Clear()
    constHistList[i].Draw()
    canvasG0.SaveAs('paramPlots/constParam_gain'+str(i)+'.pdf')
    canvasG0.Clear()
    DNLHistList[i].SetXTitle('DNL')
    DNLHistList[i].Draw()
    canvasG0.SaveAs('paramPlots/DNLParam_gain'+str(i)+'.pdf')
    canvasG0.Clear()
    INLHistList[i].SetXTitle('INL (mW)')
    INLHistList[i].Draw()
    canvasG0.SaveAs('paramPlots/INLParam_gain'+str(i)+'.pdf')
    canvasG0.Clear()


  for i in range(0,4):
    print 'MSE ave:',i,np.mean(np.array(MSEAveList[i]))
    print 'MSE std:',i,np.std(np.array(MSEAveList[i]))
  print
  for i in range(0,4):
    print 'DNL ave:',i,np.mean(np.array(DNLAveList[i]))
    print 'DNL std:',i,np.std(np.array(DNLAveList[i]))
  print
  for i in range(0,4):
    print 'INL ave:',i,np.mean(np.array(INLAveList[i]))
    print 'INL std:',i,np.std(np.array(INLAveList[i]))

  canvasI2C.cd()
  I2C_id10756_amp = np.array([i/1100 for i in I2C_id10756])
  I2C_mZFarA_amp = np.array([i/1100 for i in I2C_mZFarA])
  frameI2C = canvasI2C.DrawFrame(0,0,I2C_input[-1],I2C_id10756_amp[-1]*1.1)
  frameI2C.SetTitle('Bias Current')
  frameI2C.SetXTitle('I2C Register')
  frameI2C.SetYTitle('Output Power (mW)')
  frameI2C.GetYaxis().CenterTitle()
  I2C_id10756_graph = TGraph(len(I2C_input),I2C_input,I2C_id10756_amp)
  I2C_id10756_graph.SetLineColor(kBlack)
  I2C_id10756_graph.SetMarkerStyle(21)
  I2C_id10756_graph.Draw('cp')
  I2C_mZFarA_graph = TGraph(len(I2C_input),I2C_input,I2C_mZFarA_amp)
  I2C_mZFarA_graph.SetLineColor(kRed)
  I2C_mZFarA_graph.SetMarkerStyle(22)
  I2C_mZFarA_graph.SetMarkerColor(kRed)
  I2C_mZFarA_graph.Draw('cp')
  I2C_legend = TLegend(0.2,0.65,0.4,0.8)
  I2C_legend.SetBorderSize(0)
  I2C_legend.SetTextSize(0.03)
  I2C_legend.SetFillColor(1)
  I2C_legend.SetFillStyle(0)
  I2C_legend.AddEntry(I2C_id10756_graph,'ID 10756, new chip','lp')
  I2C_legend.AddEntry(I2C_mZFarA_graph,'-Z Far, old chip','lp')
  I2C_legend.Draw()
  canvasI2C.Modified()
  canvasI2C.Update()
  canvasI2C.SaveAs('I2C_graph.pdf')





if __name__=="__main__":
    makeLaserPlots()
