#!/usr/bin/python

# This utility receives a stereo audio file as input and splits the two channels into 
# separate mono files of the same codec and file type.

import os, sys, subprocess, re


def splitter(file):
	nfile = os.path.splitext(file)[0]
	ffprobe = subprocess.Popen(['ffprobe','-show_streams','-print_format','compact',
	'-i',file],stdout=subprocess.PIPE).stdout.readlines()
	
	print ffprobe
	for item in ffprobe:
		codec_type = re.search('codec_type=(\w+)', item).group(1)
		if codec_type=='audio':
			codec_name = re.search('codec_name=(\w+)', item).group(1)
			codec_long_name = re.search('codec_long_name=(.+)[|]profile', item).group(1)
			codec_time_base = re.search('|.+=(\w+|)', item).group(1)
			bit_rate = re.search('bit_rate=(\w+)', item).group(1)
			channels = re.search('channels=(\w+)', item).group(1)
			index = re.search('index=(\w+)', item).group(1)

			ext = os.path.splitext(file)[1]
			outfile = os.path.splitext(file)[0]

			print
			print 'index:',index
			print 'codec_type:',codec_type
			print 'ext:',ext
			print 'codec_name:',codec_name
			print 'codec_long_name:',codec_long_name
			print 'codec_time_base:',codec_time_base
			print 'channels:',channels
			print 'bit_rate:', bit_rate
			print

			if re.search('mov|MOV',ext):
				print 'reassigning ext to aif'
				ext = '.aif'

			if channels == '2':
				splitCMD = subprocess.Popen(['ffmbc','-y','-i',file,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':0:0:0:0',outfile+'_L'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':1:1:0:0',outfile+'_R'+ext
				],stdout=subprocess.PIPE)
				 
			if channels == '6':
				splitCMD = subprocess.Popen(['ffmbc','-y','-i',file,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':0:0:0:0',outfile+'_L'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':1:1:0:0',outfile+'_R'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':2:2:0:0',outfile+'_C'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':3:3:0:0',outfile+'_LFE'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':4:4:0:0',outfile+'_Ls'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':5:5:0:0',outfile+'_Rs'+ext,
				],stdout=subprocess.PIPE)

			if channels == '8':
				splitCMD = subprocess.Popen(['ffmbc','-y','-i',file,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':0:0:0:0',outfile+'_L'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':1:1:0:0',outfile+'_R'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':2:2:0:0',outfile+'_C'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':3:3:0:0',outfile+'_LFE'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':4:4:0:0',outfile+'_Ls'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':5:5:0:0',outfile+'_Rs'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':6:6:0:0',outfile+'_Lt'+ext,
				'-acodec',codec_name,'-ac','1','-map_audio_channel','0:'+index+':7:7:0:0',outfile+'_Rt'+ext,
				],stdout=subprocess.PIPE)

def main():
	if len(sys.argv) < 2:
		print
		print 'a_splitter needs an input file!'
		print
		print 'usage: a_splitter input_file'
		print 'extracts audio into individual streams following dolby track layouts'
		print 'ex: L,R,C,LFE,Ls,Rs'
		print 'ex: L,R,C,LFE,Ls,Rs,Lt,Rt'
		print 'ex: L,R'
		
		
		sys.exit()
	file = sys.argv[1]
	splitter(file)


if __name__ == '__main__':
	main()