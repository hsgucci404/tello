echo=1/*>nul&@cls
@echo off
setlocal enableDelayedExpansion
::runas administrator
%1 start "" mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cls
::setlocal
call :setdir
call :configx86orx64
set extract=extract
set pythonLib="C:\Python27\Lib\site-packages\"
set /a maxRetry=3
set /a retryCount=0
echo ------------------------------------------------------

::-------------------down python2.7 and install-------------------
echo ------------------------------------------------------
echo                Downloading python2.7                  
echo ------------------------------------------------------
::このレジストリキーは、複数のバージョンのsslおよびtlsのサポートを有効にするために使用され、公式のPython Webサイトへのアクセスを拒否する問題を解決するために使用されます。
REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v SecureProtocols /t REG_DWORD /d 2728 /f >nul
set /a retryCount=0
for %%# in (certutil.exe) do (
    if not exist "%%~f$PATH:#" (
        goto downpython
    )
)
if exist %pythonPackage% goto :downpythoncheck
:downpython
call :down %pythonDown% %pythonPackage%
:downpythoncheck
call :checkMD5 %pythonPackage% %pythonMD5% MD5pass
if "%MD5pass%" == "NO" (
    set /a retryCount=!retryCount!+1 && if !retryCount! == %maxRetry% (
        echo Retried %maxRetry% times, all failed. Skip.
        goto downpythonend
    ) else (
        echo Download %pythonPackage% failed. Retrying... !retryCount! of %maxRetry%
        goto downpython
    )
)
call :installmsiPackage %pythonPackage%
::python2.7環境変数を追加する
::wmicはすぐに有効にならないので、setする
echo %PATH%|findstr "c:\python27" >nul
if %errorlevel% neq 0 (
    wmic ENVIRONMENT where "name='PATH' and username='<system>'" set VariableValue="%PATH%;c:\python27"
    set "path=%path%;c:\python27;"
)
echo %PATHEXT%|findstr ".PY;.PYM" >nul
if %errorlevel% neq 0 (
    wmic ENVIRONMENT where "name='PATHEXT' and username='<system>'" set VariableValue="%PATHEXT%;.PY;.PYM"
    set "pathext=%pathext%;.PY;.PYM;"
)
:downpythonend
::-------------------python pipインストール-------------------
echo ------------------------------------------------------
echo                   Downloading pip                    
echo ------------------------------------------------------
set /a retryCount=0
for %%# in (certutil.exe) do (
    if not exist "%%~f$PATH:#" (
        goto downpip
    )
)
if exist %pipPackage% goto :downpipcheck
:downpip
call :down %pipDown% %pipPackage%
:downpipcheck
call :checkMD5 %pipPackage% %pipMD5% MD5pass
if "%MD5pass%" == "NO" (
    set /a retryCount=!retryCount!+1 && if !retryCount! == %maxRetry% (
        echo Retried %maxRetry% times, all failed. Skip.
        goto downpipend
    ) else (
        echo Download %pipPackage% failed. Retrying... !retryCount! of %maxRetry%
        goto downpip
    )
)
python %pipPackage%
python -m pip install -U pip
:downpipend
::-------------------libboost-all-devのインストール-------------------
echo ------------------------------------------------------
echo                Downloading libboost                   
echo ------------------------------------------------------
echo Please wait a few minutes...
set /a retryCount=0
for %%# in (certutil.exe) do (
    if not exist "%%~f$PATH:#" (
        goto downlibboost
    )
)
if exist %libboostPackage% goto :downlibboostcheck
:downlibboost
call :down %libboostDown% %libboostPackage%
:downlibboostcheck
call :checkMD5 %libboostPackage% %libboostMD5% MD5pass
if "%MD5pass%" == "NO" (
    set /a retryCount=!retryCount!+1 && if !retryCount! == %maxRetry% (
        echo Retried %maxRetry% times, all failed. Skip.
        goto downlibboostend
    ) else (
        echo Download %libboostPackage% failed. Retrying... !retryCount! of %maxRetry%
        goto downlibboost
    )
)
call %libboostPackage% /SILENT /NORESTART
:downlibboostend
::-------------------ffmpegのインストールは、Linuxのlibavcodec-dev libswscale-devの2つに依存します-------------------
echo ------------------------------------------------------
echo                  Downloading ffmpeg                   
echo ------------------------------------------------------
set /a retryCount=0
for %%# in (certutil.exe) do (
    if not exist "%%~f$PATH:#" (
        goto downffmpeg
    )
)
if exist %ffmpegPackage% goto :downffmpegcheck
:downffmpeg
call :down %ffmpegDown% %ffmpegPackage%
:downffmpegcheck
call :checkMD5 %ffmpegPackage% %ffmpegMD5% MD5pass
if "%MD5pass%" == "NO" (
    set /a retryCount=!retryCount!+1 && if !retryCount! == %maxRetry% (
        echo Retried %maxRetry% times, all failed. Skip.
        goto downffmpegend
    ) else (
        echo Download %ffmpegPackage% failed. Retrying... !retryCount! of %maxRetry%
        goto downffmpeg
    )
)
call :unpack %ffmpegPackage% %extract%
:downffmpegend
echo ------------------------------------------------------
echo              Downloading VS2013 runtime         
echo ------------------------------------------------------
set /a retryCount=0
for %%# in (certutil.exe) do (
    if not exist "%%~f$PATH:#" (
        goto downvs2013
    )
)
if exist %vs2013package% goto :downvs2013check
:downvs2013
call :down %vs2013depend% %vs2013package%
:downvs2013check
call :checkMD5 %vs2013package% %vs2013MD5% MD5pass
if "%MD5pass%" == "NO" (
    set /a retryCount=!retryCount!+1 && if !retryCount! == %maxRetry% (
        echo Retried %maxRetry% times, all failed. Skip.
        goto downvs2013end
    ) else (
        echo Download %vs2013package% failed. Retrying... !retryCount! of %maxRetry%
        goto downvs2013
    )
)
call %vs2013package% /passive /NORESTART
:downvs2013end
::-------------------python-numpy python-matplotlib opencv-pythonのインストール(pip方式)-------------------
echo ------------------------------------------------------
echo                  Downloading numpy                    
echo ------------------------------------------------------
python -m pip install numpy
echo ------------------------------------------------------
echo                Downloading matplotlib                 
echo ------------------------------------------------------
python -m pip install matplotlib
echo ------------------------------------------------------
echo              Downloading opencv-python                   
echo ------------------------------------------------------
python -m pip install -v opencv-python==3.4.2.17
echo ------------------------------------------------------
echo                  Downloading pillow                   
echo ------------------------------------------------------
python -m pip install pillow
:copydependencies
::-------------------依存ライブラリのすべてのdllをc：\ python27 \ lib \ site-packagesに配置します-------------------
echo ------------------------------------------------------
echo                 Copying dependencies                  
echo ------------------------------------------------------
echo %extract%\%ffmpegPackage:~0,-4%\bin\ 
echo %libboostPackageCopy%
echo %libh264%
xcopy /Y /E /I %extract%\%ffmpegPackage:~0,-4%\bin\*.dll %pythonLib%
xcopy /Y /E /I %libboostPackageCopy% %pythonLib%
xcopy /Y /E /I %libh264%\*.pyd %pythonLib%
endlocal
echo ------------------------------------------------------
echo                  Installation done.                
echo ------------------------------------------------------
pause
goto :eof

::--------------------------------------------------------------------------------------------

::-----------------以下はMD5チェックの定義エリアです------------------
:checkMD5
set file=%~1
call :MD5get %file% MD5
if "%MD5%" equ "%~2" (
      echo MD5 identical.
      set "%~3=YES"
) else (
      if "%MD5%" equ "skip" (
        echo MD5 check skipped.
        set "%~3=YES"
      ) else (
        echo Warning: MD5 does not match!
        set "%~3=NO"
      )
)
goto :eof

::-----------------以下はMD5チェックの定義エリアです------------------
:MD5get
echo %~1
for %%# in (certutil.exe) do (
    if not exist "%%~f$PATH:#" (
        echo certutil.exe not found
        echo for Windows XP professional and Windows 2003
        echo you need Windows Server 2003 Administration Tools Pack
        echo https://www.microsoft.com/en-us/download/details.aspx?id=16770
        echo now skip the MD5 check
        if "%~2" neq "" (
            set "%~2=skip"
        )
        ::exit /b 4
        goto :eof
    )
)

set "md5="
for /f "skip=1 tokens=* delims=" %%# in ('certutil -hashfile "%~f1" MD5') do (
    if not defined md5 (
        for %%Z in (%%#) do set "md5=!md5!%%Z"
    )
)

if "%~2" neq "" (
    set "%~2=%md5%" 
) else (
    echo %md5%
)

goto :eof

::-----------------以下はディレクトリ切り替え定義エリアです------------------
::管理者モードで実行すると、デフォルトのパスが変更され、ディレクトリはここに戻ります
:setdir
set char=%~dp0%
%char:~0,2%
cd  %~dp0%
goto :eof

::-----------------以下はバージョン関数定義エリアです------------------
:configx86orx64
IF %PROCESSOR_ARCHITECTURE% == AMD64 (
    set versionFlag=win64
) else ( 
    set versionFlag=win32
)

echo Windows Version: %versionFlag%
if %versionFlag%==win64 (
    set pythonDown="https://www.python.org/ftp/python/2.7.17/python-2.7.17.amd64.msi"
    set pythonPackage=python-2.7.17.amd64.msi
    set pythonMD5="55040ce1c1ab34c32e71efe9533656b8"

    set pipDown="https://bootstrap.pypa.io/get-pip.py"
    set pipPackage=get-pip.py
    set pipMD5="7036ca015e814fc2619fdb0b73f2ed19"

    set ffmpegDown="https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2020-12-21-12-38/ffmpeg-N-100455-g5dbabb020e-win64-gpl-shared.zip"
    set ffmpegPackage=ffmpeg-N-100455-g5dbabb020e-win64-gpl-shared.zip
    set ffmpegMD5="fc376995d94dc50949555202f5a435c4"

    set libboostDown="https://nchc.dl.sourceforge.net/project/boost/boost-binaries/1.68.0/boost_1_68_0-msvc-12.0-64.exe"
    set libboostPackage="boost_1_68_0-msvc-12.0-64.exe"
    set libboostPackageCopy="c:\local\boost_1_68_0\lib64-msvc-12.0\boost_python27-vc120-mt-x64-1_68.dll"
    set libboostMD5="4e6b11a971502639ba5cc564c7f2d568"

    set libh264=..\..\h264decoder\windows\x64

    set vs2013depend="https://download.microsoft.com/download/2/E/6/2E61CFA4-993B-4DD4-91DA-3737CD5CD6E3/vcredist_x64.exe"
    set vs2013package=vcredist_x64.exe
    set vs2013MD5="96b61b8e069832e6b809f24ea74567ba"

) else (
    set pythonDown="https://www.python.org/ftp/python/2.7.17/python-2.7.17.msi"
    set pythonPackage=python-2.7.17.msi
    set pythonMD5="4cc27e99ad41cd3e0f2a50d9b6a34f79"

    set pipDown="https://bootstrap.pypa.io/get-pip.py"
    set pipPackage=get-pip.py
    set pipMD5="b7666e8e7f98f513096601d4203fb007"

    set ffmpegDown="https://ffmpeg.zeranoe.com/builds/win32/shared/ffmpeg-20200311-36aaee2-win32-shared.zip"
    set ffmpegPackage=ffmpeg-20200311-36aaee2-win32-shared.zip
    set ffmpegMD5="bc9eae5466ca033e54588d7c25fe3ea9"

    set libboostDown="https://excellmedia.dl.sourceforge.net/project/boost/boost-binaries/1.68.0/boost_1_68_0-msvc-12.0-32.exe"
    set libboostPackage="boost_1_68_0-msvc-12.0-32.exe"
    set libboostPackageCopy="c:\local\boost_1_68_0\lib32-msvc-12.0\boost_python27-vc120-mt-x32-1_68.dll"
    set libboostMD5="d5d5ee205c87078245eb7df72789f407"

    set libh264=..\..\h264decoder\windows\x86

    set vs2013depend="https://download.microsoft.com/download/2/E/6/2E61CFA4-993B-4DD4-91DA-3737CD5CD6E3/vcredist_x86.exe"
    set vs2013package=vcredist_x86.exe
    set vs2013MD5="0fc525b6b7b96a87523daa7a0013c69d"
)

goto :eof

::-----------------これがh264関数定義領域です------------------
:h264install
cd h264decoder
if exist build (
    rd /s /q build 
    mkdir build
) else (
    mkdir build
)
cd build
cmake ..
make
goto :eof

::-----------------以下はダウンロード機能定義エリアです------------------
:down
echo Source:      "%~1"
echo Destination: "%~f2"
echo Start downloading "%~2"...
cscript -nologo -e:jscript "%~f0" "download" "%~1" "%~2"
::echo Download "%~2" OK!
echo ------------------------------------------------------
goto :eof

::-----------------解凍機能の定義エリアは次のとおりです------------------
:unpack
echo Source:      "%~f1"
echo Destination: "%~f2"
echo Start unpacking "%~1"...
cscript -nologo -e:jscript "%~f0" "unpack" "%~1" "%~2" "%~dp0"
echo Unpack "%~1" OK!
echo ------------------------------------------------------
goto :eof
::-----------------以下はインストール機能定義エリアです-----------------
:installmsiPackage
echo Source:      "%~f1"
echo Strat installing "%~f1"...
msiexec /i "%~f1" /passive
echo install "%~1" OK!
echo ------------------------------------------------------
goto :eof
*/

