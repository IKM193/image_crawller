import os
import re

import urllib
import requests
class ImageCrawller:
    def __int__(self,save,save_dirpath,start_page,maximum_download):
        self.save_dirpath=save_dirpath #画像を保存するためのディレクトリ
        self.crawl_url_list=[start_page] #最初に画像を回収するページのURL
        self.stocked_url=set()
        self.maximum_download=maximum_download #集める画像数の上限。これを超えると処理を打ち切る
        self.download_counter=0

    def run(self):
        while True:
            #処理1: 探索するURLがなければ終了。規定数以上を集めていても終了
            if len(self.crawl_url_list)==0:
                break
            if self.download_counter>=self.maximum_download:
                break

            #処理2: 次に調べるHTMLのURLを取得
            crawl_url=self.crawl_url_list.pop(0)

            #処理3: HTMLページから絶対URLを抽出する
            urls=self.get_abs_urls(crawl_url)

            #処理4: 絶対URLをHTMLかイメージかに分散する。イメージのリストを返す
            image_url_list=self.get_image_url_list(urls)

            #処理5: リストに格納されたイメージをすべて保存する
            self.save_images(image_url_list)

        print('Finished')


        def get_abs_urls(self,url):
            try:
                #URLから文字列のHTMLを取得
                response=requests.get(url)
                html=response.text

                #HTMLからURLを抜き出してリストに格納
                relative_url_list=re.findall('https?://[\w/:%#\$&\?\(\)~\.=\+\-]+',html)

                #相対URLを絶対URLに変換。HTTP/HTTPS以外のURLは除外
                abs_url_list=[]
                for relative_url in relative_url_list:
                    abs_url=urllib.parse.urljoin(url,relative_url)
                    if abs_url.startswith('http://') or abs_url.startswith('https://'):
                        abs_url_list.append(abs_url)

                    return abs_url_list

            except Exception as e:
                print('Error: {}'.format(e))
                return []
    

        def get_image_url_list(self,url_list):
            try:
                image_url=[]
                for url in url_list:
                    if url in self.stocked_url:
                        continue

                    if '.jpg' in url:
                        image_url_list.append(url)
                    elif '.png' in url:
                        image_url_list.append(url)
                    elif '.gif' in url:
                        image_url_list.append(url)
                    else:
                        self.crawl_url_list.append(url) #画像ファイルではないのでURL取得に使う

                    self.stocked_url.add(url) #URLを取得。同じものは再登録しない
                
                return image_url_list

            except Exception as e:
                print('Error: {}'.format(e))
                return []

        def save_images(self,image_url_list):
            for image_url in image_url_list:
                try:
                    #決められた回数以上のダウンロードをした場合は終了
                    if self.download_counter>=self.maximum_download:
                        return

                    #イメージを取得
                    response=requests.get(image_url,stream=True)
                    image=response.content

                    #イメージをファイルに保存
                    file_name=image_url.split('/').pop()
                    save_path=os.path.join(self.save_dirpath,file_name)
                    fout=open(save_path,'wb')
                    fout.write(image)
                    fout.close()

                    self.download_counter+=1
                    print('save image:{}/{}'.format(self.download_counter,self.maximum_download))

                except Exception as e:
                    print('Error: {}'.format(e))
            
            
        if __name__=='__main__':
            save_dirpath='text'
            start_page='https://gihyo.jp/book/list'
            maximum_download=10
            crawller=ImageCrawller(save_dirpath,start_page,maximum_download)
            crawller.run()

