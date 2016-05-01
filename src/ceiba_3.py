# encoding: utf-8
from __future__ import print_function
__all__ =['OpenWeb']
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import urllib
import getpass
import sys
import os 
reload(sys)
sys.setdefaultencoding('UTF8')
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class OpenWeb:
   def __init__(self, driver=None):
      if driver==None:
         driver=webdriver.PhantomJS("/home/chto/node_modules/phantomjs/lib/phantom/bin/phantomjs")
      self.driver=driver
      self.driver.implicitly_wait(3)
      ##Private##
      self._nameList={}
#      self._fileList={}
   def execute(self):
      self.loginCeiba()
      self.getContent()
      while True:
         className=raw_input("Enter className: ") or "電磁學上"
         if not self.goToClass(className.decode("utf-8")):
            self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL+'w')
            continue
         while True:
            frameName=raw_input("Enter FrameName: ") or "syllabus"
            if self.goToframe(frameName):
               break
         if frameName==r"syllabus":
            self.Save(className,frameName)
         if frameName==r"hw":
            self.SaveHW(className,frameName)
         if frameName==r"bulletin":
            self.SaveBu(className,frameName)
         self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')
         finish=raw_input("finish? ") or "F"
         if finish=="t":
            break

   def loginCeiba(self):
      url = "https://ceiba.ntu.edu.tw/"
      self.driver.get(url)
      login_form = self.driver.find_element_by_name('login2')
      newPage=login_form.find_element_by_class_name('btn').click()
      username = self.driver.find_element_by_name("user")
      password = self.driver.find_element_by_name("pass")
      user=raw_input("Enter your userName: ") or "b00202047"
      passwd=getpass.getpass("Enter your password: ")
      username.send_keys(user)
      password.send_keys(passwd)
      self.driver.find_element_by_name('Submit').click() 
   def getContent(self):
      links = self.driver.find_elements_by_xpath("//*[@href]")
      self._nameList={}
      for link in links:
         if "mailto" in link.get_attribute("href"):
            continue
         if "https://ceiba.ntu.edu.tw/student/"in link.get_attribute("href"):
            continue
         self._nameList[link.text]=link.get_attribute("href")
   def printList(self):
      for key in self._nameList.keys():
         print(key)

   def goToClass(self,className):
      self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
      try:
         self.driver.get(self._nameList[className])
      except:
         eprint("%s is not in the list\n Pleas use printList to see available one\n"%className)
         self.printList()
         return False
      self.driver.switch_to.frame(self.driver.find_element_by_name("Main"))
      return True
   def goToframe(self,frameName):
      try:
         self.driver.switch_to.frame(self.driver.find_element_by_name("leftFrame"))
      except:
         None
      try:
         link=self.driver.find_element_by_id(frameName)
      except:
         eprint("%s is not OK"%frameName)
         return False
      link.click()
      self.driver.switch_to.frame(self.driver.find_element_by_name("mainFrame"))
      return True
   def getLink(self,hashTable):
      links = self.driver.find_elements_by_xpath("//*[@href]")
      for link in links:
         if link.text==u'':
            continue
         hashTable[link.text]=link.get_attribute("href")
      
   def Save(self, className,frameName):
      _fileList={}
      self.getLink(_fileList)
      dirName="./Ceiba_Crawler/test/%s/"%(className.replace('/', '_'))
      if not os.path.isdir(dirName.decode("utf8")):
         os.mkdir(dirName.decode("utf8"))
      dirName="./Ceiba_Crawler/test/%s/%s/"%(className.replace('/','_'),frameName.replace('/','_'))
      if not os.path.isdir(dirName.decode("utf8")):
         os.mkdir(dirName.decode("utf8"))
      for key in _fileList.keys():
         urllib.urlretrieve(_fileList[key],(dirName+key.replace('/','_')).decode("utf8"))
         print("\r downloading %s ."%(_fileList[key]),end="")
         sys.stdout.flush()
      print("\n")
   def SaveHW(self, className,frameName):
      dirName="./Ceiba_Crawler/test/%s/"%(className.replace('/', '_'))
      if not os.path.isdir(dirName.decode("utf8")):
         os.mkdir(dirName.decode("utf8"))
      dirName="./Ceiba_Crawler/test/%s/%s/"%(className.replace('/', '_'),frameName.replace('/', '_'))
      if not os.path.isdir(dirName.decode("utf8")):
         os.mkdir(dirName.decode("utf8"))
      self.SaveTwoLayerFile(dirName)
   def SaveTwoLayerFile(self,DirName):
      _fileList={}
      self.getLink(_fileList)
      for key in _fileList.keys():
         self.driver.get(_fileList[key])
         tempTable={}
         self.getLink(tempTable)
         newDirName=DirName+key.replace('/', '_')+"/"
         if tempTable=={}:
            continue
         if not os.path.isdir(newDirName.decode("utf8")):
            os.mkdir(newDirName.decode("utf8"))
         for key2 in tempTable.keys():
            urllib.urlretrieve(tempTable[key2],(newDirName+key2.replace('/', '_')).decode("utf8"))
            print("\r downloading %s ."%(tempTable[key2]),end="")
            sys.stdout.flush()
         print("\n")
      print("\n")

   def SaveBu(self, className,frameName):
      dirName="./Ceiba_Crawler/test/%s/"%(className.replace('/', '_'))
      if not os.path.isdir(dirName.decode("utf8")):
         os.mkdir(dirName.decode("utf8"))
      dirName="./Ceiba_Crawler/test/%s/%s/"%(className.replace('/', '_'),frameName.replace('/', '_'))
      if not os.path.isdir(dirName.decode("utf8")):
         os.mkdir(dirName.decode("utf8"))
      select = Select(self.driver.find_element_by_name("jump"))
      num=len(select.options)
      for number in xrange(num):
         option=select.options[number]
         self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL +'t')
         option.click()
         self.SaveTwoLayerFile(dirName)
         self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL +'w')
         self.driver.switch_to.frame(self.driver.find_element_by_name("mainFrame"))
         select = Select(self.driver.find_element_by_name("jump"))

#print(driver.page_source)

if __name__=="__main__":
   web=OpenWeb(webdriver.Firefox())
   web.execute()
