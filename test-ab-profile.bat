REM @echo off

REM Daftar host yang diuji
set PROFILE_ENDPOINT=http://192.168.99.100:31000/main/profile/username/
REM Daftar nama output sebelum autoscale
set BEFORE_OUTPUT_PROFILE_ENDPOINT=_OUTPUT\test-output-before-ProfileEndpoint-v%2%.txt
REM Daftar nama output setelah autoscale
set AFTER_OUTPUT_PROFILE_ENDPOINT=_OUTPUT\test-output-after-ProfileEndpoint-v%2%.txt
REM Konfigurasi banyak request (N) dan concurrency (C)
set N=1000
set C=200

IF "%1" == "before" (
  ab -n %N% -c %C% %PROFILE_ENDPOINT% > %BEFORE_OUTPUT_PROFILE_ENDPOINT%
)

IF "%1" == "after" (
  ab -n %N% -c %C% %PROFILE_ENDPOINT% > %AFTER_OUTPUT_PROFILE_ENDPOINT%
)
