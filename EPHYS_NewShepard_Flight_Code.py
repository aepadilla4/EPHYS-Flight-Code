# -*- coding: utf-8 -*-
"""
Created on Tue May 5 13:45:21 2022

@author: LattePanda
"""


import NeuropixAPI as npx
import time
import pyfirmata as pf
from ctypes import cast, POINTER 
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from playsound import playsound
from pycaw.pycaw import AudioUtilities,  IAudioEndpointVolume
from comtypes import CLSCTX_ALL




       

def configureProbe(slotNumber, portNumber, dockNumber, bank, numChannels, apGain, lfGain, refElectrode):
    
    shank  = 0
    channelReference = npx.ChannelReference(0)
    intRefElectrodeBank = 0
    
    print('\n\nConfiguring slot number ' + str(slotNumber) + ', port number ' + str(portNumber))
    
    if bank == 0 or bank == 1:
        for channel in range(0, 384):

            if channel != 191:
               npx.selectElectrode(slotNumber, portNumber, dockNumber, channel, shank, bank)
               # print(str(channel))
            
        print('selectElectrode() complete')
    
        for channel in range(0, 384):
            npx.setReference(slotNumber, portNumber, dockNumber, channel, shank, channelReference, intRefElectrodeBank)
            
        print('setReference() complete')

        for channel in range(0, 384):   
            npx.setGain(slotNumber, portNumber, dockNumber, channel, apGain, lfGain)
            
        print('setGain() complete')
        
            
        for channel in range(0, 384):
            npx.setAPCornerFrequency(slotNumber, portNumber, dockNumber, channel, False)
            
        print('setAPCornerFrequency() complete')
         
            
        for channel in range(0, 384):   
            npx.setStdb(slotNumber, portNumber, dockNumber, channel, False)
            
        print('setStdb() complete')
      
        
    if bank == 2:
        for channel in range(0, 192):

            if channel != 191:
               npx.selectElectrode(slotNumber, portNumber, dockNumber, channel, shank, bank)
               # print(str(channel))
            
        print('selectElectrode() complete')
    
        for channel in range(0, 192):
            npx.setReference(slotNumber, portNumber, dockNumber, channel, shank, channelReference, intRefElectrodeBank)
            
        print('setReference() complete')

        for channel in range(0, 192):   
            npx.setGain(slotNumber, portNumber, dockNumber, channel, apGain, lfGain)
            
        print('setGain() complete')
        
            
        for channel in range(0, 192):
            npx.setAPCornerFrequency(slotNumber, portNumber, dockNumber, channel, False)
            
        print('setAPCornerFrequency() complete')
         
            
        for channel in range(0, 192):   
            npx.setStdb(slotNumber, portNumber, dockNumber, channel, False)
            
        print('setStdb() complete')        

        
        
    writeProbeConf = npx.writeProbeConfiguration(slotNumber, portNumber, dockNumber, False)

        

def acquireBinData(slotNumber, portNumber, dockNumber, captureDuration, fileNameAP, fileNameLFP):
    #  This function acquires data and returns it as a packed int16 bin format

      
    signalSourceAP = npx.StreamSource(0)
    signalSourceLFP = npx.StreamSource(1)
    
    
    channels = 384
    numPacketsAP = 12
    numPacktsLFP = round(numPacketsAP/12)
    
    numAcquisitions = round(captureDuration*30000/numPacketsAP)


    # t00 = time.time()
    # npx.arm(slotNumber)
    
    # npx.setSWTrigger(slotNumber)
    # t01 = time.time()
    # print("\narm() and setSWTrigger() executed in " + str(t01-t00) + " sec")
    
    
    t0 = time.time()
    i=0
    while i < numAcquisitions:
        
        # (packetsAvailable, headRoom) = npx.getPacketFifoStatus(slotNumber, portNumber , dockNumber, signalSourceAP)
        # print("Number of Packets available:" + str(packetsAvailable))
        # while packetsAvailable < numPacketsAP:
        #     (packetsAvailable, headRoom) = npx.getPacketFifoStatus(slotNumber, portNumber , dockNumber, signalSourceAP)
            # print("Number of Packets available:" + str(packetsAvailable))
            # time.sleep(0.01)



        
        if i==0:
            
            with open(fileNameAP, "wb") as binary_file:
    
                # Write bytes to file
                binDatTemp = npx.readPacketsBin(slotNumber, portNumber, dockNumber, signalSourceAP, channels, numPacketsAP)
                binary_file.write(binDatTemp)
                # print("Data type from readPacketsBin:  " + str(type(binDatTemp)))
              
            with open(fileNameLFP, "wb") as binary_file:
       
                # Write bytes to file
                binary_file.write(npx.readPacketsBin(slotNumber, portNumber, dockNumber, signalSourceLFP, channels, numPacktsLFP))
                    
                    

        else:
            
            with open(fileNameAP, "ab") as binary_file:
    
                # Write bytes to file
                binDatTemp = npx.readPacketsBin(slotNumber, portNumber, dockNumber, signalSourceAP, channels, numPacketsAP)
                binary_file.write(binDatTemp)
                # print("Data type from readPacketsBin:  " + str(type(binDatTemp)))
              
            with open(fileNameLFP, "ab") as binary_file:
       
                # Write bytes to file
                binary_file.write(npx.readPacketsBin(slotNumber, portNumber, dockNumber, signalSourceLFP, channels, numPacktsLFP))
        
        i+=1
        
    t1 = time.time()
    print("\nacquireBinData() executed in " + str(t1-t0) + " sec")

    
    return True

        
    
