from lolFem.core.time_assistant import TimeAssistant

time = [0,1.5,2.5,3,4,5]

TA = TimeAssistant(time)

for i in TA.times():
    print "curr"
    print TA.curr_time
    print "dt"
    print TA.dt

