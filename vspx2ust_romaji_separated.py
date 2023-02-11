from xml.etree import ElementTree as ET
fname=input("要转为ust的文件：")
tree = ET.parse(fname)
fname_=fname[:-5]+".ust"
f=open(fname_,"w")
root = tree.getroot()
for tempo in root.iter("bpm"):
    bpm=tempo.text
    break
for barDivide in root.iter("barDivide"):
    beat=barDivide.text
    break
print("bpm=",bpm,sep="")
print("beats=",beat,sep="")
f.write("[#SETTING]\nUstVersion=1.19\nTempo="+bpm+"\nTracks=1\nProjectName=\nVoiceDir=\nOutFile=\nCacheDir=\nTool1=\nTool2=\n")
count=0
out_t=[0]
notenum=["","","","","","","","","","","","","","","","","","","","","","","","","C1","C#1","D1","D#1","E1","F1","Gb1","G1","G#1","A1","A#1","B1","C2","C#2","D2","D#2","E2","F2","Gb2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","Gb3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","Gb4","G4","G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5","F5","Gb5","G5","G#5","A5","A#5","B5","C6","C#6","D6","D#6","E6","F6","Gb6","G6","G#6","A6","A#6","B6","C7","C#7","D7","D#7","E7","F7","Gb7","G7","G#7","A7","A#7","B7"]
for note in root.iter("Note"):
    ly=note.find("lyric")
    if(len(ly.text)!=1):
        ly.text=ly.text[:-1]+" "+ly.text[-1]
    pi=note.find("pitch")
    po=[]
    for cur in note.iter("cur"):
        for x in cur.iter("x"):
            po.append(x.text)
    po[0]=int(round(float(po[0]),0))
    po[-1]=int(round(float(po[-1]),0))
    print(po)
    if(len(out_t)==1):
        f.write("[#0000]\nLength="+str(po[0])+"\nLyric=R\nNoteNum=48\n")
        count=count+1
        out_t.append(po[0])
    if(po[0]>out_t[-1]):
        f.write("[#"+"0"*(4-len(str(count)))+str(count)+"]\nLength="+str(po[0]-out_t[-1])+"\nLyric=R\nNoteNum=48\n")
        count=count+1
        out_t.append(po[0])
    elif(po[0]<out_t[-1]):
        po[0]=out_t[-1]
    f.write("[#"+"0"*(4-len(str(count)))+str(count)+"]\nLength="+str(po[-1]-po[0])+"\nLyric="+ly.text+"\nNoteNum="+str(notenum.index(pi.text))+"\n")
    count=count+1
    out_t.append(po[-1])
f.write("[#TRACKEND]")
