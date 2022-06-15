from socket import *
serverPort = 1000
# 为代理服务器 创建一个套接字、绑定端口号、设置服务器最大连接客户机数量为3(因为是多线程)
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(3)


while True:
     #准备接收响应
     print('Ready to receive')
     connectionSocket, address = serverSocket.accept()
     print('Address:',address)     
     sentence = connectionSocket.recv(1024).decode('utf-8')

     #提取请求 
     client_request = []
     client_request = sentence.split(' ')
     data = client_request[0]
     requested_file = client_request[1]     #请求文件 
     #打印请求
     print('Client request',requested_file)


     try:
        if(data=='tes.html'): 
            response = ''
            redirect = ''
            response = response.encode()
            header = 'HTTP/1.1 301 Moved Permanently\r\n'   
            
            if(data.endswith(".jpg")):  #若接收图片        
                mimetype = 'image/jpg'
            elif(data.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'
            
            
            header += 'Type: '+str(mimetype)+'\r\n'
            
            
            redirect = 'Location: http://localhost:'+str(serverPort) + '/test.html\r\n\r\n' 
            #print(header)
            header = header + redirect
            
            print(header)
        else:
            file = open(data,'rb') # 以二进制模式读取字节格式打开文件 
            response = file.read()
            file.close()
        
            header = 'HTTP/1.1 200 OK\n'       #响应 200

         


            if(data.endswith(".jpg")):         #图片 
                mimetype = 'image/jpg'
            elif(data.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'
    
            header += 'Type: '+str(mimetype)+'\n\n'
     except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
     final = header.encode('utf-8')
     final += response
     #print(final.decode('utf-8'))
     connectionSocket.send(final)
     connectionSocket.close()