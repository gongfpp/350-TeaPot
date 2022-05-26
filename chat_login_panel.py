from tkinter import *  # 导入模块，用户创建GUI界面
import face_recognition
import cv2
from pymysql import NULL
from sqlalchemy import null
import chat_mysql
from main import handding_faceing
import time

# 登陆界面类


class LoginPanel:

    # 构造方法，参数为按钮事件处理函数，从客户端main传进来，可以实现按钮回调
    def __init__(self, handle_login, handle_register, close_login_window,handding_faceing):
        # 初始化参数实例变量
        self.handle_login = handle_login
        self.handle_register = handle_register
        self.close_login_window = close_login_window
        self.handding_faceing=handding_faceing

    # 显示登录界面的实例方法
    def show_login_panel(self):
        # 声明全局变量方便，在静态函数重调用
        global login_frame
        global frames
        global imgLabel
        global numIdx

        self.login_frame = Tk()  # 创建主窗口
        # 设置背景颜色
        self.login_frame.configure(background="white")
        login_frame = self.login_frame  # 绑定全局变量

        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        self.login_frame.protocol("WM_DELETE_WINDOW", self.close_login_window)

        # 得到屏幕宽度，高度
        screen_width = self.login_frame.winfo_screenwidth()
        screen_height = self.login_frame.winfo_screenheight()
        # 声明宽度，高度变量
        width = 503
        height = 400
        # 设置窗口在屏幕局中变量
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        self.login_frame.geometry(gm_str)  # 设置窗口局中
        self.login_frame.title("登录")   # 设置窗口标题
        # 设置窗口不能改变大小
        self.login_frame.resizable(width=False, height=False)

        numIdx = 3  # gif的帧数
        # 循环遍历动图的帧
        frames = [PhotoImage(file='pictures/login.gif',
                             format='gif -index %i' % (i)) for i in range(numIdx)]
        # # 创建存放gif的标签
        imgLabel = Label(self.login_frame, height=400, width=500)
        # # 设置标签的位置
        imgLabel.place(x=-252, y=-200, relx=0.5,
                       rely=0.5, relwidth=1, relheigh=0.5)

        # 设置文本标签和位置
        Label(login_frame, text="昵称：", font=("宋体", 12), bg="white", fg="black") \
            .place(x=110, y=230)
        Label(login_frame, text="密码：", font=("宋体", 12), bg="white", fg="black") \
            .place(x=110, y=260)

        # 声明用户名密码变量
        self.user_name = StringVar()
        self.password = StringVar()

        # 设置输入框及位置
        self.entry1 = Entry(
            login_frame,  textvariable=self.user_name, fg="black", width=25)
        self.entry1.place(x=180, y=230)
        self.entry2 = Entry(
            login_frame, textvariable=self.password, show='*', fg="black", width=25)
        self.entry2.place(x=180, y=260)

        # 设置注册按钮及位置，按钮事件为handle_register函数
        self.button_register = Button(login_frame, text="注册账号", relief=RAISED, bg='white', fg='green',
                             font=('黑体', 15), command=self.handle_register).place(x=5, y=360)

        self.login_frame.bind('<Return>', self.handle_login)  # 绑定回车键
        # 设置登录按钮及位置，按钮事件为handle_login函数
        self.button_login = Button(login_frame, text="登录", bg="#00BFFF", fg="white", width=21, height=2,
                                font=('黑体', 15), command=lambda: self.handle_login(self))
        self.button_login.place(x=160, y=300)
        # 设置人脸识别登录按钮
        self.button_facereg = Button(login_frame, text="人脸识别", relief=RAISED, bg='white', fg='brown',
                             font=('黑体', 15),command=self.handding_faceing).place(x=405, y=360)

    # 定时器函数，用于刷新gif的帧
    @staticmethod
    def update(idx):
        frame = frames[idx]
        idx += 1  # 下一张的序号
        imgLabel.configure(image=frame)
        login_frame.after(300, LoginPanel.update, idx %
                          numIdx)  # 200毫秒之后继续执行定时器函数

    # 调用定时器函数，执行循环mainloop显示界面实例方法
    def load(self):
        LoginPanel.update(0)
        self.login_frame.mainloop()

    # 关闭登录界面实例方法
    def close_login_panel(self):
        if self.login_frame == None:
            print("未显示界面")
        else:
            # 关闭登录界面
            self.login_frame.destroy()

    # 获取输入的用户名密码实例方法
    def get_input(self):
        return self.user_name.get(), self.password.get()

    def showface(self):
        #开启摄像头
        video_capture = cv2.VideoCapture(0)
        #获取用户名
        u_n=self.user_name.get()
        flag=0
        if u_n == "":
          return flag
        password1=chat_mysql.LogInformation.down_reco(u_n)
        time.sleep(2)
        # 本地图像
        user_image = face_recognition.load_image_file("faceReco/识别人脸.png")
        user_face_encoding = face_recognition.face_encodings(user_image)[0]
        # 脸部特征数据的集合
        known_face_encodings = [user_face_encoding]
        # 人物名称的集合
        known_face_names = ["%s"%u_n]
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        while True:
          # 读取摄像头画面
          ret, frame = video_capture.read()

          # 改变摄像头图像的大小，图像小，所做的计算就少
          small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
  
          # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
          rgb_small_frame = small_frame[:, :, ::-1]
  
          # Only process every other frame of video to save time
          if process_this_frame:
            # 根据encoding来判断是不是同一个人，是就输出true，不是为flase
              face_locations = face_recognition.face_locations(rgb_small_frame)
              face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
  
              face_names = []
              for face_encoding in face_encodings:
                  # 默认为unknown
                  matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                  name = "Unknown"
  
                  # if match[0]:
                  #     name = "michong"
                  # If a match was found in known_face_encodings, just use the first one.
                  if True in matches:
                      first_match_index = matches.index(True)
                      name = known_face_names[first_match_index]
                      flag=1
                  face_names.append(name)
  
          process_this_frame = not process_this_frame
  
          # 将捕捉到的人脸显示出来
          for (top, right, bottom, left), name in zip(face_locations, face_names):
              # Scale back up face locations since the frame we detected in was scaled to 1/4 size
              top *= 4
              right *= 4
              bottom *= 4
              left *= 4
  
              # 矩形框
              cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
  
              #加上标签
              cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
              font = cv2.FONT_HERSHEY_DUPLEX
              cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
  
          # Display
          cv2.imshow('monitor', frame)
  
          # 按Q退出
          if cv2.waitKey(1) & 0xFF == ord('q'):
              break

        video_capture.release()
        cv2.destroyAllWindows()
        return flag,password1

        
