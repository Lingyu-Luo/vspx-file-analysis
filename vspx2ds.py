from xml.etree import ElementTree as ET
import os
fname=input("请输入要解析的vspx文件名：")
fname_=fname[:-5]+".lab"
f=open(fname_,"w")
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
consonant=["b","c","ch","d","f","g","h","j","k","l","m","n","p","q","r","s","sh","t","w","x","y","z","zh"]
text=[]
start=[]
end=[]
lyri=[]
pitch=[]
if_pbs=[]
for note in root.iter("Note"):
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
            #if(str(int(float(po[0])*tlength))!=out_t[-1]):
             #   f.write(out_t[-1]+" "+str(int(float(po[0])*tlength))+" pau\n")
             #   out_t.append(str(int(float(po[0])*tlength)))
            start.append(round(po[0]*tlength,6))
            end.append(round(po[-1]*tlength,6))
            pitch.append(pit.text)
            if_pbs.append(0)
            if ly.text=="br":
                lyri.append("AP")
                continue
            if ly.text[0] in consonant:
                if ly.text[1]=='h':
                    lyri.append(ly.text[0:2])
                    ly.text=ly.text[2:]
                else:
                    lyri.append(ly.text[0])
                    ly.text=ly.text[1:]
            else:
                if ly.text=="ue":
                    ly.text="ve"
                if lyri[-1]=="j" or lyri[-1]=="x" or lyri[-1]=="q" or lyri[-1]=="y":
                    if ly.text=="u":
                        ly.text="v"
                    elif ly.text=="un":
                        ly.text="vn"
                    lyri.append(ly.text)
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
