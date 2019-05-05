# -*- coding: utf-8 -*- 
from PIL import Image
import cv2
import numpy as np
import os
import random
import datetime
import json
import operator 

RootDir = 'G:\\heartbot\\'
DreamyDir = RootDir+'Dreamy\\'
cPath = DreamyDir+'collage\\'
oPath = DreamyDir+'object\\'
fPath = DreamyDir+'filter\\'
OBJUsedFrequency = RootDir + '\\OBJUsedFrequency.json'

bgWordsCount = {'test_1':0}
objWordsCount = {} 
objList = []

def dreamy(words):
	## bacground image initialization
	bgimg = DreamyDir+'background\\'+words['bg']+'.jpg'
	bgimg = Image.open(bgimg)
	bgimg = bgimg.convert('RGBA') 
	final1= Image.new("RGBA",bgimg.size)
	final1= Image.alpha_composite(final1,bgimg)

	## object image initialization
	with open(RootDir+'Objects.json') as data_file:
		jsonList = json.load(data_file)

	### objWordsCount 객체 initialization
	for i in range(len(jsonList)):
		if i % 2 == 0:
			name = jsonList[i]['name'].split('_')[0]
			objWordsCount[name] = 0

	######### Appending objData list 
	# get image 1 or 2
	numWords = len(wordsList['object'])
	ranObjNum=[random.randint(1,2) for i in range(numWords)]
	
	objData = []
	for i in range(len(wordsList['object'])):
		searchKeywords = wordsList['object'][i] + '_' + str(ranObjNum[i])
		for j in range(len(jsonList)):
			if searchKeywords in jsonList[j]['name']:
				#키워드 카운팅 로직 : objWordsCount 1++ 
				cname = wordsList['object'][i].split('_')[0] 
				objWordsCount[cname] += 1
				objData.append(jsonList[j])

	### layer sorting 
	sortedbyLayer = sorted(objData,key=operator.itemgetter('layer'))
	print(sortedbyLayer)

	### get image data (size, location) from json list
	objimgs = []
	for i,d in enumerate(sortedbyLayer):
		oPath = DreamyDir+'object/'+d['name']+'.png'
		img = Image.open(oPath)

		width = int(bgimg.width*d['ratio'])
		wpercent = (width/float(img.width))
		height = int((float(img.height)*float(wpercent)))
		img = img.resize((width,height),Image.ANTIALIAS)
		cPossiton = d['location']
		final1.paste(img,(cPossiton[0],cPossiton[1]),mask=img)

		objimgs.append(img)

	###### file numbering with date & time ######
	now = datetime.datetime.now()
	dt = now.strftime('%m%d%H%M%S') #print(dt) 0424173516
	
	cPath = DreamyDir+'collage\\'
	
	print('Current Path : ' + cPath)
	nCount = len(os.listdir(cPath))
	print('File Count : ' + str(nCount))
	savedFileName = DreamyDir+'collage\\collageImg_'+str(dt)+'_'+ str(nCount + 1) + '.png'
	print('savedFileName: ' + savedFileName)
	final1.save(savedFileName)

	writeJSONToFile(words)

	cv2.waitKey(0)

	return savedFileName







