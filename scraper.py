import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 1000, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '')
    # Print New Line on Complete
    if iteration == total: 
        print()

def webScrape (url, file, pageStart, pageEnd, elements = [], columns = []):
	csvFile = open(file, 'w+', encoding = 'utf-8', newline = '')
	writer = csv.writer(csvFile, delimiter = ',')
	writer.writerow(columns)
	i = 0
	l = pageEnd - pageStart + 1
	printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = l)
	try:
		for pageURL in range(l):
			sleep(0.1)
			html = urlopen(url+str(pageURL+1))
			bsObj = BeautifulSoup(html, "html.parser")
			blocks = bsObj.findAll(class_ = elements[0])
			for block in blocks:
				findName = block.findAll(class_= elements[1])
				findWebsite = block.findAll(class_= elements[2])
				findAddress = block.findAll(class_= elements[3])
				findPhone = block.findAll(class_= elements[4])
				findCategories = block.findAll(class_= elements[5])
				csvRow = []
				fieldsArray = [findName,findWebsite,findAddress,findPhone,findCategories]
				for findElement in fieldsArray:
					if findElement is not None:
						if findElement is findWebsite:
							for element in findElement:
								if element is not '':
									csvRow.append(element.attrs['href'])
								else:
									print(findName)
									print(element.attrs['href'])
									csvRow.append(' ')
						else:
							for element in findElement:
								csvRow.append(element.get_text())
					else:	
						csvRow.append('N/A')
				#print(csvRow)	
				writer.writerow(csvRow)
			i += 1
			printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = l)

	finally:
		csvFile.close()
		print('Data imported!')

webScrape('https://www.yellowpages.com/search?search_terms=Business%20Brokers&geo_location_terms=New%20York%2C%20NY&page=', 
	'D:\WEB\python\scrape.csv', 1, 100,
	['info', 'n', 'track-visit-website', 'adr', 'phone', 'categories'],
	["Company Name", "Website", "Address", "Phone", "Category"])