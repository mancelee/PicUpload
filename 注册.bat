@echo 开始注册
copy CameraDll.dll %windir%\system32\
regsvr32 %windir%\system32\CameraDll.dll /s
@echo CameraDll.dll注册成功
@pause