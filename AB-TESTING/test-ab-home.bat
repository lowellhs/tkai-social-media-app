REM @echo off

REM Daftar host yang diuji
set HOME_ENDPOINT=http://192.168.99.100:31000/main/home-detail/username/
REM Daftar nama output sebelum autoscale
set BEFORE_OUTPUT_HOME_ENDPOINT=_OUTPUT\test-output-before-HomeEndpoint-v%2%.txt
REM Daftar nama output setelah autoscale
set AFTER_OUTPUT_HOME_ENDPOINT=_OUTPUT\test-output-after-HomeEndpoint-v%2%.txt
REM Konfigurasi banyak request (N) dan concurrency (C)
set N=1000
set C=200

IF "%1" == "before" (
  ab -n %N% -c %C% %HOME_ENDPOINT% > %BEFORE_OUTPUT_HOME_ENDPOINT%
)

IF "%1" == "after" (
  ab -n %N% -c %C% %HOME_ENDPOINT% > %AFTER_OUTPUT_HOME_ENDPOINT%
)
