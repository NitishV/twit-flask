import sys
import json
import re
import string
import heapq
import twitterstream

'''
code_state_json = '{"AL":"Alabama","AK":"Alaska","AS":"American Samoa","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"District Of Columbia","FM":"Federated States Of Micronesia","FL":"Florida","GA":"Georgia","GU":"Guam","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MH":"Marshall Islands","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","MP":"Northern Mariana Islands","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PW":"Palau","PA":"Pennsylvania","PR":"Puerto Rico","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VI":"Virgin Islands","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}'

state_code_json = '{"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District Of Columbia":"DC","Federated States Of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}'

state_bounds_json = '{"Mississippi":[30.1477890014648,34.9960556030273,-91.6550140380859,-88.0980072021484],"Oklahoma":[33.6191940307617,37.0021362304688,-103.002571105957,-94.4312133789062],"Delaware":[38.4511260986328,39.8394355773926,-75.7890472412109,-74.9846343994141],"Minnesota":[43.4994277954102,49.3844909667969,-97.2392654418945,-89.4833831787109],"Illinois":[36.9701309204102,42.5083045959473,-91.513053894043,-87.0199203491211],"Arkansas":[33.0041046142578,36.4996032714844,-94.6178131103516,-89.6422424316406],"New Mexico":[31.3323001861572,37.0001411437988,-109.050178527832,-103.000862121582],"Indiana":[37.7717399597168,41.7613716125488,-88.0997085571289,-84.7845764160156],"Louisiana":[28.9210300445557,33.019458770752,-94.0431518554688,-88.817008972168],"Texas":[25.8370609283447,36.5007057189941,-106.645652770996,-93.5078201293945],"Wisconsin":[42.491943359375,47.3025016784668,-92.8881149291992,-86.2495422363281],"Kansas":[36.9930801391602,40.0030975341797,-102.0517578125,-94.5882034301758],"Connecticut":[40.9667053222656,42.0505905151367,-73.7277755737305,-71.7869873046875],"Virgin Islands":[17.6234664916992,18.4649848937988,-65.1590957641602,-64.5126724243164],"California":[32.5295219421387,42.0095024108887,-124.482009887695,-114.13077545166],"Puerto Rico":[17.8315086364746,18.5680027008057,-67.9987564086914,-65.1685028076172],"Georgia":[30.3557567596436,35.0008316040039,-85.6051712036133,-80.7514266967773],"North Dakota":[45.9350357055664,49.0004920959473,-104.049270629883,-96.5543899536133],"Pennsylvania":[39.7197647094727,42.5146903991699,-80.5210876464844,-74.6894989013672],"West Virginia":[37.2014808654785,40.638801574707,-82.6447448730469,-77.7190246582031],"Alaska":[51.0228691101074,71.6048278808594,-180.0,-140.0],"Missouri":[35.9956817626953,40.6136360168457,-95.7741470336914,-89.0988388061523],"South Dakota":[42.4798889160156,45.9454536437988,-104.05770111084,-96.4363327026367],"Colorado":[36.9924240112305,41.0023612976074,-109.060256958008,-102.041580200195],"New Jersey":[38.7887535095215,41.3574256896973,-75.5633926391602,-73.8850555419922],"Washington":[45.5437202453613,49.00244140625,-124.836097717285,-116.917427062988],"New York":[40.4773979187012,45.0158615112305,-79.7625122070312,-71.8527069091797],"Nevada":[35.0018730163574,42.0022087097168,-120.005729675293,-114.039642333984],"Maryland":[37.8856391906738,39.7229347229004,-79.4871978759766,-75.0395584106445],"Idaho":[41.9880561828613,49.000846862793,-117.243034362793,-111.043563842773],"Wyoming":[40.9948768615723,45.0034217834473,-111.05689239502,-104.052154541016],"Arizona":[31.3321762084961,37.0042610168457,-114.818359375,-109.045196533203],"Iowa":[40.3755989074707,43.5011367797852,-96.6397171020508,-90.1400604248047],"Michigan":[41.6960868835449,48.3060646057129,-90.4186248779297,-82.122802734375],"Utah":[36.9979667663574,42.0013885498047,-114.053932189941,-109.041069030762],"Virginia":[36.5407867431641,39.4660148620605,-83.6754150390625,-75.2312240600586],"Oregon":[41.9917907714844,46.2991027832031,-124.703544616699,-116.463500976562],"Montana":[44.3582191467285,49.0011100769043,-116.050003051758,-104.039558410645],"New Hampshire":[42.6970405578613,45.3057823181152,-72.55712890625,-70.534065246582],"Massachusetts":[41.1863288879395,42.8867149353027,-73.5081481933594,-69.8615341186523],"South Carolina":[32.0333099365234,35.2155418395996,-83.35400390625,-78.4992980957031],"Vermont":[42.7269325256348,45.0166664123535,-73.437744140625,-71.4653549194336],"Florida":[24.3963069915771,31.0009689331055,-87.6349029541016,-79.9743041992188],"Hawaii":[18.8654594421387,28.5172691345215,-178.443603515625,-154.755783081055],"Kentucky":[36.4967155456543,39.1474609375,-89.5715103149414,-81.9645385742188],"Rhode Island":[41.055534362793,42.018856048584,-71.9070053100586,-71.1204681396484],"Nebraska":[39.9999961853027,43.0017013549805,-104.053520202637,-95.3080520629883],"Ohio":[38.4031982421875,42.3232383728027,-84.8203430175781,-80.5189895629883],"Alabama":[30.1375217437744,35.0080299377441,-88.4731369018555,-84.8882446289062],"North Carolina":[33.7528762817383,36.5880393981934,-84.3218765258789,-75.4001159667969],"Tennessee":[34.9829788208008,36.6781196594238,-90.310302734375,-81.6468963623047],"Maine":[42.9561233520508,47.4598426818848,-71.0841751098633,-66.9250717163086]}'

code_state = json.loads(code_state_json)
state_code = json.loads(state_code_json)
state_bounds = json.loads(state_bounds_json)
'''



