REM @echo off

REM Daftar host yang diuji
set LOGIN_ENDPOINT=http://192.168.99.100:31000/main/login/
REM Daftar nama output sebelum autoscale
set BEFORE_OUTPUT_LOGIN_ENDPOINT=_OUTPUT\test-output-before-LoginEndpoint-v%2%.txt
REM Daftar nama output setelah autoscale
set AFTER_OUTPUT_LOGIN_ENDPOINT=_OUTPUT\test-output-after-LoginEndpoint-v%2%.txt
REM data post
set DATA_LOGIN=_INPUT\data-login.txt
REM post type
set TYPE=application/x-www-form-urlencoded
REM Konfigurasi banyak request (N) dan concurrency (C)
set N=100
set C=20

IF "%1" == "before" (
  ab -n %N% -c %C% -p %DATA_LOGIN% -T %TYPE% %LOGIN_ENDPOINT% > %BEFORE_OUTPUT_LOGIN_ENDPOINT%
)

IF "%1" == "after" (
  ab -n %N% -c %C% -p %DATA_LOGIN% -T %TYPE% %LOGIN_ENDPOINT% > %AFTER_OUTPUT_LOGIN_ENDPOINT%
)
