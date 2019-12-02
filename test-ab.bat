REM @echo off
REM Daftar host yang diuji
set SESSION_ID=quw4viv8gx21bogp6crehl1tnh6r8e1e
set LOGIN_PAGE=http://192.168.99.100:31000/main/login/
set HOME_PAGE=http://192.168.99.100:31000/main/home/
set PROFILE_PAGE=http://192.168.99.100:31000/main/profile/
REM Daftar nama output sebelum autoscale
set BEFORE_OUTPUT_LOGIN_PAGE=test-output-before-LoginPage.txt
set BEFORE_OUTPUT_HOME_PAGE=test-output-before-HomePage.txt
set BEFORE_OUTPUT_PROFILE_PAGE=test-output-before-ProfilePage.txt
REM Daftar nama output setelah autoscale
set AFTER_OUTPUT_LOGIN_PAGE=test-output-after-LoginPage.txt
set AFTER_OUTPUT_HOME_PAGE=test-output-after-HomePage.txt
set AFTER_OUTPUT_PROFILE_PAGE=test-output-after-ProfilePage.txt
REM Konfigurasi banyak request (N) dan concurrency (C)
set N=200
set C=20

IF "%1" == "before" (
  ab -n %N% -c %C% %LOGIN_PAGE% > %BEFORE_OUTPUT_LOGIN_PAGE%
  ab -n %N% -c %C% -C sessionid=%SESSION_ID% %HOME_PAGE% > %BEFORE_OUTPUT_HOME_PAGE%
  ab -n %N% -c %C% -C sessionid=%SESSION_ID% %PROFILE_PAGE% > %BEFORE_OUTPUT_PROFILE_PAGE%
)

IF "%1" == "after" (
  ab -n %N% -c %C% %LOGIN_PAGE% > %AFTER_OUTPUT_LOGIN_PAGE%
  ab -n %N% -c %C% -C sessionid=%SESSION_ID% %HOME_PAGE% > %AFTER_OUTPUT_HOME_PAGE%
  ab -n %N% -c %C% -C sessionid=%SESSION_ID% %PROFILE_PAGE% > %AFTER_OUTPUT_PROFILE_PAGE%
)
