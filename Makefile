.PHONY: all test clean

rsync:
	cd ../ && rsync -av -e "ssh -i  ~/.ssh/bioinformatics-cro/user2135/id_rsa" \
		./aws_pcluster_helpers \
		--exclude .idea \
		user2135@hpc.bioinformaticscro.io:/scratch/ftp/user2135/internal/

watch:
	python ./watch.py

run:
	source activate aws_pcluster
