


def rpkm(aligns,length,total):
	if length == 0 or total == 0:
		return 0
	return float(aligns * 1000000000) / length / total
