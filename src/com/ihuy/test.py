#-*- coding:utf-8 -*-
'''
Created on 2011-3-22

@author: 123
'''
import wx
import random

#Í¼Æ¬ÊôÐÔ·â×°
class ImageProperty():
    checked=False#±»Ñ¡ÖÐ×´Ì¬
    def __init__(self):
        randnum=-1
    def setrandnum(self,num):
        self.randnum=num
    def getrandnum(self):
        return self.randnum
    def setchecked(self,checked):
        self.checked=checked
    def getchecked(self):
        return self.checked
    #Ñ¡ÖÐ×´Ì¬×ª±ä
    def checkedshift(self):
        if self.checked:
           self.checked=False
        else:
           self.checked=True


class MyFrame(wx.Frame):
    gridwidth=10
    gridheight=10
    imagelist=[]#Í¼Æ¬¶ÔÏóÁÐ±í
    imageProlist=[]#Í¼Æ¬ÊôÐÔÁÐ±í£¬´ú±íÄÄÒ»¸öÍ¼Æ¬
    prevcheckedimageindex=-1#Ç°Ò»´ÎÑ¡ÖÐµÄÍ¼Æ¬
    checkedimageindex=-1#µ±Ç°Ñ¡ÖÐµÄÍ¼Æ¬
    panel=None
    def __init__(self):
            wx.Frame.__init__(self,None,-1,"My Frame",size=(540,600))
            self.panel=wx.Panel(self,-1)
            self.panel.Bind(wx.EVT_MOTION,self.OnMove)
            self.panel.Bind(wx.EVT_LEFT_DOWN,self.OnClickPanel)
            self.Bind(wx.EVT_PAINT,self.OnPaint)
            wx.StaticText(self.panel,-1,"mousePos:",pos=(10,534))
            self.posCtrl=wx.TextCtrl(self.panel,-1,"",pos=(80,530))
            fgs=wx.FlexGridSizer(cols=10,hgap=3,vgap=3)
            
            for col in range(self.gridwidth):
                for row in range(self.gridheight):
                    randnum=int(random.random()*5)
                    imagename='image'+str(randnum)+'.jpg'
                    img1=wx.Image(imagename,wx.BITMAP_TYPE_ANY)
                    img1=img1.Scale(50,50)#2 ËõÐ¡Í¼Ïñ
                    sb1=wx.StaticBitmap(self.panel,-1,wx.BitmapFromImage(img1))
                    sb1.Bind(wx.EVT_LEFT_DOWN,self.OnClickImage)
                    self.imagelist.append(sb1)
                    imageproperty=ImageProperty()
                    imageproperty.setrandnum(randnum)
                    self.imageProlist.append(imageproperty)
                    fgs.Add(sb1)
            self.panel.SetSizerAndFit(fgs)

            
            
    def OnMove(self,event):
        pass
        pos=event.GetPosition()
        self.posCtrl.SetValue("%s, %s"%(pos.x,pos.y))
    def OnClickPanel(self,event):
        pos=event.GetPosition()
        self.posCtrl.SetValue("%s, %s"%(pos.x,pos.y))
    
    #ÖÃ¿ÕÒ»¸öÎ»ÖÃ
    def setBlank(self,imageindex):
        #´¦Àíimagelist
        img1=wx.Image('image-1.jpg',wx.BITMAP_TYPE_ANY)
        img1=img1.Scale(50,50)#2 ËõÐ¡Í¼Ïñ
        self.imagelist[imageindex].SetBitmap(wx.BitmapFromImage(img1))
        self.imageProlist[imageindex].setrandnum(-1)#¿Õ°×Í¼Æ¬ÓÃ-1±íÊ¾        
    #ÉèÖÃalpha
    def setAlpha(self,imageindex):
        #´¦Àíimagelist
        imagename='image'+str(self.imageProlist[imageindex].getrandnum())+'.jpg'
        print 'imagename:',self.imageProlist[imageindex].getrandnum()
        img1=wx.Image(imagename,wx.BITMAP_TYPE_ANY)
        if self.imageProlist[imageindex].getchecked():
           img1=img1.Scale(45,45)#2 ËõÐ¡Í¼Ïñ
        else:
           img1=img1.Scale(50,50) 
        self.imagelist[imageindex].SetBitmap(wx.BitmapFromImage(img1))
        
    #µÃµ½Í¼Æ¬µÄx,y×ø±ê
    def getX_Y(self,imageindex):
        x=imageindex%self.gridwidth
        y=imageindex/self.gridwidth
        return [x,y]
    def getIndex(self,x,y):
        return y*self.gridwidth+x
    
    #µ¥ÏßÁ¬Í¨
    def linecheck(self,index0,index1):
        x_y0=self.getX_Y(index0)
        x_y1=self.getX_Y(index1)
        x0=x_y0[0]
        y0=x_y0[1]
        x1=x_y1[0]
        y1=x_y1[1]
        if x0==x1:#Í¬Ò»ÁÐÊÇ·ñÓÐÍ¨Â·
           if abs(y0-y1)==1:
               return True#ÏàÁÚ
           tempflag=True
           for i in range(min(y0,y1)+1,max(y0,y1),1):
               if self.imageProlist[self.getIndex(x0,i)].getrandnum()!=(-1):
                  tempflag=False
                  break #Í¬Ò»ÁÐ²»Í¨
           if tempflag:
               return True
        if y0==y1:#Í¬Ò»ÐÐÊÇ·ñÓÐÍ¨Â·  
            if abs(x0-x1)==1:
                return True#ÏàÁÚ
            tempflag=True
            for i in range(min(x0,x1)+1,max(x0,x1),1):
                if self.imageProlist[self.getIndex(i,y0)].getrandnum()!=(-1):
                    tempflag=False
                    break#Í¬Ò»ÐÐ²»Í¨
            if tempflag:
                return True     
        return False#Ã»ÓÐµ¥ÏßÁ¬Í¨
    
    #µ¥Ö±½ÇÁ¬Í¨£¬¼´ÓÐÁ½¸ùÏßÏà½»
    def secondlinecheck(self,index0,index1):
        x_y0=self.getX_Y(index0)
        x_y1=self.getX_Y(index1)
        x0=x_y0[0]
        y0=x_y0[1]
        x1=x_y1[0]
        y1=x_y1[1]
        #¼´ÅÐ¶Ï(x0,y1)ºÍÁ½µãµ¥ÏßÁ¬Í¨£¬»òÕß(x1,y0)ºÍÁ½µãµ¥ÏßÁ¬Í¨
        index01=self.getIndex(x0,y1)
        index10=self.getIndex(x1,y0)
        #ÕâÁ½µã±¾ÉíÒªÎª¿Õ     
        if self.linecheck(index01,index0)\
           and self.linecheck(index01,index1)\
           and self.imageProlist[index01].getrandnum()==(-1):
            return True
        if self.linecheck(index10,index0)\
           and self.linecheck(index10,index1)\
           and self.imageProlist[index10].getrandnum()==(-1):
            return True
        return False
        
    #Ë«Ö±½Ç£¬ÈýÏßÁ¬½Ó
    def trilinecheck(self,index0,index1):
        x_y0=self.getX_Y(index0)
        x0=x_y0[0]
        y0=x_y0[1]
        #ÔÚp1ÖÜÎ§Ñ°ÕÒÒ»¸ö¿Õ¸ñÓëp2µ¥Ö±½ÇÁ¬Í¨¼´¿É
        #ÏÈ¹Ì¶¨y0Ñ°ÕÒ¿Õ¸ñ£¬·Ç¿Õ¸ñÍ£Ö¹£¬Ô½½çÍ£Ö¹
        iter_x=x0-1#ÔÚ×ó±ßÑ°ÕÒ
        while iter_x>=0 and iter_x<self.gridwidth:
            if self.imageProlist[self.getIndex(iter_x,y0)].getrandnum()==(-1):
                #ÕâÊÇp0ÖÜÎ§¿Õ¸ñµÄµã
                if self.secondlinecheck(self.getIndex(iter_x,y0),index1):
                    return True
            else:
               #ÍË³öÕâ²ãÑ­»·
               break
            iter_x-=1 
        iter_x=x0+1#ÔÚÓÒ±ßÑ°ÕÒ
        while iter_x>=0 and iter_x<self.gridwidth:
            if self.imageProlist[self.getIndex(iter_x,y0)].getrandnum()==(-1):
                #ÕâÊÇp0ÖÜÎ§¿Õ¸ñµÄµã
                if self.secondlinecheck(self.getIndex(iter_x,y0),index1):
                    return True
            else:
               #ÍË³öÕâ²ãÑ­»·
               break
            iter_x+=1
        #ÏÈ¹Ì¶¨x0Ñ°ÕÒ¿Õ¸ñ£¬·Ç¿Õ¸ñÍ£Ö¹£¬Ô½½çÍ£Ö¹
        iter_y=y0-1#ÔÚÉÏ±ßÑ°ÕÒ
        while iter_y>=0 and iter_y<self.gridheight:
            if self.imageProlist[self.getIndex(x0,iter_y)].getrandnum()==(-1):
                #ÕâÊÇp0ÖÜÎ§¿Õ¸ñµÄµã
                if self.secondlinecheck(self.getIndex(x0,iter_y),index1):
                    return True
            else:
               #ÍË³öÕâ²ãÑ­»·
               break
            iter_y-=1
        iter_y=y0+1#ÔÚÏÂ±ßÑ°ÕÒ
        while iter_y>=0 and iter_y<self.gridheight:
            if self.imageProlist[self.getIndex(x0,iter_y)].getrandnum()==(-1):
                #ÕâÊÇp0ÖÜÎ§¿Õ¸ñµÄµã
                if self.secondlinecheck(self.getIndex(x0,iter_y),index1):
                    return True
            else:
               #ÍË³öÕâ²ãÑ­»·
               break
            iter_y+=1
        return False #¶¼²»Âú×ã
    
    
    #ÑéÖ¤Á½ÕÅÍ¼Æ¬ÊÇ·ñÏàÏû
    def verifyPair(self,index0,index1):
        #ÓÎÏ·Ëã·¨´¦:Á½´ÎÑ¡Í¬Ò»ÖÖ£¨ÇÒ²»ÊÇÒ»ÕÅ£©£¬Â·¾¶²»³¬¹ýÁ½¸öÍä
        
        if self.imageProlist[index0].getrandnum()\
           ==self.imageProlist[index1].getrandnum()and\
           index0!=index1:
           #ÊÇ·ñµ¥ÏßÁ¬Í¨
           if self.linecheck(index0,index1):
               print '1ÏßÁ¬Í¨'
               return True
           #ÊÇ·ñµ¥Ö±½ÇÁ¬Í¨
           if self.secondlinecheck(index0,index1):
               print '2ÏßÁ¬Í¨'
               return True
           #ÊÇ·ñ3ÏßÁ¬Í¨
           if self.trilinecheck(index0,index1):
               print '3ÏßÁ¬Í¨'
               return True
           
        else:
           return False
           
    def OnClickImage(self,event):
        #°Ñ³ýÑ¡ÖÐµÄÍ¼Æ¬»Ö¸´Õý³££¬Í»³öÑ¡ÖÐÍ¼Æ¬
        #ÖØÐÂÅÅÁÐÍ¼Æ¬
        self.checkedimageindex=self.imagelist.index(event.GetEventObject())
        
        checkedx_y=self.getX_Y(self.checkedimageindex)
        #print 'checkedx:',checkedx_y[0],'  y:',checkedx_y[1]
        #¼ì²éÊÇ·ñÁ¬Í¨Åä¶Ô
        if self.verifyPair(self.prevcheckedimageindex,self.checkedimageindex):
           self.setBlank(self.prevcheckedimageindex)
           self.setBlank(self.checkedimageindex)
        
        
        
        fgs0=wx.FlexGridSizer(cols=10,hgap=3,vgap=3)
        tempindex=0
        for sb in self.imagelist:
            #´¦Àíimagelist
            imagename='image'+str(self.imageProlist[tempindex].getrandnum())+'.jpg'
            img1=wx.Image(imagename,wx.BITMAP_TYPE_ANY)
            if tempindex==self.checkedimageindex:
               img1=img1.Scale(45,45)#2 ËõÐ¡Í¼Ïñ
            else:
               img1=img1.Scale(50,50) 
            self.imagelist[tempindex].SetBitmap(wx.BitmapFromImage(img1))
            fgs0.Add(sb)
            tempindex+=1
        self.panel.SetSizerAndFit(fgs0)
        del fgs0        
        
        #Ñ¡ÖÐ×´Ì¬×ª±ä
        self.imageProlist[self.checkedimageindex].checkedshift()
        self.prevcheckedimageindex=self.checkedimageindex 

    
        
    
    #ÖØ»æº¯Êý
    def OnPaint(self,evt):
        print 'ÖØ»æ'
        dc=wx.PaintDC(self)
        dc.Clear()
        self.PrepareDC(dc)
        
        for sb0 in self.imagelist:
            pass
        #self.panel.SetSizerAndFit(self.fgs)
        
        #Ìí¼ÓÍ¼Æ¬

#        
        
if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=MyFrame()
    frame.Show(True)
    app.MainLoop()