def acquireListData(slotNumber, portNumber, dockNumber, captureDuration):
    #  This function acquires data and returns it as a List data type.  This is required
    #  both for plotting and for saving data as CSV or txt types.

      
    signalSourceAP = npx.StreamSource(0)
    signalSourceLFP = npx.StreamSource(1)
    
    
    channels = 384
    numPacketsAP = 12
    numPacktsLFP = round(numPacketsAP/12)
    
    numAcquisitions = round(captureDuration*30000/numPacketsAP)

    
    
    dataPacketsAP = [None]*numPacketsAP
    dataPacketsLFP = [None]*numPacktsLFP
    
    
    packetsAvailable = 0
        
    # while round(packetsAvailable*30000/numPacketsAF) < numAcquisitions:
    #     (packetsAvailable, headRoom) = npx.getPacketFifoStatus(slotNumber, portNumber , dockNumber, signalSourceAP)
   
    
    headRoom = 1
    while headRoom > 0:
        (packetsAvailable, headRoom) = npx.getPacketFifoStatus(slotNumber, portNumber , dockNumber, signalSourceAP)

    
    
    i=0
    while i < numAcquisitions:

        
        if i==0:
            dataPacketsAP = npx.readPackets(slotNumber, portNumber, dockNumber, signalSourceAP, channels, numPacketsAP)
            dataPacketsLFP = npx.readPackets(slotNumber, portNumber, dockNumber, signalSourceLFP, channels, numPacktsLFP)
        else:
            dataPacketsAP.extend(npx.readPackets(slotNumber, portNumber, dockNumber, signalSourceAP, channels, numPacketsAP))
            dataPacketsLFP.extend(npx.readPackets(slotNumber, portNumber, dockNumber, signalSourceLFP, channels, numPacktsLFP))
        
        i+=1
        


    
    return dataPacketsAP, dataPacketsLFP








def formatData(dataPackets, signalSource, channelsToFormat):
    #  This function currently creates a numpy array, dataMatrix, from the selected channelsToFormat
    #  It ALSO creates a time axis which is the first column of the numpy array.
    #  This formatData() function is necessary to save data in the CSV or txt formats 
    #  (as opposed to bin data)
    
    if signalSource.value == 0:
        fs = 30000
    elif signalSource.value == 1:
        fs = 2500
    
    # Creating time axis column
    #  IMPORTANT:  The np.arange() methods below 'artificially' creates a time 
    #  axis/column which has no discontinuities.  This approach is OK if it is known that there are none.
    #  However, using the dataPackets.timestamp value is more informative.
    timeStampArray = np.arange(len(dataPackets))/fs
    

    
    t0 = dataPackets[0].timestamp  
    # timeStampArray = [(i.timestamp-t0)/100000 for i in dataPackets]
    dataMatrix = [[i.data[j].astype(float) for j in channelsToFormat] for i in dataPackets]    
    dataMatrix = np.insert(dataMatrix, 0, timeStampArray, axis=1)    
      
    return dataMatrix, timeStampArray
 
    
    



