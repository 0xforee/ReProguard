ReProguard，通过 mapping 文件反混淆

使用说明：
```bash
python3 reproguard.py -s stack_trace -m mapping.txt -f trace.txt
```

参数说明：
* -h 帮助
* -s strategy，策略（nanoscope, systrace, stack_trace, android_hprof, hprof)
* -m mapping 文件
* -f input_file 要转译的文件
* -o output 输出（输出路径默认是输入文件所在路径，输出文件名为输入文件名_after）

支持说明：
* nanoscope，支持
* stack_trace, 支持
* android_hprof，当前仅支持 class 名称反混淆
* hprof，暂不支持
* systrace，暂不支持