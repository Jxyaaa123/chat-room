#coding:utf-8
import threading
import wx
from socket import socket,AF_INET,SOCK_STREAM
class jxyclient(wx.Frame):
    def __init__(self,client_name):
        wx.Frame.__init__(self,None,id=1001,title=client_name+'的客户端界面',pos=wx.DefaultPosition,size=(400,450))
        pl=wx.Panel(self)#创建面板对象
        #在面板中放入盒子
        box=wx.BoxSizer(wx.VERTICAL)#垂直方向布局
        fgz1=wx.FlexGridSizer(1,2,0,0)#水平方向布局
        #创建两个按钮
        conn_btn=wx.Button(pl,size=(200,40),label='连接')
        dix_conn_btn=wx.Button(pl,size=(200,40),label='断开')
        
        #把两个按钮放入布局中
        fgz1.Add(conn_btn,1,wx.TOP|wx.LEFT)
        fgz1.Add(dix_conn_btn,1,wx.TOP|wx.RIGHT)
        #添加到box中
        box.Add(fgz1,1,wx.ALIGN_CENTER)
        #只读文本框
        self.show_text=wx.TextCtrl(pl,size=(400,210),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.show_text,1,wx.EXPAND)
        #创建聊天内容文本框
        self.chat_text=wx.TextCtrl(pl,size=(400,120),style=wx.TE_MULTILINE)
        box.Add(self.chat_text,1,wx.EXPAND)
        fgz2=wx.FlexGridSizer(1,2,0,0)
        reset_btn=wx.Button(pl,size=(200,40),label='重置 ')
        send_btn=wx.Button(pl,size=(200,40),label='发送')
        fgz2.Add(reset_btn,1,wx.TOP|wx.LEFT)
        fgz2.Add(send_btn,1,wx.TOP|wx.RIGHT)
        box.Add(fgz2,1,wx.ALIGN_CENTER)
        # 将盒子放入面版中
        pl.SetSizer(box)
        
        #以上都是绘制界面的代码------------------------------------------------
        self.Bind(wx.EVT_BUTTON,self.connect_to_server,conn_btn)
        self.client_name=client_name
        self.isconnect=False
        self.client_socket=None#设置客户端的socket对象为空
        self.Bind(wx.EVT_BUTTON,self.send_to_server,send_btn)
        self.Bind(wx.EVT_BUTTON,self.dix_conn_server,dix_conn_btn)
        if self.isconnect:
            input_data=self.chat_text.GetValue()
            if input_data!='':
                self.client_socket.send(input_data.encode('utf-8'))
                self.chat_text.SetValue('')#清空了
    def connect_to_server(self,event):
       print(f'客户端{self.client_name}连接服务器成功')
       if not self.isconnect:
           server_host_port=('127.0.0.1',8888)
           # socket 已在开头用 from socket import socket 导入，因此这里直接调用 socket(...) 即可
           self.client_socket=socket(AF_INET,SOCK_STREAM)    
           self.client_socket.connect(server_host_port)
           #只要连接成功立刻发送一条数据
           self.client_socket.send(self.client_name.encode('utf-8'))
           # 启动一个线程与服务器线程进行通信
           client_thread=threading.Thread(target=self.recv_data)
           #设置成守护线程
           client_thread.daemon=True
           self.isconnect=True
           client_thread.start()
    def recv_data(self):
        while self.isconnect:
            data=self.client_socket.recv(1024).decode('utf-8')
            #显示到只读文本框
            self.show_text.AppendText('-'*40+'\n'+data+'\n')
                  
           
           
                
if __name__=='__main__':
    app=wx.App()
    name=input('请输入客户端名称')
    client=jxyclient(name)
    client.Show()
    #循环刷新
    app.MainLoop()        