if __name__ == '__main__':
 

 
    ###########################################################################
    ###########################################################################
    # 
    #  Set the code mode:  "Plotting" to plot, "DataSave" to save
    #  Set playSoundFile to True if playing audio test (such as sine wave or 
    #      simulated neuronal signal)
    
    codeMode = "DataSave"
    playSoundFile = False
       
    ###########################################################################
    ###########################################################################
    #  Setting OneBox parameters for all probes
    # Presenty, only one bank (0, 1 or 2) may be aqcuired from on each probe, but this can be changed per-probe with the banks tuple
    banks = (1, 0, 0, 0)
    # Reference electrode must be selected for each probe,  EXT_REF = 0 , TIP_REF = 1, INT_REF = 2
    refElectrodes = (0, 0, 0, 0)

    apGains = (3, 5, 5, 5)

    
    
    numberOfProbes = 1
    slotNums = (1, 1, 2, 2)
    portNums = (2, 2, 1, 2) 
    dockNums = (1, 1, 1, 1)
    
    lfGains = (3, 5, 5, 5)

    probe1GaincalFiles = ['C:/Users/aepadilla4/Desktop/BS Calibration/19398104162_gainCalValues.csv',
                          'C:/Users/aepadilla4/Desktop/PROBE_CALIBRATION_SO1342/19301411351_gainCalValues.csv',
                          'C:/Users/LattePanda/Desktop/Release_v20201103-phase30/SpikeGLX/_Calibration/19051008532/19051008532_gainCalValues.csv'          
                          ]
    
    probe1ADCcalFiles = ['C:/Users/aepadilla4/Desktop/BS Calibration/19398104162_ADCCalibration.csv',
                         'C:/Users/aepadilla4/Desktop/PROBE_CALIBRATION_SO1342/19301411802_ADCCalibration.csv',
                         'C:/Users/LattePanda/Desktop/Release_v20201103-phase30/SpikeGLX/_Calibration/19051008532/19051008532_ADCCalibration.csv'
                         ]
    
    
    #  The duration of a single probe measurement (sec)
    dataSaveDuration = 60
     
    #  File save location (NOTE: D:/ is the NVMe drive intended for the experiment)
    fileSaveSpot = "C:/Users/aepadilla4/Desktop/"
    
    

    #  StreamSource(0) for AP and StreamSource(1) for LFP
    signalSourceAP = npx.StreamSource(0)
    signalSourceLFP = npx.StreamSource(1)
    numChannels = 384

    #  Plot duration is the t-axis on plots.  Only used in "Plotting" mode.
    plotDuration = 0.10
    
    #  Select electrode to plot.  Only used in "Plotting" mode.
    electrodeToPlot = 100   
    



    ###########################################################################
    ###########################################################################        
    #  Setting up GPIO pins to detect flight trigger points
    
    # board = pf.Arduino('COM4') #internal com port of Arduino on LattePanda, found by opening Arduino IDE
    
    # #  Currently, the code will look for pin D2 to go HIGH before beginning data gathering.  This should be "liftoff detected"
    # in_D2 = board.digital[2]
    
    # #  The code will then wait for D3 to go HIGH (and D2 return to LOW) to stop data collection.
    # #  This should be the "deploy drogues chutes detected"
    # in_D3 = board.digital[3]

    # it = pf.util.Iterator(board)
    # it.start()

    # in_D2.mode = pf.INPUT
    # in_D3.mode = pf.INPUT



    ###########################################################################
    ###########################################################################
    #  Setting Volume and Opening audio File
    
    if playSoundFile:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
     
        # Control volume
        # volume.SetMasterVolumeLevel(-0.0, None) #max
        # volume.SetMasterVolumeLevel(-5.0, None) #72%
        # volume.SetMasterVolumeLevel(-10.0, None) #51%
          # volume.SetMasterVolumeLevel(-15.0, None) #36%
        volume.SetMasterVolumeLevel(-20.0, None) # 26%
        
                
        song = 'C:/Users/LattePanda/Music/60s_Sine_1000Hz_-5dBFS.wav'
        # song = 'C:/Users/LattePanda/Music/AnteriorCingulateInterneuron.wav'
        playsound(song, block=False)
        print("\n  Sound file initiated \n ")




    ###########################################################################
    ###########################################################################
    #  Setting up OneBoxes

    t0 = time.time()    

    #  Basestation scan and map
    npx.scanBS()
    
    deviceList = npx.getDeviceList(2)
    getSlotIDOut = npx.tryGetSlotID(deviceList[0])
    
    

    #  This initial for loop sets up the probes according to slotNums, portNums, etc.      
    for m in range(0, len(deviceList)):
        npx.mapBS(deviceList[m].ID, m+1)
        npx.openBS(m+1) 
        
    t1 = time.time()
    print("\n\nTime to open basestations: " + str(t1-t0) + "sec")    
        
    for n in range(0, numberOfProbes):
        
        # npx.openPort(slotNums[n], portNums[n])
        npx.openProbe(slotNums[n], portNums[n], dockNums[n])  
        
        # Init() funtion was found to fail 50% of the time, and determined to not be needed 
        # for code execution. It's left here for posterity
        #
        # npx.Init(slotNums, portNums, dockNums) 

        
    
        npx.setADCCalibration(slotNums[n], portNums[n],  probe1ADCcalFiles[n])   
        npx.setGainCalibration(slotNums[n], portNums[n],  dockNums[n], probe1GaincalFiles[n])

    
     
        configureProbe(slotNums[n], portNums[n],  dockNums[n],  banks[n], numChannels, apGains[n], lfGains[n], refElectrodes[n])
        
        
        
        npx.arm(slotNums[n])
    
        npx.setSWTrigger(slotNums[n])
        
        t2 = time.time()
        print('\nTime to openProbe(), arm() and setSWTrigger() for Port #' + str(portNums[n]) +" = " + str(t2-t1) + "sec")
        
        t1 = t2
        print
        
        
        # npx.closePort(slotNums[n], portNums[n])
        
        # print('\nPort #' + str(portNums[n]) + ' closed')
        
        # npx.closeProbe(slotNums[n], portNums[n], dockNums[n])
    
