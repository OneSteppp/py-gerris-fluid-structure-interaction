#定义类  矢量，并且重载运算符
class Vector:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    #加法 +
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x,y,z)
    #减法 -
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x,y,z)
    #乘法 *
    def __mul__(self,other):
        x = self.x*other
        y = self.y*other
        z = self.z*other
        return Vector(x,y,z)
    #除法 /
    def __truediv__(self, other):
        x = self.x/other
        y = self.y/other
        z = self.z/other
        return Vector(x,y,z)
    #除法 // 对位相除
    def __floordiv__(self, other):
        x = self.x/other.x
        y = self.y/other.y
        z = self.z/other.z
        return  Vector(x,y,z)

    def __repr__(self):
        return self.x + "\t" + self.y + "\t" + self.z


    def __del__(self):
        class_name = self.__class__.__name__

#读取bodyforce的后两行
def get_force(filename):
    with open(filename, 'rb') as f:  #读取方式要以字节读取
        flag = -10
        while 1:
            f.seek(flag, 2)         #参数flag表示逆序读取的位数，参数2表示逆序读取
            result = f.readlines()
            if len(result) > 2:
                break
            else:
                flag *=2

        L1 = [float(i) for i in result[-1].split()]
        L0 = [float(i) for i in result[-2].split()]
        ForceData = list(zip(L0,L1))

    return ForceData

#读取上一时刻速度，位移，角速度，转角
# T VelX VelY VelZ DispX DispY DispZ AngularVelX AngularVelY AngularVelZ AngleX AngleY AngleZ
def get_data0(filename):
    with open(filename, 'rb') as f:  #读取方式要以字节读取
        flag = -10
        while 1:
            f.seek(flag, 2)         #参数flag表示逆序读取的位数，参数2表示逆序读取
            result = f.readlines()
            if len(result) > 1:
                break
            else:
                flag *=2
    data0 = [float(i) for i in result[-1].split()]
    return data0

#写下当前时刻速度，位移，角速度，转角
def write_data1(filename,data1):
    with open(filename,'a+')as f:
        for i in data1:
            f.write(str(i)+"\t")
        f.write("\n")

#----------------------#
#--------主程序---------#
#----------------------#

#设置质量 转动惯量
m = 0.1
I = Vector(1,1,1)

#读入力文件
result = get_force("a.txt")

T0 = result[0][0]
T1 = result[0][1]
dt = T1 - T0

F0 = Vector(result[1][0]+result[4][0],
            result[2][0]+result[5][0],
            result[3][0]+result[6][0])

F1 = Vector(result[1][1]+result[4][1],
            result[2][1]+result[5][1],
            result[3][1]+result[6][1])
M1 = Vector(result[7][0]+result[10][0],
            result[8][0]+result[11][0],
            result[9][0]+result[12][0])
M2 = Vector(result[7][1]+result[10][1],
            result[8][1]+result[11][1],
            result[9][1]+result[12][1])

#读入上一时刻速度，位移，角速度，转角
data0 = get_data0("b.txt")

Vel0 = Vector(data0[1],data0[2],data0[3])
Disp0 = Vector(data0[4],data0[5],data0[6])
AngularVel0 = Vector(data0[7],data0[8],data0[9])
Angle0 = Vector(data0[10],data0[11],data0[12])

#计算下一时刻速度，位移，角速度，转角
Vel1 = Vel0 + ((F0 + F1)/(2*m))*dt

DIx = m*(2*Disp0.y*Vel0.y + 2*Disp0.z*Vel0.z)
DIy = m*(2*Disp0.z*Vel0.z + 2*Disp0.x*Vel0.x)
DIz = m*(2*Disp0.x*Vel0.x + 2*Disp0.y*Vel0.y)

I = I + Vector(Disp0.y*Disp0.y+Disp0.z*Disp0.z,
                 Disp0.z*Disp0.z+Disp0.x*Disp0.x,
                 Disp0.x*Disp0.x+Disp0.y*Disp0.y)*m

AngularVel1 = AngularVel0 + \
              (((M1 + M2)/2 - Vector(AngularVel0.x*DIx,
                                       AngularVel0.y*DIy,
                                       AngularVel0.z*DIz))//I)*dt

Disp1 = Disp0 + Vel0*dt
Angle1 = Angle0 + AngularVel0*dt

data1 = [T1,Vel1.x,Vel1.y,Vel1.z,
         Disp1.x,Disp1.y,Disp1.z,
         AngularVel1.x,AngularVel1.y,AngularVel1.z,
         Angle1.x,Angle1.y,Angle1.z]

#写入当前时刻速度，位移，角速度，转角
write_data1("b.txt",data1)










