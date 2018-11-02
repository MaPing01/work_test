#setup代码
from cx_Freeze import setup, Executable
executables = [
  Executable(
  script='c.py', #目标引用脚本
  base="win32gui",     #GUI程序需要隐藏控制台   
  targetName = 'c',#生成exe的名字
  )]
