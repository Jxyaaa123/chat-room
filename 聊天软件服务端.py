from asyncio import start_server
from threading import main_thread
import wx
import threading
import socket
from socket import socket,AF_INET,SOCK_STREAM

class jxyserver(wx.Frame):
    def __init__(
        self,
        server_name: str = "姜轩宇",
        id: int = 1002,
        title: str = "服务器端",
        pos=wx.DefaultPosition,
        size=(400, 450),
    ):
        # 正确初始化 wx.Frame
        super().__init__(None, id=id, title=f"{server_name}{title}", pos=pos, size=size)

        # 面板与布局
        pl = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # 顶部按钮条：启动服务 / 保存聊天记录 / 停止服务
        btn_row = wx.BoxSizer(wx.HORIZONTAL)
        start_btn = wx.Button(pl, label="启动服务")
        save_btn = wx.Button(pl, label="保存聊天记录")
        stop_btn = wx.Button(pl, label="停止服务")
        btn_row.Add(start_btn, 0, wx.ALL, 5)
        btn_row.Add(save_btn, 0, wx.ALL, 5)
        btn_row.Add(stop_btn, 0, wx.ALL, 5)
        box.Add(btn_row, 0, wx.EXPAND)

        # 服务器日志（先做展示用，后续再接 socket）
        self.log_text = wx.TextCtrl(
            pl,
            style=wx.TE_MULTILINE | wx.TE_READONLY,
        )
        box.Add(self.log_text, 1, wx.EXPAND | wx.ALL, 5)

        pl.SetSizer(box)

        # 服务器状态与 socket 初始化（用于“启动服务/停止服务”按钮）
        self.isOn = False  # 存储服务器的启动状态
        self.host_port = ("", 8888)  # '' 表示本机所有 IP
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(self.host_port)
        self.server_socket.listen(5)
        #创建一个字典存储与客户端的会话线程
        self.session_thread_dict={}
        
        
        #当你鼠标点击启动服务按钮时要执行的操作
        self.Bind(wx.EVT_BUTTON,self.start_server,start_btn)
    def start_server(self,event):
        #判断服务器启动没 
        if not self.isOn:
            self.isOn=True
            #创建主线程
            main_thread=threading.Thread(target=self.do_work)
            #设置为守护线程，父线程执行结束子线程也跟着关闭
            main_thread.daemon=True
            
            main_thread.start()
    def do_work(self):
        while self.isOn:
            #接收客户端的连接请求
            sesion_socket,client_addr=self.server_socket.accept()
            #客户端发送请求之后第一条为客户端的名称作为字典中的key
            user_name=sesion_socket.recv(1024).decode('utf-8')
            #创建一个会话进程对象
            sesstion_thread=SesstionThread(sesion_socket,user_name,self)
            #存储到字典之中
            self.session_thread_dict[user_name]=sesstion_thread
            sesstion_thread.start()
        self.server_socket.close()        
               
    def log(self, msg: str) -> None:
        """向界面追加日志。"""
        self.log_text.AppendText(msg + "\n")
#服务器会话线程的类        
class SesstionThread(threading.Thread):
    def __init__(self,client_socket,user_name,server):
        threading.Thread.__init__(self)
        self.client_socket=client_socket
        self.user_name=user_name
        self.server=server
        self.isOn=True
        
    def run(self)->None:
        print(f'客户端：{self.user_name}已经和服务器连接成功')
        while self.isOn:
            data=self.client_socket.recv(1024).decode('utf-8')
            #如果客户端点击的是断开按钮
            if data=='J-disconnect-xy':
                self.isOn = False
            else:
                pass
        self.client_socket.close()#关闭socket      

if __name__ == "__main__":
    app = wx.App()
    client = jxyserver()
    client.Show()
    app.MainLoop()