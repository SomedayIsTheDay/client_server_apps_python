import subprocess
import platform
import locale

default_encoding = locale.getpreferredencoding()
param = "-n" if platform.system().lower() == "windows" else "-c"
urls = ["yandex.ru", "youtube.com"]
for url in urls:
    args = ["ping", param, "2", url]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        line = line.decode(encoding=default_encoding)
        print(line)
    print(url)

print(default_encoding)

# for myself
# for line in process.stdout:
#     result = chardet.detect(line)
#     print('result = ', result)
#     line = line.decode(result['encoding']).encode('utf-8')
#     print(line.decode('utf-8'))
