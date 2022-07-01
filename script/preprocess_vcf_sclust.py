
## preprocess befor this script
## select only PASS mutation
# grep '#' -v OS0130Tissue_mutect_filter.filter.vcf |awk '$7 == "PASS"' >  OS0130Tissue_pass.vcf

## Run
# python3 preprocess_vcf_sclust.py OS0130Tissue_pass.vcf > OS0130Tissue_pass_processed.vcf

## output
# vcf file contain only 4 values in INFO collumn

import sys

input_file=sys.argv[1]

header="""##fileformat=VCFv4.0
##INFO=<ID=DP,Number=1,Type=Integer, Description="Read Depth Tumor">
##INFO=<ID=DP_N,Number=1,Type=Integer, Description="Read Depth Normal">
##INFO=<ID=AF,Number=A,Type=Float, Description="Allelic Frequency Tumor">
##INFO=<ID=AF_N,Number=A,Type=Float, Description="Allelic Frequency Normal">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO"""

print(header)

# be care of tumor collumn
col_format=9	#column format info 
col_n=11	#column normal info 
col_t=10	#column tumor info 

for line in open(input_file) :
	line = line.rstrip()
	col = line.split('\t')

	format_col = col[col_format-1] #format column
	n_col = col[col_n-1] #normal column
	t_col = col[col_t-1] #tumor column

	count = 0
	for i in format_col.split(':') :
		if i == "DP":
			col_DP = count
		if i == "AF":
			col_AF = count
		count+=1

	DP_N = str(n_col.split(':')[col_DP])
	DP = str(t_col.split(':')[col_DP])

	AF_N = str(n_col.split(':')[col_AF])
	AF = str(t_col.split(':')[col_AF])

	info = "DP="+DP+";DP_N="+DP_N+";AF="+AF+";AF_N="+AF_N

	print(col[0],col[1],col[2],col[3],col[4],col[5],col[6],info,sep='\t')