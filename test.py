from downloader import download_driver
import filecmp
if __name__ == "__main__":
    download_driver("https://www.cs.cmu.edu/~mgormley/courses/10601/slides/lecture7-linreg.pdf",5)
    file_comp = filecmp.cmp("lecture7-linreg.pdf","lecture7-linreg_ref.pdf")
    if file_comp == True:
        print("test download success")