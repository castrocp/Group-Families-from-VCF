
#!/usr/bin/env python
import gzip

'''
Using a single VCF file containing all families mixed together and ID-mapping file, creates and uses dictionaries to group 
family members together and create a new VCF file for each family. Family member columns 1-4 are written as 
father, mother, sibling, proband, respectively.

'''

def main():

	#Create dictionary to link individual family member ID to it's sample ID #
	#Create dictionary to link family ID without extension to a number counting the families
	FamilyMemberdictionary = {}
	FamilyIDdictionary = {}
	counter = 1 #keep track of number of families

	with open("PilotIDs") as f:   #absolute path from ~/SSCvcf; "../../../data/SSC/WGS/IDmapping/PilotIDs"
		
		for line in f:
			(key, val) = line.split()
			FamilyMemberdictionary[key] = val #keys are family IDs with extension, values are sample IDs

			familyID = key.split(".")[0]  #removes the extension (.fa, .ma, .p1, .s1)

			if familyID not in FamilyIDdictionary:
				FamilyIDdictionary[familyID] = counter #keys are family IDs without extension
				counter += 1

	Columns = [] #Columns list seems to be "lost" once exiting these loops if I don't initiate it first

	with open("testVCF") as originalVCF: #Use this line instead of next when running on test file
	#with gzip.open("2014-11-06_REI_final.recalibrated_variants.vcf.gz") as originalVCF: #absolute path from ~/SSCvcf; "../../../data/SSC/WGS/SNP/2014-11-06_REI_final.recalibrated_variants.vcf.gz"
		for line in originalVCF:
			if line.startswith("#CHROM"):   # This is the line with the column header names 
				Columns = line.strip("\n").split("\t")
	
	#Create dictionary to link column numbers to sample ID #s		
	ColumnDictionary = {} 
	counter = 0  #to keep track of column number
	for i in Columns[9:]:  #will start iterating at 10th column, where first SSC ID is found
		ColumnDictionary[counter] = i #keys are column numbers, values are sample IDs
		counter+=1
	
	#to go through each family ID returning the column that each member of that family is in
	for ID in sorted(FamilyIDdictionary):
		with open (ID +".vcf", "w") as famVCF: #create one vcf file for each family
			
			for member, SSC in sorted(FamilyMemberdictionary.items()): #find the SSC# for the father belonging to a particular family
				if member.startswith(ID) and member.endswith("fa"):  
					for column, ssc in ColumnDictionary.items(): #find which column the SSC# comes from
						if ssc == SSC:  
							fathercolumn = column

						
			for member, SSC in sorted(FamilyMemberdictionary.items()): 
				if member.startswith(ID) and member.endswith("mo"): #find mother column
					for column, ssc in ColumnDictionary.items(): 
						if ssc == SSC:  
							mothercolumn = column

						
			for member, SSC in sorted(FamilyMemberdictionary.items()): 
				if member.startswith(ID) and member.endswith("s1"):  #find sibling column
					for column, ssc in ColumnDictionary.items(): 
						if ssc == SSC:  
							probandcolumn = column

						
			for member, SSC in sorted(FamilyMemberdictionary.items()): 
				if member.startswith(ID) and member.endswith("p1"): #find proband column
					for column, ssc in ColumnDictionary.items(): 
						if ssc == SSC:  
							siblingcolumn = column

			with open("testVCF") as originalVCF: #Use this line instead of next when running on test file
			#with gzip.open("2014-11-06_REI_final.recalibrated_variants.vcf.gz") as originalVCF:
				for line in originalVCF:
					if not line.startswith("##"): #skips over info lines. Starts with column header line
						famVCF.write(line.split("\t")[0]+"\t"+line.split("\t")[1]+"\t"+line.split("\t")[2]+"\t"+line.split("\t")[3]+"\t"+line.split("\t")[4]+"\t"+line.split("\t")[5]+"\t"+line.split("\t")[6]+"\t"+line.split("\t")[7]+"\t"+line.split("\t")[8]+"\t"+line.split("\t")[fathercolumn+9]+"\t"+line.split("\t")[mothercolumn+9]+"\t"+line.split("\t")[probandcolumn+9]+"\t"+line.split("\t")[siblingcolumn+9]+"\n")  #account for first SSC column starting at column 10			
						

if __name__ == '__main__':
	main()