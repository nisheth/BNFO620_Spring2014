import argparse
import re



parser = argparse.ArgumentParser(description="This program parses the Clinical Excel File")


parser.add_argument('input_file', type=file, help="clinical excel file")
args = parser.parse_args()

clinical_file = args.input_file

SID_Results_Standardized = open('Final_Clinical_Parsed.txt', 'w')

header_line = clinical_file.readline().split('\t')
Date2 = re.search('(\d+)\/(\d+)\/(\d+)', header_line[3])
Date2 = Date2.group(3) + "_" + Date2.group(1) + "_" + Date2.group(2)
FDate2 = re.search('(\d+)\/(\d+)\/(\d+)', header_line[3])
FormatDate2 = FDate2.group(1) + "/" + FDate2.group(2) + "/" + FDate2.group(3)
Date3 = re.search('(\d+)\/(\d+)\/(\d+)', header_line[7])
Date3 = Date3.group(3) + "_" + Date3.group(1) + "_" + Date3.group(2)
FDate3 = re.search('(\d+)\/(\d+)\/(\d+)', header_line[7])
FormatDate3 = FDate3.group(1) + "/" + FDate3.group(2) + "/" + FDate3.group(3)

line = next(clinical_file)
print >> SID_Results_Standardized, "SampleName\tRegion\tDate\tPatientID\tDepth"
for line in clinical_file:
    line = line.split('\t')

    if not line[0] == "":
        sample1_pid = re.search('(\d+)_(\w)', line[0])
        sample1_pid6 = sample1_pid.group(1) + sample1_pid.group(2)
        sid1 = re.search('\d+_\w_(\w\d+)_\d{4}_\d+_\d+_\d_\w+', line[0]).group(1)
        Date1 = re.search('\d+_\w_\w\d+_(\d{4}_\d+_\d+)_\d_\w+', line[0]).group(1)
        FormatDate = re.search('\d+_\w_\w\d+_(\d{4})_(\d+)_(\d+)_\d_\w+', line[0])
        FormatDate1 = FormatDate.group(2) + "/" + FormatDate.group(3) + "/" + FormatDate.group(1)
        region = re.search('\d+_\w_\w\d+_\d{4}_\d+_\d+_(\d)', line[0]).group(1)
        patient_ids = line[1]
        ptid_n_1 = re.search('(\d+)_', patient_ids).group(1)
        depth1 = re.search('\d+_(\w)', patient_ids).group(1)

        line1 =  sample1_pid.group(1) + "_" + sample1_pid.group(2) + "_" + sid1 + "_" + Date1 + "_" + region + "\t" + region  + "\t" + FormatDate1 + "\t" + ptid_n_1

        if depth1 == "D":
            print >> SID_Results_Standardized, line1 + "\t" + "Deep"
        elif depth1 == "S":
            print >> SID_Results_Standardized, line1+ "\t" + "Shallow"




    sample2_pid = re.search('(\d+)(\w)',line[4])
    sample2_pid = sample2_pid.group(1)
    sid = re.search('(\w+)_', line[3]).group(1)
    region2 = re.search('\w+_(\d+)', line[3]).group(1)
    sample2 = sid + "_" + region2 + "_" + Date2 + "_" + region2 + "\t" + region2 + "\t" + FormatDate2 + "\t" + sample2_pid
    patient_ids2 = line[4]
    ptid_n_2 = re.search('(\d+)', patient_ids2).group(1)
    depth2 = re.search('\d+(\w)', patient_ids2).group(1)
    line2 = sample2

    if depth2 == "D":
            print >> SID_Results_Standardized, line2 + "\t" + "Deep"
    elif depth2 == "S":
            print >> SID_Results_Standardized, line2 + "\t" + "Shallow"



    if not line[8] == "":
        sample3_pid = re.search('(\d+)(\w)',line[8])
        sample3_pid = sample3_pid.group(1)
        sid3 = re.search('(\w+)_', line[7]).group(1)
        region3 = re.search('\w+_(\d+)', line[7]).group(1)
        sample3 = sid3 + "_" + region3 + "_" + Date3 + "_" + region3 + "\t" + region3 + "\t" + FormatDate3 + "\t" + sample3_pid
        line3 = sample3

        if depth2 == "D":
            print >> SID_Results_Standardized, line3 + "\t" + "Deep"
        elif depth2 == "S":
            print >> SID_Results_Standardized, line3 + "\t" + "Shallow"















