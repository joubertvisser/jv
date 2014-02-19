# Backup program 
'''            for filename in fileList:
                try:
                    file = logDir + "\\" + filename.rstrip()
                    stats = os.stat(file)
                    lastmod_date = time.localtime(stats[8])
                    file_date = datetime.date(lastmod_date.tm_year, lastmod_date.tm_mon, lastmod_date.tm_mday)
                    file_time = datetime.time(lastmod_date.tm_hour, lastmod_date.tm_min)
                    if file_date >= yesterday:
                        if file_date == yesterday and file_time < chktime:
                            pass
                        else:
'''
from os import chdir, stat, listdir, path, walk, system
from shutil import copy
#from sys import stderr, exc_info
import sys
from datetime import date, time, timedelta, datetime

targetroot = 'c:\\data2\\'
sourcefolders = ['c:\\analog', 'c:\\data1']
dt = date.today()

#logMsg.smsg = '<h3>Summary of minidumps in Peregrine for %s<h3>' % dt
#logMsg.smsg = logMsg.smsg + '<table><tr><td><b>Gateway</b></td><th># of mdmp files</th></tr>'
if dt.isoweekday() == 1:  #Monday will take weekend into account
	yesterday = dt + timedelta(-3)
else:
	yesterday = dt + timedelta(-1)
    
chktime = time(8,30)

class File(object):
    #To store file properties
	datetime = 0
	name = 0
    
def get_source():
    # Loop through the directories
    for sourcefolder in sourcefolders:
    #	try:
         for root, dirs, files in walk(sourcefolder):
                targetfolder = targetroot + root.split(':\\')[1]
                if path.exists(targetfolder):
                    check_updated_files(root,targetfolder)
                else:
                    make_target_dir(targetfolder)
                    copy_source_files(root, targetfolder)
#     	except Exception as err:
			#stderr.write('ERROR: %s\n' % str(err))
			
			
			
    
def check_updated_files(sourcefolder,targetfolder):
    #Files to write the directory info to 
    sourcefiles = 'c:/temp/sourcefiles.txt'
    targetfiles = 'c:/temp/targetfiles.txt'
	#Open the list of filenames
    system('del c:\\temp\\*files.txt')
    system('dir ' + sourcefolder + ' /t:w /o:-d /a:-h-d | find "/" >> ' + sourcefiles)
    system('dir ' + targetfolder + ' /t:w /o:-d /a:-h-d | find "/" >> ' + targetfiles)
    emptysrc = empty_file(sourcefiles)
    emptytrg = empty_file(targetfiles)
    fs = open(sourcefiles, 'r')
    ft = open(targetfiles, 'r')
    #Instantiate class 
    fsdt = File()
    ftdt = File()
    if emptysrc:
	print 'Source is empty'
	return 0
    if emptytrg:
	print 'Target file list is empty'
        copy_source_files(sourcefolder, targetfolder)
        return 0
    else:
        tline = ft.readline()
        ftdt.name, ftdt.datetime = check_file_date(tline)
    filelist = []
    for line in fs:
        fsdt.name, fsdt.datetime = check_file_date(line)
#	print 'FS: %s TS: %s' % (fsdt.datetime, ftdt.datetime)
#	print 'Source: %sTarget: %s' % (line, tline)
#	print 'Comparing fsdt: %s and ftdt: %s for folder: %s ' % (fsdt.datetime, ftdt.datetime, sourcefolder)
        if fsdt.datetime == ftdt.datetime:
            if fsdt.name == ftdt.name:
#		print 'Names and dates are equal'
#		print 'Filelist:  %s' % filelist
		if filelist:
		   copy_source_files(sourcefolder,targetfolder,filelist)
                return 0
            else:
                filelist.append(fsdt.name)
                continue
        elif fsdt.name != ftdt.name:
            filelist.append(fsdt.name)
            continue
        else:
            filelist.append(fsdt.name)
            tline = ft.readline()
	    if tline:
               ftdt.name, ftdt.datetime = check_file_date(tline)
    
    print 'Closing files'
    fs.close()
    ft.close()
        
def empty_file(filename):
    p = stat(filename).st_size
    if p == 0:
        return True
    else:
        return False
    
def check_file_date(line):
#Check the date and time of last update to the file.
        #print 'Line value: %s ' % line
        lsf = line.split(' ')
        m,d,y = lsf[0].split('/')
        hr,mn = lsf[2].split(':')
        dt = datetime(int(y),int(m),int(d), int(hr),int(mn))
	if lsf[3] == 'PM' and int(hr) != 12:
            dt = dt + timedelta(hours=12)
	name = lsf[-1].rstrip()
        return name, dt 
        
def make_target_dir(targetfolder):
    #Creating the target folder
    system('mkdir ' + targetfolder)
    print 'Created folder: %s' % targetfolder 
    
def copy_source_files(sourcefolder, targetfolder, files=None):
    #Copy the sourcefiles to 
    if files:
        for file in files:
            sourcefile = sourcefolder + '\\' + file
            targetfile = targetfolder + '\\' + file
            system('copy ' + sourcefile + ' ' + targetfile)
            print 'File: %s copied to %s ' % (sourcefile, targetfile)
    else:
        system('copy ' + sourcefolder + '\*.* ' + targetfolder + '/Y')
        print 'Sourcefiles: %s copied to %s' % (sourcefolder, targetfolder)
    
if __name__ == '__main__':
    get_source()
    #system('del c:\\temp\\*files.txt')