function download(DownSource, DownDestination)
{
    var DownPost
    ,DownGet;

    DownDestination=DownDestination.toLowerCase();
    DownSource=DownSource.toLowerCase();
    //DownPost = new ActiveXObject("Msxml2"+String.fromCharCode(0x2e)+"ServerXMLHTTP");
    //DownPost = new ActiveXObject("Microsoft"+String.fromCharCode(0x2e)+"XMLHTTP");
    //DownPost.setOption(2, 13056);
    var DownPost=null; 
    try{ 
        DownPost=new XMLHttpRequest(); 
    }catch(e){ 
        try{ 
            DownPost=new ActiveXObject("Msxml2.XMLHTTP"); 
            DownPost.setOption(2, 13056);
        }catch(ex){ 
            try{ 
                DownPost=new ActiveXObject("Microsoft.XMLHTTP"); 
            }catch(e3){ 
                DownPost=null; 
            } 
        } 
    } 
    DownPost.open("GET",DownSource,0);
    DownPost.send();
    DownGet = new ActiveXObject("ADODB"+String.fromCharCode(0x2e)+"Stream");
    DownGet.Mode = 3;
    DownGet.Type = 1; 
    DownGet.Open(); 
    DownGet.Write(DownPost.responseBody);
    DownGet.SaveToFile(DownDestination,2); 
}

