from xml.etree import ElementTree as ET
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
out_t=["0.0"]
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
        end[-2]=str(round(float(note.find("pos").text)*tlength,6))
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
            start.append(str(round(po[0]*tlength,6)))
            end.append(str(round(po[-1]*tlength,6)))
            pitch.append(pit.text)
            if_pbs.append(0)
            if ly.text=="br":
                lyri.append("AP")
                continue
            if len(ly.text)>1:
                lyri.append(ly.text[0:-1])
                ly.text=ly.text[-1]
            else:
                lyri.append(ly.text)
for i in range(0,len(start)-1):
    if(end[i]>start[i+1]):
        end[i]=start[i+1]
    if(start[i]>out_t[-1]):
        f.write(out_t[-1]+" "+start[i]+" SP rest 0\n")
        out_t.append(start[i])
    if(lyri[i]=="AP"):
        f.write(start[i]+" "+end[i]+" "+lyri[i]+" rest "+str(if_pbs[i])+"\n")
    else:
        f.write(start[i]+" "+end[i]+" "+lyri[i]+" "+pitch[i]+" "+str(if_pbs[i])+"\n")
    out_t.append(end[i])
os.system("lab2ds.exe "+fname_[:-4])
