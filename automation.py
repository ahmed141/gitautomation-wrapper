import os
import glob
import random
import datetime, time

## Auto file copy command
parent_path = r"D:\\AllGithubMine\\myGithubAllRep"
parent_path_automation = r"D:\\AllGithubMine\\myGithubAllRep\\gitautomation\\"
# print(os.listdir())

source_folder = "gitautolocalfiles"
dest_folder = "gitautomation"

auto_log = 'log-file.log'

try:
    num_loop = random.randint(1, 10)
    
    print("Total Runs to-do:\t\t", num_loop)
    
    FirstBool = True
    os.chdir(parent_path_automation)
    
    # os.system("bash")
    # time.sleep(5)

    os.system("eval $(ssh-agent -s)")
    os.system("ssh-add \"C:\\Users\\geniu\\.ssh\\github-ssh2\"")
    
    for i in range(num_loop):
        os.chdir(parent_path)

        with open(auto_log, 'a') as f_log:
            all_files = glob.glob('.\\'+source_folder+'\\*')
            print("===== Running \t\t", i)
            # print(source_folder, all_files)
            # print(all_files)
            source_file = all_files[random.randint(0, len(all_files))]
            # print(source_file.split('\\')[-1])
            # print('got source')
            copy_cmd = "copy /Y \"" + source_file + "\" " + '\".\\'+dest_folder+'\\'+source_file.split('\\')[-1].split('.')[0].split(' ')[0]+'.py'+'\"'
            # print(copy_cmd)
            f_log.write(str(datetime.datetime.now())+"\t"+copy_cmd+'\n')
            os.system(copy_cmd)
            os.chdir(dest_folder)
            # print(os.listdir())
            os.system('git add -A')
            os.system('git commit -m \"Auto Push Done\"')
            os.system('git push origin')
            print("\n*************************************")
            time.sleep(random.randint(1, 7))
except Exception as e:
    os.chdir(parent_path)
    with open(auto_log, 'a') as f_log:
       f_log.write(str(datetime.datetime.now())+"\t"+"ERROR Occured:\t"+str(e)+"\n")