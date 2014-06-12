import freesound
c = freesound.FreesoundClient()
c.set_token("36e286ba563287f86eed608c13cacd520ced010e","token")

text_file = open('3pigs.txt', 'r')

words = text_file.read().split()
sounds = {}

for word in words:
	if word not in sounds.keys() and '.' in word:
		word = word.replace('.', '')
		print "Searching for " + word + ":"
		print "----------------------------"
		results_pager = c.text_search(query=word, filter="duration:[0 TO 1.5]" , sort="rating_desc", fields="id,name,previews")
		sounds[word] = results_pager[0].retrieve_preview('.', word+'.mp3')