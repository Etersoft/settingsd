# -*- coding: utf-8 -*-


##### Public #####
def joinPath(first, *others_list) :
	return joinItems("/", first, *others_list)

def joinMethod(first, *others_list) :
	return joinItems(".", first, *others_list)


##### Private #####
def joinItems(separator, first, *others_list) :
	for others_list_item in others_list :
		if len(first) == 0 :
			first = others_list_item
		else :
			first += separator + others_list_item
	return first
