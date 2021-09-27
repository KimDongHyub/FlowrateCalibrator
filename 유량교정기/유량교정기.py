import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from matplotlib import pyplot as plt

form_class = uic.loadUiType("FA.ui")[0]
class FA(QMainWindow,form_class):
    Count=60
    timerstate=0
    newvoltagelist=[]
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    
####################################################################START버튼#####################################################################################
    def start(self):
        if FA.timerstate==0:                                      ###############timerstate 처리를 안해주면 start를 n번 눌렀을 시 함수가 n번 호출되어 시간이 n배 빠르게 흐른다.
            self.timer = QTimer(self)
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.timeout)
            self.timer.start()   
            FA.Count=60
            self.timerlabel.setText(str(FA.Count))
            self.startbutton.setText('STOP')
        else:                                                    #################### start를 누르고 시간이 지나가기 시작하면 timerstate=1 이 된다. 따라서 한번 더 누르면 stop되고 초기화되고 timerstate는 다시 0으로 된다.
            self.timer_stop()

    def timeout(self):
        if FA.Count!=0: 
            FA.timerstate=1
            FA.Count -= 1
            self.timerlabel.setText(str(FA.Count))
        else:                                                    #################### stop버튼과 마찬가지로 시간이 0초가 되면 stop 눌렀을 때와 같은 함수 발생
            self.timer_stop()
    
    def timer_stop(self):
        self.timer.stop()
        FA.timerstate=0        
        self.timerlabel.setText('60')
        self.startbutton.setText('START')
####################################################################START버튼#####################################################################################
####################################################################SAVE버튼#####################################################################################
    def save(self):
        
        self.newvaluelist=[]
        self.standardvaluelist=[100,200,300,400,500,600,700,800,900,1000]
        self.oldvoltagelist=[]
        self.newvoltagelist=[]
        temp_list=[]
        for i in range(0,10):
            self.newvalue=self.LUT.item(i,2).text()
            warningflag=self.newvalue=self.LUT.item(i,2).text()  ######################나누는 값이 0이면 플래그값이 변한다
            self.oldvoltage=self.LUT.item(i,0).text()
            temp_list.append(self.oldvoltage)
            if int(warningflag)==0:              ##############int 를 안해주면 newvalue 입력에 00을 입력할 경우 0 나누기 예외처리가 불가하다
                self.warninglabel.setText('WARNING: 0 OBSERVED NOT VALID')
                ##self.oldvoltagelist.append(self.oldvoltage) ##############여기에 있으면 break되어 인덱스 개수가 안맞아 1.정상값 save 2.0입력 save 누르기 3.그래프 plot 시 그래프가 안뜨는 오류 발생한다
                break                            ###################### break를 안하면  여러 값 중 한개만 인풋이 0인 상황에서 index out of range 오류가 나온다.

            else:
                self.newvaluelist.append(self.newvalue)
                self.oldvoltagelist.append(self.oldvoltage)
                temp=float(self.oldvoltagelist[i])*int(self.standardvaluelist[i])/float(self.newvaluelist[i]) #### float이 아닌 int로 했을 시, 여러번 돌려야 할 때 oldvoltagelist가 실수일 경우 오류가 발생
                self.newvoltagelist.append(temp)
                self.warninglabel.setText('WARNING: N/A')
        
        if int(warningflag)==0:
            
            self.newvoltagelist=temp_list  ####################이 부분이 없으면 그래프를 그릴 때 1.정상값 save 2.0입력 save 누르기 3.그래프 plot 시 그래프가 안뜨는 오류 발생한다.
        else: 
            for i in range(0,10): 
                self.LUT.setItem(i,0,QTableWidgetItem(str(round(self.newvoltagelist[i],2))))
                self.LUT.setItem(i,0,QTableWidgetItem(str(round(self.newvoltagelist[i],2))))  
                #self.LUT.setItem(i,1,QTableWidgetItem(self.newvaluelist[i])) ###원래는 이렇게 했었는데 이렇게 하면 여러번 돌렸을 때 실측값이 어느정도 맞게 되면 볼티지가 다시 처음으로 돌아가는 현상이 발생한다. 
                self.LUT.setItem(i,2,QTableWidgetItem(str(100*(i+1))))

####################################################################SAVE버튼#####################################################################################
####################################################################그래프 그리기###################################################################################
    def showgraph(self):
        
        if len(self.newvoltagelist)==10:
            plt.plot([100,200,300,400,500,600,700,800,900,1000],[1,2,3,4,5,6,7,8,9,10], color='black', marker='x', label='Standard Voltage(V)')
            plt.plot([100,200,300,400,500,600,700,800,900,1000],list(map(float,self.newvoltagelist)),color='red', marker='D', label='Current Voltage(V)') 
            #---------------------------------------------------이렇게 float형으로 요소를 바꾸지 않으면 1.정상값 save 2.입력 없이 save 누르기 3.그래프 plot 시 y축이 정렬되지 않은 상태로 표시된다
            plt.xlabel('Standard Flowrate(ml/m)')
            plt.ylabel('Voltage(V)')
            plt.axis([0, 2000, 0, 20])
            plt.legend(loc=0)
            plt.show()
        else:
            self.warninglabel.setText('WARNING: CANNOT PLOT GRAPH')
####################################################################그래프 그리기####################################################################################
####################################################################3가지 유체 종류 radiobutton으로 실행하는 부분####################################################

    def fluid1(self):                 
        fluid1.show()
    def fluid2(self):
        fluid2.show()
    def fluid3(self):
        fluid3.show()
####################################################################3가지 유체 종류 radiobutton으로 실행하는 부분####################################################        
#####################################################################main문######################################################################################
if __name__=="__main__":
    app=QApplication(sys.argv)
    fluid1=FA()
    fluid2=FA()
    fluid3=FA()
    fluid1.radioButton_1.setChecked(True)################ 이부분이 없으면 라디오버튼에 체크가 안된상태로 새로운 객체가 실행된다.
    fluid2.radioButton_2.setChecked(True)
    fluid3.radioButton_3.setChecked(True)
    fluid1.setWindowTitle('fluid1')
    fluid2.setWindowTitle('fluid2')
    fluid3.setWindowTitle('fluid3')
    fluid1.show() 
    app.exec_()

input('press enter to exit')