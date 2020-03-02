import jamotools

region_words = ['일월', '이월', '삼월', '사월', '오월', '육월', '칠월', '팔월', '구월', '십월', '십일월', '십이월']
				# '이일', '삼일', '사일', '오일', '육일', '칠일', '팔일', '구일', '십일', '십일일', '일일', ]


f = open("date_words.txt", 'w')
for v in region_words:
    data = jamotools.split_syllables(v)+'\n'
    f.write(data)

f.close()
    