def get_state_happiness(score_file, tweet_count):

	print 'get_state_happiness' 
	tweets = twitterstream.fetchsamples(tweet_count)
	
	print 'Tweets retrieval completed.'
	
	code_state = json.load(open('us_states_code_name.json'))
	state_code = json.load(open('us_states_name_code.json'))
	state_bounds = json.load(open('us_states_geo_bounds.json'))
	
	scores = {}
	with open(score_file) as f:
		for line in f.readlines():
			splits = line.split('\t')
			term = splits[0]
			score = splits[1]
			scores[term] = int(score)
	
	'''
	for key in state_code.keys():
		if key not in state_bounds.keys():
			print key
	'''

	state_score = {}
	state_count = {}
	coord_count = 0 
	place_count = 0
	count = 0

	for line in tweets:
		t_score = 0
		tweet_dict = json.loads(line)
		if 'text' in tweet_dict.keys():
			tweet_text = tweet_dict['text'].encode('utf-8')
			for word in re.split('\s+', tweet_text):
				if '#' not in word:
					word = word.translate(string.maketrans('',''), string.punctuation)
				t_score = t_score + scores.get(word, 0)
	
		state_c = ''	
		if 'coordinates' in tweet_dict.keys():
			if tweet_dict['coordinates']:
				if tweet_dict['coordinates']['type'] == 'Point':
					coords = tweet_dict['coordinates']['coordinates']
					long, lat = coords
				
					for key, val in state_bounds.items():
						minlat, maxlat, minlong, maxlong = val
						if (lat > minlat) & (lat < maxlat) & (long > minlong) & (long < maxlong):
							state_c = key
							coord_count = coord_count + 1
		
		state_p = ''	
		if 'place' in tweet_dict.keys():
			place = tweet_dict['place']
			if place:
				country = place['country_code']
				if country == 'US':
					state_p = place['name'].encode('utf-8')
					if state_p not in state_code.keys():
						state_p = ''
						for word in re.split('\s+', place['full_name'].encode('utf-8')):
							word = word.translate(string.maketrans('',''), string.punctuation)
							if word in code_state.keys():
								state_p = code_state[word]
								place_count = place_count + 1
					else:
						place_count = place_count + 1
		
		state = ''
		if state_c == state_p:
			state = state_c
		elif (state_c != '') & (state_p != ''):
			state = state_p
			val = tweet_dict['coordinates']['coordinates']
			val.reverse()
			'''
			print val
			print state_c
			print state_p
			'''
		elif state_p:
			state = state_p
		elif state_c:
			state = state_c
		
		if state:
			code = state_code.get(state,'')
			if code:
				count = count + 1
				state_score[code] = state_score.get(code, 0) + t_score 
				state_count[code] = state_count.get(code, 0) + 1 
							

	#print str(coord_count)
	#print str(place_count)
	#print str(count)

	h = []
	for key, val in state_score.items():
 		heapq.heappush(h, (-val, key))
	
	results = []
	for x in range(len(h)):
		val, key = heapq.heappop(h)
		state_code = key
		state_name = code_state[state_code]
		count = state_count[state_code]
		results.append([state_code, state_name, count, -val])
		
	print results
	return results
	
def main():
	score_file = (sys.argv[1])
	tweet_count = (sys.argv[2])
	get_state_happiness(score_file, tweet_count)

if __name__ == '__main__':
	main()