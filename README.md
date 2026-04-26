本项目用于极速将一场杭电比赛导入uoj-based OJ，也为其他比赛导入提供范式。

## 

## 用法



1.运行CSVbuild.py，注意需要有效的cookies；



2.运行SQLbuild.py，然后将其在app\_uoj233中运行；



3.运行statement\_update.py，注意需要有效cookies；



4.将hdu数据（1001.in等）放入raw，运行transform.py；



5.运行upload\_data.py，注意需要有效cookies；（这步前先运行reset）



6.运行testfile\_update.py，注意需要有效cookies



## DLC



我们做了一个从hydro导入的版本。放在hydro分支中。



实际上，真正的关键是抓包分析，并制造类似请求的方法。



以这个为基础，这样的工具只要vibe coding即可构建。

