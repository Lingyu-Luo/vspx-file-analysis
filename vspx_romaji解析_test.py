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
out_t=["0"]
tlength=600000000/int(bpm)/(1920/int(beat))#每tick的时间长度
start=[]
end=[]
lyri=[]
for note in root.iter("Note"):
    ly=note.find("lyric")
    for syllable in note.iter("Syllable"):
        for cur in syllable.iter("cur"):
            po=[]
            for x in cur.iter("x"):
                po.append(x.text)
            #if(str(int(float(po[0])*tlength))!=out_t[-1]):
             #   f.write(out_t[-1]+" "+str(int(float(po[0])*tlength))+" pau\n")
             #   out_t.append(str(int(float(po[0])*tlength)))
            if(len(ly.text)!=1):
                start.append(str(int(round(float(po[0]),0)*tlength)))
                end.append(str(int(round(float(po[-1]),0)*tlength)))
                lyri.append(ly.text[:-1])
                ly.text=ly.text[-1]
            else:
                start.append(str(int(round(float(po[0]),0)*tlength)))
                end.append(str(int(round(float(po[-1]),0)*tlength)))
                lyri.append(ly.text[-1])
for i in range(0,len(start)-1):
    if(end[i]>start[i+1]):
        end[i]=start[i+1]
    if(start[i]!=out_t[-1]):
        f.write(out_t[-1]+" "+start[i]+" pau\n")
        out_t.append(start[i])
    f.write(start[i]+" "+end[i]+" "+lyri[i]+"\n")
    out_t.append(end[i])
    
