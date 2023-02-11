#include<iostream>
#include<string>
#include<vector>
using namespace std;
string str,jw=".ds",jw1=".lab";
float t1,t2;
string ph,pit,consonant[23]={"b","c","ch","d","f","g","h","j","k","l","m","n","p","q","r","s","sh","t","w","x","y","z","zh"},SP="SP",rest="rest";
bool if_pbs,flag;
vector<string>ph_seq;
vector<string>note_seq;
vector<string>text;
vector<bool>is_slur_seq;
vector<float>note_dur_seq;
vector<float>ph_dur;
int main(/*string str*/)
{
	//cout<<"输入你需要转换的lab文件名称（不带.lab结尾）:";
	//cin>>str;
	string str="一半的梦"; 
	freopen(string(str+".lab").c_str(),"r",stdin);
	freopen(string(str+".ds").c_str(),"w",stdout);
	while(cin>>t1>>t2>>ph>>pit>>if_pbs)
	{
		if(t1==0&&ph=="SP")continue;
		flag=false;
		for(int i=0;i<23;++i)if(ph==consonant[i])flag=true;
		if((flag)&&t2-t1>0.2)
		{
			float t3=t1;
			while(t2-t3>0.2)t3+=0.1;
			ph_dur.push_back(t3-t1);
			ph_seq.push_back(SP);
			is_slur_seq.push_back(0);
			note_seq.push_back(rest);
			t1=t3;
		}
		ph_dur.push_back(t2-t1);
		ph_seq.push_back(ph);
		is_slur_seq.push_back(if_pbs);
		note_seq.push_back(pit);
	}
	for(int i=0;i<ph_dur.size();++i)
	{
		flag=false;
		for(int j=0;j<23;++j)
		{
			if(ph_seq[i]==consonant[j])flag=true;
		}
		if(flag&&i<ph_dur.size()-1)
		{
			note_dur_seq.push_back(ph_dur[i]+ph_dur[i+1]);
			note_dur_seq.push_back(ph_dur[i]+ph_dur[i+1]);
			++i;
		}
		else
		{
			note_dur_seq.push_back(ph_dur[i]);
			//if(i>0)if(ph_seq[i]!=ph_seq[i-1])text.push_back(ph_seq[i]);
		}
	}
	cout<<"{\n"<<char(34)<<"text"<<char(34)<<": "<<char(34);
	for(int i=0;i<ph_seq.size()-1;++i)
	{
		flag=false;
		for(int j=0;j<23;++j)
		{
			if(ph_seq[i]==consonant[j])flag=true;
		}
		if(flag)
		{
			if((ph_seq[i]=="j"||ph_seq[i]=="q"||ph_seq[i]=="x"||ph_seq[i]=="y")&&(ph_seq[i+1]=="v"))cout<<ph_seq[i]<<"u"<<" ";
			else if((ph_seq[i]=="j"||ph_seq[i]=="q"||ph_seq[i]=="x"||ph_seq[i]=="y")&&(ph_seq[i+1]=="vn"))cout<<ph_seq[i]<<"un"<<" ";
			else if(ph_seq[i+1]=="ve")cout<<ph_seq[i]<<"ue"<<" ";
			else cout<<ph_seq[i]<<ph_seq[i+1]<<" ";
			++i;
		}
		else
		{
			if(i>0)if(ph_seq[i]!=ph_seq[i-1]||ph_seq[i]=="SP")cout<<ph_seq[i]<<" ";
			if(i==0)cout<<ph_seq[i]<<" ";
		}
	}
	cout<<char(34)<<",\n"<<char(34)<<"ph_seq"<<char(34)<<": "<<char(34);
	for(int i=0;i<ph_seq.size();++i)cout<<ph_seq[i]<<" ";
	cout<<char(34)<<",\n"<<char(34)<<"note_seq"<<char(34)<<": "<<char(34);
	for(int i=0;i<note_seq.size();++i)cout<<note_seq[i]<<" ";
	cout<<char(34)<<",\n"<<char(34)<<"note_dur_seq"<<char(34)<<": "<<char(34);
	for(int i=0;i<note_dur_seq.size();++i)cout<<note_dur_seq[i]<<" ";
	cout<<char(34)<<",\n"<<char(34)<<"is_slur_seq"<<char(34)<<": "<<char(34);
	for(int i=0;i<is_slur_seq.size();++i)cout<<is_slur_seq[i]<<" ";
	cout<<char(34)<<",\n"<<char(34)<<"ph_dur"<<char(34)<<": "<<char(34);
	for(int i=0;i<ph_dur.size();++i)cout<<ph_dur[i]<<" ";
	cout<<char(34)<<",\n"<<char(34)<<"input_type"<<char(34)<<": "<<char(34)<<"phoneme"<<char(34)<<"\n}";
}
