import freesound
c = freesound.FreesoundClient()
c.set_token("36e286ba563287f86eed608c13cacd520ced010e","token")

tag = "bird"

print "Searching for " + tag + ":"
print "----------------------------"
results_pager = c.text_search(query=tag,sort="rating_desc")
print "Num results: " + str(results_pager.count)
print "\t ----- PAGE 1 -----"
for i in range(0, len(results_pager.results)):
    sound = results_pager[i]
    print "\t- " + sound.name + " by " + sound.username
print "\t ----- PAGE 2 -----"
results_pager = results_pager.next_page()
for i in range(0, len(results_pager.results)):
    sound = results_pager[i]
    print "\t- " + sound.name + " by " + sound.username
print "\n"