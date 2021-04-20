import requests, argparse, wget, math, os
from fpdf import FPDF
from bs4 import BeautifulSoup as _soup
from PIL import Image

DOUJIN_URL = 'https://www.nhentai.net/g/{}'
GALLERY_URL = "https://i.nhentai.net/galleries/{}/{}"

session = requests.Session()

def doujin_download(link):
	images = []
	file_ext = None
	link = link.split('/')
	temp = False
	for item in link:
		if temp:
			doujin_id = item
			break
		elif item == 'g':
			temp = True
	res = _get(DOUJIN_URL.format(doujin_id))
	name = 'doujin'
	try:
		cover = res.find(id='cover').img['data-src']
	except:
		cover = 'https:' + res.find(id='cover').img['src']
	gid = int(cover.rsplit('/', 2)[-2])
	for url in res(class_='gallerythumb'):
		url = url.noscript.img['src'].rsplit('/', 1)[-1]
		file_ext = url.replace('t', '')
		images.append(GALLERY_URL.format(gid, url.replace('t', '')))
	pages = len(images)
	temp = True
	for image in images:
		alt_img = image.split('/')[-1][:-4]+'.jpg'
		wget.download(image,alt_img)
		if temp:
			image = Image.open(alt_img)
			width, height = image.size
			pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
			width, height = float(width * 0.264583), float(height * 0.264583)
			orientation = 'P' if width < height else 'L'
			width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
			height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
			pdf = FPDF()
			temp = False
		pdf.add_page(orientation=orientation)
		pdf.image(alt_img,x=0,y=0,w=width,h=height)
		os.remove(alt_img)
	pdf.output(name+'.pdf','F')
		
def _get(endpoint:str):
	return _soup(session.get(endpoint).text, 'lxml')
	
if __name__ == '__main__':
	p = argparse.ArgumentParser(description='nhentai PDF downloader.')
	p.add_argument('--url','-u')
	##p.add_argument('--')
	
	args = p.parse_args()
	doujin_download(args.url)
	
