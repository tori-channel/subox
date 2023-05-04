import pyxel
import copy

class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.v=[0,-1]
        self.move_count=0
        self.move_x=0
        self.move_y=0
class Box:
    def __init__(self,x,y,w,h):
        #座標
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        #この箱は動くか、動かないか(←後で使う)
        self.move=0     
        

class Stage:
    def __init__(self,s,w,h):
        self.s=s
        self.w=w
        self.h=h
             
class App:
    #初期設定
    rows = 64

    tempdata=[['64,64', '0,0', '24,16,14,0', '8,8,3,0', '40,16,10,0', '32,16,4,0', '24,24,7,0'], ['64,64', '0,0', '24,16,14,0', '8,8,7,0', '8,16,11,0', '32,16,2,0', '24,24,5,0'], ['64,64', '0,0', '24,16,14,0', '8,8,5,0', '8,16,12,0', '32,16,3,0', '24,24,1,0', '8,24,5,0'], ['64,64', '0,0', '24,16,14,0', '8,8,1,0', '8,16,2,0', '32,16,13,0', '24,24,3,0', '8,24,4,0'], ['64,64', '0,0', '24,16,14,0', '8,8,2,0', '8,16,10,0', '32,16,4,0', '24,24,12,0', '8,24,3,0', '8,32,1,0', '8,40,4,0'], ['64,64', '0,0', '24,16,14,0', '8,8,2,0', '8,16,5,0', '32,16,11,0', '24,24,3,0', '8,24,12,0', '8,32,4,0', '8,40,1,0', '8,48,3,0'], ['64,64', '0,0', '24,16,14,0', '8,8,8,0', '8,16,13,0', '32,16,4,0', '24,24,10,0', '8,24,2,0', '8,32,12,0', '8,40,5,0', '8,48,1,0', '8,56,2,0'], ['64,64', '0,0', '24,16,14,0', '8,8,2,0', '8,16,15,0', '32,16,2,0', '24,24,10,0', '8,24,3,0', '8,32,15,0', '8,40,2,0', '8,48,1,0', '8,56,3,0'], ['64,64', '0,0', '24,16,14,0', '8,8,7,0', '8,16,15,0', '32,16,2,0', '24,24,11,0', '8,24,4,0', '8,32,15,0', '8,40,2,0', '8,48,3,0', '8,56,3,0'], ['64,64', '0,0', '24,16,14,0', '8,8,4,0', '8,16,15,0', '32,16,3,0', '24,24,6,0', '8,24,4,0'], ['64,64', '0,0', '24,16,14,0', '8,8,1,0', '8,16,6,0', '32,16,13,0', '24,24,4,0', '8,24,10,0', '8,32,3,0', '8,40,12,0', '8,48,5,0', '8,56,11,0', '16,8,7,0', '16,16,1,0', '16,24,2,0'], ['64,64', '0,0', '24,16,14,0', '8,8,2,0', '8,16,15,0', '32,16,3,0', '24,24,12,0', '8,24,3,0', '8,32,10,0', '8,40,5,0', '8,40,15,0', '8,48,2,0', '8,56,11,0', '16,8,1,0', '16,16,0,0', '16,24,3,0', '16,32,9,0'], ['64,64', '0,0', '24,16,14,0', '8,8,2,0', '8,16,15,0', '32,16,5,0', '24,24,12,0', '8,24,7,0', '8,32,10,0', '8,40,5,0', '8,48,15,0', '8,56,2,0', '16,8,11,0', '16,16,8,0', '16,24,15,0', '16,32,2,0', '16,40,10,0', '16,48,9,0', '16,56,15,0', '24,8,2,0', '24,16,11,0', '24,24,6,0', '24,32,15,0', '24,40,3,0', '24,48,5,0', '24,56,0,0']]
    stagesdata=[[] for _ in range(rows)]
    playerdata=[[] for _ in range(rows)]
    boxdata=[[]for _ in range(rows)]
    count = 0 
    for stages in tempdata:
            stages = [s.split(',') for s in stages]
            num = 0
            for data in stages:
                if num==0:
                    stagesdata[count].append(data[0])
                    stagesdata[count].append(data[1])
                elif num ==1:
                    playerdata[count].append(data[0])
                    playerdata[count].append(data[1])
                else:
                    boxdata[count].append(data[0])
                    boxdata[count].append(data[1])
                    boxdata[count].append(data[2])
                    boxdata[count].append(data[3])
                num += 1
            count += 1
    player =[]
    box=[]
    stage=[]
    
    def playeropen(self,n):
        return Player((128-int(self.stagesdata[n][0]))/2+int(self.playerdata[n][0]),
                      (128-int(self.stagesdata[n][1]))/2+int(self.playerdata[n][1]))
    def stageopen(self,n):
        return Stage(n,int(self.stagesdata[n][0]),int(self.stagesdata[n][1]))
    def boxopen(self,n):
        temp=[]
        i = (len(self.boxdata[n])) / 4
        for f in range(int(i)):
            temp.append(Box((128-int(self.stagesdata[n][0]))/2+int(self.boxdata[n][0+4*f]),(128-int(self.stagesdata[n][1]))/2+int(self.boxdata[n][1+f*4])
                       ,int(self.boxdata[n][2+f*4]),int(self.boxdata[n][3+f*4])))
        return temp

    history_player_stack=[]
    previous_move=None    
    position=[0,0]
    
    def __init__(self):
        pyxel.init(128,128,title="box")
        
        #pyxeleditorで作成した画像を読み込む
        #box.pyxelはbox.pyと同じ場所に用意してね
        pyxel.load('numbers.pyxres')
        self.clear=0
        self.stagenumber=0
        self.select=False
        self.mapY=0
        self.mapY2=0
        self.elapsed_time = 0
        self.iscleard=False
        self.sound_box=False
        self.speed=1
        self.start=True
        self.back=False
        self.end=False
        
        self.player = self.playeropen(self.stagenumber)
        self.stage = self.stageopen(self.stagenumber)
        self.box =(self.boxopen(self.stagenumber))
        
        pyxel.run(self.update,self.draw)
                    
    def update(self):
        pyxel.mouse(self.select)
    
        if(self.start==True)or(self.back==True)or(self.end==True):
            return
        
        if self.clear>0:
            if pyxel.btn(pyxel.KEY_SPACE):
                self.nextstage()
            return
        if pyxel.btn(pyxel.KEY_R):
            self.restart()
        if pyxel.btn(pyxel.KEY_X)and self.select==False:
            pyxel.play(0,5)
            self.select = True
            
        if self.select==True:
            if pyxel.btn(pyxel.KEY_Z):
                self.select = False
            return
        self.tilemapLopping()
        #それぞれ十字キーの各方向を押したらmove関数を呼び出す
        if pyxel.btn(pyxel.KEY_W):
            self.move(0,-1)
        elif pyxel.btn(pyxel.KEY_S):
            self.move(0,1)
        elif pyxel.btn(pyxel.KEY_D):
            self.move(1,0)
        elif pyxel.btn(pyxel.KEY_A):
            self.move(-1,0)
        
        if self.player.move_count>0:
            if self.player.move_count==8/self.speed:
                pyxel.play(0, 2,loop=False)             
            self.player.move_count-=1
            self.player.x+=self.player.move_x*self.speed
            self.player.y+=self.player.move_y*self.speed
            if len(self.box) < 2:
                return
            for box in self.box:
                list1=self.boxobserver(box)
                list1.insert(0,box.w)
                #print(list1)
                if len(list1)==len(self.box):
                    self.checklist(list1)
                if box.move:
                    pyxel.play(0, 0,loop=False)
                        
                    box.x+=self.player.move_x*self.speed
                    box.y+=self.player.move_y*self.speed  
            
    def draw(self):
        pyxel.cls(7)
        if(self.start==True):
            pyxel.bltm(0,0,0,0,128,128,128)
            pyxel.bltm(0,0,3,0,0,128,40)
            self.titleselect()
            return
        self.backtitle()
        if(self.back==True):
            return
        if(self.end==True):
            pyxel.text(40,30,"You Are Great!",12)
            pyxel.text(40,50,"Please End this Game!",12)
            return
        #タイルマップを貼り付ける
        pyxel.bltm(0,0,2,0,0,128,128,0)
        pyxel.bltm((128-self.stage.w)/2,(128-self.stage.h)/2,0,0,0,self.stage.w,self.stage.h)
        pyxel.bltm(0,self.mapY,1,0,0,128,128,0)
        pyxel.bltm(0,self.mapY2+64,1,0,0,128,128,0)
        
        pyxel.blt(self.player.x,self.player.y,0,8*self.player.v[0],32,
                  8*self.player.v[1],8*self.player.v[1],0)
        for box in self.box:
            pyxel.blt(box.x,box.y,0,box.w*8,box.h*8,8,8,0)
            
        self.death()
        self.clearMessage()
        self.stageUI()
        if self.select==True:
            self.stageselect()
            if pyxel.btn(pyxel.KEY_D):
                self.select = False
            return
    def move(self,x,y):
        if self.player.move_count == 0:
            self.player.move_count = 8/self.speed
            self.player.move_x=x
            self.player.move_y=y
            #↓この命令は前回に書いたものなので注意してね
            self.player.v=[abs(x),(x+y)]
            #壁を検知
            if ((pyxel.tilemap(2).pget(self.player.x/8+self.player.move_x,self.player.y/8+self.player.move_y)==(0,6))):
                self.player.move_count=0
                pyxel.play(0,4)
                return
            
        for box in self.box:
                #進行方向に箱があればクラス変数moveをTrueにする
                if (self.player.x+self.player.move_x*8==box.x) and (self.player.y+self.player.move_y*8==box.y):
                    box.move=self.speed
                    #箱が動かないものならbreak
                    if(box.h!=0):
                        box.move=0
                        self.player.move_count=0
                        return
                
                    for box_2 in self.box:
                           #プレイヤーが押そうとした箱の移動方向に箱がある、もしくはプレイヤーが押そうとした箱の移動方向に壁がある(タイルマップからデータを取得して判断)なら箱もプレイヤーも移動しない
                            if (box.x+self.player.move_x*8==box_2.x) and (box.y+self.player.move_y*8==box_2.y):
                                box.move=0
                                self.player.move_count=0
                                return
                #箱を押していない時
                else:
                    box.move=0
        self.previous_move = (self.player.x,self.player.y ) 
        new_position = [self.position[0] + x, self.position[1] + y]
        self.history_player_stack.append((copy.deepcopy(self.position), self.previous_move)) # 現在の位置と1手前の操作を保存する
        self.position = new_position    
        
    def death(self):
        self.deathflag=0
        if (self.deathflag>0):
            pyxel.rect(12,32,36,5,15)
            pyxel.text(16,32,"Restart",pyxel.frame_count % 16)  
    def stageUI(self):
        pyxel.text(90,120,"Stage:{}".format(self.stagenumber+1),2)

                             
    def boxobserver(self,boxes):
        observe=[]
        for box in self.box:
           if ((boxes.x+8==box.x) and (boxes.y==box.y))or((boxes.x==box.x) and (boxes.y+8==box.y)): 
               observe.append(box.w)
               break
        if(observe==[]):
            return[]
        observe.extend(self.boxobserver(box))
        return observe
               
    def clearMessage(self):
        if(self.clear > 0):
            if not self.iscleard:
                pyxel.play(1,1)
            pyxel.rect(0,60,128,8,15)
            pyxel.text(40,62,"GAME CLEAR!",pyxel.frame_count % 16)
            self.iscleard = True
            
    def checklist(self,list):
        if(list[0]>=10):
            return
        list.reverse()
        answer=list.pop(0)
        i=0
        while(list[0]<10 and i<1):
            answer=answer+10*list.pop(0)
            i+=1
        equal =list.pop(0)
        if(equal==14):
            if(answer==self.comprehensivecul(list)):
                        self.clear=1
                        return
            else:
                return
            
    def tilemapLopping(self):
        self.elapsed_time += 1
        if self.elapsed_time % 3 ==0:
            self.mapY=-self.elapsed_time/3
        if self.elapsed_time % 4 ==0:
            self.mapY2=-self.elapsed_time/3
        if self.elapsed_time>64*3:
            self.elapsed_time=0
            
    def restart(self):
        self.clear=0
        self.elapsed_time = 0
        self.iscleard=False
        self.sound_box=False
        
        self.player=self.playeropen(self.stagenumber)
        self.stage = self.stageopen(self.stagenumber)
        self.box =(self.boxopen(self.stagenumber))
    
    def nextstage(self):
        self.clear=0
        self.elapsed_time = 0
        self.iscleard=False
        self.sound_box=False
        self.stagenumber+=1
        if(self.stagenumber>=13):
            self.end=True
            
        self.player=self.playeropen(self.stagenumber)
        self.stage = self.stageopen(self.stagenumber)
        self.box =(self.boxopen(self.stagenumber))
      
    def undo(self):
        if len(self.history_player_stack) >= 10: # 現在の履歴が10手以上ある場合
            for i in range(10): # 10手分の操作を戻す
                self.previous_position, self.previous_move = self.history_player_stack.pop()
                self.position = self.previous_position # 最後に戻った位置を現在の位置とする
        else: # 履歴が10手未満の場合は全ての操作を取り消す
            for i in range(len(self.history_player_stack)):
                self.previous_position, self.previous_move = self.history_stack.pop()
        self.position = self.previous_position # 最初の位置に戻す           

    def stageselect(self):
        self.select=True
        pyxel.bltm(0,0,1,128,128,128,128)
        pyxel.rect(0,28,128,10,15)
        pyxel.text(40,30,"STAGE SELECT",12)
        i=0
        for i  in range(13):
            pyxel.blt(8+8*i,60,0,8+8*i,16,8,8,0)
            if 8*i+8 <= pyxel.mouse_x < 8*i + 16 and \
               56 <= pyxel.mouse_y < 64:
                   pyxel.rectb(8*i+8,60,8,8,3)
                   if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                       pyxel.play(1, 1)
                       self.stagenumber=i
                       self.restart()
                       self.select=False
                       
    def titleselect(self):
        self.select=True
        pyxel.rect(0,46,128,14,8)
        pyxel.rect(2,48,124,10,7)
        pyxel.text(40,50,"New Game",12)
        pyxel.rect(0,68,128,10,7)
        pyxel.text(40,70,"Stage Select",12)
        pyxel.rect(0,88,128,10,7)
        pyxel.text(40,90,"Quit",12)
        txt=["New Game","Stage Select","Quit"]
        i=0
        for i  in range(3):
            if 20*i+48 <= pyxel.mouse_y < 20*i+48+10 and \
               40 <= pyxel.mouse_x < 60:
                   pyxel.text(40,20*i+50,txt[i],0)
                   if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                       if(i==0):
                           pyxel.play(1, 1)
                           self.stagenumber=i
                           self.start=False
                           self.restart()
                           self.select=False
                       elif(i==1):
                           self.start=False
                           self.select=True
                       elif(i==2):
                           pyxel.quit()
                           
    def backtitle(self):
        if(pyxel.btn(pyxel.KEY_1)):
            self.back=True
        if(self.back==True):
            self.select=True
            pyxel.rect(0,28,128,10,15)
            pyxel.text(40,30,"Back to Title",12)
            pyxel.rect(0,48,128,10,15)
            pyxel.text(40,50,"Yes",12)
            pyxel.rect(0,68,128,10,15)
            pyxel.text(40,70,"No",12)
            txt=["Back to Title","Yes","No"]
            i=0
            for i  in range(3):
                if 20*i+28 <= pyxel.mouse_y < 20*i+28+15 and \
                   40 <= pyxel.mouse_x < 60:
                       pyxel.text(40,20*i+30,txt[i],0)
                       if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                           if(i==1):
                               self.start=True
                               self.select=False
                               self.back=False
                               self.end=False
                           elif(i==2):
                               self.select=False
                               self.back=False
    def secondsort(self,expr):
        index=0
        exp=[]
        while(index!=len(expr)):
            if index<len(expr)-1:    
                if (0<=expr[index]<10) and (0<=expr[index+1] < 10):
                    exp.append(expr[index]+expr[index+1]*10)
                    index+=1
                else:
                    exp.append(expr[index])
            else:
                exp.append(expr[index])
            index+=1
        return exp
    def calreverese(self,expr):
        for index,item in enumerate(expr):
            if expr[index]>=10:
                expr[index]=-item
        return expr
    def multiplication(self,expr):
        index=0
        exp=[]
        while(index!=len(expr)):
            if index<len(expr)-1:    
                if (expr[index+1]==-15):
                    exp.append(expr[index+2]**expr[index])
                    index+=2
                else:
                    exp.append(expr[index])
            else:
                exp.append(expr[index])
            index+=1
        return exp
    def muldiv(self,expr):
        index=0
        exp=[]
        while(index!=len(expr)):
            if index<len(expr)-1:    
                if (expr[index+1]==-12):
                    exp.append(expr[index]*expr[index+2])
                    index+=2
                elif(expr[index+1]==-13):
                    exp.append(int(expr[index+2]/expr[index]))
                    index+=2
                else:
                    exp.append(expr[index])
            else:
                exp.append(expr[index])
            index+=1
        return exp
    def addsub(self,expr):
        index=0
        exp=expr[0]
        while(index!=len(expr)):
            if index<len(expr)-1:
                if (expr[index+1]==-10):
                    exp=exp+expr[index+2]
                    index+=1
                elif(expr[index+1]==-11):
                    exp=-exp+expr[index+2]
                    index+=1
                else:
                    if (expr[index-1]==-10):
                        exp=exp+expr[index]
                    elif(expr[index-1]==-11):
                        exp=-exp+expr[index]
            index+=1
        return exp
    def comprehensivecul(self,expr):
        expr=self.calreverese(expr)
        expr=self.secondsort(expr)
        expr=self.multiplication(expr)
        expr=self.muldiv(expr)
        expr=self.addsub(expr)
        return(expr)
    

App()