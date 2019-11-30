## Build image
~~~
docker build . -t [nama image]
~~~
contohnya,
~~~
docker build . -t main_interface_image
~~~

<br />

## Run Image as container
~~~
docker run -itd --rm --name=[nama container] -p [nomor port]:8000 [nama built image]
~~~
contohnya,
~~~
docker run -itd --rm --name=main_interface_container -p 8000:8000 main_interface_image
~~~
Aplikasi dapat diakses pada `localhost:8000` (jika menggunakan docker desktop) <br />
Aplikasi dapat diakses pada `[ip virtual machine]:8000` (jika menggunakan docker toolbox)
