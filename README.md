# Sclust
A docker container for Sclust analysis following paper:
Copy-number analysis and inference of subclonal populations in cancer genomes using Sclust
doi:10.1038/nprot.2018.033

## Usage
### 1. Pull docker image
```

```

### 2. Create docker container and mount your working folder (-v) 
```
docker run -v /home/HDD:/home/HDD -it ubuntu:16.04 bash
```


### 3. Run Sclust inside working containing 
```
# Set path to sample bam files and vcf files #
sample_name="OS0130_Tissue"
tumor_bam="/home/HDD/OS0130_recheck10/OS0130_T_recal.bam"
normal_bam="/home/HDD/OS0130_recheck10/OS0130_blood_recal.bam"
vcf_raw="/home/HDD/OS0130_recheck10/03_Mutect2/T/9_somatic_oncefiltered.vcf"

lambda="1e-7"
dir_out="Sclust_output_${sample_name}"
mode="genome" #exome or genome
ref_version="hg38" #hg38 or hg19

###############################################

#0. Convert the .vcf files to the Sclust-specific format.
mkdir ${dir_out}
grep '#' -v ${vcf_raw} |awk '$7 == "PASS"' >  ${dir_out}/${sample_name}_pass.vcf
python3 preprocess_vcf_sclust.py ${dir_out}/${sample_name}_pass.vcf >  ${dir_out}/${sample_name}_pass_processed.vcf

#1. Extract thr read ratio and SNP information of the chromosome (<chr>) from  the .bam-files 

#preparing parameters
if [[ $mode = "exome" ]]; then	
	part=1
	ns=100
elif [[ $mode = "genome" ]]; then
	part=2
	ns=1000
fi
echo -e "# Sclust: Running Sclust with mode = whole ${mode}\n"
echo -e "# Sclust: part = ${part}"
echo -e "# Sclust: ns = ${ns}"

for x in {1..22};
do
chr="chr"${x}
echo "# Sclust: Running ....."${chr}".............."
${sclust} bamprocess -t ${tumor_bam} -n ${normal_bam} -o ${dir_out}/${sample_name} -part ${part} -build ${ref_version} -r ${chr} &
done

#echo "# Sclust: Running .....chrY.............."
#${sclust} bamprocess -t ${tumor_bam} -n ${normal_bam} -o ${dir_out}/${sample} -part 2 -build hg38 -r chrY
echo "# Sclust: Running ......chrX.............."
${sclust} bamprocess -t ${tumor_bam} -n ${normal_bam} -o ${dir_out}/${sample_name} -part ${part} -build ${ref_version} -r chrX &

#2. Merge temporary data files following this command: 
${sclust} bamprocess -i ${dir_out}/${sample_name} -o ${dir_out}/${sample_name} # --> generarte snps and rcount file

#3. Perform the copy-number analysis using the converted mutation call.vcf file <sample>_mutations.vcf, the read-count file <sample>_rcount.txt, and the SNP base-count file <sample>_snps.txt
echo "# Sclust: Perform the copy-number analysis"
${sclust} cn -rc ${dir_out}/${sample_name}_rcount.txt \
	-snp ${dir_out}/${sample_name}_snps.txt \
	-vcf ${dir_out}/${sample_name}_pass_processed.vcf \
	-o ${dir_out}/${sample_name} -pyclone -ns ${ns}

#4. perform mutational clustering
echo "# Sclust: Perform mutational clustering..."
${sclust} cluster -i ${dir_out}/${sample_name} -lambda ${lambda} -o ${dir_out}/${sample_name}

```

### 4. Check output in "Sclust_output_${sample_name}" folder
