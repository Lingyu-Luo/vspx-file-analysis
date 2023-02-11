from xml.etree import ElementTree as ET
import os

dic_path="opencpop-strict.txt"
dic_f=open(dic_path,"r",encoding="utf-8")
dlines=dic_f.readlines()
diction={}
for line in dlines:
    line=line.strip("\n")
    ph_s=[]
    nph=0
    for i in range(len(line)):
        if line[i]=='\t':
            nph=i
        if line[i]==" ":
            vl=[]
            vl.append(line[nph+1:i])
            vl.append(line[i+1:])
            diction[line[:nph]]=vl
#print(diction)

fname=input("请输入要解析的vspx文件名：")

tree = ET.parse(fname)
root = tree.getroot()
for tempo in root.iter("bpm"):
    bpm=tempo.text
    break
for barDivide in root.iter("barDivide"):
    beat=barDivide.text
    break
print("bpm=",bpm,sep="")
print("beats=",beat,sep="")
out_t=[0]
tlength=60/float(bpm)/(1920/int(beat))#每tick的时间长度
#consonant=["b","c","ch","d","f","g","h","j","k","l","m","n","p","q","r","s","sh","t","w","x","y","z","zh"]
text=[]
start=[]
end=[]
lyri=[]
pitch=[]
if_pbs=[]

tracknum=0
for nt in root.iter("NoteTrack"):
    tracknum=tracknum+1
print("TrackNums=",tracknums,sep="")
cnt=1
for tracks in root.iter("NoteTrack"):
    if(tracknum>1):
        fname_=fname[:-5]+"_track"+str(cnt)+".lab"
        f=open(fname_,"w")
    else:
        fname_=fname[:-5]+".lab"
        f=open(fname_,"w")
    for note in track.iter("Note"):
        ly=note.find("lyric")
        pit=note.find("pitch")
        if ly.text=="-":
            if_pbs.append(1)
            lyri.append(lyri[-1])
            pitch.append(pit.text)
            end.append(end[-1])
            end[-2]=round(float(note.find("pos").text)*tlength,6)
            start.append(end[-2])
            continue
        for syllable in note.iter("Syllable"):
            for cur in syllable.iter("cur"):
                po=[]
                for x in cur.iter("x"):
                    po.append(float(x.text))
                start.append(round(po[0]*tlength,6))
                end.append(round(po[-1]*tlength,6))
                pitch.append(pit.text)
                if_pbs.append(0)
                if ly.text=="br":
                    lyri.append("AP")
                    continue
                if ly.text in diction:
                    lyri.append(diction[ly.text][0])
                    ly.text=diction[ly.text][1]
                else:
                    lyri.append(ly.text)
    for i in range(0,len(start)-1):
        if(end[i]>start[i+1]):
            end[i]=start[i+1]
        if(start[i]>out_t[-1]):
            f.write(str(out_t[-1])+" "+str(start[i])+" SP rest 0\n")
            out_t.append(start[i])
        while(end[i]<start[i]):
            end[i]=end[i]+0.2
            start[i+1]=start[i+1]+0.2
        if(lyri[i]=="AP"):
            f.write(str(start[i])+" "+str(end[i])+" "+lyri[i]+" rest "+str(if_pbs[i])+"\n")
        else:
            f.write(str(start[i])+" "+str(end[i])+" "+lyri[i]+" "+pitch[i]+" "+str(if_pbs[i])+"\n")
        out_t.append(end[i])
    os.system("lab2ds.exe "+fname_[:-4])
