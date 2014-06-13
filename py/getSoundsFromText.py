import freesound
import subprocess

c = freesound.FreesoundClient()
c.set_token("36e286ba563287f86eed608c13cacd520ced010e","token")

text_file = open('../data/text/sonar_knights.txt', 'r')

words = text_file.read().split()
sounds = {}

i = 0
for word in words:
	i = i+1
	if word not in sounds.keys() and '.' in word:
		word = word.replace('.', '')
		print "Searching for " + word + ":"
		print "----------------------------"
		results_pager = c.text_search(query=word, filter="duration:[0.5 TO 3]" , sort="downloads_desc", fields="id,name,previews")
		if len(results_pager.results) > 0:
			sounds[word] = results_pager[0].retrieve_preview('.', word+'.mp3')
			convertedfile = word+'.mp3'
			outputfilename = '../data/audio/' + str(i)+'.wav'
			cmd = 'lame --decode --resample 44.1 ' + convertedfile + ' ' + outputfilename
			subprocess.call(cmd, shell=True)
			