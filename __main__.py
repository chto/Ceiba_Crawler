from src.ceiba_3 import *
from selenium import webdriver
def main():
   web=OpenWeb(webdriver.Firefox())
   web.execute()
if __name__=='__main__':
   main()