#These lines should be uncommented for flight
    # state2 = in_D2.read()
    # state3 = in_D3.read()
    
    # while (not(state2) ):
    #     print("\nWaiting on D2 pin to read HIGH")
    #     time.sleep(1)
    #     state2 = in_D2.read()
    
    #These lines should be deleted for flight
    state2=1
    state3=0      
    i = 0 
    while (state2 and not(state3)):        
                
        print('Acquisition #: ' + str(i))
        i = i+1

    
        for n in range(0, numberOfProbes):
                
            if codeMode == "Plotting":
                    
                channelsToPlot = [j for j in range(1,382)]
                channelsToFormat = channelsToPlot
                
                t2 = time.time()
                
                dataPacketsAP, dataPacketsLFP = acquireListData(slotNums[n], portNums[n], dockNums[n], plotDuration)
                
                t3 = time.time()
                print("\nTime to acquire data: " + str(t3-t2) + "sec")
                
    
                
                dataMatrixAP, timeStampsAP = formatData(dataPacketsAP, signalSourceAP, channelsToFormat)
                dataMatrixLFP, timeStampsLFP = formatData(dataPacketsLFP, signalSourceLFP, channelsToFormat)
                # plt.plot(timeStampArray1)   
                t4 = time.time()
                print("Time to format data: " + str(t4-t3) + "sec")
                
                #  Plotting data
                plt.figure(1)
                plt.figure(1).clear()
                
                plt.subplot(211)
                plt.plot(dataMatrixAP[:,0], dataMatrixAP[:,electrodeToPlot], 'g')
                plt.xlim((0, plotDuration))
                title1 = "AP Signal, Probe #" + str(n)
                plt.title(title1,fontsize=12)
                plt.xlabel("t (sec)",fontsize=10)
                plt.ylabel("signal (DN)",fontsize=10)
                
                
                plt.subplot(212)
                plt.plot(dataMatrixLFP[:,0], dataMatrixLFP[:,electrodeToPlot])
                plt.xlim((0, plotDuration))
                title2 = "LFP Signal, Probe #" + str(n)
                plt.title(title2,fontsize=12)
                plt.xlabel("t (sec)",fontsize=10)
                plt.ylabel("signal (DN)",fontsize=10)
    
                plt.show()
                # print('plot complete')
                
                t5 = time.time()
                print("Time to plot: " + str(t5-t4) + "sec")
        
    
            if codeMode == "DataSave":
                
               
                #  Plotting data
                channelsToSave = [j for j in range(1,382)]
                    
                
                convertToCSV = False
                
                if convertToCSV:
                    
                    dataPacketsAP, dataPacketsLFP = acquireListData(slotNums[n], portNums[n], dockNums[n], dataSaveDuration)      
                    dataMatrixAP, timeStampsAP = formatData(dataPacketsAP, signalSourceAP, channelsToSave)
                    dataMatrixLFP, timeStampsLFP = formatData(dataPacketsLFP, signalSourceLFP, channelsToSave)  
                    
                    now = datetime.now()
                    date_time = now.strftime("%m%d%Y%H%M%S")
                    
                    fileNameAP = fileSaveSpot + "SlotNum" + str(slotNums[n]) + "_PortNum" + str(portNums[n]) + "_AP_" +  date_time + ".csv"
                    fileNameLFP = fileSaveSpot + "SlotNum" + str(slotNums[n]) + "_PortNum" + str(portNums[n]) + "_LFP_" +  date_time + ".csv"
                    
                    np.savetxt(fileNameAP, dataMatrixAP) 
                    np.savetxt(fileNameLFP, dataMatrixLFP) 
                    
                else:
                    now = datetime.now()
                    date_time = now.strftime("%m%d%Y%H%M%S")
                
                    fileNameAP = fileSaveSpot + "SlotNum" + str(slotNums[n]) + "_PortNum" + str(portNums[n]) + "_AP_" +  date_time
                    fileNameLFP = fileSaveSpot + "SlotNum" + str(slotNums[n]) + "_PortNum" + str(portNums[n]) + "_LFP_" +  date_time
                    
                    acquireBinData(slotNums[n], portNums[n], dockNums[n], dataSaveDuration, fileNameAP, fileNameLFP)

                  
        # state2 = in_D2.read()
        # state3 = in_D3.read()


    for m in range(0, len(deviceList)):

        npx.closeBS(m+1) 
    

