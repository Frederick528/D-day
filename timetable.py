import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        pal = QPalette()
        pal.setColor(QPalette.Background,QColor('#7DFDFE'))
        self.setPalette(pal)

    def initUI(self):
        self.schedule = QTextBrowser()                          #D-day 일정을 보여주는 텍스트창 
        file = open('test.txt','a+',encoding='utf8')            #test.txt 파일이 없을 경우 만들어주는 코드
        file.close()
        with open('test.txt','r',encoding='utf8') as file:      #test.txt 파일을 읽어주는 코드
            lines = file.readlines()
            self.time = datetime.now()                          #2022-06-15 10:47:43.904103
            i = 1
            for line in lines:                                                            #test.txt 파일에서 내용 읽어서 GUI에 추가
                line = line.strip()                                                       #줄 끝의 줄 바꿈 문자를 제거
                if line == '':                                                            #test.txt 파일에 혹시나 있을지도 모르는 공백 무시 처리
                    pass
                else:
                    if i % 2 != 0:                                                        #test.txt 파일에 홀수번째 줄마다 적용
                        date_time_obj = datetime.strptime(line, '%Y-%m-%d %H:%M:%S')      #홀수번째 줄마다 텍스트를 datetime값으로 변환 / 2022-06-15 00:00:00
                        if self.time >= date_time_obj:                                    #현재 시간과 일정 시간을 비교하여 그 차이의 절댓값을 구하는 코드
                            date_diff_tmp = self.time - date_time_obj
                            date_diff = str(date_diff_tmp)[:-7]                           #datetime값을 글자화하여 인덱싱(인덱싱 안 하면 마이크로초까지 계산함.)
                        else:
                            date_diff_tmp = date_time_obj - self.time
                            date_diff = str(date_diff_tmp)[:-7]                           #datetime값을 글자화하여 인덱싱
                        i += 1
                    else:
                        if self.time >= date_time_obj:
                            self.schedule.append(f'<b>{line} 후 지난시간:</b>')           #텍스트를 굵게
                        else:
                            self.schedule.append(f'<b>{line}까지 남은시간:</b>')
                        self.schedule.setStyleSheet("color: black; border-style: solid; border-width: 3px; border-color: white; border-radius: 10px; ")
                        self.schedule.append(f'<p style="color: red">{date_diff}</p>')    #텍스트 색 변경
                        self.schedule.append(f'<p style="font-size: 10px">ㅤ</p>')        #일정 표시 간격 설정(공백 문자를 이용, 스페이스바로는 구분X)
                        i += 1            
        self.now = datetime.today().strftime("%Y%m%d")                  #20220615
        main_layout = QHBoxLayout()
        sub_layout1 = QVBoxLayout()
        sub_layout2 = QVBoxLayout()
        schedule_layout = QHBoxLayout()
        input_layout = QHBoxLayout()
        
        self.datetime_widget_y = QComboBox(self)
        self.datetime_widget_m = QComboBox(self)
        self.datetime_widget_d = QComboBox(self)
        self.title = QLineEdit("일정 이름")
        self.title.setStyleSheet("color: black; border-style: solid; border-width: 2px; border-color: white; border-radius: 5px; ")
        self.btn = QPushButton("입력")
        self.btn.setStyleSheet('QPushButton{background-color: rgb(251,206,177)} QPushButton:hover{background-color: rgb(248,140,101)}')
        self.clear_btn = QPushButton('전체 일정 제거')
        self.clear_btn.setStyleSheet('QPushButton{background-color: rgb(251,206,177)} QPushButton:hover{background-color: rgb(248,140,101)}')
        
        self.input = QLineEdit(str(self.now))                           #LineEdit 창에 날짜가 보이도록 출력(20220615)
        self.input.setStyleSheet("color: black; border-style: solid; border-width: 2px; border-color: white; border-radius: 5px; ")

        for year in range(2100,1899,-1):
            self.datetime_widget_y.addItem(str(year))
        for month in range(1,13):
            if month <10:
                self.datetime_widget_m.addItem("0"+str(month))          #00,01,02,···,09
            else:
                self.datetime_widget_m.addItem(str(month))              #10,···,12
        for day in range(1,32):
            if day <10:
                self.datetime_widget_d.addItem("0"+str(day))            #00,01,02,···,09
            else:
                self.datetime_widget_d.addItem(str(day))                #10,11,···,31
        self.datetime_widget_y.currentTextChanged.connect(self.combo1)
        self.datetime_widget_m.currentTextChanged.connect(self.combo2)
        self.datetime_widget_d.currentTextChanged.connect(self.combo3)

        self.btn.clicked.connect(self.UD_schedule)
        self.clear_btn.clicked.connect(self.clear_event_text)

        schedule_layout.addWidget(self.datetime_widget_y)
        schedule_layout.addWidget(self.datetime_widget_m)
        schedule_layout.addWidget(self.datetime_widget_d)
        schedule_layout.addWidget(self.title)
        schedule_layout.addWidget(self.btn)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.clear_btn)                          #일정 프로그램 코드 끝


        time_schedule_layout = QHBoxLayout()
        schedule_input_layout = QHBoxLayout()

        self.schedule_time_h = QComboBox(self)      
        self.schedule_time_m = QComboBox(self) 
        self.schedule_title = QLineEdit("일정")
        self.schedule_title.setStyleSheet("color: black; border-style: solid; border-width: 2px; border-color: white; border-radius: 5px; ")
        self.schedule_btn = QPushButton("입력")
        self.schedule_btn.setStyleSheet('QPushButton{background-color: rgb(251,206,177)} QPushButton:hover{background-color: rgb(248,140,101)}')
        self.schedule_clear_btn = QPushButton('전체 계획 제거')
        self.schedule_clear_btn.setStyleSheet('QPushButton{background-color: rgb(251,206,177)} QPushButton:hover{background-color: rgb(248,140,101)}')
        self.schedule_input = QLineEdit('00시부터 01시까지')
        self.schedule_input.setStyleSheet("color: black; border-style: solid; border-width: 2px; border-color: white; border-radius: 5px; ")

        for time1 in range(0,24):
            if time1 <10:
                self.schedule_time_h.addItem("0"+str(time1))                #00,01,02,···,09
            else:
                self.schedule_time_h.addItem(str(time1))                    #10,11,···,23
        
        for time2 in range(1,25):
            if time2 <10:
                self.schedule_time_m.addItem("0"+str(time2))                #01,02,03,···,09
            else:
                self.schedule_time_m.addItem(str(time2))                    #10,11,···,24
        self.schedule_time_h.currentTextChanged.connect(self.combo4)
        self.schedule_time_m.currentTextChanged.connect(self.combo5)

        self.schedule_btn.clicked.connect(self.UD_timetable)
        self.schedule_clear_btn.clicked.connect(self.clear_event_schedule)

        time_schedule_layout.addWidget(self.schedule_time_h)
        time_schedule_layout.addWidget(QLabel('시'))
        time_schedule_layout.addWidget(QLabel('~'))
        time_schedule_layout.addWidget(self.schedule_time_m)
        time_schedule_layout.addWidget(QLabel('시까지'))
        time_schedule_layout.addWidget(self.schedule_title)
        time_schedule_layout.addWidget(self.schedule_btn)
        schedule_input_layout.addWidget(self.schedule_input)
        schedule_input_layout.addWidget(self.schedule_clear_btn)

        self.timetable_layout_V = QVBoxLayout()
        with open('test2.txt','a+',encoding='utf8') as file2:
            if os.stat("test2.txt").st_size == 0:                 #test2.txt 파일에 아무 내용도 없을 때 실행
                for time in range(0,24):
                    if time < 10:
                        time = '0'+str(time)                      #00,01,02,···,09
                    time_plus = int(time) + 1
                    if time_plus < 10:
                        time_plus = '0'+str(time_plus)            #01,02,03,···,09
                    file2.write(f'{time}:{time_plus}\n')          #00:01\n 01:02\n ··· 23:24\n
        file2 = open('test2.txt','r',encoding='utf8')
        for x,l in enumerate(file2):                                                                                    #x은 라인 위치(0부터 시작) l은 그 라인에 있는 텍스트
            for time in range(0,24):
                if time < 10:
                    time = '0'+str(time)                                                                                #00,01,02,···,09
                time_plus = int(time) + 1                                                                               #1,2,3,···,9
                if time_plus < 10:
                    time_plus = '0'+str(time_plus)                                                                      #01,02,03,···,09
                if x == int(time):                                                                                      #x가 time번째 줄일 때 실행(0번째 줄부터)
                    new_str = l[6:]                                                                                     #new_str은 텍스트 6번째 인덱스부터(일정 이름)
                    globals()['timetable_label{}'.format(x)] = QLabel(f'{time}~{time_plus}')                            #for문 내에서 각각의 Label변수명 생성(라벨0,라벨1,···,라벨23)
                    globals()['timetable_label{}'.format(x)].setStyleSheet("color: black; border-style: solid; border-width: 3px; border-color: white; border-radius: 10px; ")
                    globals()['timetable_lineedit{}'.format(x)] = QLineEdit(str(new_str))                               #for문 내에서 각각의 LineEdit변수명 생성(위와 동일)
                    globals()['timetable_lineedit{}'.format(x)].setStyleSheet("color: black; border-style: solid; border-width: 3px; border-color: white; border-radius: 10px; ")
                    globals()['timetable_lineedit{}'.format(x)].editingFinished.connect(lambda n = x:self.saveText(n))  #LineEdit이 편질될 때 x값을 받으면서 함수 실행
                    globals()['timetable_layout{}'.format(x)] = QHBoxLayout()                                           #for문 내에서 각기 다른 Layout변수명 생성(위와 동일)
                    globals()['timetable_layout{}'.format(x)].addWidget(globals()['timetable_label{}'.format(x)])       #for문 내에서 Layout에 Widget 추가
                    globals()['timetable_layout{}'.format(x)].addWidget(globals()['timetable_lineedit{}'.format(x)])    #위와 동일
                    self.timetable_layout_V.addLayout(globals()['timetable_layout{}'.format(x)])                        #for문 내에서 Layout에 다른 Layout 추가
        file2.close()                                                                                                   #계획표 프로그램 코드 끝
        
        sub_layout1.addLayout(schedule_layout)
        sub_layout1.addLayout(input_layout)
        sub_layout1.addWidget(self.schedule)
        sub_layout2.addLayout(time_schedule_layout)
        sub_layout2.addLayout(schedule_input_layout)
        sub_layout2.addLayout(self.timetable_layout_V)
        main_layout.addLayout(sub_layout1)
        main_layout.addLayout(sub_layout2)

        self.setWindowTitle('D-day')
        self.setLayout(main_layout)
        # self.resize(300,300)
        self.show()
    

    def combo1(self,year):                                              #일정 프로그램: 연도 콤보박스(2022년)
        tmp1 = str(year)
        tmp2 = tmp1 + self.input.text()[4:]                             #콤보로 변한 연도+그 외 날짜([2022]0615)
        self.input.setText(str(tmp2))
    def combo2(self,month):                                             #일정 프로그램: 월 콤보박스(6월)
        tmp1 = str(month)
        tmp2 = self.input.text()[:4] + tmp1 + self.input.text()[6:]     #연도 + 콤보로 변한 월 + 일(2022[06]15)
        self.input.setText(str(tmp2))
    def combo3(self,day):                                               #일정 프로그램: 일 콤보박스(15일)
        tmp1 = str(day)
        tmp2 = self.input.text()[:6] + tmp1                             #그 외 날짜+콤보로 변한 일(202206[15])
        self.input.setText(str(tmp2))

    def combo4(self,time1):                                                             #계획표 프로그램: 시작 시간 콤보박스(00시부터)
        tmp1 = str(time1)
        tmp2 = tmp1 + self.schedule_input.text()[2:]                                    #콤보로 변한 시작 시간+그 외 텍스트([00]시부터 01시까지)
        self.schedule_input.setText(str(tmp2))
    def combo5(self,time2):                                                             #계획표 프로그램: 종료 시간 콤보박스(01시까지)
        tmp1 = str(time2)
        tmp2 = self.schedule_input.text()[:6] + tmp1 + self.schedule_input.text()[8:]   #텍스트+콤보로 변한 종료 시간+텍스트(00시부터 [01]시까지)
        self.schedule_input.setText(str(tmp2))
    
    def UD_schedule(self):
        alarm_=self.input.text()                                                #20220615
        date_to_compare = datetime.strptime(alarm_, "%Y%m%d")                   #텍스트를 datetime값으로 변환
        if self.time >= date_to_compare:                                        #현재 시각과 일정 시간 차이 절대값 구하기
            date_diff_tmp = self.time - date_to_compare
            date_diff = str(date_diff_tmp)[:-7]                                 #datetime값을 글자화하여 인덱싱
        else:
            date_diff_tmp = date_to_compare - self.time
            date_diff = str(date_diff_tmp)[:-7]                                 #datetime값을 글자화하여 인덱싱
        if int(self.input.text()) > int(self.now):                              #일정 시간이 현재 시각보다 더 나중일 경우 실행
            with open('test.txt','a', encoding='utf8') as f:                    #test.txt 파일에 일정 이름 및 일정 시간 저장
                f.write(f'{date_to_compare}\n')
                f.write(f'{self.title.text()}\n')
            self.schedule.append(f'<b>{self.title.text()}까지 남은시간:</b>')   #일정 텍스트창에 일정이름 및 남은시간 업데이트
            self.schedule.append(f'<p style="color: red">{date_diff}</p>')
            self.schedule.append(f'<p style="font-size: 8px">ㅤ</p>')

        else:                                                                   #현재 시각이 일정 시간보다 더 나중일 경우 실행
            with open('test.txt','a', encoding='utf8') as f:                    #test.txt 파일에 일정 이름 및 일정 시간 저장
                f.write(f'{date_to_compare}\n')
                f.write(f'{self.title.text()}\n')
            self.schedule.append(f'<b>{self.title.text()} 후 지난시간:</b>')    #일정 텍스트창에 일정이름 및 지난시간 업데이트
            self.schedule.append(f'<p style="color: red">{date_diff}</p>')
            self.schedule.append(f'<p style="font-size: 8px">ㅤ</p>')

    def UD_timetable(self):
        timetable1 = self.schedule_input.text()                                                         #00시부터 01시까지
        timetable2 = self.schedule_title.text()                                                         #스케쥴명
        new_text_content = ''
        with open('test2.txt', 'r', encoding='utf-8') as f:                                             #test2.txt파일을 읽어오기
            lines = f.readlines()
            for first_number in range(0,24):
                for second_number in range(first_number+1,25):
                    if int(timetable1[:2]) == first_number and int(timetable1[6:8]) == second_number:   #([00](=first_number)시부터 [01](=second_number)시까지)일 경우 실행
                        for i, l in enumerate(lines):                                                   #i는 라인 위치(0부터 시작) l은 그 라인에 있는 텍스트
                            if i in range(first_number,second_number):                                  #i는 first_number부터 second_number-1의 범위일 때 실행
                                globals()['timetable_lineedit{}'.format(i)].setText(timetable2)         #계획표 프로그램에 스케쥴명을 업데이트
                                new_string = f'{l.strip()[:5]} {timetable2}'                            #새로운 스케쥴을 적는 코드
                            else:
                                new_string = l.strip()                                                  #i의 범위가 first_number부터 second_number-1이 아니면, 원본으로 가져오는 코드
                        
                            if new_string:
                                new_text_content += new_string+'\n'                                     #new_text_content에다가 각각의 new_string을 넣고 줄바꿈해주는 코드
        if int(timetable1[:2]) < int(timetable1[6:8]):                                                  #시작 시간이 종료 시간보다 이전일 경우([00]시~[01]까지)
            with open('test2.txt', 'w+', encoding='utf-8') as f:                                        #test2.txt 파일 업데이트
                f.write(new_text_content)
    
    def saveText(self, n):
        with open('test2.txt','r',encoding='utf-8') as file2:                               #LineEdit에 적은 스케쥴을 파일에 저장하는 함수
            new_text_content = ''
            tmp = globals()['timetable_lineedit{}'.format(n)].text()                        #tmp에 LineEdit에 적은 스케쥴을 받는 코드
            lines = file2.readlines()
            for i, l in enumerate(lines):                                                   #i는 라인 위치(0부터 시작) l은 그 라인에 있는 텍스트
                if i == n:
                    new_string = f'{l.strip()[:5]} {tmp}'                                   #새로운 스케쥴을 적는 코드
                else:
                    new_string = l.strip()                                                  #i의 범위가 first_number부터 second_number-1이 아니면, 원본으로 가져오는 코드
            
                if new_string:
                    new_text_content += new_string+'\n'                                     #new_text_content에다가 각각의 new_string을 넣고 줄바꿈해주는 코드
            
        with open('test2.txt', 'w', encoding='utf-8') as file2:
            file2.write(new_text_content)
        
    def clear_event_text(self):                                                                             #전체 삭제 버튼 누르면, 질문박스가 등장하는 함수
        buttonClick = QMessageBox.question(self, '전체 삭제 버튼', '정말 일정을 모두 삭제하시겠습니까?')
        if buttonClick == QMessageBox.Yes:                                                                  #Yes 누를 경우, clear_text 함수를 실행하는 코드
            self.clear_text()
        else:
            pass

    def clear_event_schedule(self):                                                                         #전체 삭제 버튼 누르면, 질문박스가 등장하는 함수
        buttonClick = QMessageBox.question(self, '전체 삭제 버튼', '정말 계획표를 모두 삭제하시겠습니까?')
        if buttonClick == QMessageBox.Yes:                                                                  #Yes 누를 경우, clear_schedule 함수를 실행하는 코드
            self.clear_schedule()
        else:
            pass

    def clear_text(self):
        self.schedule.clear()                                      #일정 전체 제거 함수
        with open('test.txt','w',encoding='utf-8') as f:
            f.write('')                                            #파일 내용 전체 제거
    
    def clear_schedule(self):
        for x in range(0,24):
            globals()['timetable_lineedit{}'.format(x)].setText('')             #계획표 내용 제거
        with open('test2.txt','w',encoding='utf8') as file2:                    #계획표 파일 기본 설정으로 초기화
            for time in range(0,24):
                if time < 10:
                    time = '0'+str(time)                                        #00,01,02,···,09
                time_plus = int(time) + 1
                if time_plus < 10:
                    time_plus = '0'+str(time_plus)                              #01,02,03,···,09
                file2.write(f'{time}:{time_plus}\n')                            #00:01\n 01:02\n ··· 23:24\n


if __name__=='__main__':
    app=QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./휴먼편지체.ttf')        #폰트 추가(컴퓨터 내에 있는 폰트만 가능)
    app.setFont(QFont('휴먼편지체'))                     #폰트 적용
    main=Main()
    sys.exit(app.exec_())
    