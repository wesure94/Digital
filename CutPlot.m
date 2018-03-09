oriDat=importdata('208_clean.txt', '\t');
[r502,c502] = size(oriDat);
oriSpeed = oriDat(:,2);
oriThick = oriDat(:,1);
oriLength = lengthCalc(oriSpeed, 0.01, 1, true);                 %计算长度序列
for i = 1:fix(r502/2)
    t = oriThick(i);
    oriThick(i) = oriThick(r502-i+1);
    oriThick(r502-i+1) = t;
end

x1 = oriLength;%(65146:65327);
y1 = oriThick;%(65146:65327);

Dat = importdata('Cut208.txt','\t');
Length = Dat(:,1);
Thick  = Dat(:,2);

figure;
x2 = Length(20025:20250);
y2 = Thick(20025:20250);
plot(x1,y1,x2,y2);
%plot(x2,y2)

%数据归一化
%208:Length,Thick
%502:502_clean.txt
[Z,Mu,Sigma] = zscore(Thick);
figure;
plot(Length,Z);
[r,c] = size(Z);
fid1=fopen('zscore208.txt','w');   %%%%需要改文件名称的地方
for i = 1:r
    count=fprintf(fid1,' %f\t %f\n',Length(i),Z(i));
end

Dat = importdata('502_clean.txt','\t');
oriSpeed = Dat(:,1);
Thick502 = Dat(:,2)*1000000;
Length502 = lengthCalc(oriSpeed, 0.008, 1, false); 
%figure;
%plot(Length502,Thick502);
[Z502,Mu,Sigma] = zscore(Thick502);
figure;
plot(Length502,Z502);
[r,c] = size(Z502);
fid1=fopen('zscore502.txt','w');   %%%%需要改文件名称的地方
for i = 1:r
    count=fprintf(fid1,' %f\t %f\n',Length502(i),Z502(i));
end