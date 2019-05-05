from PIL import Image
import cv2
import numpy as np
import os
import random
import datetime
import json
import operator

RootDir = 'E:/Heartbot/'
DreamyDir = 'E:/Heartbot/Dreamy/'
cPath = DreamyDir+'collage/'
oPath = DreamyDir+'object/'
fPath = DreamyDir+'filter/'
bgWordsCount = {'test_1':0}
objWordsCount = {} 
objList = []

def dreamy(words,data):
	bgimg = DreamyDir+'background/'+words['bg']+'.jpg'
	bgimg = Image.open(bgimg)
	bgimg = bgimg.convert('RGBA') # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=2000x1333 at 0x1CB1FD7ACC0>
	final1= Image.new("RGBA",bgimg.size)
	final1= Image.alpha_composite(final1,bgimg)
	

	#json data에서 image file, size 읽어오기 
	objimgs = []
	for d in data:
		oPath = DreamyDir+'object/'+d['name']+'.png'
		img = Image.open(oPath)
		width = int(bgimg.width*d['ratio'])
		print(d['ratio'])
		wpercent = (width/float(img.width))
		height = int((float(img.height)*float(wpercent)))
		img = img.resize((width,height),Image.ANTIALIAS)
		print(width,height,wpercent)

		objimgs.append(img)
	
	#print(wordsList['object'])	

	#json data에서 position값 가져오고 type 마다 다르게 매칭 
	#위에 변환한 image 데이터와 같이 final image에 paste
	for i,o in enumerate(objimgs):
		#cPossiton = position[objPosition[i]]
		if data[i]['type'] == 0:
			cPossiton = [0,0]
		else :
			cPossiton = data[i]['location']
			cPossiton[0] = cPossiton[0] #+ random.randint(-50,0)
			cPossiton[1] = cPossiton[1] #+ random.randint(-50,0)

		final1.paste(o,(cPossiton[0],cPossiton[1]),mask=o)
		

	###### file numbering with date & time ######
	### 1000 개 째 reset 하는 로직 필요 
	now = datetime.datetime.now()
	dt = now.strftime('%m%d%H%M%S') #print(dt) 0424173516
	
	cPath = DreamyDir+'collage/'
	print(os.path.exists(cPath+'collageImg*'))
	

	if os.path.exists(cPath+'collageImg*') !=1:
		print(os.path.exists(cPath+'collageImg*')) 
		fList = os.listdir(cPath)
		lastFile=os.path.basename(fList[-1])
		lastNum = int(lastFile[-7:-4])
		
		#Grayscale로 저장할 수 있게 on/off 
		#final1 = final1.convert('L') 
		final1.save(DreamyDir+'collage/collageImg_'+str(dt)+'_'+'{:03}'.format(lastNum+1)+'.png')  
	else :
		final1.save(DreamyDir+'collage/collageImg001.jpg') # 뭔가 파일이 없을때 동작을 안한다 수정필요 

	final1.show()

	cv2.waitKey(0)

	#return objWords  ## 새로운객체에 넣을 경우 return 

