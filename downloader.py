import requests
import threading
import sys

def downloader(start,end,url,filename,file_size):
    headers = {"Range":"bytes=%d-%d" %(start,end)}
    r = requests.get(url,headers = headers,stream=True)
    retry = 0
    while (int(r.headers['content-length']) != end-start+1):
        #handle disconnection by retryting download
        if int(r.headers['content-length']) == file_size-start:
            break
        retry+=1
        if retry >3:
            print("Network failure")
            return
        r = requests.get(url,headers = headers,stream=True)

    with open(filename, "r+b") as fp:
        fp.seek(start)
        fp.write(r.content)
    
def download_driver(url, num_thread):
    r = requests.head(url)
    file_name = url.split("/")[-1]
    file_size = int(r.headers['content-length'])
    if r.status_code == 404:
        #check if the url is invalid
        print("invalid url")
        return
    div = file_size//num_thread+1
    fp = open(file_name,"wb")
    fp.write(b'\0'*file_size)
    #using multithread to download multiple chunk in parallel
    for i in range(num_thread):
        start = int(div*i)
        end = start+div
        t= threading.Thread(target=downloader, kwargs={'start':start,'end':end,'url':url,'filename':file_name, 'file_size':file_size})
        t.start()
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t == main_thread:
            continue
        t.join()
    print("download finishes")

if __name__ == "__main__":
    url = sys.argv[1]
    num_thread = int(sys.argv[3])
    download_driver(url, num_thread)