function unpack(PackedFileSource, UnpackFileDestination, ParentFolder)
{
    var FileSysObject = new Object
    ,ShellObject = new ActiveXObject("Shell.Application")
    ,intOptions = 4 + 16
    ,DestinationObj
    ,SourceObj;

    if (!UnpackFileDestination) UnpackFileDestination = '.';
    var FolderTest = ShellObject.NameSpace(ParentFolder + UnpackFileDestination);
    FileSysObject = ShellObject.NameSpace(ParentFolder);
    while (!FolderTest) 
    {
        WSH.Echo ('Unpack Destination Folder Not Exist, Creating...');
        FileSysObject.NewFolder(UnpackFileDestination);
        FolderTest = ShellObject.NameSpace(ParentFolder + UnpackFileDestination);
        if (FolderTest) 
        WSH.Echo('Unpack Destination Folder Created.');
    }
    DestinationObj = ShellObject.NameSpace(ParentFolder + UnpackFileDestination); 
    SourceObj = ShellObject.NameSpace(ParentFolder + PackedFileSource);
    for (var i = 0; i < SourceObj.Items().Count; i++) 
    {
        try {
            if (SourceObj) {
                WSH.Echo('Unpacking ' + SourceObj.Items().Item(i) + '... ');
                DestinationObj.CopyHere(SourceObj.Items().Item(i), intOptions);
                WSH.Echo('Unpack ' + SourceObj.Items().Item(i) + ' Done.');
            }
        }
        catch(e) {
            WSH.Echo('Failed: ' + e);
        }
    }
}

switch (WScript.Arguments(0)){
    case "download":
        download(WScript.Arguments(1), WScript.Arguments(2));
        break;
    case "unpack":
        unpack(WScript.Arguments(1), WScript.Arguments(2), WScript.Arguments(3));
        break;
    default:
}