def projector():
	Lists = readJSONFromFile()
	bg = Lists['bg']
	bg = sorted(bg,key=operator.itemgetter('freq'),reverse=True)
	#print(bg[0]['bgName'])
	bgimg = DreamyDir+'background/'+bg[0]['bgName']+'.jpg' ## 임의배경
	bgimg = Image.open(bgimg)
	bgimg = bgimg.convert('RGBA') 
	final1= Image.new("RGBA",bgimg.size)
	final1= Image.alpha_composite(final1,bgimg)

	
	objList = Lists['object']
	sObjCount = sorted(objList,key=operator.itemgetter('freq'),reverse=True)
	print(sObjCount[0])
	
	## object image initialization
	with open(RootDir+'Objects.json') as data_file:
		jsonList = json.load(data_file)

	
	ranObjNum=[random.randint(1,2) for i in range(6)]
	
	objData = []
	for i in range(6):
		searchKeywords = sObjCount[i]['objName'] + '_' + str(ranObjNum[i])
		for j in range(len(jsonList)):
			if searchKeywords in jsonList[j]['name']:
				objData.append(jsonList[j])
	#print(objData)

	### layer sorting 
	sortedbyLayer = sorted(objData,key=operator.itemgetter('layer'))
	#print(sortedbyLayer)

	### get image data from json list
	objimgs = []
	for i,d in enumerate(sortedbyLayer):
		oPath = DreamyDir+'object/'+d['name']+'.png'
		img = Image.open(oPath)

		width = int(bgimg.width*d['ratio'])
		wpercent = (width/float(img.width))
		height = int((float(img.height)*float(wpercent)))
		img = img.resize((width,height),Image.ANTIALIAS)
		cPossiton = d['location']
		final1.paste(img,(cPossiton[0],cPossiton[1]),mask=img)

		objimgs.append(img)

	######## image filter ########
	fCount = len(os.listdir(fPath))
	r = int(random.randint(0,fCount-1))
	flter = Image.open(fPath+os.listdir(fPath)[r])
	
	#flter = Image.open(fPath+'c.jpeg')
	flter = flter.resize(bgimg.size)
	result = Image.new('RGBA',size=(bgimg.size),color=(0,0,0,0))
	result = Image.blend(flter.convert('RGBA'),final1,alpha=0.75)


	###### file numbering with date & time ######
	now = datetime.datetime.now()
	dt = now.strftime('%m%d%H%M%S') #print(dt) 0424173516
	
	cPath = RootDir+'Projector\\'
	print('Current Path : ' + cPath)
	nCount = len(os.listdir(cPath))
	print('File Count : ' + str(nCount))
	savedFileName = cPath+'\\ProjectionImg_'+str(dt)+'_'+ str(nCount + 1) + '.png'
	print('savedFileName: ' + savedFileName)
	result.save(savedFileName)

	return savedFileName 



def writeJSONToFile(wordsList):
	if wordsList == '':
		print('wordsList is Empty')
		return -1
	else:
		fJSONFile = open(OBJUsedFrequency, 'r+')
		objFreqData = readJSONFromFile()

		# find bg's freq value in json data
		isInputBGExist = False;
		for i in objFreqData['bg']:
			isInputBGExist = False
			if i['bgName'] == wordsList['bg']:
				i['freq'] = i['freq']+1
				print('find it with: '+str(i['bgName']))
				print(str(i['bgName']+' values update with : '+str(i['freq'])))
				isInputBGExist = True
		
		# if input bg name is not exist, then append data to bg field
		if isInputBGExist == False:
			extraBGInfo = {}
			extraBGInfo['bgName'] = wordsList['bg']
			extraBGInfo['freq'] = 1
			objFreqData['bg'].append(extraBGInfo)
		
		# find object's freq value in json data
		for i in wordsList['object']:
			isInputObjectExist = False
			for j in objFreqData['object']:
				if i == j['objName']:
					j['freq'] = j['freq']+1
					print('find it with: '+str(j['objName']))
					print(str(j['objName']+' values update with : '+str(j['freq'])))
					isInputObjectExist = True
			
			# if input object is not exist, then append data to object field
			if isInputObjectExist == False:
				extraObjectInfo = {}
				extraObjectInfo['objName'] = i
				extraObjectInfo['freq'] = 1
				objFreqData['object'].append(extraObjectInfo)
				extraObjectInfo = ''

		print(objFreqData)
		fJSONFile.seek(0)
		fJSONFile.truncate()
		json.dump(objFreqData, fJSONFile, ensure_ascii=False, indent=4)
		fJSONFile.close()

	#return JObject

def readJSONFromFile():
	if os.path.exists(OBJUsedFrequency):
		with open(OBJUsedFrequency) as jsonFile:
			objFreqData = json.load(jsonFile)
	else:
		print('objfreq json file '+ OBJUsedFrequency +' not exist')
		return -1

	jsonFile.close()

	return objFreqData;




if __name__ == '__main__':
	#wordsList : 배경 1, object 3개 
	wordsList={'bg':'subway','object':['doll','dog','drone']}

	#writeJSONToFile(wordsList)
	dreamy(wordsList)
	projector()