def projector(objWordsCount, objList):
	
	#bgimg = DreamyDir+'background/'+words['bg']+'.jpg' #배경도 가장 많이쓰인것 카운트 해서 가져오기 
	bgimg = DreamyDir+'background/'+'amusementpark.jpg' ## 임의배경
	bgimg = Image.open(bgimg)
	bgimg = bgimg.convert('RGBA') # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=2000x1333 at 0x1CB1FD7ACC0>
	final1= Image.new("RGBA",bgimg.size)
	final1= Image.alpha_composite(final1,bgimg)


	#print(objWordsCount)
	#for c in objWordsCount : 
	#print(max(objWordsCount,key = lambda x:objWordsCount.get(x)))
	#임의 값 넣어줌 
	objWordsCount = {'angel': 3, 'apple': 1, 'boat': 4, 'bus': 1, 'butterfly': 1, 'curtain': 0, 'cat': 7, 'deer': 0, 'moon': 2, 'beer': 1, 'owl': 4}
	sObjCount = sorted(objWordsCount.items(),key=operator.itemgetter(1),reverse=True)
	#print(sObjCount)

	#상위 값에 대해 json파일에서 object data get
	#같은 이름 이미지 중 random pick
	ranObjNum=[random.randint(1,2) for i in range(6)]
	print(ranObjNum)
	objData = []
	for i in range(6):
		searchKeywords = sObjCount[i][0] + '_' + str(ranObjNum[i])
		for j in range(len(jsonList)):
			if searchKeywords in jsonList[j]['name']:
				#keyword append data
				objData.append(jsonList[j])
	print(objData)


	#json data에서 image file, size 읽어오기 
	objimgs = []
	for d in objData:
		oPath = DreamyDir+'object/'+d['name']+'.png'
		img = Image.open(oPath)
		#print(width,height,wpercent)

		objimgs.append(img)
	
	#print(objimgs)

	#type 마다 다르게 매칭 
	#json data에서 location, size 값 가져오고
	#위에 변환한 image 데이터와 같이 final image에 paste
	for i,o in enumerate(objimgs):
		#cPossiton = position[objPosition[i]]
		if objData[i]['type'] == 0:
			#o.resize(bgimg.size)
			#final1 = Image.blend(o,bgimg,alpha=0.5)
			final1.paste(o,(0,0),mask=o)
		else :
			#location
			cPossiton = objData[i]['location']
			cPossiton[0] = cPossiton[0] + random.randint(30,30)
			cPossiton[1] = cPossiton[1] + random.randint(30,30)

			#size
			width = int(bgimg.width*objData[i]['ratio']*0.965)
			wpercent = (width/float(o.width))
			height = int((float(o.height)*float(wpercent)))
			o = o.resize((width,height),Image.ANTIALIAS)

			final1.paste(o,(cPossiton[0],cPossiton[1]),mask=o)



	####### #image filter 적용 
	flter = Image.open(fPath+'universe-2742113_1280.jpg')		
	flter = flter.resize(bgimg.size)
	result = Image.new('RGBA',size=(bgimg.size),color=(0,0,0,0))
	result = Image.blend(flter.convert('RGBA'),final1,alpha=0.65)


	###### file numbering with date & time ######
	### 1000 개 째 reset 하는 로직 필요 
	now = datetime.datetime.now()
	dt = now.strftime('%m%d%H%M%S') #print(dt) 0424173516
	
	cPath = RootDir+'Projector/'
	
	if os.path.exists(cPath+'ProjectionImg*') !=1:
		print(os.path.exists(cPath+'ProjectionImg*'))
		fList = os.listdir(cPath)
		lastFile=os.path.basename(fList[-1])
		lastNum = int(lastFile[-7:-4])
		
		#Grayscale로 저장할 수 있게 on/off 
		#final1 = final1.convert('L') 
		result.save(RootDir+'Projector/ProjectionImg_'+str(dt)+'_'+'{:03}'.format(lastNum+1)+'.png')  
	else :
		result.save(RootDir+'Projector/ProjectionImg001.jpg') # 뭔가 파일이 없을때 동작을 안한다 수정필요 

	result.show()

	cv2.waitKey(0)


	return 0 

if __name__ == '__main__':
	with open(RootDir+'Objects.json') as data_file:
		jsonList = json.load(data_file)
	#wordsList : 진욱이가 넘겨주는 keywords list : 배경 1, object 3개 
	wordsList={'bg':'forest','object':['angel','deer','butterfly']}

	
	### objWordsCount 객체 initialization
	for i in range(len(jsonList)):
		if i % 2 == 0:
			name = jsonList[i]['name'].split('_')[0]
			objWordsCount[name] = 0


	######### data list appending 모듈
	
	#같은 이름 이미지 중 random pick
	numWords = len(wordsList['object'])
	ranObjNum=[random.randint(1,2) for i in range(numWords)]
	#print(ranObjNum)
	
	#objData : 음성 인식 키워드에 대한 object 이미지 데이터
	objData = []
	for i in range(len(wordsList['object'])):
		searchKeywords = wordsList['object'][i] + '_' + str(ranObjNum[i])
		for j in range(len(jsonList)):
			if searchKeywords in jsonList[j]['name']:
				#키워드 카운팅 로직 : objWordsCount 1++ 
				cname = wordsList['object'][i].split('_')[0] 
				objWordsCount[cname] += 1
				#keyword append data
				objData.append(jsonList[j])
	#print(objData)
	#print(objWordsCount)

	#배경 json도 만들고 가져와야함 > 배경 json 안함 
	
	dreamy(wordsList,objData)
	#projector(objWordsCount, jsonList)

